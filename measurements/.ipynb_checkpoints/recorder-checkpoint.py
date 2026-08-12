"""
HF2LI measurement recorder.

Records X,Y,R,phase from selected demodulators.
"""


import time



class HF2LIRecorder:


    def __init__(
        self,
        lockin,
        demods=(0,1)
    ):

        self.lockin = lockin

        self.demods = demods



    # -------------------------------------------------
    # Record measurement
    # -------------------------------------------------

    def record(
        self,
        duration=2.0
    ):

        """
        Record HF2LI data using LabOne streaming.

        Returns dictionary compatible with old recorder.
        """


        print(
            "Starting measurement"
        )


        self.lockin.enable_excitation()


        data = {}


        # -----------------------------------------
        # Stream all demodulators
        # -----------------------------------------

        streams = self.lockin.read_stream_multi(
            demods=self.demods,
            duration=duration
        )


        # -----------------------------------------
        # Use first demod time base
        # -----------------------------------------

        first = streams[self.demods[0]]


        data["time"] = (
            first["timestamp"]
            -
            first["timestamp"][0]
        )


        # -----------------------------------------
        # Copy demod data
        # -----------------------------------------

        for d in self.demods:

            stream = streams[d]


            data[f"x_{d}"] = stream["x"]

            data[f"y_{d}"] = stream["y"]

            data[f"r_{d}"] = stream["r"]

            data[f"phase_{d}"] = stream["phase"]


        print(
            "Points recorded:",
            len(data["time"])
        )


        self.lockin.disable_excitation()


        print(
            "Excitation disabled"
        )


        return data