#! /usr/bin/env python3

import time
import sqlite3

import pyvisa
from pymeasure.instruments.hp import HP3478A

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

def freq_power_v_graph(conn, session_id, freq_values, power_levels, nr_samples):
    for f in freq_values_mhz:
        swp_gen.write(f"F1{f}MH")

        for p in power_levels_dbm:
            swp_gen.write(f"LVL{p}DM")
            time.sleep(0.5)
            for i in range(0,nr_samples):
                time.sleep(0.2)
                v = dmv.measure_DCV
                print(f"Freq={f}MHz, Power={p}dBm -> {v}V")
                record_measurement(conn, session_id, f, p, v)

            print()
    pass


# Frequency values to measure
freq_values_mhz = [ 10, 30, 50, 70, 100, 200, 500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 100000, 11000, 12000, 13000, 15000, 17000, 19000 ]


# Power levels to measure
power_levels_dbm = [ 
    -115, -110, -100, -90, -80, -70]

for p in range(-60, 20, 10):
    for pp in [0, 3, 7]:
        if p+pp < -115 or p+pp > 15:
            continue
        power_levels_dbm.append(p + pp)
power_levels_dbm.append(15)

print("Number of power levels: ", len(power_levels_dbm))
print("Number of frequency values: ", len(freq_values_mhz))

# Database 
conn=create_db("measurements.db")

# Connect to instruments
dmv=HP3478A("GPIB::7")
rm=pyvisa.ResourceManager()
swp_gen=rm.open_resource("GPIB::23")

# Initialize signal generator
swp_gen.write("RF1")            # RF output on
swp_gen.write("IL1")            # Internal leveling - for now

# Do all the measurements...
cur_session = create_session(conn, "V/dBm graph")
freq_power_v_graph(conn, cur_session, freq_values_mhz, power_levels_dbm, 10)

