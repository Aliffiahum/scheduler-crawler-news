import torch

from app.sentiment.loader import SentimentLoader


class SentimentPredictor:

    LABELS = {
        0: "negative",
        1: "neutral",
        2: "positive",
    }

    def __init__(self, loader: SentimentLoader):

        self.model = loader.get_model()

        self.tokenizer = loader.get_tokenizer()

        self.device = loader.get_device()

    # =====================================================
    # Predict
    # =====================================================

    def predict(self, text: str) -> dict:

        inputs = self.tokenizer(

            text,

            return_tensors="pt",

            truncation=True,

            padding=True,

            max_length=512,

        )

        inputs = {

            key: value.to(self.device)

            for key, value in inputs.items()

        }

        with torch.no_grad():

            outputs = self.model(**inputs)

            probabilities = torch.softmax(

                outputs.logits,

                dim=1,

            )

            confidence, prediction = torch.max(

                probabilities,

                dim=1,

            )

        return {

            "label": self.LABELS[prediction.item()],

            "confidence": round(

                confidence.item(),

                4,

            ),

        }