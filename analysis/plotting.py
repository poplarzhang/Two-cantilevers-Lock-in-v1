import numpy as np
import matplotlib.pyplot as plt
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
    
    
    """
    Plot measured data and fitted Lorentzian.

    Parameters
    ----------
    frequency :
        frequency array

    amplitude :
        measured amplitude

    fit_result :
        dictionary returned by fit_resonance()

    """



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

    

def plot_amplitude_summary( # amplitude changed from measurements //18AUG YZ
    summary,
    save_path = None # add saving feature //15AUG YZ
):
   
    plt.figure(
        figsize=(9,5)
    )


    plt.plot(
        summary["angle"],#["number"], //18AUG YZ
        summary["r_0"],
        'o-',
        label="Demod 0"
    )


    plt.plot(
        summary["angle"],#["number"], //18AUG YZ
        summary["r_1"],
        'o-',
        label="Demod 1"
    )


    plt.xlabel(
        "Measurement angle"# change number to angel //18AUG YZ
    )

    plt.ylabel(
        "Amplitude R"
    )

    plt.title(        
        f"Cantilever amplitude evolution\n{timestamp}" # "Cantilever amplitude evolution" timestamp added //11AUG YZ
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
        f"Cantilever phase evolution\n{timestamp}" #timestamp added //11AUG YZ        
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
        "Phase"
    )

    plt.title(
       f"Cantilever in-phase evolution\n{timestamp}" 
    )


    plt.grid()
    plt.legend()

    if save_path is not None: 
        plt.savefig(
            save_path,
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
        "Phase"
    )

    plt.title(
       f"Cantilever quadrature evolution\n{timestamp}" 
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


# plot the sweep result has been move from main.ipynb to plotting.py //15AUG YZ

def plot_sweep(
    frequency, # frequency for sweeping
    amplitude_0, # responses from cantilever
    amplitude_1,
    fit_0, # resonance fitting result
    fit_1,
    timestamp=None, # timestampe as the 1st cell in main.ipynt
    save_path=None # file path to save
):
    """
    Plot sweep result for two cantilevers.

    Parameters
    ----------
    frequency : array-like
        Frequency array.

    amplitude_0 : array-like
        Amplitude of demodulator 0.

    amplitude_1 : array-like
        Amplitude of demodulator 1.

    fit_0 : dict
        Resonance fitting result for demodulator 0.

    fit_1 : dict
        Resonance fitting result for demodulator 1.

    timestamp : str, optional
        Timestamp shown in the plot title.

    save_path : str, optional
        Path where the plot will be saved.
    """

    # =====================================================
    # Amplitude at fitted resonance frequencies
    # =====================================================

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
# lables

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

# list intersections 15AUG YZ

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
            print(f_cross,"'",r_cross)# new intersection will be printed 16AUG YZ// amplitudes are in float, equal floats are difficult to be met. 16AUG YZ

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
            print(f_cross,"'",r_cross)# new intersection will be printed 16AUG YZ

            intx_freqs.append(
                f_cross
            )

            intx_amps.append(
                r_cross
            )
# find top 3 intersections //15AUG YZ

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

# printting intersections //15AUG YZ

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
# plotting intersections //15AUG YZ

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

# annotation of intersections //15AUG YZ

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
# plotting //15AUG YZ

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

# config plot style

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

# save plot

    if save_path is not None:

        plt.savefig(
            save_path,
            dpi=300,
            bbox_inches="tight"
        )

    plt.show()
    plt.close()

# plot the sweep result, ends //12AUG YZ
# plot the sweep result has been move from main.ipynb to plotting.py //15AUG YZ
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