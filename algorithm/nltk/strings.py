import nltk
from nltk.tokenize import sent_tokenize

# nltk.download('punkt')


def modify_review(review):
    # Tokenize the review into sentences
    sentences = sent_tokenize(review)

    # Capitalize the first letter of each sentence and join them back
    modified_review = ' '.join(sentence.capitalize() for sentence in sentences)

    return modified_review
