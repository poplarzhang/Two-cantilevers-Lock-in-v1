import os
import numpy as np



def load_measurements(folder):

    """
    Load all interactive measurements
    from an experiment folder.

    Returns a list of dictionaries.
    """

    files = sorted(
        [
            f for f in os.listdir(folder)
            if f.endswith(".npy")
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


    return measurements




def summarize_measurements(measurements):

    """
    Extract simple parameters
    from every measurement.
    """


    summary = {

        "number": [],

        "r_0": [],

        "r_1": [],

        "phase_0": [],

        "phase_1": []

    }



    for i, measurement in enumerate(
        measurements,
        start=1
    ):


        summary["number"].append(i)


        summary["r_0"].append(
            np.mean(
                measurement["r_0"]
            )
        )


        summary["r_1"].append(
            np.mean(
                measurement["r_1"]
            )
        )


        summary["phase_0"].append(
            np.mean(
                measurement["phase_0"]
            )
        )


        summary["phase_1"].append(
            np.mean(
                measurement["phase_1"]
            )
        )


    return summary