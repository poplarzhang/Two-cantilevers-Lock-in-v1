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
        Record HF2LI data for a given time.

        Returns:
            dictionary with arrays
        """
        print(
                "Starting measurement"
        )


        self.lockin.enable_excitation()
        


        
        data = {

            "time": []

        }


        for d in self.demods:

            data[f"x_{d}"] = []

            data[f"y_{d}"] = []

            data[f"r_{d}"] = []

            data[f"phase_{d}"] = []



        start = time.time()



        print(
            "Recording..."
        )



        while (
            time.time() - start
            <
            duration
        ):


            timestamp = time.time()



            data["time"].append(
                timestamp
            )



            for d in self.demods:


                x, y, r, phase = (
                    self.lockin.read_xy(d)
                )


                data[f"x_{d}"].append(x)

                data[f"y_{d}"].append(y)

                data[f"r_{d}"].append(r)

                data[f"phase_{d}"].append(phase)



        print(
            "Recording finished."
        )


        self.lockin.disable_excitation()

        print("Excitation disabled")

        return data