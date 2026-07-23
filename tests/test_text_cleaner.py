from app.preprocessing.text_cleaner import TextCleaner


cleaner = TextCleaner()


text = """

<h1>Halo!!!</h1>

Kunjungi https://google.com

Indonesia Hebat!!!!

"""

print(cleaner.clean(text))