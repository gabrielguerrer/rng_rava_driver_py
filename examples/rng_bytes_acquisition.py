'''
This example showcases the generation of a binary file containing random bytes.

This example code is in the public domain.
Author: Gabriel Guerrer
'''

import itertools
import rng_rava as rava

# Variables
FILE_OUTPUT = 'random.bin'
N_BYTES = 1000000 # 1MB
N_CHUNK = 10000

# Find RAVA device and connect
rng = rava.RAVA_RNG()
dev_sns = rava.find_rava_sns()
if len(dev_sns):
    rng.connect(serial_number=dev_sns[0])
else:
    rava.lg.error('No device found')
    exit()

# Calculate n measurements
n_measurements = N_BYTES // N_CHUNK
n_bytes_remmaining = (N_BYTES % N_CHUNK)

# Open file
with open(FILE_OUTPUT, mode='bw') as f:

    # Loop over n measurements
    for i in range(n_measurements):
        print('{:.0f}%'.format(i / n_measurements * 100))

        # Generate bytes
        bytes_a, bytes_b = rng.get_rng_bytes(n_bytes=N_CHUNK // 2,
                                        postproc_id=rava.D_RNG_POSTPROC['NONE'],
                                        list_output=False,
                                        timeout=None)

        # Alternate RNG A and B bytes    
        bytes_ab = bytes(itertools.chain.from_iterable(zip(bytes_a, bytes_b)))
        
        # Write to file
        f.write(bytes_ab)

    # Remaining bytes
    if n_bytes_remmaining:
        
        # Generate bytes
        bytes_a, bytes_b = rng.get_rng_bytes(n_bytes=n_bytes_remmaining // 2,
                                        postproc_id=rava.D_RNG_POSTPROC['NONE'],
                                        list_output=False,
                                        timeout=None)

        # Alternate RNG A and B bytes    
        bytes_ab = bytes(itertools.chain.from_iterable(zip(bytes_a, bytes_b)))
        
        # Write to file
        f.write(bytes_ab)

    # Finished
    print('100%')

# Close device
rng.close()