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
    return np.mean(z0), np.mean(z1), (np.mean(z0)) / (np.mean(z1)), (np.mean(z0))-(np.mean(z1)), np.mean(np.abs(z0)) / np.mean(np.abs(z1))# //12AUG YZ
# return adds np.mean(np.abs(z0)) / np.mean(np.abs(z1)) //14AUG YZ

# =====================================================
# Build calibration from folder
# =====================================================

def build_calibration(folder):
   
    angles = []
    z0_means = [] #store z0_mean values for cantilever 1 //11AUG YZ
    z1_means = [] #store z1_mean values for cantilever 2 //11AUG YZ
    ratio_points = [] #store ratio of z0_mean/z2_mean, nothing changed, comments for clarficatin //14AUG YZ
    diff_points = [] #store difference between cantilever 1 and cantilever 2//12AUG YZ
    r_m_mags = [] #store the ratio of the mean magnitude of z0 to that of z1 //14AUG YZ
    source_files = []



    # files = sorted(
    #     os.listdir(folder)
    # )
    # npy_files = [
    #     f for f in files
    #     if f.endswith(".npy")
    # ] # check if file type is correct


    # print(
    #     "Found",
    #     len(npy_files),
    #     "measurement files"
    # )
    files = sorted(
    os.listdir(folder)
)

    npy_files = [
        f for f in files
        if f.endswith(".npy")
        and f != "calibration.npy"
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
        z0_mean, z1_mean, zr_mean, zd_mean, zm_mean = calculate_complex_point(measurement) 
        #zr_mean = mean(z0)/mean(z1) //11AUG YZ
        #zd_mean = mean(z0)-mean(z1) //12AUG YZ
        #zm_mean = mean(abs(z0))/mean(abs(z1)) //14AUG YZ

        # code sorted, and z0_means, z1_means are added //11AUG YZ 
        #np.mean(np.abs(z0)) / np.mean(np.abs(z1)) added //14AUG YZ
        angles.append(angle)

        z0_means.append(z0_mean)
        z1_means.append(z1_mean)        
        ratio_points.append(zr_mean)
        diff_points.append(zd_mean)
        r_m_mags.append(zm_mean) #Mean(|z0|) / Mean(|z1|), ratio of mean of magnitude //14AUG YZ


        source_files.append(filename)



        print(
            f"{filename}: angle={angle:.1f}° | "
            f"z0={z0_mean:.4f} | "
            f"z1={z1_mean:.4f} | "
            f"zr={zr_mean:.4f} | "
            f"zd={zd_mean:.4f} | "
            f"zm={zm_mean:.4f}"
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
        "ratio_points":
            np.array(ratio_points),
        # calibration  takes the ratio of two cantilevers for plotting 
        "diff_points":
            np.array(diff_points),
        # calibration takes the difference of mean values of two cantileverss for plotting //12AUG YZ
        "ratio_mean_mag":
            np.array(r_m_mags),
        # calibration takes the ratio of mean magnitude of two cantilevers for plotting //14AUG YZ
        "source_files":
            source_files,
        "created":
            datetime.now().isoformat()
    }
    print()
    print("71 67 77 89")
    print("=-=-=-=-=-=")
    print("calibration built")
    return calibration



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