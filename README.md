# Optics Library

A Python library for optical communications calculations with numpy and matplotlib support.

## Features

- Frequency/wavelength conversions
- Optical bandwidth calculations
- Mathematical functions for optics applications

## Installation

```bash
# Clone the repository
git clone https://gitlab.com/thkam/optics-comms-slides.git
cd optics-comms-slides
```

## Usage

```python
import optics_lib

# Convert frequency to wavelength
wavelength = optics_lib.frequency_to_wavelength(193.1e12, unit='THz')

# Convert wavelength to frequency  
frequency = optics_lib.wavelength_to_frequency(1550e-9, unit='nm')

# Calculate frequency bandwidth from wavelength bandwidth
delta_f = optics_lib.delta_lambda_to_delta_frequency(0.1e-9, 1550e-9)
```

## Functions

### Basic Conversions
- `frequency_to_wavelength(frequency, unit='Hz')` - Convert frequency to wavelength
- `wavelength_to_frequency(wavelength, unit='m')` - Convert wavelength to frequency

### Optical Calculations
- `delta_lambda_to_delta_frequency(delta_lambda, lambda_0, method='exact')` - Convert wavelength bandwidth to frequency bandwidth

## License

MIT License

Copyright (c) 2026 Thomas Kamalakis

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
