#! /usr/bin/env python3

import sqlite3
import pandas as pd

if False:
    conn = sqlite3.connect("measurements.db")
    c = conn.cursor()
    c.execute("select freq,power_dbm,v from measurements where session_id=1 order by created")
    rows = c.fetchall()
    for row in rows:
        (freq, power_dbm, v) = row
        print(freq, power_dbm, v)

if True:
    conn = sqlite3.connect("measurements.db")
    df = pd.read_sql_query("select * from measurements where session_id=1 order by created", conn)
    print(df)

