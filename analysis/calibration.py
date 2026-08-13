# analysis/calibration.py
# Apply two cantilevers

import os
import numpy as np
from datetime import datetime


# =====================================================
# Calculate mean complex response of one measurement // one meansurement means one round of measurement
# =====================================================

def calculate_complex_point(measurement):
    """
    Calculate:

        Zr = (x0 + j*y0) / (x1 + j*y1) //Zr changed from Z

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

    # zr = mean(z0) / mean(z1) # ratio //11AUG YZ 
    # zd = mean(z0) - mean(z1) # difference //12AUG YZ

    # return np.mean(z0) 
    # the upper line is changed to the next line to return 3 mean values of mean(z0), mean(z1), and zr=mean(z0)/mean(z1) //11AUG YZ
    # return np.mean(z0), np.mean(z1), (np.mean(z0))/(np.mean(z1)) #11AUG YZ
    # return adds the difference // 12AUG YZ
    return np.mean(z0), np.mean(z1), (np.mean(z0))/(np.mean(z1)), (np.mean(z0))-(np.mean(z1)) # //12AUG YZ

# =====================================================
# Build calibration from folder
# =====================================================

def build_calibration(folder):
    """
    Read all calibration experiments from folder.

    The angle is taken from:

        measurement["metadata"]["experiment_angle"]

    The filename is ignored.// filename contains angle //11AUG YZ

    Returns:

    {
        "angles": [...],
        "complex_points": [...],
        "source_files": [...]
    }

    """


    angles = []
    z0_means = [] #store z0_mean values for cantilever 1 //11AUG YZ
    z1_means = [] #store z1_mean values for cantilever 2 //11AUG YZ
    complex_points = []
    diff_points =[] #store difference between cantilever 1 and cantilever 2//12AUG YZ
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
        # commented to take mean(z0)/mean(z1) for calibration, begins //11AUG YZ
        # z = calculate_complex_point(measurement)
        # commented to take man(z0)/mean(z1)) for calibration, ends //11AUG YZ
        z0_mean, z1_mean, zr_mean, zd_mean = calculate_complex_point(measurement) 
        #zr_mean = mean(z0)/mean(z1) //11AUG YZ
        #zd_mean = mean(z0)-mean(z1) //12AUG YZ

        # code sorted, and z0_means, z1_means are added //11AUG YZ 
        angles.append(angle)

        z0_means.append(z0_mean)
        z1_means.append(z1_mean)
        
        complex_points.append(zr_mean)
        diff_points.append(zd_mean)

        source_files.append(filename)



        print(
            f"{filename}: "
            f"angle={angle}°, "
            f"Z={zr_mean}"
        )



    calibration = {

        "angles":
            np.array(angles),
        # calibration takes the mean values of two cantilevers for plotting begins //11AUG YZ    
        "Cantilever 1":
            np.array(z0_means),
        "Cantilever 2":
            np.array(z1_means),
        # calibration takes the mean values of two cantilevers for plotting ends //11AUG YZ   
        "complex_points":
            np.array(complex_points),
        # calibration takes the difference of mean values of two cantileverss for plotting //12AUG YZ
        "difference_points":
            np.array(diff_points),
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