from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
import numpy as np
import csv

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
            score = cider(candiate, reference)
            totalScore+=score
        except Exception as e:
            print(e)

    return round(totalScore/len(referenceList),4)
    




# start calculating for 380 dependent methods
print("Cider similarity score")
print('-----------------------------------------------------------------')
groundTruth_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/gtSummaryPython.csv'
#codeT5_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/codeT5Summarydep.csv'

gt=[]
#codeT5=[]

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
        gt.append(data)

# with open(codeT5_filePath, mode="r") as file:
#     csv_reader = csv.reader(file)
#     # Skip the header row if the CSV has one
#     header = next(csv_reader)
#     #print("Header:", header)
    
#     # Read and print the rows
#     for row in csv_reader:
#         id = row[0]
#         summary = row[1]
#         data={
#             'id':id,
#             'summary':summary
#         }
#         codeT5.append(data)

# referenceList=[]
# predictionList=[]


# for item in gt:
#     target_id = item['id']
#     referenceList.append(item['summary'])
#     found = False
#     for element in codeT5:
#         if(target_id==element['id']):
#             found=True
#             predictionList.append(element['summary'])
#             break
#     if found == False:
#         predictionList.append('')

#print(referenceList)
#print(predictionList)

# score = cider_score(referenceList, predictionList)
# print('CodeT5 Similarity: ',score)


# #######CodeBert######################

# codeBert_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/codeBertSummarydep.csv'
# codeBert=[]

# with open(codeBert_filePath, mode="r") as file:
#     csv_reader = csv.reader(file)
#     # Skip the header row if the CSV has one
#     header = next(csv_reader)
#     #print("Header:", header)
    
#     # Read and print the rows
#     for row in csv_reader:
#         id = row[0]
#         summary = row[1]
#         data={
#             'id':id,
#             'summary':summary
#         }
#         codeBert.append(data)

# predictionList = []

# for item in gt:
#     target_id = item['id']
#     #referenceList.append(item['summary'])
#     found = False
#     for element in codeBert:
#         if(target_id==element['id']):
#             found=True
#             predictionList.append(element['summary'])
#             break
#     if found == False:
#         predictionList.append('')

# score = cider_score(referenceList, predictionList)
# print('CodeBert Similarity: ',score)

# #######ASAP_Base######################

# asapBase_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/asapSummarydep.csv'
# asapBase=[]

# with open(asapBase_filePath, mode="r") as file:
#     csv_reader = csv.reader(file)
#     # Skip the header row if the CSV has one
#     header = next(csv_reader)
#     #print("Header:", header)
    
#     # Read and print the rows
#     for row in csv_reader:
#         id = row[0]
#         summary = row[1]
#         data={
#             'id':id,
#             'summary':summary
#         }
#         asapBase.append(data)

# predictionList = []

# for item in gt:
#     target_id = item['id']
#     #referenceList.append(item['summary'])
#     found = False
#     for element in asapBase:
#         if(target_id==element['id']):
#             found=True
#             predictionList.append(element['summary'])
#             break
#     if found == False:
#         predictionList.append('')

# score = cider_score(referenceList, predictionList)
# print('ASAP_Base Similarity: ',score)



#######ASAP_4o######################

# asap4o_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/ASAPresults4o.csv'
# asap4o=[]

# with open(asap4o_filePath, mode="r") as file:
#     csv_reader = csv.reader(file)
#     # Skip the header row if the CSV has one
#     #header = next(csv_reader)
#     #print("Header:", header)
    
#     # Read and print the rows
#     for row in csv_reader:
#         id = row[0]
#         summary = row[2]
#         data={
#             'id':id,
#             'summary':summary
#         }
#         asap4o.append(data)

# predictionList = []

# for item in gt:
#     target_id = item['id']
#     #referenceList.append(item['summary'])
#     found = False
#     for element in asap4o:
#         if(target_id==element['id']):
#             found=True
#             predictionList.append(element['summary'])
#             break
#     if found == False:
#         predictionList.append('')

# score = cider_score(referenceList, predictionList)
# print('ASAP_4o Similarity: ',score)

# #######GPT_4o######################

# gpt4o_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/gpt4oSummary.csv'
# gpt4o=[]

