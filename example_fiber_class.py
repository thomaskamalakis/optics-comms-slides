#!/usr/bin/env python3
"""
Example script to demonstrate the Fiber class usage.
This script shows how to create and use Fiber objects with the new class.
"""

from optics_lib import Fiber

print("Fiber Class Examples")
print("=" * 20)

# Example 1: Create a standard single-mode fiber
print("\n1. Standard Single-Mode Fiber:")
smf = Fiber(n1=1.46, n2=1.44, a_dB=0.2, D=16)
print(f"Core refractive index (n1): {smf.n1}")
print(f"Cladding refractive index (n2): {smf.n2}")
print(f"Attenuation coefficient (a_dB): {smf.a_dB} dB/km")
print(f"Dispersion coefficient (D): {smf.D} ps/(nm·km)")
print(f"β² parameter: {smf.beta2:.2e} s²/m")

# Example 2: Create a different fiber type
print("\n2. Different Fiber Type:")
dispersion_aware_fiber = Fiber(n1=1.48, n2=1.46, a_dB=0.15, D=20)
print(f"Core refractive index (n1): {dispersion_aware_fiber.n1}")
print(f"Cladding refractive index (n2): {dispersion_aware_fiber.n2}")
print(f"Attenuation coefficient (a_dB): {dispersion_aware_fiber.a_dB} dB/km")
print(f"Dispersion coefficient (D): {dispersion_aware_fiber.D} ps/(nm·km)")
print(f"β² parameter: {dispersion_aware_fiber.beta2:.2e} s²/m")

# Example 3: Access all parameters
print("\n3. Parameter Access:")
print("All fiber parameters can be accessed directly:")
print(f"smf.n1 = {smf.n1}")
print(f"smf.n2 = {smf.n2}")
print(f"smf.a_dB = {smf.a_dB}")
print(f"smf.D = {smf.D}")
print(f"smf.beta2 = {smf.beta2:.2e}")

# Example 4: Practical usage in optical calculations
print("\n4. Practical Usage:")
# Calculate attenuation over distance
distance_km = 100  # km
total_loss_dB = smf.a_dB * distance_km
print(f"For a {distance_km} km fiber span:")
print(f"Total loss: {total_loss_dB:.2f} dB")

# Calculate dispersion effects
wavelength_nm = 1550  # nm
dispersion_effect = smf.D * wavelength_nm * 1e-3  # Convert to ps·nm
print(f"At {wavelength_nm} nm, dispersion effect: {dispersion_effect:.2f} ps")

print("\nFiber class example completed successfully!")