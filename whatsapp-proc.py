import re
import sys
from collections import defaultdict, Counter
import os
from googletrans import Translator

def extract_messages_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    pattern = r"\d{1,2}/\d{1,2}/\d{2}, \d{1,2}:\d{2}\s?[AP]M - (.*?): (.*)"
    return re.findall(pattern, text)

def select_user_name(names):
    unique_names = sorted(set(names))
    print("\nWho are you? Choose your name by number:\n")
    for i, name in enumerate(unique_names):
        print(f"{i + 1}. {name}")
    
    while True:
        try:
            choice = int(input("\nEnter the number corresponding to your name: "))
            if 1 <= choice <= len(unique_names):
                return unique_names[choice - 1]
            else:
                print("Please enter a valid number from the list.")
        except ValueError:
            print("Please enter a numeric value.")

def count_word_frequencies(messages):
    word_freq = defaultdict(int)

    for name, message in messages:
        words = re.findall(r"\b\w+(?:'\w+)?\b", message.lower())
        for word in words:
            word_freq[word] += 1

    return dict(word_freq)


def count_expression_frequencies(messages, min_length=5):
    expression_freq = defaultdict(int)

    for name, message in messages:
        # Remove URLs from the message
        message = re.sub(r"(https?://\S+|www\.\S+)", "", message)
        # Extract words from the cleaned message
        words = re.findall(r"\b\w+(?:'\w+)?\b", message.lower())
        for i in range(len(words) - min_length + 1):
            for j in range(i + min_length, len(words) + 1):
                expression = " ".join(words[i:j])
                expression_freq[expression] += 1

    return dict(expression_freq)

if __name__ == "__main__":
    if len(sys.argv) < 2 or (len(sys.argv) == 2 and sys.argv[1] not in ['-f']):
        if len(sys.argv) != 2:
            print("Usage: python extract_user_wordfreq.py <path_to_text_file> or -f <path_to_folder>")
            sys.exit(1)
        file_path = sys.argv[1]
        if not os.path.isfile(file_path):
            print(f"Error: {file_path} is not a valid file.")
            sys.exit(1)
        files = [file_path]
    elif sys.argv[1] == '-f':
        if len(sys.argv) != 3:
            print("Usage: python extract_user_wordfreq.py -f <path_to_folder>")
            sys.exit(1)
        folder_path = sys.argv[2]
        if not os.path.isdir(folder_path):
            print(f"Error: {folder_path} is not a valid folder.")
            sys.exit(1)
        files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.txt')]
        if not files:
            print(f"No text files found in folder: {folder_path}")
            sys.exit(1)
    else:
        print("Usage: python extract_user_wordfreq.py <path_to_text_file> or -f <path_to_folder>")
        sys.exit(1)

    all_messages = []
    all_names = set()

    for file_path in files:
        messages = extract_messages_from_file(file_path)
        all_messages.extend(messages)
        all_names.update(name for name, _ in messages)

    all_names = sorted(all_names)
    selected_name = select_user_name(all_names)

    # Filter messages to only include those from the selected user
    selected_messages = [(name, message) for name, message in all_messages if name == selected_name]

    # Count expression frequencies for the selected user
    translator = Translator()
    expression_frequencies = count_expression_frequencies(selected_messages)

    print(f"\nExpression frequencies for {selected_name}:\n")
    for expression, count in sorted(expression_frequencies.items(), key=lambda x: -x[1])[:10]:
        # Translate the expression to Hebrew
        translated_expression = translator.translate(expression, src='en', dest='he').text
        print(f"{expression} : {translated_expression[::-1]} : {count}")

    # Count word frequencies for the selected user
    frequencies = count_word_frequencies(selected_messages)

    print(f"\nWord frequencies for {selected_name}:\n")
    for word, count in sorted(frequencies.items(), key=lambda x: -x[1])[:10]:
        translated_expression = translator.translate(word, src='en', dest='he').text
        print(f"{word} : {translated_expression[::-1]} : {count}")
