import os
import numpy as np
from pathlib import Path
from datetime import datetime

from measurements.recorder import HF2LIRecorder

from instrument.hf2li import HF2LI

from instrument.config import (
     DEVICE_ID,
    SERVER_HOST,
    HF2,

    OUTPUT_CHANNEL,

    ADC_1,
    ADC_2,

    DEMOD_1,
    DEMOD_2,

    DEMOD_RATE_1,
    DEMOD_RATE_2,

    OSCILLATOR_1,
    OSCILLATOR_2,
)


class ExperimentRunner:
    """
    Interactive experiment controller.
    """

    def __init__(
        self,
        recorder,
        settings,
        metadata=None,
        base_folder="Data",
    ):
        """
        Parameters
        ----------
        recorder :
            HF2LIRecorder object.

        settings :
            Dictionary containing experiment settings.

        metadata :
            Optional dictionary containing additional
            information such as resonance frequency.

        base_folder :
            Directory where all experiments are stored.
        """

        self.recorder = recorder
        self.settings = settings
        self.metadata = metadata if metadata is not None else {}

        # --------------------------------------------------
        # Create experiment folder
        # --------------------------------------------------

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        self.run_folder = os.path.join(
            base_folder,
            timestamp
        )

        os.makedirs(
            self.run_folder,
            exist_ok=True
        )

        print()
        # print("====================================")
        print("Experiment folder created")
        print(self.run_folder)
        # print("====================================")
        # print()

        self.save_settings()

    # ======================================================
    # Save settings
    # ======================================================

    def save_settings(self):
        """
        Save experiment settings to a text file.
        """

        filename = os.path.join(
            self.run_folder,
            "settings.txt"
        )

        with open(filename, "w") as file:

            file.write("HF2LI Experiment\n")
            file.write("=========================\n\n")

            file.write("Settings\n")
            file.write("-------------------------\n")

            for key, value in self.settings.items():
                file.write(f"{key}: {value}\n")

            if len(self.metadata) > 0:

                file.write("\nMetadata\n")
                file.write("-------------------------\n")

                for key, value in self.metadata.items():
                    file.write(f"{key}: {value}\n")

        print("Settings saved.",filename)
        print()

    # ======================================================
    # Save one measurement
    # ======================================================

    def save_measurement(
        self,
        measurement,
        number,
        # label, remove the label input as decription //10AUG YZ
        experiment_angle,
        prefix=None,
        
    ):
        """
        Save one measurement.
        """

        # save_label = label.replace(" ", "_") remove the label input as decription //10AUG YZ
        if prefix is None:
            filename = (
                # f"{number:03d}_{safe_label}.npy" //change to show angle in filename instead of label //10AUG YZ
                f"{number:03d}_angle_{int(experiment_angle)}.npy"
            )
        else:
            filename = (f"{prefix}.npy")

        filepath = os.path.join(
            self.run_folder,
            filename
        )

        # Add metadata to saved measurement

        measurement["metadata"] = {

            
            **self.metadata,

            "number": number,

            "experiment_angle": experiment_angle,

            "timestamp": datetime.now().isoformat(),
        }

        np.save(
            filepath,
            measurement,
            allow_pickle=True,
        )

        print(f"Saved: {filepath}")

    # ======================================================
    # Main experiment loop
    # ======================================================

    def run(
        self,
        duration=2.0,
    ):
        """
        Interactive experiment.
        """

        measurement_number = 1

        while True:

            self.recorder.lockin.disable_excitation()
            
            print()
            print("--------------------------------")

            print(
                f"Measurement {measurement_number}"
            )
           
            experiment_angle_input = input(
                "Experimental angle (deg), q = quit: "  
            )

            if experiment_angle_input.lower() == "q":
                print()
                print("Experiment finished.")
                break

            experiment_angle = float(experiment_angle_input)
            
            
            input(
                "Adjust experiment and press ENTER..."
            )

            print()
            print("Recording...")

            measurement = self.recorder.record(
                duration=duration
            )

            print("Recording finished.")


            print("DEBUG experiment_angle =",experiment_angle)

            
            self.save_measurement(
                measurement,
                measurement_number,
                #label, remove the label input as decription //10AUG YZ
                experiment_angle,
            )

            measurement_number += 1

            
    def loc_run( # new function of localization experiment //20AUG YZ
        self,
        duration=2.0,
    ):      
        self.recorder.lockin.disable_excitation() 
        measurement_number = 1       
         
        experiment_angle_input = input("Experimental angle (deg), q = quit: ")

        if experiment_angle_input.lower() == "q":
            print()
            print("localization quit.")
            return

        experiment_angle = float(experiment_angle_input)
    
        excitation_source_input = input("Excitation source (e = external, l = lock-in amplifier, q = quit): ")

        if excitation_source_input.lower() == "q":
            print()
            print("localization quit.")
            return

        if excitation_source_input.lower() == "e":
            excitation_source = "EXT"
        elif excitation_source_input.lower() == "l":
            excitation_source = "LIA"
        else:
            print("Invalid excitation source.")
            return

    # Distance
        distance_input = input("Distance (cm), q = quit: ")

        if distance_input.lower() == "q":
            print()
            print("localization quit.")
            return

        try:
            distance = float(distance_input)
        except ValueError:
            print("Invalid distance.")
            return

        input("confirm to execute, press ENTER...")
        print("Recording...")

        measurement = self.recorder.record(duration=duration)

        print(f"Recording finished, {(experiment_angle)}° - {(distance)}cm - {(excitation_source)}.")

        prefix_label = (f"AUE{int(experiment_angle)}_{int(distance)}_{excitation_source}")
        self.save_measurement(
            measurement,
            measurement_number,
            experiment_angle,
            prefix= prefix_label
        )


