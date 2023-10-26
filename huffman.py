import heapq
import os

class HuffmanNode:
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right
    
    def __lt__(self, other):
        return self.freq < other.freq

class HuffmanEncode:
    def _build_freq_table(self, filepath):
        freq_table = {}
        with open(filepath, 'r') as f:
            for line in f:
                for char in line:
                    if char in freq_table:
                        freq_table[char] += 1
                    else:
                        freq_table[char] = 1
        return freq_table

    def _build_huffman_tree(self, freq_table):
        heap = []
        for char, freq in freq_table.items():
            node = HuffmanNode(char, freq)
            heapq.heappush(heap, node)
        
        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            freq = left.freq + right.freq
            node = HuffmanNode(None, freq, left, right)
            heapq.heappush(heap, node)
        
        return heap[0]

    def _build_encoding_table(self, node, code='', table={}):
        if node.char:
            table[node.char] = code
        else:
            self._build_encoding_table(node.left, code+'0', table)
            self._build_encoding_table(node.right, code+'1', table)
        return table

    def __init__(self, input_filepath, output_filepath):
        freq_table = self._build_freq_table(input_filepath)
        huffman_tree = self._build_huffman_tree(freq_table)
        encoding_table = self._build_encoding_table(huffman_tree)
        
        with open(input_filepath, 'r') as f, open(output_filepath, 'wb') as out:
            out.write(bytes(str(freq_table)+'\n', 'utf-8'))
            code = ''
            for line in f:
                for char in line:
                    code += encoding_table[char]
                    while len(code) >= 8:
                        byte = int(code[:8], 2)
                        out.write(bytes([byte]))
                        code = code[8:]
            
            # write any remaining bits
            if code:
                byte = int(code.ljust(8, '0'), 2)
                out.write(bytes([byte]))

class HuffmanDecode:
    def _read_freq_table(self, input_filepath):
        freq_table = {}
        with open(input_filepath, 'rb') as f:
            header = ''
            byte = f.read(1)
            while byte != b'\n':
                header += byte.decode('utf-8')
                byte = f.read(1)
            freq_table = eval(header)
        return freq_table

    def _build_huffman_tree_from_encoding_table(self, encoding_table):
        root = HuffmanNode()
        for char, code in encoding_table.items():
            node = root
            for bit in code:
                if bit == '0':
                    if not node.left:
                        node.left = HuffmanNode()
                    node = node.left
                else:
                    if not node.right:
                        node.right = HuffmanNode()
                    node = node.right
            node.char = char
        return root
    
    def _build_huffman_tree(self, freq_table):
        heap = []
        for char, freq in freq_table.items():
            node = HuffmanNode(char, freq)
            heapq.heappush(heap, node)
        
        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            freq = left.freq + right.freq
            node = HuffmanNode(None, freq, left, right)
            heapq.heappush(heap, node)
        
        return heap[0]

    def _build_encoding_table(self, node, code='', table={}):
        if node.char:
            table[node.char] = code
        else:
            self._build_encoding_table(node.left, code+'0', table)
            self._build_encoding_table(node.right, code+'1', table)
        return table

    def __init__(self, input_filepath, output_filepath):
        freq_table = self._read_freq_table(input_filepath)
        huffman_tree = self._build_huffman_tree_from_encoding_table(self._build_encoding_table(self._build_huffman_tree(freq_table)))
        
        with open(input_filepath, 'rb') as f, open(output_filepath, 'w') as out:
            # skip header
            while f.read(1) != b'\n':
                pass
            
            node = huffman_tree
            bit = f.read(1)
            while bit:
                bit = int.from_bytes(bit)
                for b in format(bit, '08b'):
                    if b == '0':
                        node = node.left
                    else:
                        node = node.right
                    if node.char:
                        if freq_table[node.char] > 0:
                            out.write(node.char)
                            freq_table[node.char] -= 1
                        node = huffman_tree
                bit = f.read(1)