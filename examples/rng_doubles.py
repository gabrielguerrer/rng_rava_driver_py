'''
This example showcases the RNG generation of double precision floating-point
numbers.

This example code is in the public domain.
Author: Gabriel Guerrer
'''

import struct
import numpy as np
import rng_rava as rava

# Find RAVA device and connect
rng = rava.RAVA_RNG()
dev_sns = rava.find_rava_sns()
if len(dev_sns):
    rng.connect(serial_number=dev_sns[0])
else:
    rava.lg.error('No device found')
    exit()

def get_rng_doubles(n_doubles):
    if n_doubles >= (2**32) // 8:
        print('RNG Doubles: Maximum n_doubles is {}'.format((2**32) // 8))
        return None

    # 64 bits floating point number
    bytes_res = rng.get_rng_bytes(n_bytes=n_doubles*8, timeout=None)
    if bytes_res is None:
        return
    rnd_bytes_a, rnd_bytes_b = bytes_res

    # XOR them
    int_a = int.from_bytes(rnd_bytes_a, 'little')
    int_b = int.from_bytes(rnd_bytes_b, 'little')
    rnd_bytes = (int_a ^ int_b).to_bytes(len(rnd_bytes_a), 'little')
    # Convert bytes to ints
    rnd_lists = struct.unpack('<{}Q'.format(n_doubles), rnd_bytes)
    rnd_ints = np.array(rnd_lists, dtype=np.uint64)

    # IEEE754 bit pattern for single precision floating point value in the
    # range of 1.0 - 2.0. Uses the first 52 bits and fixes the float
    # exponent to 1023
    rnd_ints_tmp = (rnd_ints & 0xFFFFFFFFFFFFF) | 0x3FF0000000000000
    rnd_bytes_filtered = rnd_ints_tmp.tobytes()
    rnd_lists_filtered = struct.unpack('<{}d'.format(n_doubles), rnd_bytes_filtered)
    rnd_doubles = np.array(rnd_lists_filtered, dtype=np.float64)
    return rnd_doubles - 1

# Get and print 100 doubles
doubles = get_rng_doubles(100)
doubles_str = '\n'.join(['{:.16f}'.format(d) for d in doubles])
print(doubles_str)

# Close device
rng.close()