#! /usr/bin/env python3

import sys
import time
import sqlite3

import pyvisa
from pymeasure.instruments.hp import HP3478A

# Rohde & Schwarz SMHU signal generator
class RS_SMHU:
    def __init__(self, rm, resource_address):
        self.conn = rm.open_resource(resource_address)
        pass

    pass

    def preset(self):
        self.conn.write(f"PRESET")

    def set_output(self, enable):
        if enable:
            self.conn.write(f"LEVEL:RF:ON")
        else:
            self.conn.write(f"LEVEL:RF:OFF")
        pass

    def set_freq(self, freq_mhz):
        self.conn.write(f"RF {freq_mhz}MHZ")
        pass

    def set_level(self, level_dbm):
        self.conn.write(f"LEVEL {level_dbm}DBM")
        pass


class Wiltron_SG1206U:
    def __init__(self, rm, resource_address):
        self.conn = rm.open_resource(resource_address)
        self.conn.write("IL1")            # Internal leveling - for now
        pass

    def preset(self):
        # FIXME
        pass

    def set_output(self, enable):
        if enable:
            self.conn.write("RF1")
        else:
            self.conn.write("RF0")
        pass

    def set_freq(self, freq_mhz):
        self.conn.write(f"F1{f}MH")
        pass

    def set_level(self, level_dbm):
        self.conn.write(f"LVL{p}DM")
        pass
        

def create_db(filename):
    conn=sqlite3.connect(filename)
    c = conn.cursor()
    c.execute('''
        create table if not exists measurements(
            [id]            integer primary key,
            [session_id]    integer,
            [created]       integer,
            [freq]          real,
            [power_dbm]     real,
            [v]             real)
        ''')
    c.execute('''
        create table if not exists sessions(
            [id]            integer primary key,
            [name]          text,
            [description]   text,
            [created]       text)
        ''')
    conn.commit()

    return conn

def create_session(conn, name, description=''):
    sql = '''insert into sessions(name, description,created)
             values(?, ?, datetime('now'))'''

    c = conn.cursor()
    c.execute(sql, (name, description))
    conn.commit()

    return c.lastrowid

def record_measurement(conn, session_id, freq, power_dbm, v):
    sql = '''insert into measurements(session_id, created, freq, power_dbm, v) values(?, datetime('now'), ?, ?, ?)'''

    c = conn.cursor()
    c.execute(sql, (session_id, freq, power_dbm, v))
    conn.commit()

def freq_power_v_graph(db_conn, session_id, freq_values, power_levels, nr_samples):
    for f in freq_values_mhz:
        sig_gen.set_freq(f)

        for p in power_levels_dbm:
            sig_gen.set_level(p)
            v = dmv.measure_DCV     # Dummy read to drop transition value
            for i in range(0,nr_samples):
                time.sleep(0.2)
                v = dmv.measure_DCV
                print(f"Freq={f}MHz, Power={p}dBm -> {v}V")
                #record_measurement(db_conn, session_id, f, p, v)

            print()
    pass


# Frequency values to measure

# Wiltron:
#freq_values_mhz = [ 10, 30, 50, 70, 100, 200, 500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 100000, 11000, 12000, 13000, 15000, 17000, 19000 ]
# max_level = 15

# SMHU:
freq_values_mhz = [ 10, 30, 50, 70, 100, 200, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4300 ]
max_level = 13


# Power levels to measure
power_levels_dbm = [ 
    -115, -110, -100, -90, -80, -70]

for p in range(-60, 20, 10):
    for pp in [0, 3, 7]:
        if p+pp < -115 or p+pp > max_level:
            continue
        power_levels_dbm.append(p + pp)
power_levels_dbm.append(max_level)

print("Number of power levels: ", len(power_levels_dbm))
print("Number of frequency values: ", len(freq_values_mhz))

# Database 
db_conn=create_db("measurements.db")

# Connect to instruments
rm=pyvisa.ResourceManager()

if True:
    sig_gen = RS_SMHU(rm, "GPIB::25")
else:
    sig_gen = Wiltron_SG1206U(rm, "GPIB::23")

sig_gen.preset()

if False:
    print(sig_gen.conn)
    sig_gen.set_freq(200)
    sig_gen.set_level(-20)
    sig_gen.set_output(True)

    sys.exit(0)

dmv=HP3478A("GPIB::7")

# Initialize signal generator
sig_gen.set_output(True)        # RF output on

# Do all the measurements...
cur_session = create_session(db_conn, "V/dBm graph")
freq_power_v_graph(db_conn, cur_session, freq_values_mhz, power_levels_dbm, 10)

