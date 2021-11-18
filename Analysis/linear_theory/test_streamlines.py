import numpy as np
import os
import sys
import matplotlib.pyplot as plt
sys.path.append('../../')
from python_codes.linear_theory_old import calculate_solution, _mu_prime
from python_codes.meteo_analysis import mu


def focus_point(eta_0, Uho_Ustar, Kappa=0.4):
    return eta_0*np.exp(Kappa*Uho_Ustar)


eta_H = 0.5
eta_0 = (2*np.pi*1e-3)/2.5e3
eta_B = 0.1
Fr = 10

max_z = 0.99*eta_H
k_xi = 0.1
k_x = np.linspace(0, 2*2*np.pi, 300)

eta = np.logspace(np.log10(eta_0), np.log10(max_z), 100)

# list = calculate_solution(eta, eta_H, eta_lim, eta_0, eta_B, Fr, max_z, Kappa=0.4, output='full')
list = calculate_solution(eta, eta_H, eta_0, eta_B, Fr, max_z, Kappa=0.4, output='full')

Ux = np.real(mu(eta, eta_0)[None, :] + k_xi*np.exp(1j*k_x[:, None]) * list[0][0, :][None, :])
Uz = np.real(k_xi*np.exp(1j*k_x[:, None]) * list[0][1, :][None, :])

U, W, St, Sn = list[0]
Ax, Bx = np.real(St), np.imag(St)
Cx, Cy = np.real(Sn), np.imag(Sn)

Results = list[1]
coeffs = list[-1]


# plt.semilogy(np.real(U) + _mu_prime(eta, eta_0), eta, '.')
# plt.semilogy(np.imag(U), eta, '.')
plt.semilogy(np.real(W), eta, '.')
plt.semilogy(np.imag(W), eta, '.')
# plt.semilogy(Ax, eta, '.')
# plt.semilogy(Bx, eta, '.')
plt.show()

# #### Free atmosphere


def q(eta_B):
    np.piecwise(eta_B, [eta_B >= 1, eta_B < 1],
                [lambda eta_B: -np.sqrt(1 - 1/eta_B**2),
                 lambda eta_B: 1j*np.sqrt(1/eta_B**2 - 1)])


eta_FA = np.linspace(eta_H, 3*eta_H, 100)
mu_H = mu(eta_H, eta_0)
W = 1j*mu_H*coeffs[-1]
Psi_b = mu_H*(eta_FA[:, None]/eta_H - 1)
Psi1 = W/(-1j*eta_H)
Psi = np.real(Psi_b + k_xi*np.exp(1j*k_x[None, :])*Psi1)

plt.contour(k_x, eta_FA, Psi, levels=30)
plt.plot(k_x, k_xi*(np.cos(k_x) + 0.8), 'k')
plt.ylim(bottom=0)
plt.show()
