# Source https://github.com/julyanserra/Basic-LZ77-in-Python/blob/master/encoder.py

import struct
import math
from typing import List


def LZ77_search(search, look_ahead):
    ls = len(search)
    llh = len(look_ahead)
    if (ls == 0):
        return (0, 0, look_ahead[0])

    if (llh) == 0:
        return (-1, -1, "")

    best_length = 0
    best_offset = 0
    buf = search + look_ahead

    search_pointer = ls
    for i in range(0, ls):
        length = 0
        while buf[i + length] == buf[search_pointer + length]:
            length = length + 1
            if search_pointer + length == len(buf):
                length = length - 1
                break
            if i + length >= search_pointer:
                break
        if length > best_length:
            best_offset = i
            best_length = length

    return (best_offset, best_length, buf[search_pointer + best_length])


def compress_2(input):
    x = 16
    MAXSEARCH = 1000
    MAXLH = int(math.pow(2, (x - (math.log(MAXSEARCH, 2)))))

    compressed = b""
    score = 0
    searchiterator = 0
    lhiterator = 0

    while lhiterator < len(input):
        search = input[searchiterator:lhiterator]
        look_ahead = input[lhiterator:lhiterator + MAXLH]
        (offset, length, char) = LZ77_search(search, look_ahead)
        if length < 3:
            offset = 0
            length = 0
            char = look_ahead[0]
        if offset or length:
            score += 3
        else:
            score += 1
        # print (offset, length, char)

        shifted_offset = offset << 6
        offset_and_length = shifted_offset + length
        # ol_bytes = struct.pack(">Hc",offset_and_length,char)
        if length:
            ol_bytes = struct.pack(">HB", offset_and_length, char)
        else:
            ol_bytes = struct.pack("B", char)
        compressed += ol_bytes
        # compressed.append(char)

        lhiterator = lhiterator + length + 1
        searchiterator = lhiterator - MAXSEARCH

        if searchiterator < 0:
            searchiterator = 0

    return compressed


# c, score = compress_2(text_str.encode('cp1255'))


# https://rosettacode.org/wiki/LZW_compression#Python
def compress_lzw(uncompressed):
    """Compress a string to a list of output symbols."""

    # Build the dictionary.
    dict_size = 256
    dictionary = dict((chr(i), i) for i in range(dict_size))
    # in Python 3: dictionary = {chr(i): i for i in range(dict_size)}

    w = ""
    result = []
    for c in uncompressed:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            # Add wc to the dictionary.
            dictionary[wc] = dict_size
            dict_size += 1
            w = c

    # Output the code for w.
    if w:
        result.append(dictionary[w])
    return result


def find_max_match(text: List[bytes], i: int, d: dict):
    max_len = 0
    dif = -1
    w = text[i]
    for j in d.get(w, []):
        if j < i - 255:
            continue
        if j >= i:
            break
        l = 0
        while i + l < len(text) and text[j + l] == text[i + l]:
            l += 1
        if l > max_len:
            max_len, dif = l, i - j
    return max_len, dif


def compress_words(text: bytes):
    text = text.split()
    d = {}
    for i, w in enumerate(text):
        d[w] = d.get(w, []) + [i]

    compressed = []
    i = 0
    while i < len(text):
        w = text[i]
        max_len, dif = find_max_match(text, i, d)
        if max_len:
            compressed.append((True, struct.pack("BB", max_len, dif)))
            i += max_len
        else:
            compressed.append((False, w))
            i += 1

    compressed_bytes = compressed[0][1]
    # Insert spaces only between words, refs dont need them
    for i in range(1, len(compressed)):
        if compressed[i][0] or compressed[i - 1][0]:
            compressed_bytes += compressed[i][1]
        else:
            compressed_bytes += b" " + compressed[i][1]
    return compressed_bytes


def main():
    print(compress_words(b"my test is my second test is my"))


if __name__ == "__main__":
    main()
