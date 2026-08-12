import time


class HF2Sweeper:

    def __init__(self, lockin):

        self.lockin = lockin
        self.session = lockin.session
        self.device = lockin.device

        # IMPORTANT:
        # use the actual device ID string
        self.device_id = lockin.device.serial


    def frequency_sweep(
            self,
            f_start,
            f_stop,
            points,
            demods=(0,1)
    ):

        print("Preparing HF2 frequency sweep")


        # --------------------------------------------------
        # Force all demodulators to oscillator 0
        # --------------------------------------------------

        for d in demods:

            print(
                f"Assigning demod {d} -> oscillator 0"
            )

            self.device.demods[d].oscselect(0)


        # --------------------------------------------------
        # Create sweeper
        # --------------------------------------------------

        sweeper = self.session.modules.sweeper

        sweeper.device(
            self.device_id
        )


        # Sweep oscillator frequency
        osc_node = (
            f"/{self.device_id}/oscs/0/freq"
        )

        print(
            "Sweep oscillator:",
            osc_node
        )


        sweeper.gridnode(
            osc_node
        )


        # Ensure oscillator is initialized
        self.device.oscs[0].freq(f_start)

        sweeper.start(
            f_start
        )

        sweeper.stop(
            f_stop
        )

        sweeper.samplecount(
            points
        )

        sweeper.xmapping(
            0
        )


        # Settling

        sweeper.settling.time(
            0.05
        )

        sweeper.settling.inaccuracy(
            0.001
        )


        # --------------------------------------------------
        # Subscribe
        # --------------------------------------------------

        nodes = []

        for d in demods:

            node = (
                f"/{self.device_id}/demods/{d}/sample"
            )

            print(
                "Subscribe:",
                node
            )

            sweeper.subscribe(node)

            nodes.append(node)


        # --------------------------------------------------
        # Run
        # --------------------------------------------------

        print("Starting sweep")

        sweeper.execute()


        while not sweeper.finished():

            progress = sweeper.progress()

            print(
                f"\r{progress*100:5.1f}%",
                end=""
            )

            time.sleep(0.1)


        print("\nSweep complete")


        raw = sweeper.read()


        # --------------------------------------------------
        # Cleanup
        # --------------------------------------------------

        for node in nodes:
            sweeper.unsubscribe(node)


        return raw