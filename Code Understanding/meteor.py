from nltk.translate import meteor
from nltk import word_tokenize


def meteor_score(reference, predicted):
    return round(meteor([word_tokenize(reference)],word_tokenize(predicted)), 4)


reference_text = 'iterate over the list'
predicted_text = 'iterate across the list'


print(meteor_score(reference_text,predicted_text))