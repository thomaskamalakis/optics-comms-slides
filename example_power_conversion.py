#!/usr/bin/env python3
"""
Example script to demonstrate power conversion functions (linear to dB and vice-versa).
This script shows how to use the new power conversion utilities in the optics library.
"""

import numpy as np
from optics_lib import power_linear_to_db, power_db_to_linear, power_ratio_db

print("Power Conversion Examples")
print("=" * 30)

# Example 1: Linear to dB conversion
print("\n1. Linear to dB Conversion:")
power_linear = 1e-3  # 1 milliwatt
power_db = power_linear_to_db(power_linear, reference_power=1e-3)  # Reference 1 mW = 0 dBm
print(f"Linear power: {power_linear:.0e} W")
print(f"dB power: {power_db:.2f} dB")

# Example 2: dB to Linear conversion  
print("\n2. dB to Linear Conversion:")
power_db = 0  # 0 dBm
power_linear = power_db_to_linear(power_db, reference_power=1e-3)  # Reference 1 mW
print(f"dB power: {power_db:.0f} dBm")
print(f"Linear power: {power_linear:.0e} W")

# Example 3: Power ratio in dB
print("\n3. Power Ratio in dB:")
power1 = 1e-3  # 1 mW
power2 = 1e-6  # 1 μW
ratio_db = power_ratio_db(power1, power2)
print(f"Power1: {power1:.0e} W")
print(f"Power2: {power2:.0e} W")
print(f"Ratio in dB: {ratio_db:.2f} dB")

# Example 4: Multiple values
print("\n4. Batch Conversion:")
powers_linear = [1e-9, 1e-6, 1e-3, 1e0]  # 1 nW, 1 μW, 1 mW, 1 W
print("Linear powers (W):", [f"{p:.0e}" for p in powers_linear])

powers_db = [power_linear_to_db(p, reference_power=1e-3) for p in powers_linear]
print("dB powers (dBm):", [f"{p:.1f}" for p in powers_db])

# Example 5: Practical optical communications example
print("\n5. Optical Communications Example:")
# Typical optical power levels in fiber optic systems
p_input = 1e-3   # 1 mW input power
p_output = 1e-6  # 1 μW output power (after 30 dB loss)
loss_db = power_ratio_db(p_input, p_output)
print(f"Input power: {p_input:.0e} W ({power_linear_to_db(p_input, 1e-3):.1f} dBm)")
print(f"Output power: {p_output:.0e} W ({power_linear_to_db(p_output, 1e-3):.1f} dBm)")
print(f"Loss: {loss_db:.1f} dB")

print("\nAll examples completed successfully!")