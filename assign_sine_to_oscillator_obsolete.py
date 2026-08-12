def assign_sine_to_oscillator(
    self,
    sine=0,
    oscillator=0,
    verbose=False
):
    """
    Assign a sine generator to an oscillator.

    sine:
        0 -> Sine 1
        1 -> Sine 2
        ...
        7 -> Sine 8

    oscillator:
        0 -> Oscillator 1
        1 -> Oscillator 2
        ...
        5 -> Oscillator 6
    """

    self.device.sines[sine].oscselect(oscillator)

    if verbose:
        print(
            f"Sine {sine+1} assigned to Oscillator {oscillator+1}"
        )