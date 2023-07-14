from heapq import *
from collections import defaultdict
import os

class HuffmanNode:
    def __init__(self, char=None, freq=0):
        self.char = char    # character
        self.freq = freq    # frequency of the character
        self.left = None    # left child
        self.right = None   # right child 

    def __lt__(self, other):
        return self.freq < other.freq

def freq_count(text):
    freq_table = defaultdict(int)
    for char in text:
        freq_table[char] += 1
    return freq_table

def build_huffman_tree(freq_table):
    pq = []
    for char, freq in freq_table.items():
        node = HuffmanNode(char, freq)
        heappush(pq, node)
    
    while len(pq) > 1:
        # Get the 2 smallest frequency nodes
        left_node = heappop(pq)
        right_node = heappop(pq)

        # Merge the two nodes
        parent = HuffmanNode(freq=left_node.freq + right_node.freq)
        parent.left = left_node
        parent.right = right_node

        # Push the merged tree into the pq
        heappush(pq, parent)

    return pq[0]    # return root node of the huffman tree

def encode(root):
    encoding_table = {}

    def traverse(node, code=""):
        if node.char:
            encoding_table[node.char] = code    # root has no character 
        else:
            traverse(node.left, code + "0")
            traverse(node.right, code + "1")

    traverse(root)
    return encoding_table 

def compress(text):
    freq_table = freq_count(text)
    huffman_tree = build_huffman_tree(freq_table)
    encoding_table = encode(huffman_tree)

    compressed_bits = ""
    for char in text:
        compressed_bits += encoding_table[char]
    return compressed_bits, encoding_table

# Decompress using the huffman coding
def decompress(compressed_bits, encoding_table):
    decoding_table = {code: char for char, code in encoding_table.items()}

    current_code = ""
    decompressed_text = ""
    for bit in compressed_bits:
        current_code += bit
        # Find a match in the huffman tree
        if current_code in decoding_table:
            char = decoding_table[current_code]
            decompressed_text += char
            current_code = ""

    return decompressed_text

def main():
    start = True 
    while start:
        text = input('Enter a string: ')
        compressed_bits, encoding_table = compress(text)
        print(f'Original bit length(assuming ASCII 7 bits) = {len(text) * 7}')
        print(f'Compressed bit length = {len(compressed_bits)}')
        print(f'Compressed bits = {compressed_bits}')
        c = input('Do you want to decompress the compressed bits? (y/n): ')
        if c == 'y':
            print(f'Decompressed text = {decompress(compressed_bits, encoding_table)}')
        c = input('Continue? (y/n): ')
        if c == 'y':
            os.system('clear')
        else:
            print('Quitting...')
            start = False

if __name__ == '__main__':
    main()   