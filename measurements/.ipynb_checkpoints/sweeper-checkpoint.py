"""
Frequency sweep module.

Controls frequency sweeps using HF2LI.

The sweeper does not communicate with the instrument directly.
It uses the HF2LI driver methods:
    - set_frequency()
    - settle()
    - read_xy()

"""

import numpy as np



class FrequencySweeper:


    def __init__(
        self,
        lockin
    ):

        """
        Connect sweeper to HF2LI driver.
        """

        self.lockin = lockin



    # =====================================================
    # Frequency sweep
    # =====================================================

    def sweep(
        self,
        start_frequency,
        stop_frequency,
        points,
        demods=(0,),
        live_plot=False
    ):

        """
        Perform frequency sweep.

        Parameters
        ----------
        start_frequency :
            Start frequency [Hz]

        stop_frequency :
            Stop frequency [Hz]

        points :
            Number of frequency points

        demods :
            Tuple of demodulators

        live_plot :
            Enable live plotting


        Returns
        -------
        dictionary with measurement data
        """



        print()
        print("="*50)
        print("Starting frequency sweep")
        print("="*50)



        # -------------------------------------------------
        # Create frequency list
        # -------------------------------------------------

        frequencies = np.linspace(
            start_frequency,
            stop_frequency,
            points
        )



        # -------------------------------------------------
        # Prepare data storage
        # -------------------------------------------------

        data = {

            "frequency": []

        }


        for demod in demods:

            data[f"x_{demod}"] = []

            data[f"y_{demod}"] = []

            data[f"r_{demod}"] = []

            data[f"phase_{demod}"] = []



        # -------------------------------------------------
        # Live plotting setup
        # -------------------------------------------------

        if live_plot:

            import matplotlib.pyplot as plt


            plt.ion()


            fig, ax = plt.subplots()


            lines = {}


            for demod in demods:

                line, = ax.plot(
                    [],
                    [],
                    label=f"Demod {demod}"
                )

                lines[demod] = line



            ax.set_xlabel(
                "Frequency (Hz)"
            )


            ax.set_ylabel(
                "Amplitude R"
            )


            ax.legend()


            plt.show()



        # -------------------------------------------------
        # Measurement loop
        # -------------------------------------------------

        for index, frequency in enumerate(
            frequencies
        ):


            # Print only about 10 updates
            if (
                index % max(1, points//10) == 0
                or index == points-1
            ):

                print(
                    f"{index+1}/{points}: "
                    f"{frequency:.2f} Hz"
                )



            # Set oscillator frequency

            self.lockin.set_frequency(
                frequency
            )


            # Allow filters to settle

            self.lockin.settle(
                0.05
            )



            # -------------------------------------------------
            # Measure all demodulators
            # -------------------------------------------------

            measurement_ok = True


            temporary = {}



            for demod in demods:


                try:

                    x, y, r, phase = (
                        self.lockin.read_xy(
                            demod
                        )
                    )


                except Exception:

                    measurement_ok = False

                    break



                temporary[f"x_{demod}"] = x

                temporary[f"y_{demod}"] = y

                temporary[f"r_{demod}"] = r

                temporary[f"phase_{demod}"] = phase



            # Store only complete points

            if measurement_ok:


                data["frequency"].append(
                    frequency
                )


                for demod in demods:

                    data[f"x_{demod}"].append(
                        temporary[f"x_{demod}"]
                    )

                    data[f"y_{demod}"].append(
                        temporary[f"y_{demod}"]
                    )

                    data[f"r_{demod}"].append(
                        temporary[f"r_{demod}"]
                    )

                    data[f"phase_{demod}"].append(
                        temporary[f"phase_{demod}"]
                    )



            # -------------------------------------------------
            # Update live plot
            # -------------------------------------------------

            if live_plot:


                for demod in demods:


                    n = len(
                        data[f"r_{demod}"]
                    )


                    lines[demod].set_data(

                        data["frequency"][:n],

                        data[f"r_{demod}"][:n]

                    )



                ax.relim()

                ax.autoscale_view()


                fig.canvas.draw()

                fig.canvas.flush_events()



        # -------------------------------------------------
        # Convert lists to arrays
        # -------------------------------------------------

        for key in data:

            data[key] = np.array(
                data[key]
            )



        print()
        print("Sweep finished.")
        print()



        return data