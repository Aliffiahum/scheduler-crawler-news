from app.preprocessing.tokenizer import Tokenizer

tokenizer = Tokenizer()

text = "berita sangat penting masyarakat indonesia"

print(tokenizer.tokenize(text))