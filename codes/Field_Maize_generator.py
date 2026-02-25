"""
Field_Maize_generator

--> Create .txt file of a field full of 
    different maize crops to give as a Dart input

Authors :   - Cousseau Pauline
            - Gayrard Tristan
"""

import numpy as np

# Paramètres du champ
l_total = 100       # Longueur (m)
L_total = 100       # Largeur (m)
row_space = 0.6     # Distance entre les rangs (X)
col_space = 0.3     # Distance entre les plants (Y)

# Index des modèles DART
FEMALE_CORN = 0
MALE_CORN = 1

# Paramètres de transformation par défaut
pos_z = 0
scale_x, scale_y, scale_z = 1, 1, 1
rot_x, rot_y, rot_z = 0, 0, 0

header = """
/* 
3D_Model_Index Pos_X Pos_Y Pos_Z Scale_X Scale_Y Scale_Z Rotate_X Rotate_Y Rotate_Z 
*/

complete transformation

"""

filename = "field_maize_config.txt"

with open(filename, "w") as f:
    f.write(header)
    
    # On itère sur les rangs (X)
    # enumerate permet de compter l'indice du rang pour alterner mâle/femelle
    for row_idx, x in enumerate(np.arange(0, L_total, row_space)):
        
        # Logique : 1 rang de mâles tous les 4 rangs de femelles
        # Cela signifie un cycle de 5 rangs : F, F, F, F, M
        if (row_idx + 1) % 5 == 0:
            current_model = MALE_CORN
        else:
            current_model = FEMALE_CORN
            
        # On itère sur les positions dans le rang (Y)
        for y in np.arange(0, l_total, col_space):
            line = f"{current_model} {x:.3f} {y:.3f} {pos_z} {scale_x} {scale_y} {scale_z} {rot_x} {rot_y} {rot_z}\n"
            f.write(line)

print(f"Fichier {filename} généré avec succès.")