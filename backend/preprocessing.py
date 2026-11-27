import re
import spacy

nlp = spacy.load("en_core_web_sm")

def mask_expression(text, expression):
    pattern = r"\b" + re.escape(expression) + r"\b"
    return re.sub(pattern, "something", text, flags=re.IGNORECASE)

def identify_speaker(text):
    doc = nlp(text)
    speech_verbs = ["say", "tell", "speak", "reply", "respond"]

    for token in doc:
        if token.lemma_ in speech_verbs and token.pos_ == "VERB":
            for child in token.children:
                if child.dep_ == "nsubj":
                    for chunk in doc.noun_chunks:
                        if chunk.root == child:
                            return chunk.text

                    return child.text

    return None

def extract_speaker_delivery(text):
    delivery_vocabulary = {
        "mockingly": "mocking", "sarcastically": "sarcastic",
        "sincerely": "sincere", "affectionately": "affectionate",
        "condescendingly": "condescending"
    }

    doc=nlp(text)
    speaking_verbs = ["say", "tell", "speak", "reply", "respond"]
    extracted_evidence = []

    speech_tokens = [
        token for token in doc
        if token.lemma_ in speaking_verbs and token.pos_ == "VERB" 
    ]

    if len(speech_tokens) != 1:
        return extracted_evidence

    speech_token = speech_tokens[0]

    if any(child.dep_ == "neg" for child in speech_token.children):
        return extracted_evidence

    for child in speech_token.children:
        if child.dep_ == "advmod":
            if child.text.lower() in delivery_vocabulary:
                extracted_evidence.append(delivery_vocabulary[child.text.lower()])

    return extracted_evidence