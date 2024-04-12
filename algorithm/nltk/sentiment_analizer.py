import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Load EmoContext model and tokenizer
model_name = "monologg/emotion-cause"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Define emotion labels
emotion_labels = ['joy', 'anger', 'love', 'sadness', 'fear', 'surprise']

def analyze_comments(comments):
    # Initialize a list to store predicted emotions
    predicted_emotions = []

    # Iterate through each comment
    for comment in comments:
        # Tokenize input text
        inputs = tokenizer(comment, return_tensors="pt", truncation=True, padding=True)

        # Forward pass through the model
        outputs = model(**inputs)
        logits = outputs.logits

        # Get predicted emotion label
        predicted_label = emotion_labels[torch.argmax(logits, dim=1)]

        # Append predicted emotion to the list
        predicted_emotions.append(predicted_label.item())

    # Calculate the counts of each predicted emotion
    emotions_count = {emotion: predicted_emotions.count(emotion) for emotion in emotion_labels}

    # Calculate the total number of comments
    total_comments = len(comments)

    # Convert counts to percentages out of a single whole
    emotions_percentages = {emotion: (count / total_comments) * 100 for emotion, count in emotions_count.items()}

    # Normalize percentages to ensure they sum up to 100
    sum_percentages = sum(emotions_percentages.values())
    emotions_percentages = {emotion: (percentage / sum_percentages) * 100 for emotion, percentage in emotions_percentages.items()}

    return emotions_percentages

# Example usage:
comments = ["I love this!", "I hate it.", "It's okay.", "This is amazing!", "I'm so sad.", "It makes me angry.", "Wow, that's surprising!"]
emotions_result = analyze_comments(comments)
print(emotions_result)
