"""
Optics Library for optical communications calculations
"""

import numpy as np
import matplotlib.pyplot as plt

def frequency_to_wavelength(frequency, unit='Hz'):
    """
    Convert frequency to wavelength using the speed of light.
    
    Parameters:
    frequency (float): Frequency value
    unit (str): Unit of frequency ('Hz', 'GHz', 'THz')
    
    Returns:
    float: Wavelength in meters
    """
    # Speed of light in vacuum (m/s)
    c = 299792458
    
    # Convert frequency to Hz if needed
    if unit == 'GHz':
        frequency *= 1e9
    elif unit == 'THz':
        frequency *= 1e12
    
    # Calculate wavelength: λ = c/f
    wavelength = c / frequency
    return wavelength

def wavelength_to_frequency(wavelength, unit='m'):
    """
    Convert wavelength to frequency using the speed of light.
    
    Parameters:
    wavelength (float): Wavelength value
    unit (str): Unit of wavelength ('m', 'nm', 'μm')
    
    Returns:
    float: Frequency in Hz
    """
    # Speed of light in vacuum (m/s)
    c = 299792458
    
    # Convert wavelength to meters if needed
    if unit == 'nm':
        wavelength *= 1e-9
    elif unit == 'μm':
        wavelength *= 1e-6
    
    # Calculate frequency: f = c/λ
    frequency = c / wavelength
    return frequency

def delta_lambda_to_delta_frequency(delta_lambda, lambda_0):
    """
    Convert wavelength bandwidth (Δλ) to frequency bandwidth (Δf).
    
    This function calculates the frequency bandwidth Δf corresponding to a 
    given wavelength bandwidth Δλ around a central wavelength λ₀.
    
    Parameters:
    delta_lambda (float): Wavelength bandwidth (m)
    lambda_0 (float): Central wavelength (m)
    
    Returns:
    float: Frequency bandwidth (Hz)
    
    Formula used:
    Δf = c * Δλ / λ₀²
    where c is the speed of light in vacuum
    
    Example:
    >>> delta_lambda_to_delta_frequency(10e-9, 1550e-9)  # 10 nm bandwidth at 1550 nm
    19375000000.0
    """
    # Speed of light in vacuum (m/s)
    c = 299792458
    
    # Calculate frequency bandwidth: Δf = c * Δλ / λ₀²
    delta_frequency = c * delta_lambda / (lambda_0 ** 2)
    
    return delta_frequency

# Library skeleton with imports
