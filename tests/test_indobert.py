import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# ======================================
# Nama model di Hugging Face
# ======================================

MODEL_NAME = "aliffiaaliffia/indobert-sentiment"

print("Mengunduh tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

print("Mengunduh model...")

model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

model.eval()

print("Model berhasil dimuat!\n")


# ======================================
# Contoh berita
# ======================================

texts = [
    "IHSG ditutup menguat setelah saham perbankan mengalami kenaikan.",
    "Gempa bumi mengguncang wilayah Sumatera Barat pagi ini.",
    "Timnas Indonesia berhasil meraih kemenangan telak atas lawannya.",
    "Harga kebutuhan pokok naik tajam menjelang hari raya.",
    "Pemerintah meluncurkan program baru untuk meningkatkan kualitas pendidikan."
]


# ======================================
# Prediksi
# ======================================

labels = {
    0: "Negative",
    1: "Neutral",
    2: "Positive"
}


with torch.no_grad():

    for text in texts:

        inputs = tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True
        )

        outputs = model(**inputs)

        probabilities = torch.softmax(outputs.logits, dim=1)

        prediction = torch.argmax(probabilities).item()

        confidence = probabilities[0][prediction].item()

        print("=" * 70)
        print("Berita : ", text)
        print("Sentimen :", labels[prediction])
        print("Confidence :", f"{confidence:.4f}")