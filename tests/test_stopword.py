from app.preprocessing.stopword_remover import StopwordRemover

remover = StopwordRemover()

text = """

ini adalah berita yang sangat penting untuk masyarakat indonesia

"""

print(

    remover.remove(text)

)