# with open(gpt4o_filePath, mode="r") as file:
#     csv_reader = csv.reader(file)
#     # Skip the header row if the CSV has one
#     header = next(csv_reader)
#     #print("Header:", header)
    
#     # Read and print the rows
#     for row in csv_reader:
#         id = row[0]
#         summary = row[1]
#         data={
#             'id':id,
#             'summary':summary
#         }
#         gpt4o.append(data)

# predictionList = []

# for item in gt:
#     target_id = item['id']
#     #referenceList.append(item['summary'])
#     found = False
#     for element in gpt4o:
#         if(target_id==element['id']):
#             found=True
#             predictionList.append(element['summary'])
#             break
#     if found == False:
#         predictionList.append('')

# score = cider_score(referenceList, predictionList)
# print('GPT_4o Similarity: ',score)

# #######helpCom_CodeLlama######################

# helpCom_codeLlama_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/helpCom_codeLlama.csv'
# helpCom_codeLlama=[]

# with open(helpCom_codeLlama_filePath, mode="r") as file:
#     csv_reader = csv.reader(file)
#     # Skip the header row if the CSV has one
#     header = next(csv_reader)
#     #print("Header:", header)
    
#     # Read and print the rows
#     for row in csv_reader:
#         id = row[0]
#         summary = row[1]
#         data={
#             'id':id,
#             'summary':summary
#         }
#         helpCom_codeLlama.append(data)

# predictionList = []

# for item in gt:
#     target_id = item['id']
#     #referenceList.append(item['summary'])
#     found = False
#     for element in helpCom_codeLlama:
#         if(target_id==element['id']):
#             found=True
#             predictionList.append(element['summary'])
#             break
#     if found == False:
#         predictionList.append('')

# score = cider_score(referenceList, predictionList)
# print('helpCom_codeLlama Similarity: ',score)

# #######helpCom_llama######################

# helpCom_llama_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/helpCom_llama.csv'
# helpCom_llama=[]

# with open(helpCom_llama_filePath, mode="r") as file:
#     csv_reader = csv.reader(file)
#     # Skip the header row if the CSV has one
#     header = next(csv_reader)
#     #print("Header:", header)
    
#     # Read and print the rows
#     for row in csv_reader:
#         id = row[0]
#         summary = row[1]
#         data={
#             'id':id,
#             'summary':summary
#         }
#         helpCom_llama.append(data)

# predictionList = []

# for item in gt:
#     target_id = item['id']
#     #referenceList.append(item['summary'])
#     found = False
#     for element in helpCom_llama:
#         if(target_id==element['id']):
#             found=True
#             predictionList.append(element['summary'])
#             break
#     if found == False:
#         predictionList.append('')

# score = cider_score(referenceList, predictionList)
# print('helpCom_llama Similarity: ',score)

# #######helpCom_N_codellama######################

# helpCom_N_codellama_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/helpCom_N_codellama.csv'
# helpCom_N_codellama=[]

# with open(helpCom_N_codellama_filePath, mode="r") as file:
#     csv_reader = csv.reader(file)
#     # Skip the header row if the CSV has one
#     header = next(csv_reader)
#     #print("Header:", header)
    
#     # Read and print the rows
#     for row in csv_reader:
#         id = row[0]
#         summary = row[1]
#         data={
#             'id':id,
#             'summary':summary
#         }
#         helpCom_N_codellama.append(data)

# predictionList = []

# for item in gt:
#     target_id = item['id']
#     #referenceList.append(item['summary'])
#     found = False
#     for element in helpCom_N_codellama:
#         if(target_id==element['id']):
#             found=True
#             predictionList.append(element['summary'])
#             break
#     if found == False:
#         predictionList.append('')

# score = cider_score(referenceList, predictionList)
# print('helpCom_N_level_codellama Similarity: ',score)

#######helpCom_N_gpt4o######################

referenceList=[]
predictionList=[]

helpCom_N_gpt4o_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/helpCom_N_gpt4o_python.csv'
helpCom_N_gpt4o = []

with open(helpCom_N_gpt4o_filePath, mode="r") as file:
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
        helpCom_N_gpt4o.append(data)

predictionList = []

for item in gt:
    target_id = item['id']
    referenceList.append(item['summary'])
    found = False
    for element in helpCom_N_gpt4o:
        if(target_id==element['id']):
            found=True
            predictionList.append(element['summary'])
            break
    if found == False:
        predictionList.append('')

