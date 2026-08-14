"""
dataio.py

Functions for saving and loading experiment data.

This module is responsible only for file input/output.
No instrument control or data analysis should be placed here.
"""

import os
from datetime import datetime
import json
import numpy as np


# ==========================================================
# Sweep data
# ==========================================================

def save_sweep(
    data,
    folder="Data",
    prefix="sweep"
):
    """
    Save a frequency sweep.

    Parameters
    ----------
    data : dict
        Sweep data dictionary.

    folder : str
        Destination folder.

    prefix : str
        Prefix for the filename.

    Returns
    -------
    str
        Full path of the saved file.
    """

    # Create folder if necessary

    os.makedirs(
        folder,
        exist_ok=True
    )

    # Timestamp

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    filename = (
        f"{prefix}_{timestamp}.npz"
    )

    filepath = os.path.join(
        folder,
        filename
    )

    # Save

    np.savez(
        filepath,
        **data
    )

    print()
    print("Sweep saved:")
    print(filepath)
    print()

    return filepath


# ==========================================================
# Load sweep
# ==========================================================

def load_sweep(filepath):
    """
    Load one sweep.

    Parameters
    ----------
    filepath : str

    Returns
    -------
    dict
    """

    archive = np.load(filepath)

    data = {}

    for key in archive.files:

        data[key] = archive[key]

    return data


# ==========================================================
# Save measurement
# ==========================================================

def save_measurement(
    measurement,
    filepath
):
    """
    Save one interactive measurement.

    Parameters
    ----------
    measurement : dict

    filepath : str
    """

    np.save(
        filepath,
        measurement,
        allow_pickle=True
    )


# ==========================================================
# Load measurement
# ==========================================================


def load_measurement(filepath):

    measurement = np.load(
        filepath,
        allow_pickle=True
    )

    return measurement.item()


# input path for load experiment, begins //14AUG YZ
def load_measurement_pathinput():
    while True:
        filepath = input(
            "enter the filepath of a measurement, q to quit: "
        ).strip()

        if filepath.lower() == "q":
            print("quit")
            return None

        try:
            measurement = load_measurement(filepath)

            print(f"loading successful: {filepath}")
            return measurement

        except FileNotFoundError:
            print(f"cannot find file: {filepath}")
            print("reenter the filepath, q to quit")

        except Exception as e:
            print(f"cannot be loaded: {e}")
            print("reenter the filepath, q to quit") 
# input path for load experiment, ends //14AUG YZ


# ==========================================================
# Load complete experiment
# ==========================================================

def load_experiment(folder):
    """
    Load every measurement contained
    in one experiment folder.

    Parameters
    ----------
    folder : str

    Returns
    -------
    list
        List of measurement dictionaries.
    """

    measurements = []

    files = sorted(
        os.listdir(folder)
    )

    for filename in files:

        if not filename.endswith(".npy"):
            continue

        filepath = os.path.join(
            folder,
            filename
        )

        measurement = load_measurement(
            filepath
        )

        measurements.append(
            measurement
        )

    print()
    print(
        f"Loaded {len(measurements)} measurements."
    )
    print()

    return measurements


# ==========================================================
# List experiment folders
# ==========================================================

def list_experiments(
    base_folder="Data"
):
    """
    List all experiment folders.

    Parameters
    ----------
    base_folder : str

    Returns
    -------
    list
    """

    if not os.path.exists(
        base_folder
    ):

        return []

    folders = []

    for name in sorted(
        os.listdir(base_folder)
    ):

        path = os.path.join(
            base_folder,
            name
        )

        if os.path.isdir(path):

            folders.append(path)

    return folders


# ==========================================================
# Save sweep into experiment folder
# ==========================================================

def save_sweep_to_folder(
    data,
    folder,
    filename="sweep.npz"
):
    """
    Save the sweep inside an experiment folder.

    Parameters
    ----------
    data : dict

    folder : str

    filename : str
    """

    filepath = os.path.join(
        folder,
        filename
    )

    np.savez(
        filepath,
        **data
    )

    print()

    print("Sweep saved:")

    print(filepath)

    print()

    return filepath


# ==========================================================
# Save resonance fit
# ==========================================================
def save_fit(
    fit,
    folder,
    filename="fit.json"
):

    """
    Save resonance fit result.

    Converts numpy objects into normal Python
    types before writing JSON.
    """

    import json
    import numpy as np
    import os


    os.makedirs(
        folder,
        exist_ok=True
    )


    filepath = os.path.join(
        folder,
        filename
    )


    # Convert numpy objects

    clean_fit = {}

    for key, value in fit.items():

        if isinstance(
            value,
            np.ndarray
        ):

            clean_fit[key] = value.tolist()


        elif isinstance(
            value,
            np.floating
        ):

            clean_fit[key] = float(value)


        elif isinstance(
            value,
            np.integer
        ):

            clean_fit[key] = int(value)


        else:

            clean_fit[key] = value



    with open(
        filepath,
        "w"
    ) as file:

        json.dump(
            clean_fit,
            file,
            indent=4
        )


    print()

    print(
        "Fit saved:"
    )

    print(
        filepath
    )


    return filepath




def save_summary(
    summary,
    folder,
    filename="summary.csv"
):

    import os
    import csv


    filepath = os.path.join(
        folder,
        filename
    )


    keys = list(
        summary.keys()
    )


    rows = zip(
        *[
            summary[key]
            for key in keys
        ]
    )


    with open(
        filepath,
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow(
            keys
        )

        writer.writerows(
            rows
        )


    print(
        "Summary saved:"
    )

    print(
        filepath
    )


    return filepath
    
    