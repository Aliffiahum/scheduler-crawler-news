from app.preprocessing.stemmer import Stemmer

stemmer = Stemmer()

text = """

pemerintah meningkatkan pembangunan infrastruktur nasional

"""

print(

    stemmer.stem(text)

)