# Optics Library Documentation

This document provides detailed information about the optics library functions and their usage.

## Overview

The optics library provides essential mathematical functions for optical communications calculations. It includes basic conversions between frequency and wavelength, as well as specialized functions for calculating bandwidth relationships in optical systems.

## Core Functions

### Frequency and Wavelength Conversions

#### `frequency_to_wavelength(frequency, unit='Hz')`

Converts a frequency value to its corresponding wavelength using the speed of light equation (λ = c/f).

**Parameters:**
- `frequency` (float): The frequency value to convert
- `unit` (str): Unit of frequency ('Hz', 'GHz', 'THz') - default is 'Hz'

**Returns:**
- float: Wavelength in meters

**Example:**
```python
# Convert 193.1 THz to wavelength
wavelength = frequency_to_wavelength(193.1e12, unit='THz')
# Returns approximately 1.550e-06 meters (1550 nm)
```

#### `wavelength_to_frequency(wavelength, unit='m')`

Converts a wavelength value to its corresponding frequency using the speed of light equation (f = c/λ).

**Parameters:**
- `wavelength` (float): The wavelength value to convert
- `unit` (str): Unit of wavelength ('m', 'nm', 'μm') - default is 'm'

**Returns:**
- float: Frequency in Hz

**Example:**
```python
# Convert 1550 nm to frequency
frequency = wavelength_to_frequency(1550e-9, unit='nm')
# Returns approximately 1.937e+14 Hz
```

### Bandwidth Calculations

#### `delta_lambda_to_delta_frequency(delta_lambda, lambda_0, method='exact')`

Converts wavelength bandwidth (Δλ) to frequency bandwidth (Δf) for optical systems.

This function offers two calculation methods:
- **Exact method** (`method='exact'`): Calculates the precise difference between frequencies at the wavelength limits
- **Approximate method** (`method='approximate'`): Uses the simplified formula Δf = c × Δλ / λ₀²

**Parameters:**
- `delta_lambda` (float): Wavelength bandwidth in meters
- `lambda_0` (float): Central wavelength in meters
- `method` (str): Calculation method ('exact' or 'approximate') - default is 'exact'

**Returns:**
- float: Frequency bandwidth in Hz

**Example:**
```python
# Calculate frequency bandwidth for 0.1 nm bandwidth at 1550 nm
delta_f = delta_lambda_to_delta_frequency(0.1e-9, 1550e-9)
# Returns approximately 19375000000.0 Hz (19.4 GHz)

# Using approximate method
delta_f_approx = delta_lambda_to_delta_frequency(0.1e-9, 1550e-9, method='approximate')
```

## Mathematical Background

### Speed of Light
The library uses the speed of light in vacuum: **c = 299,792,458 m/s**

### Wavelength-Frequency Relationship
The fundamental relationship between wavelength (λ) and frequency (f):
- λ = c/f  
- f = c/λ

### Bandwidth Conversion
For small bandwidths around a central wavelength λ₀:
- **Exact method**: Δf = c/λ₁ - c/λ₂ where λ₁ = λ₀ - Δλ/2 and λ₂ = λ₀ + Δλ/2
- **Approximate method**: Δf = c × Δλ / λ₀²

## Usage in Optical Communications

This library is particularly useful for:
- Fiber optic system design
- Spectral analysis of optical signals
- Wavelength division multiplexing (WDM) calculations
- Optical filter specifications
- Laser wavelength tuning calculations

The functions provide the mathematical foundation needed for accurate optical communications engineering calculations.