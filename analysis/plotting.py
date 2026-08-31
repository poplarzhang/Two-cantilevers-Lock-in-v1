import numpy as np

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

import os

from .resonance import lorentzian

from datetime import datetime # added for enabling timestamp in the plot title //11AUG YZ

timestamp = datetime.now().strftime("%m-%d %H:%M:%S") # implemenet the timestamp in the plot title //11AUG YZ


def plot_resonance_fit(
    frequency,
    amplitude,
    fit_result,
    save_path = None, # add saving feature //15AUG YZ
    title= None
    
):

    parameters = fit_result["parameters"]

    f0 = fit_result["f0"]

    Q = fit_result["Q"]

    # Smooth frequency axis for fitted curve

    frequency_fit = np.linspace(
        frequency[0],
        frequency[-1],
        1000
    )

    amplitude_fit = lorentzian(
        frequency_fit,
        *parameters
    )

    plt.figure(
        figsize=(9,5)
    )

    # measured data

    plt.plot(
        frequency,
        amplitude,
        "o",
        label="Measurement"
    )

    # fitted curve

    plt.plot(
        frequency_fit,
        amplitude_fit,
        "-",
        label="Lorentzian fit"
    )

    plt.yscale("log") # log scale on y axis //16AUG YZ

    # resonance frequency

    plt.axvline(
        f0,
        color="red",
        linestyle="--",
        label=f"f0 = {f0:.2f} Hz"
    )

    plt.xlabel(
        "Frequency (Hz)"
    )

    plt.ylabel(
        "Amplitude R"
    )

    plt.title(
        f"{title}\nQ = {Q:.1f}"
    )

    plt.grid()
    plt.legend()

    if save_path is not None: #save to a given path from external calling for //15AUG YZ
        plt.savefig(
            save_path,
            dpi=300,
            bbox_inches="tight"

        )

    plt.show()
    plt.close( )
    

def plot_amplitude_summary(
    summary,
    save_path=None
):

    fig, ax1 = plt.subplots(
        figsize=(9, 5)
    )

#demod0 - CL1 - left Y axis

    ax1.plot(
        summary["angle"],
        summary["r_0"],
        'o-',
        color="#1f77b4",
        label="Demod 0",
        linewidth=1,
        markersize=4
    )

    ax1.set_xlabel(
        "Measurement angle"
    )

    ax1.set_ylabel(
        "Demod 0 Amplitude R",
        color="#1f77b4"
    )

    ax1.tick_params(
        axis="y",
        labelcolor="#1f77b4"
    )

    ax1.grid()

#demod1 - CL2 - right Y axis

    ax2 = ax1.twinx()

    ax2.plot(
        summary["angle"],
        summary["r_1"],
        'o-',
        color="#d62728",
        label="Demod 1",
        linewidth=1,
        markersize=4
    )

    ax2.set_ylabel(
        "Demod 1 Amplitude R",
        color="#d62728"
    )

    ax2.tick_params(
        axis="y",
        labelcolor="#d62728"
    )

#title

    ax1.set_title(
        f'AMP evolution by {summary["created"][-1]}\n'
        f'on {timestamp}'
    )

#legends handler

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()

    ax1.legend(
        lines1 + lines2,
        labels1 + labels2
    )

    if save_path is not None:

        plt.savefig(
            save_path,
            dpi=300,
            bbox_inches="tight"
        )

    plt.show()
    plt.close()
   
def plot_phase_summary(
    summary,
    save_path = None # add saving feature //15AUG YZ
):

    plt.figure(
        figsize=(9,5)
    )

    plt.plot(
        summary["angle"],#["number"], change number to angel //18AUG YZ
        summary["phase_0"],
        'o-',
        label="Phase 0"
    )

    plt.plot(
        summary["angle"],#["number"],
        summary["phase_1"],
        'o-',
        label="Phase 1"
    )

    plt.xlabel(
        "Measurement angle" #change number to angel //18AUG YZ
    )

    plt.ylabel(
        "Phase"
    )

    plt.title(
        # "Phase evolution" title changed to "Cantilever phase evolution" //10AUG YZ
        # "Cantilever phase evolution" #10AUG YZ
        f'Ph. evolution by {summary["created"][-1]}\n'
        f'on {timestamp}'        
    )

    plt.grid()
    plt.legend()

    if save_path is not None: #save to a given path from external calling for //15AUG YZ
        plt.savefig(
            save_path,
            dpi=300,
            bbox_inches="tight"
        )

    plt.show()
    plt.close()

