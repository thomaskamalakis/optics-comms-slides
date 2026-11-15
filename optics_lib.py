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

def delta_lambda_to_delta_frequency(delta_lambda, lambda_0, method='exact'):
    """
    Convert wavelength bandwidth (Δλ) to frequency bandwidth (Δf).
    
    This function calculates the frequency bandwidth Δf corresponding to a 
    given wavelength bandwidth Δλ around a central wavelength λ₀.
    
    Parameters:
    delta_lambda (float): Wavelength bandwidth (m)
    lambda_0 (float): Central wavelength (m)
    method (str): Calculation method ('exact' or 'approximate')
    
    Returns:
    float: Frequency bandwidth (Hz)
    
    Formula used:
    - For 'exact': Calculate λ₁ = λ₀ - Δλ/2 and λ₂ = λ₀ + Δλ/2,
      then Δf = c/λ₁ - c/λ₂
    - For 'approximate': Δf = c × Δλ / λ₀²
    
    Example:
    >>> delta_lambda_to_delta_frequency(10e-9, 1550e-9)  # Default exact method
    19375000000.0
    >>> delta_lambda_to_delta_frequency(10e-9, 1550e-9, method='approximate')
    19375000000.0
    """
    # Speed of light in vacuum (m/s)
    c = 299792458
    
    if method == 'exact':
        # Calculate exact values using the two wavelength limits
        lambda_1 = lambda_0 - delta_lambda / 2
        lambda_2 = lambda_0 + delta_lambda / 2
        
        # Calculate frequency difference: Δf = c/λ₁ - c/λ₂
        delta_frequency = c / lambda_1 - c / lambda_2
        
    elif method == 'approximate':
        # Use the approximate formula: Δf = c × Δλ / λ₀²
        delta_frequency = c * delta_lambda / (lambda_0 ** 2)
        
    else:
        raise ValueError("Method must be 'exact' or 'approximate'")
    
    return delta_frequency

def power_linear_to_db(power_linear, reference_power=1.0):
    """
    Convert linear power to decibel (dB) scale.
    
    Parameters:
    power_linear (float): Power in linear scale
    reference_power (float): Reference power level (default 1.0 for dBm, 1.0 for dB)
    
    Returns:
    float: Power in dB scale
    
    Formula used:
    P(dB) = 10 * log10(P_linear / P_reference)
    """
    if power_linear <= 0:
        raise ValueError("Power must be positive")
    
    return 10 * np.log10(power_linear / reference_power)

def power_db_to_linear(power_db, reference_power=1.0):
    """
    Convert decibel (dB) power to linear scale.
    
    Parameters:
    power_db (float): Power in dB scale
    reference_power (float): Reference power level (default 1.0 for dBm, 1.0 for dB)
    
    Returns:
    float: Power in linear scale
    
    Formula used:
    P_linear = P_reference * 10^(P_dB / 10)
    """
    return reference_power * np.power(10, power_db / 10)

def power_ratio_db(power1, power2):
    """
    Calculate the power ratio in decibels.
    
    Parameters:
    power1 (float): First power value
    power2 (float): Second power value
    
    Returns:
    float: Power ratio in dB
    
    Formula used:
    P_ratio(dB) = 10 * log10(P1 / P2)
    """
    if power1 <= 0 or power2 <= 0:
        raise ValueError("Power values must be positive")
    
    return 10 * np.log10(power1 / power2)

def gain_linear_to_db(gain_linear, reference_gain=1.0):
    """
    Convert linear gain to decibel (dB) scale.
    
    Parameters:
    gain_linear (float): Gain in linear scale
    reference_gain (float): Reference gain level (default 1.0 for dB)
    
    Returns:
    float: Gain in dB scale
    
    Formula used:
    G(dB) = 10 * log10(G_linear / G_reference)
    """
    if gain_linear <= 0:
        raise ValueError("Gain must be positive")
    
    return 10 * np.log10(gain_linear / reference_gain)

def gain_db_to_linear(gain_db, reference_gain=1.0):
    """
    Convert decibel (dB) gain to linear scale.
    
    Parameters:
    gain_db (float): Gain in dB scale
    reference_gain (float): Reference gain level (default 1.0 for dB)
    
    Returns:
    float: Gain in linear scale
    
    Formula used:
    G_linear = G_reference * 10^(G_dB / 10)
    """
    return reference_gain * np.power(10, gain_db / 10)

def loss_linear_to_db(loss_linear, reference_loss=1.0):
    """
    Convert linear loss to decibel (dB) scale.
    
    Parameters:
    loss_linear (float): Loss in linear scale
    reference_loss (float): Reference loss level (default 1.0 for dB)
    
    Returns:
    float: Loss in dB scale
    
    Formula used:
    L(dB) = 10 * log10(L_linear / L_reference)
    """
    if loss_linear <= 0:
        raise ValueError("Loss must be positive")
    
    return 10 * np.log10(loss_linear / reference_loss)

def loss_db_to_linear(loss_db, reference_loss=1.0):
    """
    Convert decibel (dB) loss to linear scale.
    
    Parameters:
    loss_db (float): Loss in dB scale
    reference_loss (float): Reference loss level (default 1.0 for dB)
    
    Returns:
    float: Loss in linear scale
    
    Formula used:
    L_linear = L_reference * 10^(L_dB / 10)
    """
    return reference_loss * np.power(10, loss_db / 10)

class Fiber:
    """
    Fiber class representing optical fiber properties.
    
    This class encapsulates the key physical parameters of an optical fiber
    including refractive indices, attenuation coefficients, and dispersion 
    parameters.
    
    Parameters:
    n1 (float): Core refractive index
    n2 (float): Cladding refractive index  
    a_dB (float): Attenuation coefficient in dB/km
    D (float): Dispersion coefficient in ps/(nm·km)
    
    Example:
    >>> fiber = Fiber(n1=1.46, n2=1.44, a_dB=0.2, D=16)
    >>> print(fiber.n1, fiber.n2, fiber.a_dB, fiber.D)
    1.46 1.44 0.2 16
    """
    
    def __init__(self, n1, n2, a_dB, D):
        """
        Initialize a Fiber object with its key parameters.
        
        Parameters:
        n1 (float): Core refractive index
        n2 (float): Cladding refractive index  
        a_dB (float): Attenuation coefficient in dB/km
        D (float): Dispersion coefficient in ps/(nm·km)
        """
        self.n1 = n1  # Core refractive index
        self.n2 = n2  # Cladding refractive index
        self.a_dB = a_dB  # Attenuation coefficient in dB/km
        self.D = D  # Dispersion coefficient in ps/(nm·km)
        
        # Calculate equivalent β² parameter (second derivative of phase constant)
        # β² = -D × λ₀² / (2πc) where c is speed of light and λ₀ is reference wavelength
        # Using standard reference wavelength of 1550 nm (1.55 μm)
        lambda_ref_m = 1.55e-6  # Reference wavelength in meters (1550 nm)
        self.beta2 = -self.D * lambda_ref_m**2 / (2 * np.pi * 299792458)  # s²/m

# Library skeleton with imports
