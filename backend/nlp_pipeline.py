from backend.dictionary import recognize_expression, get_expression
from backend.preprocessing import mask_expression, identify_speaker
from backend.nli import classify_evidence

def analyze_text(text):
    expression = recognize_expression(text)

    if expression is None:
        return {
            "recognized": False, "text": text
        }

    linguistic_details = get_expression(expression)

    masked_text = mask_expression(text, expression)

    speaker = identify_speaker(masked_text)

    generic_hypothesis = "The speaker used a mocking tone."

    generic_scores = classify_evidence(masked_text, generic_hypothesis)

    specific_hypothesis = None

    specific_scores = None

    if speaker is not None:
        subject = speaker[0].upper() + speaker[1:]
        specific_hypothesis = f"{subject} used a mocking tone."

        specific_scores = classify_evidence(masked_text, specific_hypothesis)

    return {
        "recognized": True, "text": text, "expression": expression,
        "details": linguistic_details, "masked_text": masked_text,
        "speaker": speaker, "generic hypothesis": generic_hypothesis,
        "generic scores": generic_scores, 
        "specific hypothesis": specific_hypothesis,
        "specific scores": specific_scores
    }
