from app.preprocessing.normalizer import TextNormalizer


normalizer = TextNormalizer()

text = """

gk ngerti bgt yg kmrn gw baca

"""

print(

    normalizer.normalize(text)

)