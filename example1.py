#!/usr/bin/env python3
"""
Example 1: Basic optics calculations using optics_lib
"""

import optics_lib

# Example 1: Snell's Law
print("=== Snell's Law Examples ===")
n1 = 1.0  # Air
n2 = 1.5  # Glass
theta1 = 30  # degrees

theta2 = optics_lib.snell_law(n1, n2, theta1)
if theta2 is not None:
    print(f"Snell's Law: n1={n1}, n2={n2}, θ1={theta1}° → θ2={theta2:.2f}°")
else:
    print(f"Total internal reflection occurs for n1={n1}, n2={n2}, θ1={theta1}°")

# Example 2: Fiber Numerical Aperture
print("
=== Fiber Numerical Aperture ===")
n_core = 1.46  # Silica fiber core
n_cladding = 1.40  # Silica fiber cladding
na = optics_lib.fiber_numerical_aperture(n_core, n_cladding)
print(f"Fiber NA: n_core={n_core}, n_cladding={n_cladding} → NA={na:.3f}")

# Example 3: Acceptance Angle
print("
=== Fiber Acceptance Angle ===")
acceptance_angle = optics_lib.fiber_acceptance_angle(n_core, n_cladding)
print(f"Fiber acceptance angle: {acceptance_angle:.2f}°")

# Example 4: Power Ratio in dB
print("
=== Power Ratio in dB ===")
P1 = 1.0  # Input power (W)
P2 = 0.5  # Output power (W)
ratio_db = optics_lib.power_ratio_db(P1, P2)
print(f"Power ratio: P1={P1}W, P2={P2}W → {ratio_db:.2f} dB")

# Example 5: Attenuation Coefficient
print("
=== Attenuation Coefficient ===")
L = 10  # Fiber length (km)
att_coeff = optics_lib.attenuation_coefficient(L, P1, P2)
print(f"Attenuation coefficient: L={L}km, P1={P1}W, P2={P2}W → {att_coeff:.3f} dB/km")

print("
=== Example completed ===")
