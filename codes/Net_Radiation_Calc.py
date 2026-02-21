"""
Calculates Short_Waves_in
Reads from an SQLITE database from DART

author: Tristan GAYRARD
"""

### Imports
import sqlite3
import numpy as np
import pandas as pd

### Data setup
db_filepath = r"data/Projet_Cousseau_Gayrard.db"

### Create an SQL connection and retrieves the data in a dataframe
con = sqlite3.connect(db_filepath)
cur = con.cursor()
df1 = pd.read_sql_query("SELECT valueResult AS exitance from Exitance LIMIT 20 ", con)
df2 = pd.read_sql_query("SELECT valueCentralWavelength AS lambda from SpectralBand LIMIT 20", con)
df3 = pd.read_sql_query("SELECT valueResult AS radiance from Radiance LIMIT 20 ", con)
df2 = df2*1e6
con.close()
df = df1.join(df2).join(df3)
# print(df)

### Spectral Integration Function
def spectralIntegration(rad=None,waveLength=None):
    # Calculates the Spectral Integration : sum(SW(λ) × Δλ)
    dt = waveLength[1]-waveLength[0]
    ray = sum(rad*dt)
    print(f"{ray=:.3f} W/m²")
    return ray

SW_in = spectralIntegration(rad=df["exitance"], waveLength=df["lambda"])
SW_out = spectralIntegration(rad=df["radiance"], waveLength=df["lambda"])