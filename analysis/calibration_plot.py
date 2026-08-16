import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime # added for enabling timestamp in the plot title //11AUG YZ
import os

timestamp = datetime.now().strftime("%m-%d %H:%M:%S") # implemenet the timestamp in the plot title //11AUG YZ


def plot_calibration(
    calibration,
    save_path
    ): #plot cantilever 1 / cantilever 2 //15AUG YZ
   
    angles = calibration["angles"]

    points = calibration["ratio_points"]

    x = np.real(points)

    y = np.imag(points)

    plt.figure(figsize=(7,6))


    scatter = plt.scatter(
        x,
        y,
        c=angles,
        cmap="viridis",
        s=10 # changed from 60 //11AUG YZ
    )

    for i, angle in enumerate(angles):

        plt.text(
            x[i],
            y[i],
            f"{angle:.0f}°",
            fontsize =6
        )

    plt.xlabel(
        "Real(Zr)" # Zr is changed from Z //12AUG YZ
    )

    plt.ylabel(
        "Imaginary(Zr)" # Zr is changed from Z //12AUG YZ
    )

    plt.title(
        # f"Calibration map"{}
        f"Cantilever ratio - ({timestamp})" # timestamp added //11AUG YZ 
        #//13AUG Cantilever ratio changed from calibration map
        
    )

    plt.colorbar(
        scatter,
        label="Angle (deg)"
    )

    plt.grid(True)
    #plt.axis("equal")
    plt.autoscale()

    if save_path is not None: # save the plot //15AUG YZ
        plt.savefig(
            save_path,
            dpi=300,
            bbox_inches="tight"
        )

    plt.show()
    plt.close()    


# plot two cantilevers mean values by angle begins //11AUG YZ

def plot_calibration_cantilevers(
    calibration,
    save_path_CL1,
    save_path_CL2
):


    angles = calibration["angles"]

    z0_means = calibration["Cantilever 1"]
    z1_means = calibration["Cantilever 2"]

# cantilever 1 takes z0_means //11AUG YZ

    x0 = np.real(z0_means)
    y0 = np.imag(z0_means)

    plt.figure(figsize=(7, 6))

    plt.plot(
        x0,
        y0,
        "o-",
        color="#1f77b4",
        markersize=4,
        linewidth=1
    )

    for i, angle in enumerate(angles):

        plt.text(
            x0[i],
            y0[i],
            f"{angle:.0f}°",
            fontsize=6
        )

    plt.xlabel("Real(Z0)")

    plt.ylabel("Imaginary(Z0)")

    plt.title(
        f"Cantilever 1 - ({timestamp})"
    )

    plt.grid(True)
    #plt.axis("equal")
    plt.autoscale()

    if save_path_CL1 is not None: # save the plot //15AUG YZ
            plt.savefig(
                save_path_CL1,
                dpi=300,
                bbox_inches="tight"
            )
            
    plt.show()
    plt.close() 
    

# cantilever 2 takes z1_means //11AUG YZ  

    x1 = np.real(z1_means)
    y1 = np.imag(z1_means)

    plt.figure(figsize=(7, 6))

    plt.plot(
        x1,
        y1,
        "o-",
        color="#ff7f0e",
        markersize=4,
        linewidth=1
    )

    for i, angle in enumerate(angles):

        plt.text(
            x1[i],
            y1[i],
            f"{angle:.0f}°",
            fontsize=6
        )

    plt.xlabel("Real(Z1)")

    plt.ylabel(
        "Imaginary(Z1)"
    )

    plt.title(
        f"Cantilever 2 - ({timestamp})"
    )

    plt.grid(True)
    #plt.axis("equal")
    plt.autoscale()

    if save_path_CL2 is not None: # save the plot //15AUG YZ
        plt.savefig(
            save_path_CL2,
            dpi=300,
            bbox_inches="tight"
        )
        
    plt.show()
    plt.close() 
# plot two cantilevers mean values by angle ends //11AUG YZ

# plot two cantilevers mean values difference by angle begins //12AUG YZ

def plot_calibration_diff(
    calibration,
    save_path
    ):

    angles = calibration["angles"]

    points = calibration["diff_points"]

    x = np.real(points)

    y = np.imag(points)

    plt.figure(figsize=(7,6))

    scatter = plt.scatter(
        x,
        y,
        c=angles,
        cmap="viridis",
        s=10 # changed from 60 //11AUG YZ
    )

    for i, angle in enumerate(angles):

        plt.text(
            x[i],
            y[i],
            f"{angle:.0f}°",
            fontsize =6
        )

    plt.xlabel("Real(Zd)")

    plt.ylabel("Imaginary(Zd)")

    plt.title(
       
        f"Cantilever diff - ({timestamp})" 
        
    )

    plt.colorbar(
        scatter,
        label="Angle (deg)"
    )

    plt.grid(True)
    #plt.axis("equal")
    if save_path is not None: # save the plot //15AUG YZ
        plt.savefig(
            save_path,
            dpi=300,
            bbox_inches="tight"
        )

    plt.show()
    plt.close()

# plot two cantilevers mean values difference by angle ends //12AUG YZ

# plot ratio of two cantilevers mean magnitude by angle begins //14AUG YZ
def plot_calibration_rmmag(
    calibration,
    save_path=None
): #rmmag is short for ratio of mean magnitude //14AUG YZ

    angles = np.asarray(
        calibration["angles"]
    )

    zm_mean = np.asarray(
        calibration["ratio_mean_mag"]
    )

    plt.figure(figsize=(7, 6))

    plt.scatter(
        angles,
        zm_mean,
        s=10,
        color="tab:blue"
    )

    for i, angle in enumerate(angles):

        plt.text(
            angles[i],
            zm_mean[i],
            f"{angle:.0f}°",
            fontsize=6
        )

    plt.xlabel("Angle (deg)")

    plt.ylabel("Ratio of Mean(|z0|) / Mean(|z1|)")

    plt.title(
        f"Cantilever ratio_mag - ({timestamp})"
    )

    plt.grid(True)

    plt.tight_layout()

    if save_path is not None: # save the plot //15AUG YZ
        plt.savefig(
            save_path,
            dpi=300,
            bbox_inches="tight"
        )

    plt.show()
    plt.close()
# plot ratio of two cantilevers mean magnitude by angle ends //14AUG YZ
