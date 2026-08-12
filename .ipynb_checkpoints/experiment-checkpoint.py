import os
import numpy as np
from datetime import datetime
from plotting import diagnostic_plot

class ExperimentRunner:

    def __init__(
        self,
        recorder,
        settings,
        metadata=None,
        base_folder="Data"
    ):

        self.recorder = recorder

        self.metadata = metadata or {}

        # Create a unique run folder

        timestamp = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )


        self.run_folder = os.path.join(
            base_folder,
            timestamp
        )


        os.makedirs(
            self.run_folder,
            exist_ok=True
        )


        print(
            f"Saving data to:\n{self.run_folder}"
        )

        self.save_settings(settings)


        def save_settings(self, settings):
        """
        Save experiment configuration
        in the run folder.
        """

        filename = os.path.join(
            self.run_folder,
            "settings.txt"
        )


        with open(filename, "w") as f:

            f.write(
                "HF2LI Calibration Experiment\n"
            )

            f.write(
                "============================\n\n"
            )


            for key, value in settings.items():

                f.write(
                    f"{key}: {value}\n"
                )


        print(
            f"Settings saved: {filename}"
        )


        
    # -------------------------------------------------
    # Save measurement
    # -------------------------------------------------

    def save(
        self,
        measurement,
        number,
        label
    ):

        filename = (
            f"{number:03d}_{label}.npy"
        )


        path = os.path.join(
            self.run_folder,
            filename
        )


        




        measurement["metadata"] = {


            # Measurement information

            "number": number,

            "label": label,

            "timestamp":
                datetime.now().isoformat(),



            # Experiment information

            **self.metadata

        }




        

        np.save(
            path,
            measurement,
            allow_pickle=True
        )


        print(
            f"Saved: {path}"
        )


        plot_file = os.path.join(
            self.run_folder,
            f"{number:03d}_{label}.png"
        )


        diagnostic_plot(
            measurement,
            plot_file
        )


print(
    f"Saved: {path}"
)

print(
    f"Plot: {plot_file}"
)

    # -------------------------------------------------
    # Main loop
    # -------------------------------------------------

    def run(
        self,
        duration=2.0
    ):


        number = 1


        while True:


            print("\n---------------------")

            print(
                f"Experiment {number}"
            )


            label = input(
                "Description "
                "(q to quit): "
            )


            if label.lower()=="q":

                print(
                    "Finished."
                )

                break



            input(
                "Adjust setup "
                "then press ENTER..."
            )



            measurement = self.recorder.record(
                duration
            )



            self.save(
                measurement,
                number,
                label
            )


            number += 1