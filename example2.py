#!/usr/bin/env python3
"""
Example 2: Advanced optics calculations using optics_lib
"""

import optics_lib

# Example 1: Gaussian Beam Propagation
print("=== Gaussian Beam Propagation ===")
w0 = 1e-6  # Beam waist radius (1 micrometer)
lambda_ = 1.55e-6  # Wavelength (1.55 micrometers)
z = 10e-3  # Propagation distance (10 mm)

z_r = optics_lib.rayleigh_range(w0, lambda_)
print(f"Rayleigh range: {z_r:.2e} m")

w_z = optics_lib.gaussian_beam_radius(w0, z, lambda_)
print(f"Beam radius at z={z*1000:.0f}mm: {w_z*1000:.2f} mm")

# Example 2: Fiber Mode Field Diameter
print("
=== Fiber Mode Field Diameter ===")
V = 2.405  # V-number (fundamental mode)
mode_diameter = optics_lib.fiber_mode_field_diameter(n_core, n_cladding, lambda_, V)
print(f"Mode field diameter: {mode_diameter*1000:.2f} mm")

# Example 3: Optical Power and Intensity
print("
=== Optical Power and Intensity ===")
intensity = 1000  # W/m^2
area = 1e-6  # m^2 (1 mm^2)
power = optics_lib.optical_power_from_intensity(intensity, area)
print(f"Power from intensity: I={intensity} W/m², A={area*1e6:.0f} mm² → P={power*1000:.2f} mW")

# Example 4: Reflection and Transmission
print("
=== Reflection and Transmission ===")
r = optics_lib.reflection_coefficient(n1, n2)
t = optics_lib.transmission_coefficient(n1, n2)
print(f"Reflection coefficient (n1={n1}, n2={n2}): {r:.3f}")
print(f"Transmission coefficient (n1={n1}, n2={n2}): {t:.3f}")

# Example 5: Critical Angle
print("
=== Critical Angle ===")
try:
    critical = optics_lib.critical_angle(n_core, n_cladding)
    print(f"Critical angle for core/cladding: {critical:.2f}°")
except ValueError as e:
    print(f"Error: {e}")

# Example 6: Cutoff Wavelength
print("
=== Cutoff Wavelength ===")
a = 5e-6  # Core radius (5 micrometers)
cutoff_wavelength = optics_lib.fiber_cutoff_wavelength(n_core, n_cladding, a)
print(f"Cutoff wavelength: {cutoff_wavelength*1000:.2f} mm")

# Example 7: Optical Path Difference
print("
=== Optical Path Difference ===")
n = 1.5  # Refractive index
d = 1e-3  # Geometric path (1 mm)
theta = 30  # Angle of incidence (degrees)

opd = optics_lib.optical_path_difference(n, d, theta)
print(f"Optical path difference: n={n}, d={d*1000:.0f}mm, θ={theta}° → OPD={opd:.2e} m")

print("
=== Example completed ===")
