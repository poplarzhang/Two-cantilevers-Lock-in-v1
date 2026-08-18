import os
import numpy as np
def load_measurements(folder):

   # read all the calibration files by degree, if a calibration.npy exists already, it would be screened out //18AUG YZ

    files = sorted( # implement screen 15AUG YZ
    [
        f for f in os.listdir(folder)
        if f.lower().endswith(".npy")
        and f.lower() != "calibration.npy"
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

        print(
            "Loaded:",
            filename
        )
        print(measurements[-1]) #print the last added item //18AUG YZ
        
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