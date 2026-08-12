import time
import numpy as np


class HF2Recorder:
    """
    Fixed-frequency recorder for HF2LI.
    """

    def __init__(self, lockin):

        self.controller = lockin

        self.device = lockin.lockin.device
        self.session = lockin.lockin.session



    def set_frequency(self, frequency):

        self.controller.set_frequency(
            frequency
        )



    def record(
        self,
        duration=1.0,
        demods=(0,1)
    ):
        """
        Record demodulator data.

        Returns:
        {
            "time": ...,
            "channels": {
                0:{...},
                1:{...}
            }
        }
        """

        print(
            f"Recording {duration} s..."
        )


        nodes = []


        # Subscribe

        for d in demods:

            node = self.device.demods[d].sample

            self.session.daq.subscribe(
                node
            )

            nodes.append(node)



        # Wait for data

        time.sleep(
            duration
        )


        # Read

        raw = self.session.daq.poll(
            duration,
            0.001,
            True,
            True
        )



        # Remove subscriptions

        for node in nodes:

            self.session.daq.unsubscribe(
                node
            )



        measurement = {

            "frequency":
                self.device.oscs[0].freq(),

            "duration":
                duration,

            "channels": {}

        }



        # Extract channels

        for d in demods:

            key = (
                f"/{self.device.serial}"
                f"/demods/{d}/sample"
            )


            sample = raw[key][0]


            measurement["channels"][d] = {

                "time":
                    np.asarray(
                        sample["timestamp"]
                    ),

                "x":
                    np.asarray(
                        sample["x"]
                    ),

                "y":
                    np.asarray(
                        sample["y"]
                    ),

                "r":
                    np.sqrt(
                        np.asarray(sample["x"])**2
                        +
                        np.asarray(sample["y"])**2
                    ),

                "phase":
                    np.asarray(
                        sample["phase"]
                    )

            }


        print("Recording finished")

        return measurement