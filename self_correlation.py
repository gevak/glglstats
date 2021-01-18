import re


def generate_heatmap(lyrics: str):
    words = []
    data = {}
    while "\n\n" in lyrics:
        lyrics = lyrics.replace("\n\n", "\n")
    lyrics = re.sub("\s+", " ", lyrics)
    lyrics = re.sub("[^a-zA-Z0-9\-א-ת', \\-\n]", '', lyrics).replace('-', ' ')
    for line in lyrics.splitlines():
        wlist = line.split()
        for word in wlist:
            words.append(word.lower().replace(",", ""))

    words_counts = {}
    for word in words:
        words_counts[word] = words_counts.get(word, 0) + 1
    number_of_words = len(words)
    matrix = []
    for x in range(number_of_words):
        row = []
        for y in range(number_of_words):
            if words[x] == words[y]:
                row.append(words_counts[words[x]])
            else:
                row.append(None)
        matrix.append(row)
    data['z'] = matrix
    data['words'] = words
    return (data)
