"""
Tools for extracting measurement channels
from saved HF2LI sweeps.
"""



def get_channel(
    data,
    demod=0,
    quantity="r"
):

    """
    Extract one measurement quantity.

    Parameters
    ----------
    data :
        sweep dictionary

    demod :
        demodulator number

    quantity :
        x, y, r, phase


    Returns
    -------
    numpy array
    """



    key = (
        f"{quantity}_{demod}"
    )


    if key not in data:

        raise KeyError(
            f"{key} not found in data"
        )


    return data[key]



def get_frequency(
    data
):

    """
    Return frequency axis.
    """

    return data["frequency"]