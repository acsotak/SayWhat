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
    extracted_delivery_evidence = []

    speech_tokens = [
        token for token in doc
        if token.lemma_ in speaking_verbs and token.pos_ == "VERB" 
    ]

    if len(speech_tokens) != 1:
        return extracted_delivery_evidence

    speech_token = speech_tokens[0]

    if any(child.dep_ == "neg" for child in speech_token.children):
        return extracted_delivery_evidence

    for child in speech_token.children:
        if child.dep_ == "advmod":
            if child.text.lower() in delivery_vocabulary:
                extracted_delivery_evidence.append(delivery_vocabulary[child.text.lower()])

    return extracted_delivery_evidence

def extract_timing_context(text):
    doc = nlp(text)
    timing_context_markers = ["when", "after", "before", "because", "while"]
    extracted_timing_evidence = []

    for token in doc:
        if token.dep_ == "advcl":
            for child in token.children:
                if child.lower_ in timing_context_markers:
                    clause = doc[token.left_edge.i:token.right_edge.i + 1]
                    extracted_timing_evidence.append(clause.text)
                    break

    return extracted_timing_evidence

def extract_social_context(speaker):
    if speaker is None:
        return None

    relationship_vocabulary = [
        "frined", "coworker", "mother", "father", "sister", "brother",
        "partner", "wife", "husband", "neighbor", "cousin", "boss"
    ]

    speaker_words = speaker.lower().split()

    for relationship in relationship_vocabulary:
        if relationship in speaker_words:
            return relationship

def extract_user_comprehension(text):
    normalized_text = text.lower()
    extracted_comprehension_evidence = []

    common_comprehension_patterns = {
        "meaning": ["what does", "what does it mean"],
        "pragmatic": ["what did she mean", "was that rude"],
        "sociocultural": ["why do people from", "cultural meaning"],
        "figurative": ["literally", "literal meaning"]
    }

    for category, patterns in common_comprehension_patterns.items():
        for pattern in patterns:
            if pattern in normalized_text:
                extracted_comprehension_evidence.append(category)
                break

    return extracted_comprehension_evidence