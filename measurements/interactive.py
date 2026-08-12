"""
Interactive measurements with HF2LI.

After a resonance frequency is found,
the lock-in stays at this frequency and
records measurements on demand.
"""


import time



class InteractiveMeasurement:


    def __init__(
        self,
        lockin
    ):

        self.lockin = lockin



    # =====================================================
    # Set measurement frequency
    # =====================================================

    def set_frequency(
        self,
        frequency
    ):

        print(
            f"Setting measurement frequency: {frequency:.3f} Hz"
        )


        self.lockin.set_frequency(
            frequency
        )


        # allow demodulator filter to settle

        self.lockin.settle(
            0.2
        )



    # =====================================================
    # Single measurement
    # =====================================================

    def measure(
        self,
        demod=0
    ):


        x, y, r, phase = self.lockin.read_xy(
            demod
        )


        result = {


            "time": time.time(),

            "x": x,

            "y": y,

            "r": r,

            "phase": phase

        }


        return result



    # =====================================================
    # Interactive loop
    # =====================================================

    def run(
        self,
        frequency,
        demod=0,
        points=100
    ):


        self.set_frequency(
            frequency
        )


        data = []



        print()
        print(
            "Interactive measurement started"
        )

        print(
            "Press ENTER for next point"
        )



        for i in range(points):


            input(
                f"{i+1}/{points}  Press ENTER..."
            )


            measurement = self.measure(
                demod
            )


            data.append(
                measurement
            )


            print(
                measurement
            )


        return data