## v1.0.1

* Changed maximum line length from 80 to 120. This change does not apply to the code's documentation
* Using "not in" and "is not None"
* Correcting firmware version in eeprom_firmware
* Adding callbacks
* Setting logger name to 'rava'
* Changed health startup results format
* Including hardware float generation


## v1.0.2
* Checking for n > 0 in data generation
* Max n of pulse counts, bytes, ints, and floats changed to 2^16 (instead of 2^32)
* Improved the disconnection detection methodology
* Corrected the int_delta in integers generation