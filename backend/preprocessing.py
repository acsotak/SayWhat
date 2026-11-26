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