#### add new plotting of in-phase and quadrature components #### //18AUG YZ
def plot_xcomp_summary(
    summary,
    save_path = None 
):

    plt.figure(
        figsize=(9,5)
    )

    plt.plot(
        summary["angle"],
        summary["x_0"],
        'o-',
        label="cantilever 1 in-phase"
    )

    plt.xlabel(
        "Measurement angle"
    )

    plt.ylabel(
        "in-Phase component"
    )

    plt.title(
        f"Cantilever 1 in-phase evolution by {summary["created"][-1]}\non {timestamp}"
    )

    plt.grid()
    plt.legend()

    if save_path is not None:

        plt.savefig(
            os.path.join(
                save_path,
                "CL1 in-phase EVL.png"
            ),
            dpi=300,
            bbox_inches="tight"
        )

    plt.show()
    plt.close()
    plt.figure(
        figsize=(9, 5)
    )

    plt.plot(
        summary["angle"],
        summary["x_1"],
        'o-',
        label="cantilever 2 in-phase"
    )

    plt.xlabel(
        "Measurement angle"
    )

    plt.ylabel(
        "in-Phase component"
    )

    plt.title(
        f"Cantilever 2 in-phase evolution by {summary["created"][-1]}\non {timestamp}"
    )

    plt.grid()
    plt.legend()

    if save_path is not None:

        plt.savefig(
            os.path.join(
                save_path,
                "CL2 in-phase EVL.png"
            ),
            dpi=300,
            bbox_inches="tight"
        )

    plt.show()
    plt.close()


def plot_ycomp_summary(
    summary,
    save_path = None 
):

    plt.figure(
        figsize=(9,5)
    )

    plt.plot(
        summary["angle"],
        summary["y_0"],
        'o-',
        label="cantilever 1 quadrature"
    )

    plt.xlabel(
        "Measurement angle"
    )

    plt.ylabel(
        "quadrature component"
    )

    plt.title(
        f"Cantilever 1 quadrature evolution by {summary["created"][-1]}\non {timestamp}"
    )

    plt.grid()
    plt.legend()

    if save_path is not None:

        plt.savefig(
            os.path.join(
                save_path,
                "CL1 quadrature EVL.png"
            ),
            dpi=300,
            bbox_inches="tight"
        )

    plt.show()
    plt.close()
    plt.figure(
        figsize=(9, 5)
    )

    plt.plot(
        summary["angle"],
        summary["y_1"],
        'o-',
        label="cantilever 2 quadrature"
    )

    plt.xlabel(
        "Measurement angle"
    )

    plt.ylabel(
        "quadrature component"
    )

    plt.title(
        f"Cantilever 2 quadrature evolution by {summary["created"][-1]}\non {timestamp}"
    )

    plt.grid()
    plt.legend()

    if save_path is not None:

        plt.savefig(
            os.path.join(
                save_path,
                "CL2 quadrature EVL.png"
            ),
            dpi=300,
            bbox_inches="tight"
        )

    plt.show()
    plt.close()

# plot all components combined //24AUG YZ
def plot_components_summary(
    summary,
    save_path=None
):

    fig, ax1 = plt.subplots(
        figsize=(10, 6)
    )

    angle = summary["angle"]

# CL1 on the left Y axis

    ax1.plot(
        angle,
        summary["x_0"],
        'o-',
        color="#1f77b4",
        label="CL1 in-phase",
        linewidth=1,
        markersize=4
    )

    ax1.plot(
        angle,
        summary["y_0"],
        'o--',
        color="#1f77b4",
        label="CL1 quadrature",
        linewidth=1,
        markersize=4
    )

    ax1.set_xlabel(
        "Measurement angle"
    )

    ax1.set_ylabel(
        "CL1 component",
        color="#1f77b4"
    )

    ax1.tick_params(
        axis="y",
        labelcolor="#1f77b4"
    )

#CL2 on the right Y axis

    ax2 = ax1.twinx()

    ax2.plot(
        angle,
        summary["x_1"],
        's-',
        color="#d62728",
        label="CL2 in-phase",
        linewidth=1,
        markersize=4
    )

    ax2.plot(
        angle,
        summary["y_1"],
        's--',
        color="#d62728",
        label="CL2 quadrature",
        linewidth=1,
        markersize=4
    )

    ax2.set_ylabel(
        "CL2 component",
        color="#d62728"
    )

    ax2.tick_params(
        axis="y",
        labelcolor="#d62728"
    )


    ax1.set_title(
        f'Cantilever components evolution by {summary["created"][-1]}\n'
        f'on {timestamp}'
    )

    ax1.grid()

# legends handler

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()

    ax1.legend(
        lines1 + lines2,
        labels1 + labels2
    )


    if save_path is not None:

        plt.savefig(
            os.path.join(
                save_path,
                "CL1_CL2_components_EVL.png"
            ),
            dpi=300,
            bbox_inches="tight"
        )

    plt.show()
    plt.close()

