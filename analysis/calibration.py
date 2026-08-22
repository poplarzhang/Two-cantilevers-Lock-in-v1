# analysis/calibration.py
# Apply two cantilevers

import os
from pathlib import Path
import numpy as np
from datetime import datetime

# import the summary.csv to build calibration //19AUG YZ

###################################commented for test 19AUG YZ ###################################################
def build_calibration_from_csv(experiment_folder):
    filename = os.path.join(experiment_folder, "summary.csv")
# load summary.csv
    data = np.genfromtxt(
        filename,
        delimiter=",",
        names=True
    )
    summary_timestamp = datetime.fromtimestamp(
        os.path.getctime(filename)
    ).isoformat()
# read values

    angles = data["angle"]

    x0 = data["x_0"]
    y0 = data["y_0"]

    x1 = data["x_1"]
    y1 = data["y_1"]

    r0 = data["r_0"]
    r1 = data["r_1"]

    phase0 = data["phase_0"]
    phase1 = data["phase_1"]

# create calibration results

    z0 = x0 + 1j * y0 # x0, x1, y0, y1 are mean values at different angles already //19AUG YZ
    z1 = x1 + 1j * y1 # create a mean complex number //19AUG YZ

   
    ratio_points = z0 / z1
    diff_points = z0 - z1

    ratio_mean_mag = r0 / r1 # r0 and r1 are mean of magnitudes at one angle, mean(abs(cantilever output))
    
    mag_mean_z0 = abs(z0)
    mag_mean_z1 = abs(z1)

    calibration_from_summary= {

        "angles":
            np.array(angles),
        "Cantilever 1":
            np.array(z0),
        "Cantilever 2":
            np.array(z1),
        "ratio_points":
            np.array(ratio_points),
        "diff_points":
            np.array(diff_points),
        "ratio_mean_mag":
            np.array(ratio_mean_mag),
        "r_0":
            np.array(r0),
        "r_1":
            np.array(r1),
        "phase_0":
            np.array(phase0),
        "phase_1":
            np.array(phase1),
        "norm_diff":
            np.array(diff_points/(mag_mean_z0+mag_mean_z1)),

        "source_files":
            [Path(filename).resolve()],
        "created":
            summary_timestamp #datetime.now().isoformat()
    }

    print()
    print("Calibration built from CSV")
    print(f"Source: {filename}")
    print(f"Number of angles: {len(angles)}")
    print(calibration_from_summary)
    print("71 67 77 89")
    print("=-=-=-=-=-=")

    return calibration_from_summary


# =====================================================
# Save calibration
# =====================================================

def save_calibration(
    calibration,
    filename
):
    
    if os.path.exists(filename):

        while True:

            answer = input(
                f"calibration exists as {filename}\n"
                f" y to overwrite or q to quit.\n"
            ).strip().lower()

            if answer == "q":
                print("Quit.")
                raise SystemExit

            elif answer in ("y", "yes"):
                break

            else:
                print("Invalid input, y to overwrite or q to quit.") 
    np.save(
        filename,
        calibration,
        allow_pickle=True
    )
    print()
    print("71 67 77 89")
    print("=-=-=-=-=-=")
    print(f"Calibration saved: {filename}") # show a successful save
    
# =====================================================
# Load calibration
# =====================================================

def load_calibration(
    filename
):

    return np.load(
        filename,
        allow_pickle=True
    ).item()


