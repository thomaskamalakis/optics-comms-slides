"""
Fiber class using constants from optics_lib.py
"""

# Import constants from optics_lib.py
from optics_lib import C, K_B, E, H

import numpy as np

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
        self.beta2 = -self.D * lambda_ref_m**2 / (2 * np.pi * C)  # s²/m

# Example usage
if __name__ == "__main__":
    # Create a standard single-mode fiber
    smf = Fiber(n1=1.46, n2=1.44, a_dB=0.2, D=16)
    print(f"Core refractive index (n1): {smf.n1}")
    print(f"Cladding refractive index (n2): {smf.n2}")
    print(f"Attenuation coefficient (a_dB): {smf.a_dB} dB/km")
    print(f"Dispersion coefficient (D): {smf.D} ps/(nm·km)")
    print(f"β² parameter: {smf.beta2:.2e} s²/m")