# Huffman File Compression in Python

This is a python project that can compress files using Huffman Algorithm

## Usage

To use this project, follow these steps:

1. Copy your file in the project folder:

2. Change the filename in `encode.py`:
```
input_filepath = "yourfilename.example"
```

3. Run the `encode.py` file this will create the `.compressed` (compressed version of your file) file you desire

4. to decode the `.compressed` file change the compressed filename and output filename in `decode.py`:
```
output_filepath = "output.example"
input_filepath = "compressedfile.example" + '.compressed'
```

5. Run the `decode.py` file this will decompress the `.compressed` file and give you the original file that is usable
