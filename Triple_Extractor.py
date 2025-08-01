import os
from collections import defaultdict
import json
import ast  # Use ast.literal_eval for safer string evaluation

# Create /Json folder if it doesn't exist
os.makedirs('Json', exist_ok=True)

# def extract_triples(triple_file, pos_file):
#     triples_map = defaultdict(list)
#     with open(triple_file, 'r') as f_triple, open(pos_file, 'r') as f_pos:
#         triple_lines = f_triple.readlines()
#         pos_lines = f_pos.readlines()
        
#         for triple_line in triple_lines:
#             triple_parts = triple_line.strip().split("||")
#             sentence_number = int(triple_parts[0])
#             triple_data = ast.literal_eval(triple_parts[1])  # Safely evaluate the triple data

#             newtriple = []
            
#             if len(triple_data) >= 3:  # Check if triple_data has at least three elements
#                 if sentence_number <= len(pos_lines):
#                     extractsentence = pos_lines[sentence_number - 1].replace('[', '').replace(']', '').replace('\n','')
#                     elements = extractsentence.split(", ")
#                     sentence = [element.strip() for element in elements]

#                     # Check if the entire subject and object are present in the sentence
#                     if any(word in triple_data[0] for word in sentence) and any(word in triple_data[2] for word in sentence):
#                         newtriple.append(triple_data)
            
#             if newtriple:
#                 triples_map[sentence_number].append(triple_data)
            
#     return triples_map

import jellyfish  # for Jaro-Winkler similarity

def has_direct_or_similar_match(text, pos_nouns, threshold=0.50):
    for noun in pos_nouns:
        if noun in text:
            return True  # direct match
        for word in text.split():
            if jellyfish.jaro_winkler_similarity(noun.lower(), word.lower()) >= threshold:
                return True  # similarity match
    return False

def extract_triples(triple_file, pos_file):
    triples_map = defaultdict(list)
    with open(triple_file, 'r') as f_triple, open(pos_file, 'r') as f_pos:
        triple_lines = f_triple.readlines()
        pos_lines = f_pos.readlines()

        for triple_line in triple_lines:
            triple_parts = triple_line.strip().split("||")
            sentence_number = int(triple_parts[0])
            triple_data = ast.literal_eval(triple_parts[1])
            newtriple = []

            if len(triple_data) >= 3:
                if sentence_number <= len(pos_lines):
                    extractsentence = pos_lines[sentence_number - 1].replace('[', '').replace(']', '').replace('\n','')
                    pos_nouns = [element.strip() for element in extractsentence.split(", ")]

                    subject = triple_data[0]
                    obj = triple_data[2]

                    subject_valid = has_direct_or_similar_match(subject, pos_nouns)
                    object_valid = has_direct_or_similar_match(obj, pos_nouns)

                    if subject_valid and object_valid:
                        newtriple.append(triple_data)

            if newtriple:
                triples_map[sentence_number].append(triple_data)

    return triples_map


# List of tool names and input file names
tools_and_files = [
    ("triple_clauseie", "triple_clauseie.txt"),
    ("triple_minie", "triple_minie.txt"),
    ("stanford_4.5.3_openie", "stanford_4.5.3_openie.txt"),
    ("stanford_4.5.6_openie", "stanford_4.5.6_openie.txt"),
    ("triple_ollie","triple_ollie.txt")
]

# Loop over each tool and input file
for tool, file in tools_and_files:
    triples = extract_triples(file, "output_det_remove.txt")
    
    # Save the output in /Json folder
    output_file = os.path.join('Json', f"{tool}.json")
    try:
        with open(output_file, 'w') as json_file:
            json.dump(triples, json_file)
        print(f"Triples extracted by {tool} saved to {output_file}")
    except IOError as e:
        print(f"Failed to write {output_file}: {e}")
