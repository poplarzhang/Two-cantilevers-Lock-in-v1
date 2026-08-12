"""
HF2LI Instrument Driver

This module contains the low-level driver for the
Zurich Instruments HF2LI lock-in amplifier.

The responsibility of this class is:

    - establish communication with the instrument
    - initialize the hardware into a known state
    - provide a clean interface for future measurements

Measurement logic, sweeps, fitting, and analysis should
not be implemented here.
"""

import numpy as np
from zhinst.toolkit import Session


class HF2LI:
    """
    Driver class for the Zurich Instruments HF2LI.

    The typical usage is:

        lockin = HF2LI("devXXX")

        lockin.connect()

        lockin.initialize()

        ...

        lockin.disconnect()

    """


    # =====================================================
    # Hardware constants
    # =====================================================

    # Number of available hardware channels
    NUMBER_OF_INPUTS = 2
    NUMBER_OF_OUTPUTS = 2

    # Internal hardware resources
    NUMBER_OF_MIXERS = 8
    NUMBER_OF_OSCILLATORS = 6
    NUMBER_OF_DEMODULATORS = 6
    NUMBER_OF_PLLS = 2
    NUMBER_OF_PIDS = 4
    NUMBER_OF_AUX_OUTPUTS = 4


    # =====================================================
    # Factory default values
    # =====================================================

    DEFAULT_INPUT_RANGE = 1.0
    DEFAULT_OUTPUT_RANGE = 1

    DEFAULT_DEMOD_RATE = 1000
    DEFAULT_TIME_CONSTANT = 0.01
    DEFAULT_FILTER_ORDER = 4
    DEFAULT_HARMONIC = 1


    # =====================================================
    # Constructor
    # =====================================================

    def __init__(
        self,
        device_id,
        host="localhost",
        hf2=True,
    ):
        """
        Create an HF2LI driver object.

        No connection with the physical instrument is made
        here. The connection happens only after calling
        connect().
        """

        self.device_id = device_id
        self.host = host
        self.hf2 = hf2

        self.session = None
        self.device = None



    # =====================================================
    # Connection
    # =====================================================

    def connect(self):
        """
        Connect to the Zurich Instruments Data Server.

        After this method finishes successfully,
        communication with the HF2LI is available.
        """

        print("=" * 60)
        print("Connecting to HF2LI...")
        print("=" * 60)


        # Create communication session with LabOne Data Server.
        self.session = Session(
            self.host,
            hf2=self.hf2
        )


        # Connect to the physical instrument.
        self.device = self.session.connect_device(
            self.device_id
        )


        print(
            f"Connected to {self.device_id}"
        )
        print()



    def disconnect(self):
        """
        Disconnect from the HF2LI.

        The references to the instrument are removed so that
        no further communication is possible accidentally.
        """

        print("Disconnecting from HF2LI...")


        self.device = None
        self.session = None


        print("Disconnected.")



    # =====================================================
    # Initialization
    # =====================================================

    def initialize(self):
        """
        Return the HF2LI to a known safe state.

        This method should be called at the beginning of every
        experiment.

        All active functions are disabled:

            - outputs
            - demodulators
            - oscillators
            - PLLs
            - PID controllers
            - scope

        """

        print("=" * 60)
        print("Initializing HF2LI...")
        print("=" * 60)


        self._initialize_inputs()

        self._initialize_outputs()

        self._initialize_oscillators()

        self._initialize_demodulators()

        self._initialize_plls()

        self._initialize_pids()

        self._initialize_scope()

        self._initialize_aux_outputs()


        print()
        print("Initialization complete.")
        print()



    # =====================================================
    # Input initialization
    # =====================================================

    def _initialize_inputs(self):
        """
        Initialize signal input channels.
        """

        print("  Initializing signal inputs...")


        for channel in range(
            self.NUMBER_OF_INPUTS
        ):

            signal_input = self.device.sigins[channel]


            # Disable AC coupling.
            signal_input.ac(False)


            # Single-ended input mode.
            signal_input.diff(False)


            # High impedance input (1 MOhm).
            signal_input.imp50(False)


            # Default voltage range.
            signal_input.range(
                self.DEFAULT_INPUT_RANGE
            )


        print("    Signal inputs initialized.")



    # =====================================================
    # Output initialization
    # =====================================================

    def _initialize_outputs(self):
        """
        Initialize signal outputs.

        Outputs are disabled to guarantee that no excitation
        signal is applied during startup.
        """

        print("  Initializing signal outputs...")


        for channel in range(
            self.NUMBER_OF_OUTPUTS
        ):

            signal_output = self.device.sigouts[channel]


            # Disable physical output connector.
            signal_output.on(False)


            # Remove DC offset.
            signal_output.offset(0.0)


            # Default output range.
            signal_output.range(
                self.DEFAULT_OUTPUT_RANGE
            )


            # Disable all mixer paths.
            for mixer in range(
                self.NUMBER_OF_MIXERS
            ):

                signal_output.enables[mixer](False)

                signal_output.amplitudes[mixer](0.0)


        print("    Signal outputs initialized.")



    # =====================================================
    # Oscillator initialization
    # =====================================================

    def _initialize_oscillators(self):
        """
        Reset all available oscillator frequencies.
        """

        print("  Initializing oscillators...")


        for oscillator_number in range(
            self.NUMBER_OF_OSCILLATORS
        ):

            oscillator = self.device.oscs[
                oscillator_number
            ]

            oscillator.freq(0.0)


        print("    Oscillators initialized.")



    # =====================================================
    # Demodulator initialization
    # =====================================================

    def _initialize_demodulators(self):
        """
        Initialize all demodulators.
        """

        print("  Initializing demodulators...")


        for demod_number in range(
            self.NUMBER_OF_DEMODULATORS
        ):

            demodulator = self.device.demods[
                demod_number
            ]


            # Disable acquisition.
            demodulator.enable(False)


            # Safe default selections.
            demodulator.adcselect(0)

            demodulator.oscselect(0)


            # Detection settings.
            demodulator.harmonic(
                self.DEFAULT_HARMONIC
            )

            demodulator.order(
                self.DEFAULT_FILTER_ORDER
            )

            demodulator.timeconstant(
                self.DEFAULT_TIME_CONSTANT
            )

            demodulator.rate(
                self.DEFAULT_DEMOD_RATE
            )


        print("    Demodulators initialized.")



    # =====================================================
    # PLL initialization
    # =====================================================

    def _initialize_plls(self):
        """
        Disable all PLL controllers.
        """

        print("  Initializing PLLs...")


        for pll_number in range(
            self.NUMBER_OF_PLLS
        ):

            pll = self.device.plls[pll_number]

            pll.enable(False)


        print("    PLLs initialized.")



    # =====================================================
    # PID initialization
    # =====================================================

    def _initialize_pids(self):
        """
        Disable and reset all PID controllers.
        """

        print("  Initializing PID controllers...")


        for pid_number in range(
            self.NUMBER_OF_PIDS
        ):

            pid = self.device.pids[pid_number]


            pid.enable(False)

            pid.p(0.0)
            pid.i(0.0)
            pid.d(0.0)


        print("    PID controllers initialized.")



    # =====================================================
    # Scope initialization
    # =====================================================

    def _initialize_scope(self):
        """
        Disable internal scope.
        """

        print("  Initializing scope...")


        scope = self.device.scopes[0]


        scope.enable(False)



        print("    Scope initialized.")



    # =====================================================
    # Auxiliary outputs initialization
    # =====================================================

    def _initialize_aux_outputs(self):
        """
        Reset auxiliary outputs to zero voltage.
        """

        print("  Initializing auxiliary outputs...")


        for aux_number in range(
            self.NUMBER_OF_AUX_OUTPUTS
        ):

            aux_output = self.device.auxouts[
                aux_number
            ]

            aux_output.offset(0.0)


        print("    Auxiliary outputs initialized.")



    

    # =====================================================
    # Experiment configuration
    # =====================================================


    def configure_output(
        self,
        channel=0,
        amplitude=0.01,
        offset=0.0
    ):

        """
        Configure excitation output.

        channel:
            0 -> Signal Output 1
            1 -> Signal Output 2

        amplitude:
            AC excitation amplitude [V]

        offset:
            DC offset [V]
        """


        print(
            f"Configuring output {channel}..."
        )


        out = self.device.sigouts[channel]


        # Set DC offset
        out.offset(offset)


        # Set AC amplitude
        out.amplitudes[0](amplitude)


        # Enable mixer path
        out.enables[0](True)


        # Enable output connector
        out.on(True)


        print(
            "  Output configured."
        )



    def configure_input(
        self,
        channel=0,
        input_range=1.0
    ):

        """
        Configure measurement input.
        """


        print(
            f"Configuring input {channel}..."
        )


        inp = self.device.sigins[channel]


        # DC coupling
        inp.ac(False)


        # Single ended
        inp.diff(False)


        # High impedance
        inp.imp50(False)


        # Voltage range
        inp.range(
            input_range
        )


        print(
            "  Input configured."
        )



    def configure_demod(
        self,
        demod=0,
        adc=0,
        oscillator=0,
        rate=1000
    ):

        """
        Configure demodulator.

        adc:
            0 -> Input 1
            1 -> Input 2

        oscillator:
            reference oscillator number
        """


        print(
            f"Configuring demodulator {demod}..."
        )


        demodulator = self.device.demods[demod]


        # Select ADC input
        demodulator.adcselect(adc)


        # Select reference oscillator
        demodulator.oscselect(
            oscillator
        )


        # Sampling rate
        demodulator.rate(
            rate
        )


        # Enable measurement
        demodulator.enable(True)



        print(
            "  Demodulator configured."
        )


    # =====================================================
    # Oscillator frequency control
    # =====================================================

    def set_frequency(
        self,
        frequency,
        oscillator=0,
        verbose=False
    ):
        """
        Set oscillator frequency.

        Parameters
        ----------
        frequency : float
            Frequency in Hz.

        oscillator : int
            HF2LI oscillator number.
        """


        if self.device is None:
            raise RuntimeError(
                "HF2LI is not connected."
            )


        if verbose:
            print(
                f"Setting oscillator {oscillator} "
                f"frequency to {frequency} Hz"
            )


        self.device.oscs[oscillator].freq(
            frequency
        )



    # =====================================================
    # Read demodulator sample
    # =====================================================

    def read_sample(
        self,
        demod=0
    ):
        """
        Read one demodulator sample.
        """


        if self.device is None:
            raise RuntimeError(
                "HF2LI is not connected."
            )


        sample = self.device.demods[
            demod
        ].sample()


        return sample



    # =====================================================
    # Read X,Y,R,Phase
    # =====================================================

    def read_xy(
        self,
        demod=0
    ):
        """
        Read demodulator X,Y,R,phase.

        Returns
        -------
        x
        y
        r
        phase
        """


        sample = self.read_sample(
            demod
        )


        x = sample["x"][0]

        y = sample["y"][0]

        phase = sample["phase"][0]


        r = (
            x*x + y*y
        )**0.5


        return x, y, r, phase



    # =====================================================
    # Settling time
    # =====================================================

    def settle(
        self,
        time_seconds=0.05
    ):
        """
        Wait for the lock-in filters to settle.
        """


        import time

        time.sleep(
            time_seconds
        )




    def enable_excitation(self):

        """
        Enable HF2LI excitation amplitude component.
        """

        #self.device.sigouts[0].enables[0](True)
        self.device.sigouts[0].on(True)

        print(
            "Excitation enabled"
        )


    def disable_excitation(self):

        """
        Disable HF2LI excitation amplitude component.
        """

        #self.device.sigouts[0].enables[0](False)
        self.device.sigouts[0].on(False)

        print(
            "Excitation disabled"
        )



    # =====================================================
    # Stream demodulator data
    # =====================================================

    def read_stream(
        self,
        demod=0,
        duration=2.0
    ):

        import numpy as np


        path = (
            f"/{self.device.serial}/demods/{demod}/sample"
        )


        print(
            "Streaming:",
            path
        )


        self.session.daq_server.flush()


        self.session.daq_server.subscribe(
            path
        )


        raw = self.session.daq_server.poll(
            duration,
            100,
            True
        )


        self.session.daq_server.unsubscribe(
            path
        )


        sample = (
            raw[self.device.serial]
            ["demods"]
            [str(demod)]
            ["sample"]
        )


        x = np.array(
            sample["x"]
        )

        y = np.array(
            sample["y"]
        )

        timestamp = np.array(
            sample["timestamp"]
        )


        r = np.sqrt(
            x*x + y*y
        )


        phase = np.angle(
            x + 1j*y,
            deg=True
        )


        print(
            "Points:",
            len(x)
        )


        return {

            "timestamp": timestamp,

            "x": x,

            "y": y,

            "r": r,

            "phase": phase

        }



    # =====================================================
    # Stream multiple demodulators simultaneously
    # =====================================================

    def read_stream_multi(
        self,
        demods=(0, 1),
        duration=2.0
    ):

        import numpy as np


        paths = []


        for d in demods:

            path = (
                f"/{self.device.serial}/demods/{d}/sample"
            )

            paths.append(path)


        print(
            "Streaming:",
            paths
        )


        # remove old buffered data

        self.session.daq_server.flush()


        # subscribe both channels

        for path in paths:

            self.session.daq_server.subscribe(
                path
            )


        # one common acquisition

        raw = self.session.daq_server.poll(
            duration,
            100,
            True
        )


        # unsubscribe

        for path in paths:

            self.session.daq_server.unsubscribe(
                path
            )


        result = {}


        for d in demods:


            sample = (
                raw[self.device.serial]
                ["demods"]
                [str(d)]
                ["sample"]
            )


            result[d] = {

                "timestamp":
                    np.array(
                        sample["timestamp"]
                    ),

                "x":
                    np.array(
                        sample["x"]
                    ),

                "y":
                    np.array(
                        sample["y"]
                    )

            }


            result[d]["r"] = np.sqrt(
                result[d]["x"]**2
                +
                result[d]["y"]**2
            )


            result[d]["phase"] = np.angle(
                result[d]["x"]
                +
                1j * result[d]["y"],
                deg=True
            )


            print(
                "Demod",
                d,
                "points:",
                len(result[d]["x"])
            )


        # -----------------------------------------
        # Synchronize lengths
        # -----------------------------------------

        lengths = [
            len(result[d]["x"])
            for d in demods
        ]


        n = min(lengths)


        print(
            "Synchronizing to",
            n,
            "points"
        )


        for d in demods:

            for key in [
                "timestamp",
                "x",
                "y",
                "r",
                "phase"
            ]:

                result[d][key] = (
                    result[d][key][:n]
                )


        return result        