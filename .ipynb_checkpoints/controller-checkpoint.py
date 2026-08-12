from hf2li import HF2LI


class HF2Controller:
    """
    High-level controller for HF2LI experiments.

    This class uses HF2LI as the hardware interface.
    """


    def __init__(self, device_id):

        self.lockin = HF2LI(device_id)


    # -------------------------------------------------
    # Connection
    # -------------------------------------------------

    def connect(self):

        #self.lockin.connect()

        #self.lockin.initialize_hf2li()


        self.session = Session("localhost", hf2=True)

        self.device = self.session.connect_device(self.device_id)


    
    def disconnect(self):

        self.lockin.disconnect()


    # -------------------------------------------------
    # Complete configuration
    # -------------------------------------------------

    def configure(
        self,
        input_ranges,
        demod_rates,
        time_constant,
        amplitude,
        offset
    ):

        self.configure_inputs(
            input_ranges
        )

        self.configure_demods(
            demod_rates,
            time_constant
        )

        self.configure_output(
            amplitude,
            offset
        )


    # -------------------------------------------------
    # Inputs
    # -------------------------------------------------

    def configure_inputs(
        self,
        input_ranges
    ):

        self.lockin.configure_input(
            input_channel=0,
            input_range=input_ranges[0]
        )

        self.lockin.configure_input(
            input_channel=1,
            input_range=input_ranges[1]
        )



    # -------------------------------------------------
    # Demodulators
    # -------------------------------------------------

    def configure_demods(
        self,
        rates,
        time_constant
    ):

        self.lockin.configure_demod(
            demod=0,
            rate=rates[0]
        )

        self.lockin.configure_demod(
            demod=1,
            rate=rates[1]
        )


        # overwrite time constants
        self.lockin.device.demods[0].timeconstant(
            time_constant
        )

        self.lockin.device.demods[1].timeconstant(
            time_constant
        )



    # -------------------------------------------------
    # Output
    # -------------------------------------------------

    def configure_output(
        self,
        amplitude,
        offset
    ):

        self.lockin.configure_output(
            output=0,
            amplitude=amplitude,
            offset=offset
        )



    # -------------------------------------------------
    # Frequency
    # -------------------------------------------------

    def set_frequency(
        self,
        frequency
    ):

        self.lockin.set_frequency(
            frequency
        )