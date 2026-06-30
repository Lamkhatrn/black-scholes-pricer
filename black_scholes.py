import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
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


# ── Visualisation : prix et Greeks en fonction de S ──────────────────────────
S_range = np.linspace(100, 200, 200)

calls = []
puts = []
deltas_call = []
gammas = []
vegas = []

for s in S_range:
    c, p = prix_call_put(s, K, T, r, sigma)
    g = greeks(s, K, T, r, sigma)
    calls.append(c)
    puts.append(p)
    deltas_call.append(g["delta_call"])
    gammas.append(g["gamma"])
    vegas.append(g["vega"])

fig, axes = plt.subplots(2, 2, figsize=(13, 9))
fig.suptitle("Black-Scholes : Prix et Greeks en fonction du prix de l'action",
             fontsize=14, fontweight="bold")

# Prix call/put
ax1 = axes[0, 0]
ax1.plot(S_range, calls, label="Call", color="#4C72B0", linewidth=2)
ax1.plot(S_range, puts, label="Put", color="#E74C3C", linewidth=2)
ax1.axvline(K, color="gray", linestyle="--", linewidth=1, label=f"K = {K}")
ax1.set_xlabel("Prix de l'action S (€)")
ax1.set_ylabel("Prix de l'option (€)")
ax1.set_title("Prix Call/Put vs S")
ax1.legend()

# Delta
ax2 = axes[0, 1]
ax2.plot(S_range, deltas_call, color="#55A868", linewidth=2)
ax2.axvline(K, color="gray", linestyle="--", linewidth=1)
ax2.set_xlabel("Prix de l'action S (€)")
ax2.set_ylabel("Delta")
ax2.set_title("Delta Call vs S")

# Gamma
ax3 = axes[1, 0]
ax3.plot(S_range, gammas, color="#8172B2", linewidth=2)
ax3.axvline(K, color="gray", linestyle="--", linewidth=1)
ax3.set_xlabel("Prix de l'action S (€)")
ax3.set_ylabel("Gamma")
ax3.set_title("Gamma vs S (max proche de K)")

# Vega
ax4 = axes[1, 1]
ax4.plot(S_range, vegas, color="#C44E52", linewidth=2)
ax4.axvline(K, color="gray", linestyle="--", linewidth=1)
ax4.set_xlabel("Prix de l'action S (€)")
ax4.set_ylabel("Vega")
ax4.set_title("Vega vs S (max proche de K)")

plt.tight_layout()
plt.savefig("black_scholes_greeks.png", dpi=150, bbox_inches="tight")
print("\nGraphique sauvegardé : black_scholes_greeks.png")