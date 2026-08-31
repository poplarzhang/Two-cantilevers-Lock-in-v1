# Device connection

DEVICE_ID = "dev376"

# Zurich Instruments Data Server address.
SERVER_HOST = "localhost"

# HF2LI communication mode.
HF2 = True


# General experiment information
# Optional name of the experiment.
EXPERIMENT_NAME = "test_measurement"


# Signal Output (excitation)
# used to configure Physical output channel.

# HF2LI:
#   0 = Signal Output 1
#   1 = Signal Output 2

OUTPUT_CHANNEL = 0


# DC offset applied to the output in volts
OFFSET = 0

# AC excitation amplitude in volts
AMPLITUDE = 0.001


# Signal Inputs in volts
# Increase range if the input signal saturates.
INPUT_RANGE_1 = 1.0
INPUT_RANGE_2 = 1.0


# Input coupling#
# False = DC coupling
# True  = AC coupling
INPUT_AC_1 = False
INPUT_AC_2 = False


# Demodulators
# Demodulator numbers used in the experiment.
# HF2LI has six demodulators:
# 0 ... 5
DEMOD_1 = 0
DEMOD_2 = 1


# Demodulator sample rates in samples/second
DEMOD_RATE_1 = 1000
DEMOD_RATE_2 = 1000

# ADC assignment.
#
# HF2LI:
#
# ADC 0 -> Signal Input 1
# ADC 1 -> Signal Input 2
ADC_1 = 0
ADC_2 = 1


# Oscillator assignment.
# For your resonance measurements both channels
# currently use oscillator 0.
OSCILLATOR_1 = 0
OSCILLATOR_2 = 0

# Lock-in filtering's time constant in seconds
TIME_CONSTANT = 0.05


# Low-pass filter order.
FILTER_ORDER = 4


# Detection harmonic.
HARMONIC = 1

# Frequency sweep parameters of start and stop frequency in Hertz, number of frequency points, sweeping in linear or log, window width of averaging
F_START = 600
F_STOP = 1300
POINTS = 1400
SWEEP_MODE = "linear"
AVERAGES = 10


# Experiment settings dictionary
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