# arbitrary experiment to estimate an unknow angle //04SEP YZ
def arb_run(
    dest_folder,
    duration=2.0,
):
  # check the given path
    os.makedirs(
        dest_folder,
        exist_ok=True
    )

   # define the parameters of the experiment, user input required //04SEP YZ
    # frequency
    frequency_input = input(
        "Drive frequency (Hz), q = quit: "
    ).strip()

    if frequency_input.lower() == "q":
        print()
        print("ARB quit.")
        return

    try:
        frequency = float(frequency_input)

    except ValueError:
        print("Invalid frequency.")
        return

   # angle

    angle_input = input(
        "Experimental angle (deg), q = quit: "
    ).strip()

    if angle_input.lower() == "q":
        print()
        print("ARB quit.")
        return

    try:
        experiment_angle = float(angle_input)

    except ValueError:
        print("Invalid angle.")
        return

    # amplitude

    amplitude_input = input(
        "Drive amplitude (V), q = quit: "
    ).strip()

    if amplitude_input.lower() == "q":
        print()
        print("ARB quit.")
        return

    try:
        amplitude = float(amplitude_input)

    except ValueError:
        print("Invalid amplitude.")
        return

    # source, mark only

    excitation_source_input = input(
        "Excitation source "
        "(e = external, l = lock-in amplifier, q = quit): "
    ).strip().lower()

    if excitation_source_input == "q":
        print()
        print("ARB quit.")
        return

    if excitation_source_input == "e":

        excitation_source = "EXT"

    elif excitation_source_input == "l":

        excitation_source = "LIA"

    else:

        print("Invalid excitation source.")
        return

    # distance

    distance_input = input(
        "Distance (cm), q = quit: "
    ).strip()

    if distance_input.lower() == "q":
        print()
        print("ARB quit.")
        return

    try:
        distance = float(distance_input)

    except ValueError:
        print("Invalid distance.")
        return

    # print paramters for hint and confirmation

    print(f"ARB - {frequency} Hz - {experiment_angle}° - {amplitude*1000} mV - {excitation_source} - {distance} cm")
    

   # confirm to execute

    confirmation = input(
        "ENTER to execute. q = quit: "
    ).strip()

    if confirmation.lower() == "q":

        print()
        print("ARB quit.")

        return

   # connect, initialize, configure, record, save

    print()
    print("start")

    lockin = HF2LI(
        device_id=DEVICE_ID,
        host=SERVER_HOST,
        hf2=HF2,
    )

    lockin.connect()

    try:  
      
        lockin.initialize()      


        lockin.set_frequency(
            frequency=frequency,
            oscillator=OSCILLATOR_1,
            verbose=True
        )

      
        lockin.configure_demod(
            demod=DEMOD_1,
            adc=ADC_1,
            oscillator=OSCILLATOR_1,
            rate=DEMOD_RATE_1
        )
       

        lockin.configure_demod(
            demod=DEMOD_2,
            adc=ADC_2,
            oscillator=OSCILLATOR_2,
            rate=DEMOD_RATE_2
        )

        
        output = lockin.device.sigouts[
            OUTPUT_CHANNEL
        ]

        output.offset(0.0)

        output.amplitudes[0](
            amplitude
        )

        output.enables[0](True)

        # Keep physical output OFF
        output.on(False)

        print(
            "Amplitude configured."
        )

    # recorder

        recorder = HF2LIRecorder(
            lockin,
            demods=(
                DEMOD_1,
                DEMOD_2
            )
        )

    
       # recording

        try:

            measurement = recorder.record(
                duration=duration
            )

        finally:

            # Safety: always turn excitation OFF
            lockin.disable_excitation()

        print()
        print("Recording finished.")

       # meatadata

        measurement["metadata"] = {

            "frequency": frequency,
            "amplitude": amplitude,
            "experiment_angle": experiment_angle,
            "distance": distance,
            "excitation_source": excitation_source,
            "duration": duration,
            "oscillator": OSCILLATOR_1,
            "output_channel": OUTPUT_CHANNEL,
            "demodulators": (
                DEMOD_1,
                DEMOD_2
            ),

            "timestamp": datetime.now().isoformat(),
        }

