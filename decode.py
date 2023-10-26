from huffman import HuffmanDecode

output_filepath = "output.txt"
input_filepath = "input.txt" + '.compressed'
HuffmanDecode(input_filepath, output_filepath)
print("Decoding Complete!")