def plot_sweep(
    frequency,
    amplitude_0,
    amplitude_1,
    fit_0,
    fit_1,
    timestamp=None,
    save_path=None
):
   # RES_0 and RES_1 are the resonances of two cantilevers //15AUG YZ
    RES_0 = np.interp( 
        fit_0["f0"],
        frequency,
        amplitude_0
    )

    RES_1 = np.interp(
        fit_1["f0"],
        frequency,
        amplitude_1
    )

# prepare figure

    plt.figure(
        figsize=(9, 5)
    )

    plt.plot(
        frequency,
        amplitude_0,
        label="Demod 0"
    )

    plt.plot(
        frequency,
        amplitude_1,
        label="Demod 1"
    )

    plt.yscale("log") # log scale for Y axis //16AUG YZ 

# find intersections

    difference = amplitude_0 - amplitude_1

    intx_freqs = []
    intx_amps = []

    for i in range(len(frequency) - 1):

        d1 = difference[i]
        d2 = difference[i + 1]

        # Exact intersection
        if d1 == 0:

            f_cross = frequency[i]
            r_cross = amplitude_0[i]

            intx_freqs.append(
                f_cross
            )

            intx_amps.append(
                r_cross
            )

        # Intersection between neighboring points
        elif d1 * d2 < 0:

            f1 = frequency[i]
            f2 = frequency[i + 1]

            # Linear interpolation
            alpha = -d1 / (d2 - d1)

            f_cross = (
                f1
                + alpha * (f2 - f1)
            )

            r0_cross = (
                amplitude_0[i]
                + alpha * (
                    amplitude_0[i + 1]
                    - amplitude_0[i]
                )
            )

            r1_cross = (
                amplitude_1[i]
                + alpha * (
                    amplitude_1[i + 1]
                    - amplitude_1[i]
                )
            )
            
            # Average the two amplitudes
            r_cross = (
                r0_cross + r1_cross
            ) / 2

            intx_freqs.append(
                f_cross
            )

            intx_amps.append(
                r_cross
            )
            print(f_cross,",", r_cross)

# pop out top 3 intersections
    intx = list(
        zip(
            intx_freqs,
            intx_amps
        )
    )

    intx.sort(
        key=lambda x: x[1],
        reverse=True
    )

    top_intx = intx[:3]

# print top 3 intersection for check

    if len(top_intx) == 0:

        print(
            "No intersection found."
        )

    else:

        print()
        print(
            "Top intersection(s) by amplitude:"
        )

        for f_cross, r_cross in top_intx:

            print(
                f"Frequency = {f_cross:.6f} Hz, "
                f"Amplitude = {r_cross:.6e}"
            )

# mark top 3 intersections

    if len(top_intx) > 0:

        intx_freqs_top = [
            x[0]
            for x in top_intx
        ]

        intx_amps_top = [
            x[1]
            for x in top_intx
        ]

        plt.scatter(
            intx_freqs_top,
            intx_amps_top,
            color="red",
            s=20,
            zorder=5,
            label="Top intersections"
        )

# annotations of intersections

    offset_y = 30

    for i, (f_cross, r_cross) in enumerate(top_intx):

        offset_y = offset_y + 10

        plt.annotate(
            f"{f_cross:.2f} Hz",
            xy=(f_cross, r_cross),
            xytext=(5, offset_y),
            textcoords="offset points",
            ha="left",
            va="bottom" if offset_y > 0 else "top",
        )

# show resonances

    plt.scatter(
        fit_0["f0"],
        RES_0,
        color="blue",
        s=30,
        zorder=6,
        label="Resonances"
    )

    plt.scatter(
        fit_1["f0"],
        RES_1,
        color="blue",
        s=30,
        zorder=6
    )

# annotation of resonances

    plt.annotate(
        f"f = {fit_0['f0']:.2f} Hz\n"
        f"R = {RES_0:.4e}",
        xy=(fit_0["f0"], RES_0),
        xytext=(5, 10),
        textcoords="offset points"
    )

    plt.annotate(
        f"f = {fit_1['f0']:.2f} Hz\n"
        f"R = {RES_1:.4e}",
        xy=(fit_1["f0"], RES_1),
        xytext=(5, 10),
        textcoords="offset points"
    )

# config labels on axises

    plt.xlabel(
        "Frequency (Hz)"
    )

    plt.ylabel(
        "Amplitude R"
    )

    if timestamp is not None:

        plt.title(
            f"Sweep result ({timestamp})"
        )

    else:

        plt.title(
            "Sweep result"
        )

    plt.grid()

    plt.legend()

    plt.tight_layout()

# save plot of sweeping

    if save_path is not None:

        plt.savefig(
            save_path,
            dpi=300,
            bbox_inches="tight"
        )

    plt.show()
    plt.close()

# commentted the plotting of ratio since not used and has been moved to calibration_plot.py //15AUG YZ

