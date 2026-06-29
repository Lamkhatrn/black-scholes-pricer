import numpy as np
from scipy.stats import norm
def calcul_d1_d2(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + sigma**2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return d1, d2

# Test avec nos valeurs d'exemple
S = 150       # Prix actuel de l'action
K = 155       # Prix d'exercice
T = 0.25      # 3 mois = 0.25 an
r = 0.03      # Taux sans risque 3%
sigma = 0.25  # Volatilité 25%

d1, d2 = calcul_d1_d2(S, K, T, r, sigma)
print(f"d1 = {d1:.4f}")
print(f"d2 = {d2:.4f}")


