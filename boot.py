# The purpose of the code in this file is to hide the drive popup
# when the keyboard is connedted to USB
#
# IF you whant the drive to popup for maintenance, then unplug The TRRS cable:
# - Left side:  Hold "Q" and plug the USB to make the drive popup
# - Right side: Hold "P" and plug the USB to make the drive popup


import board
import digitalio
import storage

# --- UNIVERSAL UNLOCK ---
# We don't care if we are Left or Right.
# We will check BOTH the "Pinky" pin (GP2/GP28) and the "Inner" pin (GP28/GP2).
# If EITHER of them is pressed, we show the drive.

# Pins to check for the "Unlock" signal
# GP2  = Left Pinky  / Right Inner
# GP28 = Left Inner  / Right Pinky
unlock_pins = [board.GP2, board.GP28]

unlock_detected = False


# We check Row 0 (GP6) for all scenarios
row = digitalio.DigitalInOut(board.GP6)
row.direction = digitalio.Direction.INPUT
row.pull = digitalio.Pull.DOWN

for pin in unlock_pins:
    # Setup the Column
    col = digitalio.DigitalInOut(pin)
    col.direction = digitalio.Direction.OUTPUT
    col.value = True
    
    # Check if the key is pressed
    if row.value == True:
        unlock_detected = True
        
    # Cleanup pin before checking the next one
    col.value = False
    col.deinit()

row.deinit()

# --- DECISION ---
if unlock_detected:
    print("Maintenance Mode: Drive Visible")
else:
    storage.disable_usb_drive()

