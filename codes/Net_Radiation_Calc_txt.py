"""
Calculates Short_Waves_in
Reads from an SQLITE database from DART

author: - Cousseau Pauline
        - Gayrard Tristan   
"""

### Imports
import pandas as pd
data_mode_R = r"C:\Users\pauli\Documents\DART\user_data\simulations\DART_PT_mode_R\output\simulation.properties.txt"
data_mode_T = r"C:\Users\pauli\Documents\DART\user_data\simulations\DART_PT_mode_T\output\simulation.properties.txt"


### Spectral Integration Function
def spectralIntegration(rad=None,waveLength=None):
    # Calculates the Spectral Integration : sum(rad(λ) × Δλ)
    dx = waveLength[1]-waveLength[0]
    ray = sum(rad*dx)
    # print(f"{ray=:.3f} W/m²")
    return ray

def PPFDIntegration(rad=None, waveLength=None):
    mask = (waveLength >= 0.4) & (waveLength <= 0.7)
    waveLength_m = waveLength[mask] 
    N = rad[mask]
    dx = waveLength_m[1] - waveLength_m[0]
    PPFD = sum(N * dx)
    print(f"{PPFD=:.3f} W/m²")
    return PPFD


### Data setup
str_lambda_max  = [f"dart.band{i}.lambdaMax" for i in range(20)]
str_lambda_min  = [f"dart.band{i}.lambdaMin" for i in range(20)]
str_exitance    = [f"dart.band{i}.COUPL.exitance" for i in range(20)]
str_irradiance  = [f"dart.band{i}.COUPL.irradiance" for i in range(20)]

df_R = pd.read_csv(data_mode_R, sep=":", names=['variable', 'value'])
exitance_R      = df_R[df_R['variable'].isin(str_exitance)]["value"].astype(float).values
irradiance_R    = df_R[df_R['variable'].isin(str_irradiance)]["value"].astype(float).values
lambda_R_max    = df_R[df_R['variable'].isin(str_lambda_max)]["value"].astype(float).values
lambda_R_min    = df_R[df_R['variable'].isin(str_lambda_min)]["value"].astype(float).values
lambda_R        = (lambda_R_min+lambda_R_min)/2

df_T = pd.read_csv(data_mode_T, sep=":", names=['variable', 'value'])
exitance_T      = df_T[df_T['variable'].isin(str_exitance)]["value"].astype(float).values
irradiance_T    = df_T[df_T['variable'].isin(str_irradiance)]["value"].astype(float).values
lambda_T_max    = df_T[df_T['variable'].isin(str_lambda_max)]["value"].astype(float).values
lambda_T_min    = df_T[df_T['variable'].isin(str_lambda_min)]["value"].astype(float).values
lambda_T        = (lambda_T_min+lambda_T_min)/2


## Function calls to calculate Rn
SW_out  = spectralIntegration(rad=exitance_R,   waveLength=lambda_R)
SW_in   = spectralIntegration(rad=irradiance_R, waveLength=lambda_R)
LW_out  = spectralIntegration(rad=exitance_T,   waveLength=lambda_T)
LW_in   = spectralIntegration(rad=irradiance_T, waveLength=lambda_T)

Rn = SW_in + LW_in - SW_out - LW_out
print(f"{Rn=:.3f} W/m²")

PPFD_result = PPFDIntegration(rad=irradiance_R, waveLength=lambda_R)