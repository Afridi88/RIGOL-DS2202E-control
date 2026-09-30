from rigol_ds2202e import RigolDS2202E

scope = RigolDS2202E("192.168.1.100")

print("Connected:")
print(scope.identify())

# Test acquisition
scope.run()
print("Oscilloscope is running.")

scope.stop()
print("Oscilloscope is stopped.")

scope.close()
print("Connection closed.")