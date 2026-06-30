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


def prix_call_put(S, K, T, r, sigma):
    d1, d2 = calcul_d1_d2(S, K, T, r, sigma)

    N_d1 = norm.cdf(d1)
    N_d2 = norm.cdf(d2)

    call = S * N_d1 - K * np.exp(-r * T) * N_d2
    put = K * np.exp(-r * T) * (1 - N_d2) - S * (1 - N_d1)

    return call, put


# Test
call, put = prix_call_put(S, K, T, r, sigma)
print(f"\nN(d1) = {norm.cdf(d1):.4f}")
print(f"N(d2) = {norm.cdf(d2):.4f}")
print(f"Prix du Call = {call:.2f} €")
print(f"Prix du Put  = {put:.2f} €")


def greeks(S, K, T, r, sigma):
    d1, d2 = calcul_d1_d2(S, K, T, r, sigma)

    # Densité de probabilité normale (différente de N qui est la fonction de répartition)
    phi_d1 = norm.pdf(d1)

    delta_call = norm.cdf(d1)
    delta_put = norm.cdf(d1) - 1

    gamma = phi_d1 / (S * sigma * np.sqrt(T))

    vega = S * phi_d1 * np.sqrt(T) / 100  # divisé par 100 pour avoir l'impact d'1% de vol

    theta_call = (-S * phi_d1 * sigma / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2)) / 365
    theta_put = (-S * phi_d1 * sigma / (2 * np.sqrt(T)) + r * K * np.exp(-r * T) * norm.cdf(-d2)) / 365

    return {
        "delta_call": delta_call,
        "delta_put": delta_put,
        "gamma": gamma,
        "vega": vega,
        "theta_call": theta_call,
        "theta_put": theta_put
    }


# Test
g = greeks(S, K, T, r, sigma)
print(f"\nDelta Call = {g['delta_call']:.4f}")
print(f"Delta Put  = {g['delta_put']:.4f}")
print(f"Gamma      = {g['gamma']:.4f}")
print(f"Vega       = {g['vega']:.4f}")
print(f"Theta Call = {g['theta_call']:.4f} (par jour)")
print(f"Theta Put  = {g['theta_put']:.4f} (par jour)")