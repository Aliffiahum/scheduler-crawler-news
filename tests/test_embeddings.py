# tests/test_embeddings.py

from sentence_transformers import SentenceTransformer

model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

docs = [
    "Timnas Indonesia menang melawan Jepang",
    "IHSG naik 2 persen hari ini",
    "Microsoft melakukan PHK ribuan karyawan",
    "BMKG memprediksi hujan deras di Jakarta",
    "OpenAI merilis model AI terbaru",
]

embeddings = model.encode(docs)

print("Jumlah embedding :", len(embeddings))
print("Dimensi :", embeddings.shape)