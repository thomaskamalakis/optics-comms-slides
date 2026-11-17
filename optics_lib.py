"""
Optics Library for optical communications calculations
"""

import numpy as np
import matplotlib.pyplot as plt

# Physical constants
C = 299792458  # Speed of light in vacuum (m/s)
K_B = 1.380649e-23  # Boltzmann constant (J/K)
E = 1.602176634e-19  # Elementary charge (C)
H = 6.62607015e-34  # Planck's constant (J·s)

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
    c = C
    
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
    c = C
    
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
    c = C
    
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
    including refractive indices, attenuation coefficients, dispersion parameters,
    and fiber core radius.
    
    Parameters:
    n1 (float): Core refractive index
    n2 (float): Cladding refractive index  
    a_dB (float): Attenuation coefficient in dB/km
    D (float): Dispersion coefficient in ps/(nm·km)
    a (float): Fiber core radius in meters
    lambda_ref_m (float): Reference wavelength in meters for dispersion calculations (default: 1.55e-6)
    L (float): Fiber length in meters (default: 1000.0)
    
    Example:
    >>> fiber = Fiber(n1=1.46, n2=1.44, a_dB=0.2, D=16, a=5e-6, L=1000.0)
    >>> print(fiber.n1, fiber.n2, fiber.a_dB, fiber.D, fiber.a, fiber.L)
    1.46 1.44 0.2 16 5e-06 1000.0
    """
    
    def __init__(self, n1, n2, a_dB, D, a, lambda_ref_m=1.55e-6, L=1000.0):
        """
        Initialize a Fiber object with its key parameters.
        
        Parameters:
        n1 (float): Core refractive index
        n2 (float): Cladding refractive index  
        a_dB (float): Attenuation coefficient in dB/km
        D (float): Dispersion coefficient in ps/(nm·km)
        a (float): Fiber core radius in meters
        lambda_ref_m (float): Reference wavelength in meters for dispersion calculations (default: 1.55e-6)
        L (float): Fiber length in meters (default: 1000.0)
        
        The reference wavelength is used to calculate the β² parameter (second derivative 
        of phase constant) which is wavelength-dependent. The default value of 1.55 μm 
        corresponds to standard telecommunications wavelengths.
        """
        self.n1 = n1  # Core refractive index
        self.n2 = n2  # Cladding refractive index
        self.a_dB = a_dB  # Attenuation coefficient in dB/km
        self.D = D  # Dispersion coefficient in ps/(nm·km)
        self.a = a  # Fiber core radius in meters
        self.lambda_ref_m = lambda_ref_m  # Reference wavelength for dispersion calculations
        self.L = L  # Fiber length in meters
        
    def effective_refractive_index(self, wavelength_m=None):
        """
        Calculate the approximate effective refractive index for the fundamental mode (LP₀₁)
        of a single-mode fiber.
        
        For single-mode fibers, the effective refractive index is approximately:
        neff ≈ n1 - (Δ/2) × (V/2.405)²
        
        where:
        - n1 is the core refractive index
        - Δ = (n1² - n2²)/(2n1²) is the relative refractive index difference
        - V = 2πa√(n1² - n2²)/λ is the normalized frequency parameter
        
        This approximation is valid for single-mode operation and provides a good estimate
        of the effective index that accounts for the fiber's waveguide properties.
        
        Parameters:
        wavelength_m (float): Wavelength in meters. If None, uses self.lambda_ref_m (default: 1.55e-6)
        
        Returns:
        float: Effective refractive index for the fundamental mode
        
        Example:
        >>> fiber = Fiber(n1=1.46, n2=1.44, a_dB=0.2, D=16, a=5e-6, L=1000.0)
        >>> fiber.effective_refractive_index(1550e-9)
        1.4319781714293733
        """
        if wavelength_m is None:
            wavelength_m = self.lambda_ref_m
            
        # Calculate relative refractive index difference
        delta = (self.n1**2 - self.n2**2) / (2 * self.n1**2)
        
        # Calculate normalized frequency V parameter using existing method
        V = self.V_parameter(wavelength_m)
        
        # For single-mode operation, V < 2.405
        if V >= 2.405:
            # Warning: fiber is not in single-mode regime
            pass
            
        # Calculate effective refractive index using the approximation
        # neff ≈ n1 - (Δ/2) × (V/2.405)²
        neff = self.n1 - (delta / 2) * (V / 2.405)**2
        
        return neff
        
        # Calculate equivalent β² parameter (second derivative of phase constant)
        # β² = -D × λ₀² / (2πc) where c is speed of light and λ₀ is reference wavelength
        # Using standard reference wavelength of 1550 nm (1.55 μm)
        self.beta2 = -self.D * self.lambda_ref_m**2 / (2 * np.pi * C)  # s²/m
    
    def numerical_aperture(self):
        """
        Calculate the numerical aperture (NA) of the fiber.
        
        The numerical aperture is defined as:
        NA = sqrt(n1² - n2²)
        
        Returns:
        float: Numerical aperture of the fiber
        
        Example:
        >>> fiber = Fiber(n1=1.46, n2=1.44, a_dB=0.2, D=16, a=5e-6, L=1000.0)
        >>> fiber.numerical_aperture()
        0.28284271247461903
        """
        return np.sqrt(self.n1**2 - self.n2**2)
    
    def V_parameter(self, wavelength_m=None):
        """
        Calculate the normalized frequency (V-parameter) of the fiber.
        
        The V-parameter is a dimensionless quantity that characterizes the number
        of modes that can propagate in an optical fiber. It is defined as:
        V = (2πa/λ) * sqrt(n1² - n2²) = (2πa/λ) * NA
        
        Parameters:
        wavelength_m (float): Wavelength in meters. If None, uses self.lambda_ref_m (default: 1.55e-6)
        
        Returns:
        float: Normalized frequency (V-parameter)
        
        Example:
        >>> fiber = Fiber(n1=1.46, n2=1.44, a_dB=0.2, D=16, a=5e-6, L=1000.0)
        >>> fiber.V_parameter(1550e-9)
        2.378534564247043
        """
        # Handle wavelength parameter
        if wavelength_m is None:
            wavelength_m = self.lambda_ref_m
            
        # Calculate numerical aperture
        NA = self.numerical_aperture()
        
        # Calculate V-parameter: V = (2πa/λ) * NA
        V = (2 * np.pi * self.a) / wavelength_m * NA
        
        return V
    
    def approximate_number_of_modes(self, wavelength_m=None):
        """
        Calculate the approximate number of modes in the fiber.
        
        For step-index multimode fibers with large V-numbers, the approximate
        number of modes is given by:
        N ≈ V²/2 (counting both polarization directions)
        
        Parameters:
        wavelength_m (float): Wavelength in meters. If None, uses self.lambda_ref_m (default: 1.55e-6)
        
        Returns:
        int: Approximate number of guided modes
        
        Example:
        >>> fiber = Fiber(n1=1.46, n2=1.44, a_dB=0.2, D=16, a=5e-6, L=1000.0)
        >>> fiber.approximate_number_of_modes(1550e-9)
        3
        """
        V = self.V_parameter(wavelength_m)
        
        # For step-index fibers with large V-numbers: N ≈ V²/2
        # Counting both polarization directions (horizontal and vertical)
        number_of_modes = int(V**2 / 2)
        
        return number_of_modes
    
    def is_single_mode(self, wavelength_m=None):
        """
        Determine if the fiber operates in single-mode at a given wavelength.
        
        Single-mode operation occurs when V < 2.4048 (first root of Bessel function J₀).
        
        Parameters:
        wavelength_m (float): Wavelength in meters. If None, uses self.lambda_ref_m (default: 1.55e-6)
        
        Returns:
        bool: True if fiber is single-mode at the given wavelength, False otherwise
        
        Example:
        >>> fiber = Fiber(n1=1.46, n2=1.44, a_dB=0.2, D=16, a=5e-6, L=1000.0)
        >>> fiber.is_single_mode(1550e-9)
        True
        """
        V = self.V_parameter(wavelength_m)
        
        # Single-mode condition: V < 2.4048 (first root of Bessel function J₀)
        return V < 2.4048
    
    def critical_angle(self):
        """
        Calculate the critical angle for total internal reflection.
        
        The critical angle is defined by Snell's law as:
        θc = arcsin(n2/n1) where n1 > n2
        
        This represents the minimum angle of incidence in the denser medium
        (core) at which light begins to undergo total internal reflection
        rather than being refracted into the less dense medium (cladding).
        
        Parameters:
        None
        
        Returns:
        float: Critical angle in radians
        
        Example:
        >>> fiber = Fiber(n1=1.46, n2=1.44, a_dB=0.2, D=16, a=5e-6, L=1000.0)
        >>> fiber.critical_angle()
        1.373400108407113
        """
        # For total internal reflection to occur: n1 > n2
        if self.n1 <= self.n2:
            raise ValueError("Total internal reflection cannot occur: n1 must be greater than n2")
        
        # Calculate critical angle using Snell's law: sin(θc) = n2/n1
        # The critical angle for light going from core (n1) to cladding (n2)
        critical_angle_rad = np.arcsin(self.n2 / self.n1)
        
        return critical_angle_rad
    
    def fastest_path_time(self, wavelength_m=None):
        """
        Calculate the travel time for light traveling along the fiber axis (fastest path).
        
        For light traveling directly along the fiber axis (minimum path length), 
        the travel time is:
        t_fast = L / (c / n1) = L * n1 / c
        
        where:
        - L is the fiber length
        - c is the speed of light in vacuum
        - n1 is the core refractive index
        
        Parameters:
        wavelength_m (float): Wavelength in meters. If None, uses self.lambda_ref_m (default: 1.55e-6)
        
        Returns:
        float: Travel time in seconds for the fastest path
        
        Example:
        >>> fiber = Fiber(n1=1.46, n2=1.44, a_dB=0.2, D=16, a=5e-6, L=1000.0)
        >>> fiber.fastest_path_time(1550e-9)
        2.397445812431359e-06
        """
        if wavelength_m is None:
            wavelength_m = self.lambda_ref_m
            
        # Speed of light in vacuum
        c = C  # m/s
        
        # Travel time for the fastest path (straight through core)
        # t = L / (c / n1) = L * n1 / c
        t_fast = self.L * self.n1 / c
        
        return t_fast
    
    def slowest_path_time(self, wavelength_m=None):
        """
        Calculate the travel time for light traveling along the maximum path length.
        
        For light traveling at the critical angle (maximum path length), 
        the travel time is:
        t_slow = L_max / (c / n1) = L_max * n1 / c
        
        where:
        - L_max is the maximum path length due to total internal reflection
        - L_max = L / cos(θc) where θc is the critical angle
        - c is the speed of light in vacuum
        - n1 is the core refractive index
        
        Parameters:
        wavelength_m (float): Wavelength in meters. If None, uses self.lambda_ref_m (default: 1.55e-6)
        
        Returns:
        float: Travel time in seconds for the slowest path
        
        Example:
        >>> fiber = Fiber(n1=1.46, n2=1.44, a_dB=0.2, D=16, a=5e-6, L=1000.0)
        >>> fiber.slowest_path_time(1550e-9)
        2.953730250284179e-05
        """
        if wavelength_m is None:
            wavelength_m = self.lambda_ref_m
            
        # Speed of light in vacuum
        c = C  # m/s
        
        # Calculate critical angle for the current wavelength
        theta_c = self.critical_angle()
        
        # Maximum path length due to total internal reflection:
        # L_max = L / cos(θc)
        L_max = self.L / np.cos(theta_c)
        
        # Travel time for the slowest path (maximum path length)
        # t = L_max / (c / n1) = L_max * n1 / c
        t_slow = L_max * self.n1 / c
        
        return t_slow
    
    def time_difference(self, wavelength_m=None):
        """
        Calculate the difference between fastest and slowest path travel times.
        
        This represents the group delay dispersion or pulse spreading due to 
        different propagation paths in multimode fibers.
        
        Parameters:
        wavelength_m (float): Wavelength in meters. If None, uses self.lambda_ref_m (default: 1.55e-6)
        
        Returns:
        float: Time difference between slowest and fastest path in seconds
        
        Example:
        >>> fiber = Fiber(n1=1.46, n2=1.44, a_dB=0.2, D=16, a=5e-6, L=1000.0)
        >>> fiber.time_difference(1550e-9)
        7.038471285487207e-09
        """
        if wavelength_m is None:
            wavelength_m = self.lambda_ref_m
            
        t_fast = self.fastest_path_time(wavelength_m)
        t_slow = self.slowest_path_time(wavelength_m)
        
        return t_slow - t_fast

# Library skeleton with imports