# save the measurement with a filename including parameters

        filename = (
            f"AUE"
            f"{int(frequency)}_"
            f"{int(experiment_angle)}_"
            f"{amplitude*1000:g}_"
            f"{int(distance)}_"
            f"{excitation_source}.npy"
        ) # format = frequency_angle_amplitude_distance_source

        filepath = os.path.join(
            dest_folder,
            filename
        )
  
        np.save(
            filepath,
            measurement,
            allow_pickle=True
        )

        print(filepath)
        print("ARB done and saved")
    
    finally:

        # turn off excitation and exit
        try:

            lockin.disable_excitation()

        except Exception:
            pass

        lockin.disconnect()

        print()
        print("ARB experiment finished.")



def con_AUE( #convert a meansurement file of the angle under estimation to a dictionary variant //20AUG YZ
    aue_filename
):
    data = np.load(
        aue_filename,
        allow_pickle=True
    ).item()
# reading
    angle = data["metadata"]["experiment_angle"]
    AUE_time = data["metadata"]["timestamp"]
    x0 = np.mean(data["x_0"])
    y0 = np.mean(data["y_0"])

    x1 = np.mean(data["x_1"])
    y1 = np.mean(data["y_1"])

    r0 = np.mean(data["r_0"])
    r1 = np.mean(data["r_1"])

    phase0 = np.mean(data["phase_0"])
    phase1 = np.mean(data["phase_1"])

# converting
    z0 = x0 + 1j * y0
    z1 = x1 + 1j * y1

    ratio_points = z0 / z1

    diff_points = z0 - z1

    ratio_mean_mag = r0 / r1

    mag_mean_z0 = abs(z0)
    mag_mean_z1 = abs(z1)

    norm_diff = (
        diff_points /
        (mag_mean_z0 + mag_mean_z1)
    )

