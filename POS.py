import nltk
from nltk import pos_tag, word_tokenize
from nltk.corpus import stopwords
from nltk.chunk import ne_chunk

# Download necessary NLTK resources (if not already downloaded)
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('maxent_ne_chunker')
nltk.download('words')

# Function to process a sentence and extract relevant phrases
def extract_phrases(sentence):
    # Tokenize the sentence into words
    words = word_tokenize(sentence)

    # Perform part-of-speech tagging
    tagged_words = pos_tag(words)

    # Extract relevant phrases (nouns/adjectives/CDs)
    n1 = ""   # Temporary string to hold concatenated nouns/adjectives/CDs
    prev = "" # Holds the part-of-speech (POS) of the previous word
    vec = []  # List to store final extracted phrases

    # Iterate through tagged words to extract relevant phrases
    for word, pos in tagged_words:
        if prev == "":
            if pos.startswith('N') or pos.startswith('J') or pos == 'CD':
                prev = pos
                n1 += (word + " ")
        elif prev.startswith('N') or prev.startswith('J') or prev == 'CD':
            if pos.startswith('N') or pos.startswith('J') or pos == 'CD':
                n1 += (word + " ")
            else:
                vec.append(n1.strip())
                prev = ""
                n1 = ""

    if n1:
        vec.append(n1.strip())

    return vec

# File paths
input_file_path = 'sentences_benchie.txt'
output_file_path = 'output_pos_ideal_benchie.txt'

# Read sentences from input file and process each line
with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
    for line in input_file:
        line = line.strip()
        if line:
            phrases = extract_phrases(line)
            # Write phrases without quotes and in desired format
            output_file.write(f"[{', '.join(phrases)}]\n ")
