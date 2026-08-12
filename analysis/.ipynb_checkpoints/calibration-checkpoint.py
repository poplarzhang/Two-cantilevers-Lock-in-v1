# analysis/calibration.py

import os
import numpy as np
from datetime import datetime


# =====================================================
# Calculate mean complex response of one measurement
# =====================================================

def calculate_complex_point(measurement):
    """
    Calculate:

        Z = (x0 + j*y0) / (x1 + j*y1)

    using all recorded samples.

    Returns:
        mean complex value
    """


    x0 = np.asarray(
        measurement["x_0"]
    )

    y0 = np.asarray(
        measurement["y_0"]
    )


    x1 = np.asarray(
        measurement["x_1"]
    )

    y1 = np.asarray(
        measurement["y_1"]
    )


    z0 = x0 + 1j * y0

    z1 = x1 + 1j * y1


    z = z0 / z1


    return np.mean(z)



# =====================================================
# Build calibration from folder
# =====================================================

def build_calibration(folder):
    """
    Read all calibration experiments from folder.

    The angle is taken from:

        measurement["metadata"]["experiment_angle"]

    The filename is ignored.

    Returns:

    {
        "angles": [...],
        "complex_points": [...],
        "source_files": [...]
    }

    """


    angles = []

    complex_points = []

    source_files = []



    files = sorted(
        os.listdir(folder)
    )


    npy_files = [
        f for f in files
        if f.endswith(".npy")
    ]


    print(
        "Found",
        len(npy_files),
        "measurement files"
    )



    for filename in npy_files:


        filepath = os.path.join(
            folder,
            filename
        )


        measurement = np.load(
            filepath,
            allow_pickle=True
        ).item()



        # -----------------------------
        # Read angle from metadata
        # -----------------------------

        angle = (
            measurement["metadata"]
            ["experiment_angle"]
        )



        # -----------------------------
        # Calculate mean complex point
        # -----------------------------

        z = calculate_complex_point(
            measurement
        )



        angles.append(
            angle
        )

        complex_points.append(
            z
        )

        source_files.append(
            filename
        )



        print(
            f"{filename}: "
            f"angle={angle}°, "
            f"Z={z}"
        )



    calibration = {

        "angles":
            np.array(angles),

        "complex_points":
            np.array(complex_points),

        "source_files":
            source_files,

        "created":
            datetime.now().isoformat()
    }


    return calibration



# =====================================================
# Save calibration
# =====================================================

def save_calibration(
    calibration,
    filename
):

    np.save(
        filename,
        calibration,
        allow_pickle=True
    )



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



# =====================================================
# Estimate unknown angle
# =====================================================

def estimate_angle(
    measurement,
    calibration
):
    """
    Estimate angle of an unknown measurement.

    Method:
        1. Calculate mean complex response
        2. Compare with calibration points
        3. Return closest angle

    """

    z_unknown = calculate_complex_point(
        measurement
    )


    calibration_points = (
        calibration["complex_points"]
    )

    angles = (
        calibration["angles"]
    )


    distances = np.abs(
        calibration_points - z_unknown
    )


    index = np.argmin(
        distances
    )


    estimated_angle = angles[index]


    return {
        "angle": estimated_angle,
        "complex_point": z_unknown,
        "distance": distances[index]
    }

# =====================================================
# Estimate unknown angle with interpolation
# =====================================================

def estimate_angle_interpolated(
    measurement,
    calibration
):
    """
    Estimate angle using linear interpolation
    between calibration points in the complex plane.
    """

    z_unknown = calculate_complex_point(
        measurement
    )

    points = calibration["complex_points"]
    angles = calibration["angles"]


    best_distance = np.inf
    best_angle = None


    # Check every segment between calibration points

    for i in range(len(points)-1):

        z1 = points[i]
        z2 = points[i+1]

        a1 = angles[i]
        a2 = angles[i+1]


        # Vector along calibration curve

        dz = z2 - z1


        if dz == 0:
            continue


        # Projection of unknown point onto segment

        t = np.real(
            (z_unknown - z1)
            * np.conj(dz)
        ) / (
            np.abs(dz)**2
        )


        # Limit to this segment

        t_clipped = np.clip(
            t,
            0,
            1
        )


        z_projection = (
            z1
            +
            t_clipped * dz
        )


        distance = abs(
            z_unknown - z_projection
        )


        if distance < best_distance:

            best_distance = distance

            best_angle = (
                a1
                +
                t_clipped
                *
                (a2 - a1)
            )


    return {
        "angle": best_angle,
        "complex_point": z_unknown,
        "distance": best_distance
    }