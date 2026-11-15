#!/usr/bin/env python3
"""
Example script to demonstrate comprehensive power and gain/loss conversion functions.
This script shows how to use all the new conversion utilities in the optics library.
"""

import numpy as np
from optics_lib import (
    power_linear_to_db, power_db_to_linear, power_ratio_db,
    gain_linear_to_db, gain_db_to_linear,
    loss_linear_to_db, loss_db_to_linear
)

print("Comprehensive Conversion Examples")
print("=" * 40)

# Example 1: Power conversions (linear to dB and vice versa)
print("\n1. Power Conversions:")
power_linear = 1e-3  # 1 milliwatt
power_db = power_linear_to_db(power_linear, reference_power=1e-3)  # Reference 1 mW = 0 dBm
print(f"Linear power: {power_linear:.0e} W")
print(f"dB power: {power_db:.2f} dBm")

power_linear_back = power_db_to_linear(power_db, reference_power=1e-3)
print(f"Back to linear: {power_linear_back:.0e} W")

# Example 2: Gain conversions
print("\n2. Gain Conversions:")
gain_linear = 10  # 10x gain
gain_db = gain_linear_to_db(gain_linear)
print(f"Linear gain: {gain_linear:.1f}")
print(f"dB gain: {gain_db:.2f} dB")

gain_linear_back = gain_db_to_linear(gain_db)
print(f"Back to linear: {gain_linear_back:.1f}")

# Example 3: Loss conversions
print("\n3. Loss Conversions:")
loss_linear = 0.1  # 10% loss (0.1x transmission)
loss_db = loss_linear_to_db(loss_linear)
print(f"Linear loss: {loss_linear:.1f}")
print(f"dB loss: {loss_db:.2f} dB")

loss_linear_back = loss_db_to_linear(loss_db)
print(f"Back to linear: {loss_linear_back:.1f}")

# Example 4: Practical optical communications example
print("\n4. Optical Communications Example:")
# Fiber optic system with gain/loss components
input_power = 1e-3   # 1 mW input
fiber_loss = 0.8     # 20% loss (0.8x transmission)
amplifier_gain = 5   # 5x gain
output_power = input_power * fiber_loss * amplifier_gain

print(f"Input power: {input_power:.0e} W ({power_linear_to_db(input_power, 1e-3):.1f} dBm)")
print(f"Fiber loss: {fiber_loss:.1f} (20% loss)")
print(f"Amplifier gain: {amplifier_gain:.0f}x")
print(f"Output power: {output_power:.0e} W ({power_linear_to_db(output_power, 1e-3):.1f} dBm)")

# Calculate total loss/gain in dB
total_loss_db = power_ratio_db(input_power, output_power)  # This will be negative for loss
print(f"Total system loss: {total_loss_db:.1f} dB")

# Example 5: Batch processing
print("\n5. Batch Processing:")
# Multiple gain values
gains_linear = [1, 2, 5, 10, 20]
print("Linear gains:", [f"{g:.0f}" for g in gains_linear])
gains_db = [gain_linear_to_db(g) for g in gains_linear]
print("dB gains:", [f"{g:.1f}" for g in gains_db])

# Multiple loss values
losses_linear = [1, 0.5, 0.1, 0.01]
print("\nLinear losses:", [f"{l:.2f}" for l in losses_linear])
losses_db = [loss_linear_to_db(l) for l in losses_linear]
print("dB losses:", [f"{l:.1f}" for l in losses_db])

# Example 6: Signal-to-noise ratio (SNR)
print("\n6. Signal-to-Noise Ratio:")
signal_power = 1e-6  # 1 μW
noise_power = 1e-12  # 1 pW
snr_linear = signal_power / noise_power
snr_db = power_ratio_db(signal_power, noise_power)
print(f"Signal power: {signal_power:.0e} W")
print(f"Noise power: {noise_power:.0e} W")
print(f"SNR linear: {snr_linear:.0e}")
print(f"SNR dB: {snr_db:.1f} dB")

print("\nAll examples completed successfully!")