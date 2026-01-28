# Specify the binary file path

import binascii


def tokenize(s):
    return [s[i: i + 2] for i in range(len(s) - 2)]


def dict_freq(s):
    ss = set(s)
    def f(ele) :
        return ele[1]
    lis = [(ele, s.count(ele)) for ele in ss]
    lis.sort(key = f,reverse=True)
    return lis


# Specify the binary file path (update this to your local MIDI file)
binary_file_path = 'file2.mid'

try:
    # Open the binary file in binary read mode ('rb')
    with open(binary_file_path, 'rb') as binary_file:
        # Read the binary data
        binary_data = binary_file.read()

        # Convert the binary data to a hexadecimal string
        hex_string = binascii.hexlify(binary_data).decode('utf-8')

        # Now, you can work with the hexadecimal string
        print(hex_string)
        print(tokenize(hex_string))
        print(dict_freq(tokenize(hex_string)))


except FileNotFoundError:
    print(f"The file '{binary_file_path}' does not exist.")
except Exception as e:
    print(f"An error occurred: {e}")
