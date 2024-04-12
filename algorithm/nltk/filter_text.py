import re

from nltk.tokenize import word_tokenize, sent_tokenize


def clean_text_list(list_of_entries) -> list:
    cleaned_entries = []

    for entry in list_of_entries:
        body = entry
        # Combine header and body for processing
        raw_text = f"{''.join(body)}"

        # Step 1: Remove non-ASCII characters and weird symbols
        cleaned_text = re.sub(r'[^\x00-\x7F.,:;"]+', ' ', raw_text)

        # Step 2: Remove anything between [ and ]
        cleaned_text = re.sub(r'\[.*?]', '', cleaned_text)

        # Step 3: Tokenize the text into sentences
        sentences = sent_tokenize(cleaned_text)

        # Step 4: Process each sentence
        processed_sentences = []

        for sentence in sentences:
            # Step 5: Tokenize the sentence into words
            words = word_tokenize(sentence)

            # Step 6: Join the words back into a sentence
            processed_sentence = ' '.join(words)

            # Add the processed sentence to the list
            processed_sentences.append(processed_sentence)

        # Step 7: Join the sentences back into a cleaned text
        cleaned_text = ' '.join(processed_sentences)
        cleaned_entries.append(cleaned_text)

    return cleaned_entries