# move all the plot function into  plotting.py, calibration_plot.py will be obsolete. //28AUG YZ

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

def plot_calibration_power(# plot power of calibration //30AUG YZ
    calibration,
    save_path=None
): 

    angles = np.asarray(
        calibration["angles"]
    )

    power = np.asarray(
        calibration["power"]
    )

    calib_timestamp = calibration["created"][:19].replace("T", " - ")

    plt.figure(figsize=(7, 6))

    plt.scatter(
        angles,
        power,
        s=10,
        color="tab:blue"
    )

    for i, angle in enumerate(angles):

        plt.text(
            angles[i],
            power[i],
            f"{angle:.0f}°",
            fontsize=6
        )

    plt.xlabel("Angle (deg)")

    plt.ylabel(
        "Power (|z0|² + |z1|²)"
    )

    plt.title(
        f"Power of calibration - ({calib_timestamp})"
    )

    plt.grid(True)

    plt.tight_layout()

    if save_path is not None: # save the plot //30AUG YZ
        plt.savefig(
            save_path,
            dpi=300,
            bbox_inches="tight"
        )

    plt.show()

    plt.close()

    print(
        "Calibration power plotted and saved", timestamp)


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
        f"EST by LDND of CAL on {calib_timestamp}\n at {timestamp} for {norm_diff_point_loc_src}" 
        # calibration time, estimation time, file name underestimation //24AUG YZ
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

def plot_pwr_est(
        comp_point_loc,
        FRES_3,
        calib_filepath,
        save_path
):
   # load calibration

    calibration = np.load(
        calib_filepath,
        allow_pickle=True
    ).item()

    power_cal = np.asarray(calibration["power"])

    angles_cal = np.asarray(calibration["angles"])

    calib_timestamp = (calibration["created"][:19].replace("T", " - "))

    # load interested point
    pwr_point_loc_src = (comp_point_loc["source_file"])

    #initial plot
    fig, ax = plt.subplots(
        figsize=(11, 7)
    )


    #plot calibration
    ax.scatter(
        angles_cal,
        power_cal,
        marker="x",
        color="gray",
        s=35,
        linewidths=1.2,
        alpha=0.55,
        zorder=3
    )
   
    for power, angle in zip(
        power_cal,
        angles_cal
    ):

        ax.annotate(
            f"{angle:+.0f}°",
            (
                angle,
                power
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


   # mark the nearest 3

    markers = [
        "o",
        "s",
        "^"
    ]

    markers_color = [
        "green",
        "orange",
        "red"
    ]


    for result, marker, color in zip(
        FRES_3,
        markers,
        markers_color
    ):

        idx = result["index"]
        angle = result["angle"]

        power = power_cal[idx]
        ax.scatter(
            angle,
            power,
            marker=marker,
            facecolors="none",
            edgecolors=color,
            s=70,
            linewidths=1.8,
            zorder=7
        )


    # axes

    ax.set_xlabel(
        "Angle (deg)"
    )

    ax.set_ylabel(
        "Power (|z0|² + |z1|²)"
    )


    # title

    ax.set_title(
        f"EST by FRES of CAL on {calib_timestamp}\n"
        f"at {timestamp} for {pwr_point_loc_src}"
    )


    ax.grid(alpha=0.3)


    # legen

    legend_handles = [

        Line2D(
            [0], [0],
            marker="x",
            color="gray",
            linestyle="None",
            markersize=7,
            markeredgewidth=1.5,
            label="Calibration"
        ),

        Line2D(
            [0], [0],
            marker="o",
            color="green",
            markerfacecolor="none",
            linestyle="None",
            markersize=8,
            markeredgewidth=1.8,
            label=(
                f"{FRES_3[0]['angle']:+.0f}° "
                f"- 1st closest"
            )
        ),

        Line2D(
            [0], [0],
            marker="s",
            color="orange",
            markerfacecolor="none",
            linestyle="None",
            markersize=8,
            markeredgewidth=1.8,
            label=(
                f"{FRES_3[1]['angle']:+.0f}° "
                f"- 2nd closest"
            )
        ),

        Line2D(
            [0], [0],
            marker="^",
            color="red",
            markerfacecolor="none",
            linestyle="None",
            markersize=8,
            markeredgewidth=1.8,
            label=(
                f"{FRES_3[2]['angle']:+.0f}° "
                f"- 3rd closest"
            )
        )
    ]


    fig.subplots_adjust(
        right=0.72
    )

    fig.legend(
        handles=legend_handles,
        loc="upper left",
        bbox_to_anchor=(0.75, 0.9),
        fontsize=7,
        frameon=True
    )


    plt.tight_layout()

    plt.savefig(
        save_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()
    plt.close()
    print("FRES estimation plotted and saved",timestamp)
