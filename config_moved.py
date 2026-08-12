"""
HF2LI Project Configuration

This file contains user-defined settings.

The purpose of this file is to keep all experiment
parameters outside the hardware driver code.

The HF2LI driver should not contain experiment-specific
values.
"""


# =========================================================
# Device connection
# =========================================================

# Zurich Instruments device identifier.
#
# This can be found in LabOne or the Zurich Instruments
# device discovery tool.
#
# Example:
# DEVICE_ID = "dev376"
#
DEVICE_ID = "dev376"


# Zurich Instruments Data Server address.
#
# Usually the Data Server runs locally.
#
SERVER_HOST = "localhost"


# HF2LI communication mode.
#
# Required for HF2 devices.
#
HF2 = True



# =========================================================
# General experiment information
# =========================================================

# Optional name of the experiment.
#
# This will later be useful when saving data.
#

# =========================================================
# Experiment information
# =========================================================

EXPERIMENT_NAME = "test_measurement"



# =========================================================
# Signal Output (excitation)
# =========================================================

# Physical output channel.
#
# HF2LI:
#   0 = Signal Output 1
#   1 = Signal Output 2
#
OUTPUT_CHANNEL = 0


# DC offset applied to the output.
#
# Units: Volt
#
OFFSET = 0.0


# AC excitation amplitude.
#
# Units: Volt
#
AMPLITUDE = 0.002



# =========================================================
# Signal Inputs
# =========================================================

# Input ranges.
#
# Units: Volt
#
# Increase range if the input signal saturates.
#

INPUT_RANGE_1 = 1.0

INPUT_RANGE_2 = 1.0


# Input coupling
#
# False = DC coupling
# True  = AC coupling
#

INPUT_AC_1 = False

INPUT_AC_2 = False



# =========================================================
# Demodulators
# =========================================================

# Demodulator numbers used in the experiment.
#
# HF2LI has six demodulators:
# 0 ... 5
#

DEMOD_1 = 0

DEMOD_2 = 1



# Demodulator sample rates.
#
# Units: samples/second
#

DEMOD_RATE_1 = 1000

DEMOD_RATE_2 = 1000



# ADC assignment.
#
# HF2LI:
#
# ADC 0 -> Signal Input 1
# ADC 1 -> Signal Input 2
#

ADC_1 = 0

ADC_2 = 1



# Oscillator assignment.
#
# For your resonance measurements both channels
# currently use oscillator 0.
#

OSCILLATOR_1 = 0

OSCILLATOR_2 = 0



# =========================================================
# Lock-in filtering
# =========================================================

# Time constant.
#
# Units: seconds
#

TIME_CONSTANT = 0.05


# Low-pass filter order.
#

FILTER_ORDER = 4


# Detection harmonic.
#

HARMONIC = 1



# =========================================================
# Frequency sweep parameters
# =========================================================

# Start frequency.
#
# Units: Hz
#

F_START = 100
# original F_START = 2000, modified to 100 to capture the resonance of the cantilever. //06AUG YZ


# Stop frequency.
#
# Units: Hz
#

F_STOP = 12000
# original F_STOP = 6000, modified to 12000 to capture the resonance of the cantilever. //06AUG YZ

# Number of frequency points.

POINTS = 200


# Sweep type.
#
# Options:
#   "linear"
#   "log"
#

SWEEP_MODE = "linear"


# Number of averages.

AVERAGES = 10


# =========================================================
# Experiment settings dictionary
#
# This is saved with every measurement run.
# It contains the parameters used for the experiment.
# =========================================================


settings = {


    "DEVICE_ID": DEVICE_ID,


    # Output

    "OUTPUT_CHANNEL": OUTPUT_CHANNEL,

    "OFFSET": OFFSET,

    "AMPLITUDE": AMPLITUDE,


    # Inputs

    "INPUT_RANGE_1": INPUT_RANGE_1,

    "INPUT_RANGE_2": INPUT_RANGE_2,


    # Demodulators

    "DEMOD_RATE_1": DEMOD_RATE_1,

    "DEMOD_RATE_2": DEMOD_RATE_2,


    # Sweep

    "F_START": F_START,

    "F_STOP": F_STOP,

    "POINTS": POINTS,

    "TIME_CONSTANT": TIME_CONSTANT,

    "SWEEP_MODE": SWEEP_MODE,

    "AVERAGES": AVERAGES

}