score = cider_score(referenceList, predictionList)
print('helpCom_N_level_gpt4o Similarity: ',score)

# #######helpCom_N_llama######################

# helpCom_N_llama_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/helpCom_N_llama.csv'
# helpCom_N_llama = []

# with open(helpCom_N_llama_filePath, mode="r") as file:
#     csv_reader = csv.reader(file)
#     # Skip the header row if the CSV has one
#     header = next(csv_reader)
#     #print("Header:", header)
    
#     # Read and print the rows
#     for row in csv_reader:
#         id = row[0]
#         summary = row[1]
#         data={
#             'id':id,
#             'summary':summary
#         }
#         helpCom_N_llama.append(data)

# predictionList = []

# for item in gt:
#     target_id = item['id']
#     #referenceList.append(item['summary'])
#     found = False
#     for element in helpCom_N_llama:
#         if(target_id==element['id']):
#             found=True
#             predictionList.append(element['summary'])
#             break
#     if found == False:
#         predictionList.append('')

# score = cider_score(referenceList, predictionList)
# print('helpCom_N_level_llama Similarity: ',score)

# #######helpCom_4o######################

# helpCom_4o_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/helpComOutput.csv'
# helpCom_4o = []

# with open(helpCom_4o_filePath, mode="r") as file:
#     csv_reader = csv.reader(file)
#     # Skip the header row if the CSV has one
#     #header = next(csv_reader)
#     #print("Header:", header)
    
#     # Read and print the rows
#     for row in csv_reader:
#         id = row[0]
#         summary = row[1]
#         data={
#             'id':id,
#             'summary':summary
#         }
#         helpCom_4o.append(data)

# predictionList = []

# for item in gt:
#     target_id = item['id']
#     #referenceList.append(item['summary'])
#     found = False
#     for element in helpCom_4o:
#         if(target_id==element['id']):
#             found=True
#             predictionList.append(element['summary'])
#             break
#     if found == False:
#         predictionList.append('')

# score = cider_score(referenceList, predictionList)
# print('helpCom_4o Similarity: ',score)

# #######self_codeLlama######################

# self_codeLlama_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/self_codeLlama.csv'
# self_codeLlama = []

# with open(self_codeLlama_filePath, mode="r") as file:
#     csv_reader = csv.reader(file)
#     # Skip the header row if the CSV has one
#     header = next(csv_reader)
#     #print("Header:", header)
    
#     # Read and print the rows
#     for row in csv_reader:
#         id = row[0]
#         summary = row[1]
#         data={
#             'id':id,
#             'summary':summary
#         }
#         self_codeLlama.append(data)

# predictionList = []

# for item in gt:
#     target_id = item['id']
#     #referenceList.append(item['summary'])
#     found = False
#     for element in self_codeLlama:
#         if(target_id==element['id']):
#             found=True
#             predictionList.append(element['summary'])
#             break
#     if found == False:
#         predictionList.append('')

# score = cider_score(referenceList, predictionList)
# print('self_codeLlama Similarity: ',score)

# #######self_Llama######################

# self_Llama_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/self_Llama.csv'
# self_Llama = []

# with open(self_Llama_filePath, mode="r") as file:
#     csv_reader = csv.reader(file)
#     # Skip the header row if the CSV has one
#     header = next(csv_reader)
#     #print("Header:", header)
    
#     # Read and print the rows
#     for row in csv_reader:
#         id = row[0]
#         summary = row[1]
#         data={
#             'id':id,
#             'summary':summary
#         }
#         self_Llama.append(data)

# predictionList = []

# for item in gt:
#     target_id = item['id']
#     #referenceList.append(item['summary'])
#     found = False
#     for element in self_Llama:
#         if(target_id==element['id']):
#             found=True
#             predictionList.append(element['summary'])
#             break
#     if found == False:
#         predictionList.append('')

# score = cider_score(referenceList, predictionList)
# print('self_Llama Similarity: ',score)

print('-----------------------------------------------------------------')


# # Example Usage
# if __name__ == "__main__":
#     candidate_summary = "Sort the array in ascending order."
#     reference_summaries = [
#         "Sort the array in ascending order."
#     ]

#     score = cider(candidate_summary, reference_summaries, n=4)
#     print(f"CIDER Score: {score:.4f}")


