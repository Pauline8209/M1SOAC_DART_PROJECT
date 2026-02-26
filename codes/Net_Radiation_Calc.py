"""
Calculates Short_Waves_in
Reads from an SQLITE database from DART

author: - Cousseau Pauline
        - Gayrard Tristan   
"""

### Imports
import sqlite3
import pandas as pd


### Data setup
db_mode_R = r"C:\Users\pauli\Documents\DART\user_data\simulations\DART_PT_mode_R\DART_PT_mode_R.db"
db_mode_T = r"C:\Users\pauli\Documents\DART\user_data\simulations\DART_PT_mode_T\DART_PT_mode_T.db"


### Create an SQL connection and retrieves the data in a dataframe
con = sqlite3.connect(db_mode_R)
cur = con.cursor()
df1 = pd.read_sql_query("SELECT valueResult AS exitance_R from Exitance LIMIT 20 ", con)
df2 = pd.read_sql_query("SELECT valueCentralWavelength AS lambda_R from SpectralBand LIMIT 20", con)*1e6
df3 = pd.read_sql_query("SELECT valueResult AS irradiance_R from Irradiance LIMIT 20 ", con)
con.close()
df = df1.join(df2).join(df3)

con = sqlite3.connect(db_mode_T)
cur = con.cursor()
df4 = pd.read_sql_query("SELECT valueResult AS exitance_T from Exitance LIMIT 20 ", con)
df5 = pd.read_sql_query("SELECT valueCentralWavelength AS lambda_T from SpectralBand LIMIT 20", con)*1e6
df6 = pd.read_sql_query("SELECT valueResult AS irradiance_T from Irradiance LIMIT 20 ", con)
con.close()
df = df.join(df4).join(df5).join(df6)


### Spectral Integration Function
def spectralIntegration(rad=None,waveLength=None):
    # Calculates the Spectral Integration : sum(rad(λ) × Δλ)
    dt = waveLength[1]-waveLength[0]
    ray = sum(rad*dt)
    print(f"{ray=:.3f} W/m²")
    return ray


### Function calls to calculate Rn
SW_out = spectralIntegration(rad=df["exitance_R"], waveLength=df["lambda_R"])   # albedo ?
SW_in = spectralIntegration(rad=df["irradiance_R"], waveLength=df["lambda_R"])
LW_out = spectralIntegration(rad=df["exitance_T"], waveLength=df["lambda_T"])   # emission #émmitance ?
LW_in = spectralIntegration(rad=df["irradiance_T"], waveLength=df["lambda_T"])  # eclairement

Rn = SW_in + LW_in - SW_out - LW_out
print(f"{Rn=:.3f} W/m²")