"""
Plotting tools for resonance analysis.
"""

import numpy as np
import matplotlib.pyplot as plt


from .resonance import lorentzian



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
        "Cantilever amplitude evolution"
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
        "Phase evolution"
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
        s=80
    )


    plt.colorbar(
        scatter,
        label=color_label
    )


    for i in range(len(x)):

        if "labels" in result:

            text = result["labels"][i]

        else:

            text = str(i+1)


        plt.text(
            x[i],
            y[i],
            text
        )


    plt.axhline(
        0,
        color="black",
        linewidth=0.8
    )


    plt.axvline(
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
        "Complex Ratio Evolution"
    )


    plt.grid()

    plt.axis(
        "equal"
    )


    plt.show()