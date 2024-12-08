import struct

"""
Binary File Function Types:
rb - read
wb - writing
ab - appending
"""
# Create binary file
with open('binTest.bin', 'wb') as f:
    # NOTE: .idx is not a real file type
    #       f is the file name
    pass

# 'wb' - writing in binary file
with open('example.bin', 'wb') as f:
    # When created we can't really see what the file contains
    # Unless we have an extention/application to decode it

    num = 34
    # Convert integer to 8 byte binary with big-endian
    binaryData = num.to_bytes(8, 'big')

    # Write into the file
    f.write(binaryData)

# 'rb' - reading from a binary file
with open('example.bin', 'rb') as f:
    # Read 8 bytes
    binary_data = f.read(8)

    # Convert from 8 bytes big endian binary to interger
    num = int.from_bytes(binary_data, 'big')
    print(num)

