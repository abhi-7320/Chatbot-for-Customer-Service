import json
import nltk
from nltk.stem import WordNetLemmatizer
import random
import re

# Ensure NLTK data is downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

class Chatbot:
    def __init__(self, intents_file):
        with open(intents_file, 'r') as f:
            self.intents = json.load(f)['intents']

    def preprocess(self, text):
        # Clean text
        text = text.lower().strip()
        # Remove special characters
        text = re.sub(r'[^\w\s]', '', text)
        tokens = nltk.word_tokenize(text)
        
        # Basic English stop words (common words that shouldn't affect scoring)
        stop_words = {
            'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd",
            'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers',
            'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
            'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been',
            'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if',
            'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
            'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out',
            'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
            'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
            'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should',
            "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't",
            'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't",
            'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't",
            'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"
        }
        
        # Filter stop words and lemmatize
        return [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]

    def get_response(self, user_input):
        processed_input = self.preprocess(user_input)
        
        if not processed_input:
            # Check if it was a very simple greeting that was mostly stop words
            raw_input = user_input.lower().strip()
            if any(greet in raw_input for greet in ['hi', 'hello', 'hey', 'greetings']):
                # Find greeting intent
                for intent in self.intents:
                    if intent['tag'] == 'greeting':
                        return random.choice(intent['responses'])
            return "I'm sorry, I don't understand that. Can you rephrase? Maybe I can help with hours, locations, or delivery times."

        best_match = None
        max_score = 0
        
        for intent in self.intents:
            intent_score = 0
            for pattern in intent['patterns']:
                pattern_tokens = self.preprocess(pattern)
                # Calculate overlap score
                common_tokens = set(processed_input) & set(pattern_tokens)
                score = len(common_tokens)
                
                # Bonus for longer matches
                if score > 0:
                    score += (score / len(pattern_tokens))
                
                if score > intent_score:
                    intent_score = score
            
            if intent_score > max_score:
                max_score = intent_score
                best_match = intent
        
        # Fallback if no match is found or score is too low
        if max_score < 0.5:
            return "I'm sorry, I don't understand that. Can you rephrase? Maybe I can help with hours, returns, or order status."
        
        return random.choice(best_match['responses'])

if __name__ == "__main__":
    bot = Chatbot('intents.json')
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
        print(f"Bot: {bot.get_response(user_input)}")