# generating, val_for_loc means value for localizing
    val_for_loc = {

        "angle":
            np.array([angle]),
        "Cantilever 1":
            np.array([z0]),
        "Cantilever 2":
            np.array([z1]),
        "ratio_points":
            np.array([ratio_points]),
        "diff_points":
            np.array([diff_points]),
        "ratio_mean_mag":
            np.array([ratio_mean_mag]),
        "r_0":
            np.array([r0]),
        "r_1":
            np.array([r1]),
        "phase_0":
            np.array([phase0]),
        "phase_1":
            np.array([phase1]),
        "norm_diff":
            np.array([norm_diff]),
        "power":
            np.array([mag_mean_z0**2 + mag_mean_z1**2]), # added for using full residual estimation //28AUG YZ
        "source_files":
            [Path(aue_filename).name],
        "created":
            AUE_time
    }

    return val_for_loc   


# estimation of an point's angle //20AUG YZ
# LDND = Least Difference of Normalized Difference of mean of response of cantilevers //20AUG YZ
def est_LDND(norm_diff_point_loc, calib_filepath): 

# read calibration data
    calibration = np.load(
        calib_filepath,
        allow_pickle=True
    ).item()

    ND_cal = calibration["norm_diff"]
    angles_cal = calibration["angles"]

# read the value of point under estimation 
    norm_diff_point_loc_val = norm_diff_point_loc["norm_diff"]
    norm_diff_point_loc_src = norm_diff_point_loc["source_file"]#source stamp //

# read the point under estimation and convert to magnitude //21AUG YZ
    if isinstance(norm_diff_point_loc_val, np.ndarray):
        z_point = norm_diff_point_loc_val[0]
    else:
        z_point = norm_diff_point_loc_val
    # Magnitude of the point under estimation
    mag_point = abs(z_point)

    # Magnitude of 36 calibration points
    mag_cal = np.abs(ND_cal)

# check absolute difference of different between the point under estimation and the known calibrations //21AUG YZ
    magnitude_diff = np.abs( mag_cal - mag_point)

# sort the differences by ascend, keep the 3 smallest, smallest means nearest //21AUG YZ
    nearest_3 = np.argsort(magnitude_diff)[:3]

    AUE_3 = [] # most possible estimation result //21AUG YZ
    print()
    for idx in nearest_3:
        AUE_3.append({
            "index": idx,
            "angle": angles_cal[idx],
            "calibration_point": ND_cal[idx],
            "magnitude": mag_cal[idx],
            "magnitude_diff": magnitude_diff[idx],
            "est_source_file": norm_diff_point_loc_src
        })
        print(
            f"Angle: {angles_cal[idx]:+.1f}°, "
            f"MAG: {mag_cal[idx]:.6f} - "
            f"ABS of MAG_DIFF: {abs(magnitude_diff[idx]):.6f}"
        )
    return AUE_3


