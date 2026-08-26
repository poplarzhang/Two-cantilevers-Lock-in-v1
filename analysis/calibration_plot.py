import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from datetime import datetime # added for enabling timestamp in the plot title //11AUG YZ
import os

timestamp = datetime.now().strftime("%m-%d %H:%M:%S") # implemenet the timestamp in the plot title //11AUG YZ


def plot_calibration(
    calibration,
    save_path
    ): #plot cantilever 1 / cantilever 2 //15AUG YZ
   
    angles = calibration["angles"]
    points = calibration["ratio_points"]
    calib_timestamp = calibration ["created"][:19].replace("T"," - ")

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
        f"ratio of calibration - ({calib_timestamp})" # timestamp added //11AUG YZ 
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
    print(f"calibration of {calib_timestamp}by ratio of mean of responses plotted and saved", timestamp)    


# plot two cantilevers mean values by angle begins //11AUG YZ

def plot_calibration_cantilevers(
    calibration,
    save_path_CL1,
    save_path_CL2
):


    angles = calibration["angles"]
    z0_means = calibration["Cantilever 1"]
    z1_means = calibration["Cantilever 2"]
    calib_timestamp = calibration ["created"][:19].replace("T"," - ")

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
        linewidth=0.5
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
        f"CL1 of calibration - ({calib_timestamp})"
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
        linewidth=0.5
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
        f"CL2 of calibration - ({calib_timestamp})"
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
    print("calibration by cantilevers complex responses plotted and saved", timestamp)
# plot two cantilevers mean values by angle ends //11AUG YZ

# plot two cantilevers mean values difference by angle begins //12AUG YZ

