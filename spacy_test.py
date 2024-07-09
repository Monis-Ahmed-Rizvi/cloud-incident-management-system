import spacy

# Load the small English model
nlp = spacy.load('en_core_web_sm')

# Process a text
doc = nlp("This is a test sentence for SpaCy.")

# Print the processed text
for token in doc:
    print(token.text, token.pos_, token.dep_)




