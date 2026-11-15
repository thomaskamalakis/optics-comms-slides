#!/usr/bin/env python3
"""
Example script to compare exact and approximate methods for wavelength to frequency bandwidth conversion.
This script demonstrates the difference between the two calculation methods using matplotlib with LaTeX rendering.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from optics_lib import delta_lambda_to_delta_frequency

# Set up the central wavelength (1550 nm)
lambda_0 = 1550e-9  # 1550 nm in meters

# Create array of delta_lambda values from 0.1 nm to 100 nm
delta_lambdas = np.linspace(0.1e-9, 100e-9, 1000)

# Calculate frequency bandwidths using both methods
exact_values = []
approximate_values = []

for delta_lambda in delta_lambdas:
    exact = delta_lambda_to_delta_frequency(delta_lambda, lambda_0, method='exact')
    approximate = delta_lambda_to_delta_frequency(delta_lambda, lambda_0, method='approximate')
    
    exact_values.append(exact)
    approximate_values.append(approximate)

# Calculate the difference between methods
exact_array = np.array(exact_values)
approximate_array = np.array(approximate_values)
difference = exact_array - approximate_array

# Create the plot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Plot 1: Both methods
ax1.plot(delta_lambdas * 1e9, exact_array / 1e9, 'b-', linewidth=2, label='Exact Method')
ax1.plot(delta_lambdas * 1e9, approximate_array / 1e9, 'r--', linewidth=2, label='Approximate Method')
ax1.set_xlabel(r'Wavelength Bandwidth $\Delta\lambda$ (nm)')
ax1.set_ylabel(r'Frequency Bandwidth $\Delta f$ (GHz)')
ax1.set_title(r'Comparison of Exact and Approximate Methods for $\Delta f = f(\Delta\lambda)$')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Plot 2: Difference between methods
ax2.plot(delta_lambdas * 1e9, difference / 1e6, 'g-', linewidth=2)
ax2.set_xlabel(r'Wavelength Bandwidth $\Delta\lambda$ (nm)')
ax2.set_ylabel(r'Difference $\Delta f_{exact} - \Delta f_{approximate}$ (MHz)')
ax2.set_title(r'Difference Between Exact and Approximate Methods')
ax2.grid(True, alpha=0.3)

# Adjust layout and save to figures directory
plt.tight_layout()
plt.savefig('figures/bandwidth_comparison.pdf', dpi=300, bbox_inches='tight')
plt.savefig('figures/bandwidth_comparison.png', dpi=300, bbox_inches='tight')
plt.close()  # Close the figure to free memory

print("Example completed successfully!")
print(f"Maximum difference: {np.max(np.abs(difference))/1e6:.2f} MHz")
print(f"Relative difference at maximum: {np.max(np.abs(difference))/np.max(exact_array)*100:.2f}%")

# Example with specific values
print("\nSpecific examples:")
test_values = [0.1e-9, 1e-9, 10e-9, 50e-9]
for delta_lambda in test_values:
    exact = delta_lambda_to_delta_frequency(delta_lambda, lambda_0, method='exact')
    approx = delta_lambda_to_delta_frequency(delta_lambda, lambda_0, method='approximate')
    diff = abs(exact - approx)
    rel_diff = diff / exact * 100
    print(f"Δλ = {delta_lambda*1e9:.1f} nm: Exact={exact/1e9:.2f} GHz, Approx={approx/1e9:.2f} GHz, Diff={diff/1e6:.2f} MHz ({rel_diff:.2f}%)")