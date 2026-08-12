# Two Cantilevers Lock-in Framework

Automatically generated project reference.



================================================================================
TWO CANTILEVERS LOCK-IN FRAMEWORK
================================================================================

################################################################################
INSTRUMENT
################################################################################

================================================================================
instrument
================================================================================

================================================================================
instrument.hf2li
================================================================================

CLASSES


CLASS: HF2LI
    Driver class for the Zurich Instruments HF2LI.
    __init__(self, device_id, host='localhost', hf2=True)
    _initialize_aux_outputs(self)
    _initialize_demodulators(self)
    _initialize_inputs(self)
    _initialize_oscillators(self)
    _initialize_outputs(self)
    _initialize_pids(self)
    _initialize_plls(self)
    _initialize_scope(self)
    configure_demod(self, demod=0, adc=0, oscillator=0, rate=1000)
    configure_input(self, channel=0, input_range=1.0)
    configure_output(self, channel=0, amplitude=0.01, offset=0.0)
    connect(self)
    disable_excitation(self)
    disconnect(self)
    enable_excitation(self)
    initialize(self)
    read_sample(self, demod=0)
    read_stream(self, demod=0, duration=2.0)
    read_stream_multi(self, demods=(0, 1), duration=2.0)
    read_xy(self, demod=0)
    set_frequency(self, frequency, oscillator=0, verbose=False)
    settle(self, time_seconds=0.05)

################################################################################
MEASUREMENTS
################################################################################

================================================================================
measurements
================================================================================

================================================================================
measurements.experiment
================================================================================

CLASSES


CLASS: ExperimentRunner
    Interactive experiment controller.
    __init__(self, recorder, settings, metadata=None, base_folder='Data')
    run(self, duration=2.0)
    save_measurement(self, measurement, number, label, experiment_angle)
    save_settings(self)

================================================================================
measurements.interactive
================================================================================

CLASSES


CLASS: InteractiveMeasurement
    __init__(self, lockin)
    measure(self, demod=0)
    run(self, frequency, demod=0, points=100)
    set_frequency(self, frequency)

================================================================================
measurements.recorder
================================================================================

CLASSES


CLASS: HF2LIRecorder
    __init__(self, lockin, demods=(0, 1))
    record(self, duration=2.0)

================================================================================
measurements.sweeper
================================================================================

CLASSES


CLASS: FrequencySweeper
    __init__(self, lockin)
    sweep(self, start_frequency, stop_frequency, points, demods=(0,), live_plot=False)

################################################################################
ANALYSIS
################################################################################

================================================================================
analysis
================================================================================

================================================================================
analysis.calibration
================================================================================

FUNCTIONS

    build_calibration(folder)
        Read all calibration experiments from folder.
        File : calibration.py
        Lines: 124

    calculate_complex_point(measurement)
        Calculate:
        File : calibration.py
        Lines: 40

    estimate_angle(measurement, calibration)
        Estimate angle of an unknown measurement.
        File : calibration.py
        Lines: 46

    estimate_angle_interpolated(measurement, calibration)
        Estimate angle using linear interpolation
        File : calibration.py
        Lines: 90

    load_calibration(filename)
        File : calibration.py
        Lines: 8

    save_calibration(calibration, filename)
        File : calibration.py
        Lines: 10


================================================================================
analysis.calibration_plot
================================================================================

FUNCTIONS

    plot_calibration(calibration)
        File : calibration_plot.py
        Lines: 56


================================================================================
analysis.complex_analysis
================================================================================

FUNCTIONS

    calculate_complex_ratio(measurement)
        Calculate the complex ratio for every sample.
        File : complex_analysis.py
        Lines: 13

    calculate_mean_complex_ratio(measurement)
        Calculate one representative complex ratio.
        File : complex_analysis.py
        Lines: 18

    calculate_mean_ratios(measurements)
        Calculate one complex ratio for each measurement.
        File : complex_analysis.py
        Lines: 25

    get_complex_signals(measurement)
        Build complex signals from one measurement.
        File : complex_analysis.py
        Lines: 24

    split_complex(ratios, experiment_angles=None, labels=None)
        Prepare complex ratios for plotting.
        File : complex_analysis.py
        Lines: 52


================================================================================
analysis.measurement_reader
================================================================================

FUNCTIONS

    load_measurements(folder)
        Load all interactive measurements
        File : measurement_reader.py
        Lines: 46

    summarize_measurements(measurements)
        Extract simple parameters
        File : measurement_reader.py
        Lines: 62


================================================================================
analysis.parser
================================================================================

FUNCTIONS

    get_channel(data, demod=0, quantity='r')
        Extract one measurement quantity.
        File : parser.py
        Lines: 41

    get_frequency(data)
        Return frequency axis.
        File : parser.py
        Lines: 9


================================================================================
analysis.plotting
================================================================================

FUNCTIONS

    plot_complex_ratio(result)
        File : plotting.py
        Lines: 110

    plot_measurement_summary(summary)
        File : plotting.py
        Lines: 44

    plot_phase_summary(summary)
        File : plotting.py
        Lines: 45

    plot_resonance_fit(frequency, amplitude, fit_result, title='Resonance fit')
        Plot measured data and fitted Lorentzian.
        File : plotting.py
        Lines: 108


================================================================================
analysis.resonance
================================================================================

FUNCTIONS

    fit_resonance(frequency, amplitude)
        Robust resonance fit.
        File : resonance.py
        Lines: 177

    lorentzian(frequency, f0, gamma, amplitude, offset)
        Lorentzian resonance function.
        File : resonance.py
        Lines: 40



================================================================================
End of summary
================================================================================
