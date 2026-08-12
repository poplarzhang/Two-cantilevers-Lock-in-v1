"""
experiment.py

Controls an interactive measurement session.

Responsibilities
----------------
- Create a unique experiment folder.
- Save experiment settings.
- Repeatedly:
    * wait for user adjustment
    * record data
    * save measurement
"""

import os
from datetime import datetime

import numpy as np


class ExperimentRunner:
    """
    Interactive experiment controller.
    """

    def __init__(
        self,
        recorder,
        settings,
        metadata=None,
        base_folder="Data",
    ):
        """
        Parameters
        ----------
        recorder :
            HF2LIRecorder object.

        settings :
            Dictionary containing experiment settings.

        metadata :
            Optional dictionary containing additional
            information such as resonance frequency.

        base_folder :
            Directory where all experiments are stored.
        """

        self.recorder = recorder
        self.settings = settings
        self.metadata = metadata if metadata is not None else {}

        # --------------------------------------------------
        # Create experiment folder
        # --------------------------------------------------

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

        print()
        print("====================================")
        print("Experiment folder created")
        print(self.run_folder)
        print("====================================")
        print()

        self.save_settings()

    # ======================================================
    # Save settings
    # ======================================================

    def save_settings(self):
        """
        Save experiment settings to a text file.
        """

        filename = os.path.join(
            self.run_folder,
            "settings.txt"
        )

        with open(filename, "w") as file:

            file.write("HF2LI Experiment\n")
            file.write("=========================\n\n")

            file.write("Settings\n")
            file.write("-------------------------\n")

            for key, value in self.settings.items():
                file.write(f"{key}: {value}\n")

            if len(self.metadata) > 0:

                file.write("\nMetadata\n")
                file.write("-------------------------\n")

                for key, value in self.metadata.items():
                    file.write(f"{key}: {value}\n")

        print("Settings saved.")
        print(filename)
        print()

    # ======================================================
    # Save one measurement
    # ======================================================

    def save_measurement(
        self,
        measurement,
        number,
        # label, remove the label input as decription //10AUG YZ
        experiment_angle,
        
    ):
        """
        Save one measurement.
        """

        # safe_label = label.replace(" ", "_") remove the label input as decription //10AUG YZ

        filename = (
            # f"{number:03d}_{safe_label}.npy" //change to show angle in filename instead of label //10AUG YZ
            f"{number:03d}_angle_{int(experiment_angle)}.npy"
        )

        filepath = os.path.join(
            self.run_folder,
            filename
        )

        # Add metadata to saved measurement

        measurement["metadata"] = {

            
            **self.metadata,

            "number": number,

            # "label": label, remove the label input as decription //10AUG YZ

            "experiment_angle": experiment_angle,

            "timestamp": datetime.now().isoformat(),
        }

        np.save(
            filepath,
            measurement,
            allow_pickle=True,
        )

        print(f"Saved: {filepath}")

    # ======================================================
    # Main experiment loop
    # ======================================================

    def run(
        self,
        duration=2.0,
    ):
        """
        Interactive experiment.
        """

        measurement_number = 1

        while True:

            self.recorder.lockin.disable_excitation()
            
            print()
            print("--------------------------------")

            print(
                f"Measurement {measurement_number}"
            )
            # label = input as the description is removed, take the angle input instead //10AUG YZ
            # label = input(
            #     "Description (q = quit): "
            # )

            # if label.lower() == "q":

            #     print()
            #     print("Experiment finished.")
            #     break



            # experiment_angle = float(
            #     input(
            #     "Experimental angle (deg): "
            #     )
            # )
            experiment_angle_input = input(
                "Experimental angle (deg), q = quit: "  
            )

            if experiment_angle_input.lower() == "q":
                print()
                print("Experiment finished.")
                break

            experiment_angle = float(experiment_angle_input)
            
            
            input(
                "Adjust experiment and press ENTER..."
            )

            print()
            print("Recording...")

            measurement = self.recorder.record(
                duration=duration
            )

            print("Recording finished.")


            print("DEBUG experiment_angle =",experiment_angle)

            
            self.save_measurement(
                measurement,
                measurement_number,
                #label, remove the label input as decription //10AUG YZ
                experiment_angle,
            )

            measurement_number += 1