from huffman import HuffmanEncode

input_filepath = "input.txt"
output_filepath = input_filepath + '.compressed'
HuffmanEncode(input_filepath, output_filepath)
print("Encoding Complete!")