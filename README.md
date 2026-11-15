# Optics Communications Library

This repository contains Python libraries and examples for optical communications calculations.

## Library

- `optics_lib.py`: Core library with optical calculations functions

## Examples

- `example1.py`: Basic optics calculations (Snell's law, fiber NA, power ratios)
- `example2.py`: Advanced optics calculations (Gaussian beams, mode field diameters, etc.)

## Usage

```python
import optics_lib

# Calculate Snell's law
theta2 = optics_lib.snell_law(n1=1.0, n2=1.5, theta1=30)

# Calculate fiber numerical aperture
na = optics_lib.fiber_numerical_aperture(n_core=1.46, n_cladding=1.40)
```

## Functions

### Basic Optics
- `snell_law(n1, n2, theta1)`: Snell's law refraction calculation
- `power_ratio_db(P1, P2)`: Power ratio in decibels
- `attenuation_coefficient(L, P1, P2)`: Attenuation coefficient

### Fiber Optics  
- `fiber_numerical_aperture(n_core, n_cladding)`: Numerical aperture
- `fiber_acceptance_angle(n_core, n_cladding)`: Acceptance angle
- `fiber_mode_field_diameter(n_core, n_cladding, lambda_, V)`: Mode field diameter
- `fiber_cutoff_wavelength(n_core, n_cladding, a)`: Cutoff wavelength

### Beam Optics
- `rayleigh_range(w0, lambda_)`: Rayleigh range for Gaussian beam
- `gaussian_beam_radius(w0, z, lambda_)`: Beam radius at distance z
- `optical_path_difference(n, d, theta)`: Optical path difference

### Power and Intensity
- `optical_power_from_intensity(intensity, area)`: Calculate power from intensity
- `intensity_from_power(power, area)`: Calculate intensity from power

### Reflection and Transmission
- `reflection_coefficient(n1, n2)`: Reflection coefficient
- `transmission_coefficient(n1, n2)`: Transmission coefficient
- `critical_angle(n1, n2)`: Critical angle for total internal reflection