#FRES, estimation by Full RESidual //28AUG YZ
def est_FRES(comp_point_loc, calib_filepath):

  # read calibration data
    calibration = np.load(
        calib_filepath,
        allow_pickle=True
    ).item()

    angles_cal = calibration["angles"] 
    cal_z0 = calibration["Cantilever 1"]
    cal_z1 = calibration["Cantilever 2"]
    cal_power =  calibration["power"]   
  
    comp_point_loc_z0 = comp_point_loc["z0"] [0]
    comp_point_loc_z1 = comp_point_loc["z1"] [0]
    comp_point_loc_vec = np. array( # vector of point's complex to localize
        [
            comp_point_loc_z0,
            comp_point_loc_z1
        ],
        dtype=complex
    )
    comp_point_loc_power = comp_point_loc["power"][0]

    FRES_result = []

    for z0, z1, power, angle in zip(
        cal_z0,
        cal_z1,
        cal_power,
        angles_cal
    ):
        cal_vec = np.array(
            [
                z0,
                z1
            ],
            dtype = complex
        )

        if (
            power < 1e-30 # check measured power //30AUG YZ
            or comp_point_loc_power < 1e-30
        ):
            residual = np.inf
            ccon = 0 + 0j# a Complex CONstant defined by calibration and point under estiamtion //30AUG YZ
          
        else:
            ccon = ( 
                np.vdot(
                    cal_vec,
                    comp_point_loc_vec
                )
                /
                power
            )
            residual = np. linalg.norm( comp_point_loc_vec-ccon*cal_vec )
            
      
        FRES_result.append(
            (
                angle,
                residual,
                ccon
            )
        )
  

    FRES_result = np. array( # format and conver result
            FRES_result,
            dtype = [
                ("angle", "f8"),
                ("residual", "f8"),
                ("ccon", "c16")
            ]
        )

    nearest_3 = np.argsort(FRES_result["residual"])[:3]

    AUE_3 = []
    for idx in nearest_3:

        AUE_3.append({

            "index":idx,

            "angle":FRES_result["angle"][idx],

            "residual":FRES_result["residual"][idx],

            "C":FRES_result["ccon"][idx],

            "est_source_file":comp_point_loc["source_file"]
        })


        print(
            f"Angle: "
            f"{FRES_result['angle'][idx]:+.1f}°, "
            f"Residual: "
            f"{FRES_result['residual'][idx]:.6f}, "
            f"C: "
            f"{FRES_result['ccon'][idx]}"
        )
        
        
    return AUE_3


def est_DIFF(comp_point_loc, calib_filepath):

    # read calibration data
    calibration = np.load(
        calib_filepath,
        allow_pickle=True
    ).item()

    angles_cal = calibration["angles"]
    cal_z0 = calibration["Cantilever 1"]
    cal_z1 = calibration["Cantilever 2"]


  # point under estimation, taking the two cantilever's complex value and convert to a vector //03SEP YZ

    comp_point_loc_z0 = comp_point_loc["z0"][0]
    comp_point_loc_z1 = comp_point_loc["z1"][0]

    comp_point_loc_vec = np.array(
        [
            comp_point_loc_z0,
            comp_point_loc_z1
        ],
        dtype=complex
    )


   # calculate the difference between the vector of point under estimation and the vector of calibration points //03SEP YZ

    DIFF_result = []

    for z0, z1, angle in zip(
        cal_z0,
        cal_z1,
        angles_cal
    ):

        # Calibration complex vector
        cal_vec = np.array(
            [
                z0,
                z1
            ],
            dtype=complex
        )


        # Difference between unknown and calibration
        diff_vec = (
            comp_point_loc_vec
            -
            cal_vec
        )


        # Sum of magnitudes of the two differences
        mag_diff = (
            abs(diff_vec[0])
            +
            abs(diff_vec[1])
        )

        DIFF_result.append(
            (
                angle,
                mag_diff
            )
        )

    # convert the result to a numpy array //03SEP YZ

    DIFF_result = np.array(
        DIFF_result,
        dtype=[
            ("angle", "f8"),
            ("mag_diff", "f8")
        ]
    )


   # sort 

    nearest_3 = np.argsort(
        DIFF_result["mag_diff"]
    )[:3]

    # take the minium 3 points and return
    AUE_3 = []

    for idx in nearest_3:

        AUE_3.append({

            "index":
                idx,

            "angle":
                DIFF_result["angle"][idx],

            "mag_diff":
                DIFF_result["mag_diff"][idx],

            "calibration_point":
                np.array(
                    [
                        cal_z0[idx],
                        cal_z1[idx]
                    ],
                    dtype=complex
                ),

            "est_source_file":
                comp_point_loc["source_file"]
        })


        print(
            f"Angle: "
            f"{DIFF_result['angle'][idx]:+.1f}°, "
            f"Difference: "
            f"{DIFF_result['mag_diff'][idx]:.6f}"
        )


    return AUE_3
 