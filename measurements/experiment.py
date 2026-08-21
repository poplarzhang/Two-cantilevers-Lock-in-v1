import os

import numpy as np

from pathlib import Path

from datetime import datetime

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

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

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
        prefix=None,
        
    ):
        """
        Save one measurement.
        """

        # safe_label = label.replace(" ", "_") remove the label input as decription //10AUG YZ
        if prefix is None:
            filename = (
                # f"{number:03d}_{safe_label}.npy" //change to show angle in filename instead of label //10AUG YZ
                f"{number:03d}_angle_{int(experiment_angle)}.npy"
            )
        else:
            filename = (f"{prefix}_angle_{int(experiment_angle)}.npy")

        filepath = os.path.join(
            self.run_folder,
            filename
        )

        # Add metadata to saved measurement

        measurement["metadata"] = {

            
            **self.metadata,

            "number": number,

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

            
    def loc_run(
        self,
        duration=2.0,
    ):      
        measurement_number = 1       

        self.recorder.lockin.disable_excitation()         
         
        experiment_angle_input = input(
            "Experimental angle (deg), q = quit: "  
        )

        if experiment_angle_input.lower() == "q":
            print()
            print("localization quit.")
            return
        

        experiment_angle = float(experiment_angle_input)

        input("confirm to execute, press ENTER...")
        print("Recording...")

        measurement = self.recorder.record(duration=duration)

        print("Recording finished.")

        print("DEBUG experiment_angle =",experiment_angle)
            
        self.save_measurement(
            measurement,
            measurement_number,
            experiment_angle,
            prefix= "AUE" #Angle Under Estimation //20AUG YZ
        )

def con_AUE( #conversion an meansurement file of the angle under estimation to a dictionary variant //20AUG YZ
    aue_filename
):
    data = np.load(
        aue_filename,
        allow_pickle=True
    ).item()
# reading
    angle = data["metadata"]["experiment_angle"]
    
    x0 = np.mean(data["x_0"])
    y0 = np.mean(data["y_0"])

    x1 = np.mean(data["x_1"])
    y1 = np.mean(data["y_1"])

    r0 = np.mean(data["r_0"])
    r1 = np.mean(data["r_1"])

    phase0 = np.mean(data["phase_0"])
    phase1 = np.mean(data["phase_1"])

# converting
    z0 = x0 + 1j * y0
    z1 = x1 + 1j * y1

    ratio_points = z0 / z1

    diff_points = z0 - z1

    ratio_mean_mag = r0 / r1

    mag_mean_z0 = abs(z0)
    mag_mean_z1 = abs(z1)

    norm_diff = (
        diff_points /
        (mag_mean_z0 + mag_mean_z1)
    )

# generating

    val_for_loc = {

        "angle":
            np.array([angle]),
        "Cantilever 1":
            np.array([z0]),
        "Cantilever 2":
            np.array([z1]),
        "ratio_points":
            np.array([ratio_points]),
        "diff_points":
            np.array([diff_points]),
        "ratio_mean_mag":
            np.array([ratio_mean_mag]),
        "r_0":
            np.array([r0]),
        "r_1":
            np.array([r1]),
        "phase_0":
            np.array([phase0]),
        "phase_1":
            np.array([phase1]),
        "norm_diff":
            np.array([norm_diff]),
        "source_files":
            [Path(aue_filename).name],
        "created":
            datetime.now().isoformat()
    }

    return val_for_loc   



# estimation of an point's angle //20AUG YZ
# LDND = Least Difference of Normalized Difference of mean of response of cantilevers //20AUG YZ
def est_LDND(norm_diff_point_loc, calib_filepath): 

# read calibration data
    calibration = np.load(
        calib_filepath,
        allow_pickle=True
    ).item()

    ND_cal = calibration["norm_diff"]
    angles_cal = calibration["angles"]

# read the interested point and convert to magnitude //21AUG YZ
    if isinstance(norm_diff_point_loc, np.ndarray):
        z_point = norm_diff_point_loc[0]
    else:
        z_point = norm_diff_point_loc

    mag_point = abs(z_point)

    # Magnitude of 36 calibration points
    mag_cal = np.abs(ND_cal)

# check absolute difference of different between the interested point and calibrations //21AUG YZ
    magnitude_diff = np.abs(
        mag_cal - mag_point
    )

# sort the differences by ascend, keep the 3 smallest, smallest means nearest //21AUG YZ
    nearest_3 = np.argsort(magnitude_diff)[:3]

    AUE_3 = []

    for idx in nearest_3:
        AUE_3.append({
            "index": idx,
            "angle": angles_cal[idx],
            "calibration_point": ND_cal[idx],
            "magnitude": mag_cal[idx],
            "magnitude_diff": magnitude_diff[idx]
        })

    return AUE_3