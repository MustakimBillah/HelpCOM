from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
import numpy as np
import csv
from scipy.stats import mannwhitneyu

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
    totalScore=[]
    for ref,pred in zip(referenceList,predictionList):
        reference = []
        candiate=pred
        reference.append(ref)
        try:
            score = cider(candiate, reference)
            totalScore.append(score)
        except Exception as e:
            totalScore.append(0)
            print(e)

    return totalScore
    



print('-----------------------------------------------------------------')
groundTruth_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/gtSummaryIndep.csv'
codeT5_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/codeT5SummaryIndep.csv'

gtIndep=[]
codeT5Indep=[]

with open(groundTruth_filePath, mode="r") as file:
    csv_reader = csv.reader(file)
    # Skip the header row if the CSV has one
    header = next(csv_reader)
    #print("Header:", header)
    
    # Read and print the rows
    for row in csv_reader:
        id = row[0]
        summary = row[1]
        data={
            'id':id,
            'summary':summary
        }
        gtIndep.append(data)

with open(codeT5_filePath, mode="r") as file:
    csv_reader = csv.reader(file)
    # Skip the header row if the CSV has one
    header = next(csv_reader)
    #print("Header:", header)
    
    # Read and print the rows
    for row in csv_reader:
        id = row[0]
        summary = row[1]
        data={
            'id':id,
            'summary':summary
        }
        codeT5Indep.append(data)

referenceList=[]
predictionList=[]


for item in gtIndep:
    target_id = item['id']
    referenceList.append(item['summary'])
    found = False
    for element in codeT5Indep:
        if(target_id==element['id']):
            found=True
            predictionList.append(element['summary'])
            break
    if found == False:
        predictionList.append('')

#print(referenceList)
#print(predictionList)

ciderIndepCodeT5 = cider_score(referenceList, predictionList)

#######CodeBert######################

codeBert_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/codeBertSummaryIndep.csv'
codeBertIndep=[]

with open(codeBert_filePath, mode="r") as file:
    csv_reader = csv.reader(file)
    # Skip the header row if the CSV has one
    header = next(csv_reader)
    #print("Header:", header)
    
    # Read and print the rows
    for row in csv_reader:
        id = row[0]
        summary = row[1]
        data={
            'id':id,
            'summary':summary
        }
        codeBertIndep.append(data)

predictionList = []

for item in gtIndep:
    target_id = item['id']
    #referenceList.append(item['summary'])
    found = False
    for element in codeBertIndep:
        if(target_id==element['id']):
            found=True
            predictionList.append(element['summary'])
            break
    if found == False:
        predictionList.append('')

ciderIndepCodeBert = cider_score(referenceList, predictionList)


#######ASAP_Base######################

asapBase_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/asapSummaryIndep.csv'
asapBaseIndep=[]

with open(asapBase_filePath, mode="r") as file:
    csv_reader = csv.reader(file)
    # Skip the header row if the CSV has one
    header = next(csv_reader)
    #print("Header:", header)
    
    # Read and print the rows
    for row in csv_reader:
        id = row[0]
        summary = row[1]
        data={
            'id':id,
            'summary':summary
        }
        asapBaseIndep.append(data)

predictionList = []

for item in gtIndep:
    target_id = item['id']
    #referenceList.append(item['summary'])
    found = False
    for element in asapBaseIndep:
        if(target_id==element['id']):
            found=True
            predictionList.append(element['summary'])
            break
    if found == False:
        predictionList.append('')

ciderIndepASAP= cider_score(referenceList, predictionList)


###########


groundTruth_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/gtSummarydep.csv'
codeT5_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/codeT5Summarydep.csv'

gtdep=[]
codeT5dep=[]

with open(groundTruth_filePath, mode="r") as file:
    csv_reader = csv.reader(file)
    # Skip the header row if the CSV has one
    header = next(csv_reader)
    #print("Header:", header)
    
    # Read and print the rows
    for row in csv_reader:
        id = row[0]
        summary = row[1]
        data={
            'id':id,
            'summary':summary
        }
        gtdep.append(data)

with open(codeT5_filePath, mode="r") as file:
    csv_reader = csv.reader(file)
    # Skip the header row if the CSV has one
    header = next(csv_reader)
    #print("Header:", header)
    
    # Read and print the rows
    for row in csv_reader:
        id = row[0]
        summary = row[1]
        data={
            'id':id,
            'summary':summary
        }
        codeT5dep.append(data)

referenceList=[]
predictionList=[]


for item in gtdep:
    target_id = item['id']
    referenceList.append(item['summary'])
    found = False
    for element in codeT5dep:
        if(target_id==element['id']):
            found=True
            predictionList.append(element['summary'])
            break
    if found == False:
        predictionList.append('')

#print(referenceList)
#print(predictionList)

ciderdepCodeT5 = cider_score(referenceList, predictionList)



#######CodeBert######################

codeBert_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/codeBertSummarydep.csv'
codeBertdep=[]

with open(codeBert_filePath, mode="r") as file:
    csv_reader = csv.reader(file)
    # Skip the header row if the CSV has one
    header = next(csv_reader)
    #print("Header:", header)
    
    # Read and print the rows
    for row in csv_reader:
        id = row[0]
        summary = row[1]
        data={
            'id':id,
            'summary':summary
        }
        codeBertdep.append(data)

predictionList = []

for item in gtdep:
    target_id = item['id']
    #referenceList.append(item['summary'])
    found = False
    for element in codeBertdep:
        if(target_id==element['id']):
            found=True
            predictionList.append(element['summary'])
            break
    if found == False:
        predictionList.append('')

ciderdepCodeBert = cider_score(referenceList, predictionList)

#######ASAP_Base######################

asapBase_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/asapSummarydep.csv'
asapBasedep=[]

with open(asapBase_filePath, mode="r") as file:
    csv_reader = csv.reader(file)
    # Skip the header row if the CSV has one
    header = next(csv_reader)
    #print("Header:", header)
    
    # Read and print the rows
    for row in csv_reader:
        id = row[0]
        summary = row[1]
        data={
            'id':id,
            'summary':summary
        }
        asapBasedep.append(data)

predictionList = []

for item in gtdep:
    target_id = item['id']
    #referenceList.append(item['summary'])
    found = False
    for element in asapBasedep:
        if(target_id==element['id']):
            found=True
            predictionList.append(element['summary'])
            break
    if found == False:
        predictionList.append('')

ciderdepASAP = cider_score(referenceList, predictionList)



stat, p_value = mannwhitneyu(ciderIndepASAP, ciderdepASAP, alternative='two-sided')

# Output the results
print("Mann-Whitney U Test Statistic:", stat)
print("p-value:", p_value)

# Interpretation
alpha = 0.05  # Significance level
if p_value < alpha:
    print("There is a statistically significant difference")
else:
    print("There is no statistically significant difference")


stat, p_value = mannwhitneyu(ciderIndepCodeT5, ciderdepCodeT5, alternative='two-sided')

# Output the results
print("Mann-Whitney U Test Statistic:", stat)
print("p-value:", p_value)

# Interpretation
alpha = 0.05  # Significance level
if p_value < alpha:
    print("There is a statistically significant difference")
else:
    print("There is no statistically significant difference")

stat, p_value = mannwhitneyu(ciderIndepCodeBert, ciderdepCodeBert, alternative='two-sided')

# Output the results
print("Mann-Whitney U Test Statistic:", stat)
print("p-value:", p_value)

# Interpretation
alpha = 0.05  # Significance level
if p_value < alpha:
    print("There is a statistically significant difference")
else:
    print("There is no statistically significant difference")