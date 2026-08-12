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
    NUMBER_OF_OSCILLATORS = 8
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
        Reset all oscillator frequencies.
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

        scope.trigenable(False)


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