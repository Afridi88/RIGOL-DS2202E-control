from rigol_ds2202e import RigolDS2202E
import time


# ==========================================================
# SETTINGS
# ==========================================================

RIGOL_IP = "10.5.1.134"


# ==========================================================
# CONNECT
# ==========================================================

scope = RigolDS2202E(RIGOL_IP)

print("Connected to:")
print(scope.identify())


# ==========================================================
# BASIC TEST
# ==========================================================

scope.run()

print("Oscilloscope running.")

time.sleep(2)

scope.stop()

print("Oscilloscope stopped.")


# ==========================================================
# CHANNEL CONFIGURATION
# ==========================================================

scope.channel_on(1)

scope.set_channel_scale(
    channel=1,
    volts_per_div=1
)

scope.set_channel_offset(
    channel=1,
    offset=0
)


# ==========================================================
# TIMEBASE
# ==========================================================

scope.set_timebase(
    seconds_per_div=1e-3
)


# ==========================================================
# TRIGGER
# ==========================================================

scope.set_trigger_source(
    "CHANnel1"
)

scope.set_trigger_slope(
    "POSitive"
)

scope.set_trigger_level(
    0
)


# ==========================================================
# ACQUIRE
# ==========================================================

scope.single()

time.sleep(1)


# ==========================================================
# MEASURE
# ==========================================================

try:

    print("\nMeasurements")
    print("-----------------------")

    print(
        "Vpp:",
        scope.measure_vpp(1)
    )

    print(
        "Frequency:",
        scope.measure_frequency(1)
    )

    print(
        "Period:",
        scope.measure_period(1)
    )

    print(
        "Vrms:",
        scope.measure_vrms(1)
    )

except Exception as error:

    print("\nMeasurement error:")
    print(error)


# ==========================================================
# DISCONNECT
# ==========================================================

scope.close()

print("\nConnection closed.")