import pyvisa
import time


class RigolDS2202E:
    """
    PyVISA driver for Rigol DS2202E oscilloscope.

    Communication:
        Ethernet / TCPIP / VISA

    Example:
        scope = RigolDS2202E("192.168.1.100")
    """

    # ==========================================================
    # INITIALIZATION / CONNECTION
    # ==========================================================

    def __init__(self, ip_address, timeout=5000):
        """
        Create VISA connection to the oscilloscope.
        """

        self.ip_address = ip_address
        self.timeout = timeout

        # VISA Resource Manager
        self.rm = pyvisa.ResourceManager()

        # Ethernet VISA resource
        resource_name = f"TCPIP::{ip_address}::INSTR"

        # Open connection
        self.scope = self.rm.open_resource(resource_name)

        # VISA settings
        self.scope.timeout = timeout
        self.scope.write_termination = "\n"
        self.scope.read_termination = "\n"

    # ==========================================================
    # BASIC VISA COMMUNICATION
    # ==========================================================

    def write(self, command):
        """
        Send a SCPI command.

        Example:
            scope.write(":RUN")
        """

        return self.scope.write(command)

    def query(self, command):
        """
        Send a SCPI query and return the response.

        Example:
            scope.query("*IDN?")
        """

        return self.scope.query(command).strip()

    def read(self):
        """
        Read response from oscilloscope.
        """

        return self.scope.read().strip()

    # ==========================================================
    # IDENTIFICATION / SYSTEM
    # ==========================================================

    def identify(self):
        """
        Return instrument identification.
        """

        return self.query("*IDN?")

    def reset(self):
        """
        Reset oscilloscope to factory/default state.
        """

        self.write("*RST")

    def clear_status(self):
        """
        Clear instrument status.
        """

        self.write("*CLS")

    def wait(self):
        """
        Wait for pending operations to complete.
        """

        self.write("*WAI")

    def operation_complete(self):
        """
        Query whether previous operation is complete.
        """

        return self.query("*OPC?")

    def get_error(self):
        """
        Read the next instrument error.
        """

        return self.query(":SYSTem:ERRor?")

    # ==========================================================
    # ACQUISITION CONTROL
    # ==========================================================

    def run(self):
        """
        Start continuous acquisition.
        """

        self.write(":RUN")

    def stop(self):
        """
        Stop acquisition.
        """

        self.write(":STOP")

    def single(self):
        """
        Perform a single acquisition.
        """

        self.write(":SINGle")

    def force_trigger(self):
        """
        Force a trigger event.
        """

        self.write(":TFORce")

    def autoscale(self):
        """
        Automatically scale the waveform.
        """

        self.write(":AUToscale")

    # ==========================================================
    # CHANNEL CONTROL
    # ==========================================================

    def channel_on(self, channel):
        """
        Turn channel ON.

        Example:
            scope.channel_on(1)
        """

        self.write(
            f":CHANnel{channel}:DISPlay ON"
        )

    def channel_off(self, channel):
        """
        Turn channel OFF.
        """

        self.write(
            f":CHANnel{channel}:DISPlay OFF"
        )

    def set_channel_scale(self, channel, volts_per_div):
        """
        Set vertical scale.

        Example:
            scope.set_channel_scale(1, 1)
        """

        self.write(
            f":CHANnel{channel}:SCALe {volts_per_div}"
        )

    def get_channel_scale(self, channel):
        """
        Read vertical scale.
        """

        return float(
            self.query(
                f":CHANnel{channel}:SCALe?"
            )
        )

    def set_channel_offset(self, channel, offset):
        """
        Set vertical offset.
        """

        self.write(
            f":CHANnel{channel}:OFFSet {offset}"
        )

    def get_channel_offset(self, channel):
        """
        Read vertical offset.
        """

        return float(
            self.query(
                f":CHANnel{channel}:OFFSet?"
            )
        )

    # ==========================================================
    # TIMEBASE
    # ==========================================================

    def set_timebase(self, seconds_per_div):
        """
        Set horizontal scale.

        Example:
            scope.set_timebase(1e-3)
        """

        self.write(
            f":TIMebase:MAIN:SCALe {seconds_per_div}"
        )

    def get_timebase(self):
        """
        Read horizontal scale.
        """

        return float(
            self.query(
                ":TIMebase:MAIN:SCALe?"
            )
        )

    # ==========================================================
    # TRIGGER
    # ==========================================================

    def set_trigger_source(self, source):
        """
        Set trigger source.

        Example:
            scope.set_trigger_source("CHANnel1")
        """

        self.write(
            f":TRIGger:EDGe:SOURce {source}"
        )

    def set_trigger_slope(self, slope):
        """
        Set trigger slope.

        Example:
            POSitive
            NEGative
        """

        self.write(
            f":TRIGger:EDGe:SLOPe {slope}"
        )

    def set_trigger_level(self, level):
        """
        Set trigger level.
        """

        self.write(
            f":TRIGger:EDGe:LEVel {level}"
        )

    def get_trigger_level(self):
        """
        Read trigger level.
        """

        return float(
            self.query(
                ":TRIGger:EDGe:LEVel?"
            )
        )

    # ==========================================================
    # MEASUREMENTS
    # ==========================================================

    def measure_vpp(self, channel):
        """
        Measure peak-to-peak voltage.
        """

        command = f":MEASure:VPP? CHANnel{channel}"

        return float(self.query(command))

    def measure_vmax(self, channel):
        """
        Measure maximum voltage.
        """

        command = f":MEASure:VMAX? CHANnel{channel}"

        return float(self.query(command))

    def measure_vmin(self, channel):
        """
        Measure minimum voltage.
        """

        command = f":MEASure:VMIN? CHANnel{channel}"

        return float(self.query(command))

    def measure_vrms(self, channel):
        """
        Measure RMS voltage.
        """

        command = f":MEASure:VRMS? CHANnel{channel}"

        return float(self.query(command))

    def measure_frequency(self, channel):
        """
        Measure frequency.
        """

        command = f":MEASure:FREQuency? CHANnel{channel}"

        return float(self.query(command))

    def measure_period(self, channel):
        """
        Measure period.
        """

        command = f":MEASure:PERiod? CHANnel{channel}"

        return float(self.query(command))

    def measure_rise_time(self, channel):
        """
        Measure rise time.
        """

        command = f":MEASure:RTIMe? CHANnel{channel}"

        return float(self.query(command))

    def measure_fall_time(self, channel):
        """
        Measure fall time.
        """

        command = f":MEASure:FTIMe? CHANnel{channel}"

        return float(self.query(command))

    def measure_positive_pulse_width(self, channel):
        """
        Measure positive pulse width.
        """

        command = f":MEASure:PWIDth? CHANnel{channel}"

        return float(self.query(command))

    def measure_negative_pulse_width(self, channel):
        """
        Measure negative pulse width.
        """

        command = f":MEASure:NWIDth? CHANnel{channel}"

        return float(self.query(command))

    def measure_positive_duty_cycle(self, channel):
        """
        Measure positive duty cycle.
        """

        command = f":MEASure:PDUTy? CHANnel{channel}"

        return float(self.query(command))

    def measure_negative_duty_cycle(self, channel):
        """
        Measure negative duty cycle.
        """

        command = f":MEASure:NDUTy? CHANnel{channel}"

        return float(self.query(command))

    # ==========================================================
    # MEASUREMENT COLLECTION
    # ==========================================================

    def get_measurements(self, channel):
        """
        Return common measurements in a dictionary.

        Note:
        Measurement command support should be verified
        against the DS2202E programming manual.
        """

        measurements = {}

        measurements["VPP"] = self.measure_vpp(channel)
        measurements["VMAX"] = self.measure_vmax(channel)
        measurements["VMIN"] = self.measure_vmin(channel)
        measurements["VRMS"] = self.measure_vrms(channel)
        measurements["Frequency"] = self.measure_frequency(channel)
        measurements["Period"] = self.measure_period(channel)

        return measurements

    # ==========================================================
    # WAVEFORM SETTINGS
    # ==========================================================

    def set_waveform_source(self, channel):
        """
        Select waveform source.

        Example:
            scope.set_waveform_source(1)
        """

        self.write(
            f":WAVeform:SOURce CHANnel{channel}"
        )

    def set_waveform_mode(self, mode="NORMal"):
        """
        Set waveform acquisition mode.
        """

        self.write(
            f":WAVeform:MODE {mode}"
        )

    def set_waveform_format(self, data_format="BYTE"):
        """
        Set waveform data format.

        Typical choices:
            BYTE
            WORD
            ASCii
        """

        self.write(
            f":WAVeform:FORMat {data_format}"
        )

    # ==========================================================
    # RAW SCPI ACCESS
    # ==========================================================

    def send_command(self, command):
        """
        Send arbitrary SCPI command.

        This provides access to commands that have not yet
        been wrapped into a dedicated Python method.
        """

        self.write(command)

    def send_query(self, command):
        """
        Send arbitrary SCPI query.
        """

        return self.query(command)

    # ==========================================================
    # CONNECTION TEST
    # ==========================================================

    def test_connection(self):
        """
        Test communication with oscilloscope.
        """

        try:

            response = self.identify()

            return {
                "connected": True,
                "identity": response
            }

        except Exception as error:

            return {
                "connected": False,
                "error": str(error)
            }

    # ==========================================================
    # CLOSE CONNECTION
    # ==========================================================

    def close(self):
        """
        Close VISA connection.
        """

        try:
            self.scope.close()
        finally:
            self.rm.close()

    # ==========================================================
    # CONTEXT MANAGER
    # ==========================================================

    def __enter__(self):
        """
        Allows:

            with RigolDS2202E(...) as scope:
        """

        return self

    def __exit__(self, exc_type, exc_value, traceback):

        self.close()