def plot_calibration_diff(
    calibration,
    save_path
    ):

    angles = calibration["angles"]
    points = calibration["diff_points"]
    calib_timestamp = calibration ["created"][:19].replace("T"," - ")


    x = np.real(points)

    y = np.imag(points)

    plt.figure(figsize=(7,6))

    scatter = plt.scatter(
        x,
        y,
        c=angles,
        cmap="hsv",
        s=10 # changed from 60 //11AUG YZ
    )

    for i, angle in enumerate(angles):

        plt.text(
            x[i],
            y[i],
            f"{angle:.0f}°",
            fontsize = 6
        )

    plt.xlabel("Real(Zd)")

    plt.ylabel("Imaginary(Zd)")

    plt.title(
       
        f"diff of calibration- ({calib_timestamp})" 
        
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
    print("calibration by difference of cantilever plotted and saved", timestamp)

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
    calib_timestamp = calibration ["created"][:19].replace("T"," - ")

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
        f"rmmage of calibration - ({calib_timestamp})"
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
    print("calibration by ration of mean magnitude plotted and saved", timestamp)
# plot ratio of two cantilevers mean magnitude by angle ends //14AUG YZ

# plot normalized difference (mean(z0)-mean(z1))/(abs(mean(z0))+abs(mean(z1)))
def plot_calibration_norm_diff(
        calibration,
        save_path = None
):
    fig, ax = plt.subplots(
        figsize=(7,6) #(10, 9) change to (7,6) //20AUG YZ
    )
    ND_cal = calibration["norm_diff"]
    angles_cal = calibration ["angles"]
    calib_timestamp = calibration ["created"][:19].replace("T"," - ")

    sc = ax.scatter(
        ND_cal.real,
        ND_cal.imag,
        c=angles_cal,
        cmap="hsv",
        s=10,
        zorder=3
    )

    ax.plot(
        ND_cal.real,
        ND_cal.imag,
        color="black",
        linewidth=0.5,
        alpha=0.25
    )

    for angle in np.arange(0, 360, 10):

        idx = np.argmin(
            np.abs(
                angles_cal - angle
            )
    )

        if np.isfinite(
        ND_cal[idx].real
        ):

            ax.annotate(
                f"{angle:+.0f}°",
                (
                    ND_cal[idx].real,
                    ND_cal[idx].imag
                ),
                xytext=(4, 4),
                textcoords="offset points",
                fontsize=6,
                bbox=dict(
                    boxstyle="round,pad=0.15",
                    fc="white",
                    ec="none",
                    alpha=0.65
                )
            )


    ax.axhline(
        0,
        color="gray",
        alpha=0.4
    )

    ax.axvline(
        0,
        color="gray",
        alpha=0.4
    )

    ax.set_aspect(
        "equal",
        adjustable="box"
    )

    ax.set_xlabel(
        "Re(ND)"
    )

    ax.set_ylabel(
        "Im(ND)"
    )

    ax.set_title(
        f" norm-diff of calibration - ({calib_timestamp})",
        
    )

    ax.grid(alpha=0.3)

    plt.colorbar(
        sc,
        ax=ax,
        label="Direction (degrees)"
    )

    plt.tight_layout()
    if save_path is not None: 
            plt.savefig(
                save_path,
                dpi=300,
                bbox_inches="tight"
            )

    plt.show()
    plt.close()
    print("calibration by norm_diff plotted and saved", timestamp)
    print("71 67 77 89")
    print("=-=-=-=-=-=")

# plot the AUE orignal and estimation //20AUG YZ
def plot_loc_est(
        norm_diff_point_loc, # normalized difference of interested point //21AUG YZ
        AUE_LDND,   # estimation by the least difference of normalized difference between the in interested point and calibration //21AUG YZ
        calib_filepath, # given calibration
        save_path # auto save plot
):
# load calibration.npy
    calibration = np.load(
        calib_filepath,
        allow_pickle=True
    ).item()

    ND_cal = calibration["norm_diff"]
    angles_cal = calibration["angles"]
    source_stamp = calibration["source_files"]
    calib_timestamp = calibration ["created"][:19].replace("T"," - ")


# read the interested point and convert to magnitude //21AUG YZ
    norm_diff_point_loc_val = norm_diff_point_loc["norm_diff"]
    norm_diff_point_loc_src = norm_diff_point_loc["source_file"]

    if isinstance(norm_diff_point_loc_val, np.ndarray):
        z_point = norm_diff_point_loc_val[0]
    else:
        z_point = norm_diff_point_loc_val

    x_point = z_point.real
    y_point = z_point.imag

    r = abs(z_point)

# initialize the plot
    fig, ax = plt.subplots(
        figsize=(11, 7)
    )

# plotting calibration
    sc = ax.scatter(
        ND_cal.real,
        ND_cal.imag,
        c=angles_cal,
        cmap="hsv",
        s=10,
        zorder=3
    )

# Calibration point labels //21AUG YZ
    for z_cal, angle in zip(ND_cal, angles_cal):

        ax.annotate(
            f"{angle:+.0f}°",
            (
                z_cal.real,
                z_cal.imag
            ),
            xytext=(4, 4),
            textcoords="offset points",
            fontsize=6,
            bbox=dict(
                boxstyle="round,pad=0.15",
                fc="white",
                ec="none",
                alpha=0.65
            )
        )

# circle by the interested point's magnitude //21AUG YZ
    theta = np.linspace(
        0,
        2 * np.pi,
        500
    )

    circle_x = r * np.cos(theta)
    circle_y = r * np.sin(theta)

    ax.plot(
        circle_x,
        circle_y,
        color="gray",
        linewidth=0.8,
        linestyle="--",
        alpha=0.35,
        zorder=1
    )

    marker_angles_deg = np.arange(
        0,
        360,
        10
    )

    marker_angles_rad = np.deg2rad(
        marker_angles_deg
    )

    marker_x = r * np.cos(marker_angles_rad)
    marker_y = r * np.sin(marker_angles_rad)

    ax.scatter(
        marker_x,
        marker_y,
        marker="x",
        color="gray",
        s=35,
        linewidths=1.2,
        alpha=0.35,
        zorder=2
    )

# plot the unknown point on the plane by a red X //21AUG YZ
    ax.scatter(
        x_point,
        y_point,
        marker="x",
        color="red",
        s=100,
        linewidths=2.5,
        zorder=6
    )

# mark the 3 possible resulf from AUE_LDND
    markers = [
        "o",
        "s",
        "^"
    ]
    markers_color = [
        "green",
        "yellow",
        "orange"
    ]

    for result, marker, color in zip(
        AUE_LDND,
        markers,
        markers_color
    ):

        z_cal = result["calibration_point"]

        ax.scatter(
            z_cal.real,
            z_cal.imag,
            marker=marker,
            facecolors="none",
            edgecolors=color,
            s=50,
            linewidths=1.5,
            zorder=7
        )

# axis, title
    ax.axhline(
        0,
        color="gray",
        alpha=0.4
    )

    ax.axvline(
        0,
        color="gray",
        alpha=0.4
    )

    ax.set_aspect(
        "equal",
        adjustable="box"
    )

    ax.set_xlabel(
        "Re(ND)"
    )

    ax.set_ylabel(
        "Im(ND)"
    )

    ax.set_title(
        f"EST by LDND of CAL on {calib_timestamp}\n at {timestamp} for {norm_diff_point_loc_src}" # calibration time, estimation time, file name underestimation //24AUG YZ
    )

    ax.grid(
        alpha=0.3
    )


    cbar = plt.colorbar(
        sc,
        ax=ax,
        label="Direction (degrees)",
        pad = 0.03
    )

# show legends
    legend_handles = [

        Line2D(
            [0], [0],
            marker="x",
            color="red",
            linestyle="None",
            markersize=8,
            markeredgewidth=2,
            label="Unknown"
        ),

        Line2D(
            [0], [0],
            marker="o",
            color="green",
            markerfacecolor="none",
            linestyle="None",
            markersize=7,
            label=f"{AUE_LDND[0]['angle']:+.0f}° - 1st closest"
        ),

        Line2D(
            [0], [0],
            marker="s",
            color="yellow",
            markerfacecolor="none",
            linestyle="None",
            markersize=7,
            label=f"{AUE_LDND[1]['angle']:+.0f}° - 2nd closest"
        ),

        Line2D(
            [0], [0],
            marker="^",
            color="orange",
            markerfacecolor="none",
            linestyle="None",
            markersize=7,
            label=f"{AUE_LDND[2]['angle']:+.0f}° - 3rd closest"
        )
    ]

    fig.subplots_adjust(
        right=0.72
    )
    legend = fig.legend(
        handles=legend_handles,
        loc="upper left",
        bbox_to_anchor=(0.75, 0.9),
        fontsize=6,
        frameon=True
    )
   
    plt.tight_layout()

# save
    plt.savefig(
        save_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()
    plt.close()

    print("estimation plotted and saved",timestamp)
    print("71 67 77 89")
    print("=-=-=-=-=-=")
    
