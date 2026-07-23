from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification

import torch


class SentimentLoader:

    MODEL_NAME = "aliffiaaliffia/indobert_sentiment_news"

    def __init__(self):

        self.device = torch.device(

            "cuda"

            if torch.cuda.is_available()

            else "cpu"

        )

        print("=" * 60)
        print("Loading Sentiment Model...")
        print("=" * 60)

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.MODEL_NAME
        )

        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.MODEL_NAME
        )

        self.model.to(self.device)

        self.model.eval()

        print("Model loaded successfully.")
        print(f"Device : {self.device}")

    # =====================================================
    # Getter
    # =====================================================

    def get_model(self):

        return self.model

    def get_tokenizer(self):

        return self.tokenizer

    def get_device(self):

        return self.device