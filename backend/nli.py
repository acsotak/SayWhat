from sentence_transformers import CrossEncoder
import torch

model = CrossEncoder("cross-encoder/nli-deberta-v3-small")

labels = model.model.config.id2label

def classify_evidence(premise, hypothesis):
    scores = model.predict(
        [(premise, hypothesis)],
        activation_fn=torch.nn.Softmax(dim=1)
    )

    return {
        labels[i]: float(score)
        for i, score in enumerate(scores[0])
    }

