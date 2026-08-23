import os
import numpy as np
import json

def load_measurements(folder):

   # read all the calibration files by degree, if a calibration.npy exists already, it would be screened out //18AUG YZ

    files = sorted( # implement screen 15AUG YZ
    [
        f for f in os.listdir(folder)
        if f.lower().endswith(".npy")
        and "calibration" not in f.lower()
        and "aue" not in f.lower()
    ]
)
    measurements = []

    for filename in files:

        path = os.path.join(
            folder,
            filename
        )


        data = np.load(
            path,
            allow_pickle=True
        ).item()


        measurements.append(
            data
        )

        # print(
        #     "Loaded:",
        #     filename
        # )
        # print(measurements[-1]) #print the last added item //18AUG YZ
        
    return measurements




def summarize_measurements(measurements):

# returned structure as below
# summary
# {
#     "angle": [0, 10, 20, 30, ...],

#     "x_0": [mean_x0_0, mean_x0_10, mean_x0_20, ...],

#     "y_0": [mean_y0_0, mean_y0_10, mean_y0_20, ...],

#     "x_1": [mean_x1_0, mean_x1_10, mean_x1_20, ...],

#     "y_1": [mean_y1_0, mean_y1_10, mean_y1_20, ...]
# }



    summary = { # the summary has been changed from the sequence of calibration,
    # magnitude of cantilevers, and phase of cantilevers to new components //17AUG
        "angle": [], #"number": [], sequence number to angle
        "created": [], # added to read calibration points created timestamp //23
        "x_0": [], #"r_0": [], CH1 magnitude to CH1 in-phase component
        "y_0": [],#"r_1": [], CH2 magnitude to CH1 quadrature component
        "x_1": [],#"phase_0": [], CH1 phase to CH2 in-phase component
        "y_1": [],# "phase_1": [], CH2 phase to CH2 quadrature component
        "r_0": [],
        "r_1": [],
        "phase_0": [],
        "phase_1":[]

    }

    for i, measurement in enumerate(
        measurements,
        start=1
    ):
        summary["angle"].append(measurement["metadata"]
            ["experiment_angle"])#summary["number"].append(i)
        summary["created"].append(measurement["metadata"]
            ["timestamp"][:19].replace("T", " ")
        )


# the following data is still taking the average from the calibration files, format is changed to: angle, x_0, y_0, x_1, y_1 //17AUG YZ
        summary["x_0"].append(# summary["r_0"].append(
            np.mean(#     np.mean(
                 measurement["x_0"]#         measurement["r_0"]
            )#     )
        )# )

        summary["y_0"].append(# summary["r_1"].append(
            np.mean(#     np.mean(
                measurement["y_0"]#         measurement["r_1"]
            )#     )
        )# )

        summary["x_1"].append(# summary["phase_0"].append(
            np.mean(#     np.mean(
                measurement["x_1"]#         measurement["phase_0"]
            )#     )
        )# )

        summary["y_1"].append(# summary["phase_1"].append(
            np.mean(   #     np.mean(
                measurement["y_1"]#         measurement["phase_1"]
            )#     )
        )# )

        summary["r_0"].append(
            np.mean(measurement["r_0"])
        )
        summary["r_1"].append(
            np.mean(measurement["r_1"])
        )

        summary["phase_0"].append(
            np.mean(measurement["phase_0"])
        )
        summary["phase_1"].append(
            np.mean(measurement["phase_1"])
        )


    return summary

def fit_load(experiment_folder):

    fit0_file = os.path.join(
        experiment_folder,
        "fit_demod0.json"
    )

    fit1_file = os.path.join(
        experiment_folder,
        "fit_demod1.json"
    )

    with open(fit0_file, "r") as f:
        fit0 = json.load(f)

    with open(fit1_file, "r") as f:
        fit1 = json.load(f)

    print()
    print("Fit demod 0:")
    print(fit0)

    print()
    print("Fit demod 1:")
    print(fit1)

    return fit0, fit1