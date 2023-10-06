# RAVA Python driver

The [RAVA Python driver](https://github.com/gabrielguerrer/rng_rava_driver_py) 
implements the code for communicating with an 
[RAVA device](https://github.com/gabrielguerrer/rng_rava) running the 
[RAVA Firmware](https://github.com/gabrielguerrer/rng_rava_firmware). 
The computer running the driver assumes the role of the leader device, sending 
command requests and reading the data replies.

The RAVA_RNG class enables the request of pulse counts, random bits, random 
bytes, and random numbers (integers and floats). Additionally, it establishes 
the circuit's basic functionality encompassing key modules such as EEPROM, PWM, 
heath tests, peripherals, and interfaces.

The RAVA_RNG_LED class implements the code for controlling the LED and LAMP 
modules within the RAVA circuit. It allows users to adjust the color and the 
intensity of the attached LED. Users can also re-activate the LAMP mode and 
retrieve statistical information on its operation.

The functions that provide access to RAVA's functionality are prefixed with 
"set" and "get". "Set" commands are unidirectional and do not expect a device's
response. Conversely, "get" commands are bidirectional, where the driver 
immediately attempts to retrieve the expected information after signaling the 
device.

The driver operates with a parallel thread running the serial_listen_loop() 
function, which continually monitors RAVA responses. When a command is detected, 
it is further processed by the serial_commands() function. This function is 
responsible for storing the received information into a queue object associated 
to each command ID. The queue data is then retrieved with the data_get() 
function. 

The thread/queue design boosts multitasking capabilities. To illustrate, let us 
consider an opposite design where the serial port is directly read in a blocking 
mode immediately after issuing a command. Then, a user initiates a byte stream 
with one byte transmitted every second. In such a design, the continuous read 
operations would block the driver's side, despite the hardware being idle during 
the byte transmission intervals. However, by implementing the thread/queue 
design, it becomes possible to issue different commands during the byte stream 
and retrieve their results without any conflict at the user's convenience. 

The thread/queue framework also benefits from being easily adaptable to an 
asyncronous version, using asyncio queues and implementing data_get() as an 
async function. The development of a RAVA_RNG_AIO class is a priority on the
development roadmap.

## Installation

The driver code is available as the 
[rng_rava PyPI package](https://pypi.org/project/rng_rava/). To install it, run:

```
pip install rng_rava
```

Requirements:
 * pyserial
 * numpy

## Usage

```
import rng_rava as rava

# Find the serial numbers of the attached RAVA devices
rava_sns = rava.find_devices(usb_vid=0x4884, usb_pid=0x1)

# Create a RNG instance and connect to the first device
rng = rava.RAVA_RNG()
rng.open(serial_number=rava_sns[0])

'''
The default PWM and RNG configuration parameters are stored in the EEPROM
memory and can be accessed with r.get_eeprom_pwm() and r.get_eeprom_rng().
If desired, users can modify the default values using the respective set_
functions. Additionally, it is possible to make non-permanent configuration
changes using the following commands.
'''

# Configure PWM
rng.set_pwm_setup(freq_id=rava.D_PWM_FREQ['50_KHZ'], duty=20)

# Configure RNG
rng.set_rng_setup(sampling_interval_us=10)

'''
Next, the generation of various random data types is demonstrated.
'''

# Measure 100 pulse counts
pc_a, pc_b = rng.get_rng_pulse_counts(n_counts=100)

# Generate a random bit XORing both channels
bit = rng.get_rng_bits(bit_type_id=rava.D_RNG_BIT_SRC['AB_XOR'])

# Generate 100 random bytes en each channel without post-processing
# Output as numpy array
bytes_a, bytes_b = rng.get_rng_bytes(n_bytes=100,  
                    postproc_id=rava.D_RNG_POSTPROC['NONE'],  
                    out_type=rava.D_RNG_BYTE_OUT['NUMPY_ARRAY'])

# Generate 100 8-bit integers between 0 and 99
ints8 = rng.get_rng_int8s(n_ints=100, int_max=100)

# Generate 100 16-bit integers between 0 and 999
ints16 = rng.get_rng_int8s(n_ints=100, int_max=999)

# Generate 100 32-bit floats ranging between 0 and 1
floats = rng.get_rng_floats(n_floats=100)

# Generate 100 64-bit doubles ranging between 0 and 1
doubles = rng.get_rng_doubles(n_doubles=100)
```

## Associated projects

- [RAVA Device](https://github.com/gabrielguerrer/rng_rava)
- [RAVA Firmware](https://github.com/gabrielguerrer/rng_rava_firmware)
- [RAVA Python Diagnostics Tool](https://github.com/gabrielguerrer/rng_rava_diagnostics_py)

## Contact

gabrielguerrer [at] gmail [dot] com
