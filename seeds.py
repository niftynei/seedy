from hashlib import sha256
import random

# You can fetch the wordlist used here by calling: `wget get https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/english.txt`
# `python -i seeds.py`
# >>> wordlist = [... list of words]
# >>> find_last(wordlist, word)
# 'profit'
# note that calling this multiple times will result in different last words
# as each 'last word' contains 3-bits of entropy (that we randomly generate here)

def arr_to_int(arr):
    total = 0
    for i, val in enumerate(arr[::-1]):
        total += 2 ** i * val
    return total

wordlist = ['']

with open ('english.txt') as f:
    words = f.read().splitlines()

def find_last(wordlist, words):
    nums = [words.index(w) for w in wordlist]

    bb = []
    for num in nums:
        b = list(map(int, '{:0b}'.format(num)))
        bb.append((11 -len(b)) * [0])
        bb.append(b)

    flat = [ item for sublist in bb for item in sublist ]
    assert len(flat) == 253

    # randomly append 3 extra bits
    x = random.randrange(1, 9)
    flat.append(1 if x & 1 else 0)
    flat.append(1 if x & 2 else 0)
    flat.append(1 if x & 4 else 0)

    assert len(flat) == 256

    g = []
    for x in range(len(flat) // 8):
        bits = flat[x*8:(x+1)*8]
        g.append(int(''.join([str(x) for x in bits]), 2))

    byte = bytearray(g)
    assert len(byte) == 32
    chksum = int.from_bytes(sha256(byte).digest()[:1], 'little')
    cc = bin(chksum)[2:]
    totes = flat + [int(c) for c in list(cc)]

    last_word_idx = arr_to_int(totes[-11:])
    return words[last_word_idx]
