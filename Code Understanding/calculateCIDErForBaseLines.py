from pymongo import MongoClient

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
import numpy as np


def ngram_counts(text, n):
    """
    Generate n-gram counts for a given text.
    """
    tokens = text.split()
    ngrams = zip(*[tokens[i:] for i in range(n)])
    return Counter([" ".join(ngram) for ngram in ngrams])

def compute_tf_idf(corpus, n):
    """
    Compute TF-IDF weights for n-grams in the corpus.
    """
    vectorizer = TfidfVectorizer(ngram_range=(n, n))
    tfidf_matrix = vectorizer.fit_transform(corpus)
    return tfidf_matrix, vectorizer.get_feature_names_out()

def cider(candidate, references, n=4):
    """
    Compute the CIDER score for a candidate summary against multiple references.

    Args:
        candidate (str): The generated summary.
        references (list of str): The reference summaries.
        n (int): Maximum n-gram length to consider (default is 4).

    Returns:
        float: The CIDER score.
    """
    cider_scores = []

    # Combine candidate and references into a corpus
    corpus = [candidate] + references

    for i in range(1, n + 1):  # Loop over n-gram lengths
        # Compute TF-IDF for n-grams
        tfidf_matrix, _ = compute_tf_idf(corpus, i)
        
        # Separate candidate vector from reference vectors
        candidate_vec = tfidf_matrix[0]
        reference_vecs = tfidf_matrix[1:]
        
        # Compute cosine similarity between candidate and each reference
        similarities = cosine_similarity(candidate_vec, reference_vecs)
        
        # Take the average similarity for the current n-gram length
        cider_scores.append(np.mean(similarities))
    
    # Final CIDER score is the average across all n-gram lengths
    return np.mean(cider_scores)

def cider_score(referenceList,predictionList):
    totalScore=0
    for ref,pred in zip(referenceList,predictionList):
        reference = []
        candiate=pred
        reference.append(ref)
        try:
            scoreC=cider(candiate, reference)
            totalScore+=scoreC
        except Exception as e:
            print('error in calculation: ',e)
            


    return round(totalScore/len(referenceList),4)

client = MongoClient('mongodb://localhost:27017/')
db = client.code_understanding             
docStringMethods = db.docStringMethods.find()


codeT5p_CIDEr = 0
codeBERT_CIDEr = 0
count = 0

codeT5p_pred = []
codeBert_pred = []
gtList = []

for item in docStringMethods:
    codeT5p=item.get('codeT5p_Summary')
    codeBERT=item.get('codeBert_Summary')
    gt = item.get('methodLevelComment')
    
    codeT5p_pred.append(codeT5p)
    codeBert_pred.append(codeBERT)
    gtList.append(gt)

#print(len(gtList),len(codeT5p_pred),len(codeBert_pred))

print("AVG CIDEr CodeT5p: ",cider_score(gtList,codeT5p_pred))
#print("AVG CIDEr CodeBERT: ",cider_score(gtList, codeBert_pred))


