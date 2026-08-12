"""
Plotting tools for resonance analysis.
"""

import numpy as np
import matplotlib.pyplot as plt


from .resonance import lorentzian

from datetime import datetime # added for enabling timestamp in the plot title //11AUG YZ

timestamp = datetime.now().strftime("%m-%d %H:%M:%S") # implemenet the timestamp in the plot title //11AUG YZ


def plot_resonance_fit(
    frequency,
    amplitude,
    fit_result,
    title="Resonance fit"
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

    plt.show()

    

def plot_measurement_summary(
    summary
):

    plt.figure(
        figsize=(9,5)
    )


    plt.plot(
        summary["number"],
        summary["r_0"],
        'o-',
        label="Demod 0"
    )


    plt.plot(
        summary["number"],
        summary["r_1"],
        'o-',
        label="Demod 1"
    )


    plt.xlabel(
        "Measurement number"
    )

    plt.ylabel(
        "Amplitude R"
    )


    plt.title(
        # "Cantilever amplitude evolution" timestamp added //11AUG YZ
        f"Cantilever amplitude evolution\n{timestamp}"
    )


    plt.grid()

    plt.legend()

    plt.show()


def plot_phase_summary(
    summary
):

    plt.figure(
        figsize=(9,5)
    )


    plt.plot(
        summary["number"],
        summary["phase_0"],
        'o-',
        label="Phase 0"
    )


    plt.plot(
        summary["number"],
        summary["phase_1"],
        'o-',
        label="Phase 1"
    )


    plt.xlabel(
        "Measurement number"
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

    plt.show()


def plot_complex_ratio(
    result
):

    import matplotlib.pyplot as plt


    x = result["real"]
    y = result["imag"]


    if "experiment_angle" in result:

        color = result["experiment_angle"]

        color_label = (
            "Experimental angle (deg)"
        )

    else:

        color = range(len(x))

        color_label = (
            "Measurement number"
        )


    plt.figure(
        figsize=(6,6)
    )


    plt.plot(
        x,
        y,
        color="gray",
        linewidth=1
    )


    scatter = plt.scatter(
        x,
        y,
        c=color,
        cmap="viridis",
        s=20 # changed from 80 //11AUG YZ
    )


    plt.colorbar(
        scatter,
        label=color_label
    )


    # for i in range(len(x)): // commented out //11AUG YZ

    #     if "labels" in result:

    #         text = result["labels"][i]

    #     else:

    #         text = str(i+1)


    #     plt.text(
    #         x[i],
    #         y[i],
    #         text
    #     )

    for i in range(len(x)): # added for plotting the experimental angle on the complex plane //11AUG YZ

        if "experiment_angle" in result:

            text = f"{result['experiment_angle'][i]:g}°"

        else:

            text = str(i + 1)

        plt.text(
            x[i],
            y[i],
            text,
            fontsize=6
    )  # added for plotting the experimental angle on the complex plane //11AUG YZ
        # angle text has font size =6


    plt.axhline( # horizontal line plotting //10AUG YZ
        0,
        color="black",
        linewidth=0.8
    )


    plt.axvline( # vertical line plotting //10AUG YZ
        0,
        color="black",
        linewidth=0.8
    )


    plt.xlabel(
        "Re(Z₀/Z₁)"
    )

    plt.ylabel(
        "Im(Z₀/Z₁)"
    )


    plt.title(
        # "Complex Ratio Evolution" timestamp added //11AUG YZ
          f"Complex Ratio Evolution\n{timestamp}"
    )


    plt.grid()

    plt.axis(
        "equal"
    )


    plt.show()