from backend.dictionary import recognize_expression, get_expression
from backend.preprocessing import mask_expression, identify_speaker, extract_speaker_delivery, extract_timing_context, extract_social_context, extract_user_comprehension
from backend.nli import classify_evidence

def reconcile_evidence(generic_label, specific_label):
    if specific_label is None:
        return "unresolved_att"

    if generic_label != specific_label:
        return "classification_conflict"

    if generic_label == "entailment":
        return "supported"

    if generic_label == "contradiction":
        return "contradicted"

    return "insufficient_evidence"

def evaluate_delivery(masked_text, speaker, characteristic):
    generic_hypothesis = f"The speaker used a {characteristic} tone."

    generic_scores = classify_evidence(masked_text, generic_hypothesis)

    generic_label = max(generic_scores, key=generic_scores.get)

    specific_hypothesis = None
    specific_scores = None
    specific_label = None

    if speaker is not None:
        subject = speaker[0].upper() + speaker[1:]

        specific_hypothesis = f"{subject} used a {characteristic} tone."

        specific_scores = classify_evidence(masked_text, specific_hypothesis)

        specific_label = max(specific_scores, key=specific_scores.get)

    speaker_delivery_status = reconcile_evidence(generic_label, specific_label)

    return {
        "characteristic": characteristic, "generic hypothesis": generic_hypothesis,
        "generic scores": generic_scores, "generic label": generic_label,
        "specific hypothesis": specific_hypothesis, "specific scores": specific_scores,
        "specific label": specific_label, "delivery status": speaker_delivery_status
    }

    
def analyze_text(text):
    expression = recognize_expression(text)

    if expression is None:
        return {
            "recognized": False, "text": text
        }

    linguistic_details = get_expression(expression)

    masked_text = mask_expression(text, expression)

    speaker = identify_speaker(masked_text)

    extracted_delivery = extract_speaker_delivery(masked_text)

    extracted_timing = extract_timing_context(text)

    extracted_social = extract_social_context(speaker)

    extracted_comprehension = extract_user_comprehension(text)

    delivery_characteristics = [
        "mocking", "sarcastic", "sincere",
        "affectionate", "condescending"
    ]

    delivery_evidence = {}

    for characteristic in delivery_characteristics:
        if characteristic in extracted_delivery:
            delivery_evidence[characteristic] = {
                "characteristic": characteristic,
                "delivery status": "supported",
                "evidence source": "explicit"
            }

        elif extracted_delivery:
            delivery_evidence[characteristic] = {
                "charcateristic": characteristic,
                "delivery status": "insufficient_evidence",
                "evidence source": None
            }

        else: 
            delivery_evidence[characteristic] = evaluate_delivery(
                masked_text, speaker, characteristic
            )

    return {
        "recognized": True, "text": text, "expression": expression,
        "details": linguistic_details, "masked_text": masked_text,
        "speaker": speaker, "delivery evidence": delivery_evidence,
        "explicit delivery": extracted_delivery, 
        "timing context": extracted_timing, "relational context": extracted_social,
        "user comprehension": extracted_comprehension
    }
