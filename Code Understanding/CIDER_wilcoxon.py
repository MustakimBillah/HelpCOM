from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
import numpy as np
import csv
from scipy.stats import wilcoxon

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
groundTruth_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/gtSummaryChecked.csv'
#codeT5_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/codeT5Summary.csv'

gt=[]

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

referenceList=[]
predictionList = []



codeT5_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/codeT5Summary.csv'

codeT5=[]

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
        codeT5.append(data)




for item in gt:
    target_id = item['id']
    referenceList.append(item['summary'])
    found = False
    for element in codeT5:
        if(target_id==element['id']):
            found=True
            predictionList.append(element['summary'])
            break
    if found == False:
        predictionList.append('')

#print(referenceList)
#print(predictionList)

ciderCodeT5 = cider_score(referenceList, predictionList)
#print('CodeT5 cider: ',cider,' cider: ',cider,' cider: ',cider)



#######CodeBert######################

codeBert_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/codeBertSummary.csv'
codeBert=[]

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
        codeBert.append(data)

predictionList = []

for item in gt:
    target_id = item['id']
    #referenceList.append(item['summary'])
    found = False
    for element in codeBert:
        if(target_id==element['id']):
            found=True
            predictionList.append(element['summary'])
            break
    if found == False:
        predictionList.append('')

ciderCodebert = cider_score(referenceList, predictionList)
#print('CodeBert cider: ',cider,' cider: ',cider,' cider: ',cider)


#######ASAP_Base######################

asapBase_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/ASAPresultsBase.csv'
asapBase=[]

with open(asapBase_filePath, mode="r") as file:
    csv_reader = csv.reader(file)
    # Skip the header row if the CSV has one
    #header = next(csv_reader)
    #print("Header:", header)
    
    # Read and print the rows
    for row in csv_reader:
        id = row[0]
        summary = row[2]
        data={
            'id':id,
            'summary':summary
        }
        asapBase.append(data)

predictionList = []

for item in gt:
    target_id = item['id']
    #referenceList.append(item['summary'])
    found = False
    for element in asapBase:
        if(target_id==element['id']):
            found=True
            predictionList.append(element['summary'])
            break
    if found == False:
        predictionList.append('')

ciderAsap = cider_score(referenceList, predictionList)
#print('ASAP_Base cider: ',cider,' cider: ',cider,' cider: ',cider)




#######ASAP_4o######################

asap4o_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/ASAPresults4o.csv'
asap4o=[]

with open(asap4o_filePath, mode="r") as file:
    csv_reader = csv.reader(file)
    # Skip the header row if the CSV has one
    #header = next(csv_reader)
    #print("Header:", header)
    
    # Read and print the rows
    for row in csv_reader:
        id = row[0]
        summary = row[2]
        data={
            'id':id,
            'summary':summary
        }
        asap4o.append(data)

predictionList = []

for item in gt:
    target_id = item['id']
    #referenceList.append(item['summary'])
    found = False
    for element in asap4o:
        if(target_id==element['id']):
            found=True
            predictionList.append(element['summary'])
            break
    if found == False:
        predictionList.append('')

ciderAsap4 = cider_score(referenceList, predictionList)
#print('ASAP_4o cider: ',cider,' cider: ',cider,' cider: ',cider)


#######GPT_4o######################

gpt4o_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/gpt4oSummary.csv'
gpt4o=[]

with open(gpt4o_filePath, mode="r") as file:
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
        gpt4o.append(data)

predictionList = []

for item in gt:
    target_id = item['id']
    #referenceList.append(item['summary'])
    found = False
    for element in gpt4o:
        if(target_id==element['id']):
            found=True
            predictionList.append(element['summary'])
            break
    if found == False:
        predictionList.append('')

ciderGPT4 = cider_score(referenceList, predictionList)
#print('GPT_4o cider: ',cider,' cider: ',cider,' cider: ',cider)


#######helpCom_CodeLlama######################

helpCom_codeLlama_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/helpCom_codeLlama.csv'
helpCom_codeLlama=[]

with open(helpCom_codeLlama_filePath, mode="r") as file:
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
        helpCom_codeLlama.append(data)

predictionList = []

for item in gt:
    target_id = item['id']
    #referenceList.append(item['summary'])
    found = False
    for element in helpCom_codeLlama:
        if(target_id==element['id']):
            found=True
            predictionList.append(element['summary'])
            break
    if found == False:
        predictionList.append('')

ciderhelpCom_codeLlama = cider_score(referenceList, predictionList)
#print('helpCom_codeLlama cider: ',cider,' cider: ',cider,' cider: ',cider)


#######helpCom_llama######################

helpCom_llama_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/helpCom_llama.csv'
helpCom_llama=[]

with open(helpCom_llama_filePath, mode="r") as file:
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
        helpCom_llama.append(data)

predictionList = []

for item in gt:
    target_id = item['id']
    #referenceList.append(item['summary'])
    found = False
    for element in helpCom_llama:
        if(target_id==element['id']):
            found=True
            predictionList.append(element['summary'])
            break
    if found == False:
        predictionList.append('')

ciderhelpCom_llama = cider_score(referenceList, predictionList)
#print('helpCom_llama cider: ',cider,' cider: ',cider,' cider: ',cider)


#######helpCom_N_gpt4o######################

helpCom_N_gpt4o_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/helpCom_N_gpt4o.csv'
helpCom_N_gpt4o = []
referenceList=[]
predictionList=[]

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

ciderhelpCom_N_gpt4o = cider_score(referenceList, predictionList)
#print('helpCom_N_level_gpt4o cider: ',cider,' cider: ',cider,' cider: ',cider)

#######helpCom_N_codellama######################

helpCom_N_codellama_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/helpCom_N_codellama.csv'
helpCom_N_codellama=[]

with open(helpCom_N_codellama_filePath, mode="r") as file:
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
        helpCom_N_codellama.append(data)

predictionList = []

for item in gt:
    target_id = item['id']
    #referenceList.append(item['summary'])
    found = False
    for element in helpCom_N_codellama:
        if(target_id==element['id']):
            found=True
            predictionList.append(element['summary'])
            break
    if found == False:
        predictionList.append('')

ciderhelpCom_N_codellama = cider_score(referenceList, predictionList)
#print('helpCom_N_level_codellama cider: ',cider,' cider: ',cider,' cider: ',cider)


#######helpCom_N_llama######################

helpCom_N_llama_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/helpCom_N_llama.csv'
helpCom_N_llama = []

with open(helpCom_N_llama_filePath, mode="r") as file:
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
        helpCom_N_llama.append(data)

predictionList = []

for item in gt:
    target_id = item['id']
    #referenceList.append(item['summary'])
    found = False
    for element in helpCom_N_llama:
        if(target_id==element['id']):
            found=True
            predictionList.append(element['summary'])
            break
    if found == False:
        predictionList.append('')

ciderhelpCom_N_llama = cider_score(referenceList, predictionList)
#print('helpCom_N_level_llama cider: ',cider,' cider: ',cider,' cider: ',cider)


#######helpCom_4o######################

helpCom_4o_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/helpComOutput.csv'
helpCom_4o = []

with open(helpCom_4o_filePath, mode="r") as file:
    csv_reader = csv.reader(file)
    # Skip the header row if the CSV has one
    #header = next(csv_reader)
    #print("Header:", header)
    
    # Read and print the rows
    for row in csv_reader:
        id = row[0]
        summary = row[1]
        data={
            'id':id,
            'summary':summary
        }
        helpCom_4o.append(data)

predictionList = []

for item in gt:
    target_id = item['id']
    #referenceList.append(item['summary'])
    found = False
    for element in helpCom_4o:
        if(target_id==element['id']):
            found=True
            predictionList.append(element['summary'])
            break
    if found == False:
        predictionList.append('')

ciderhelpCom_4o = cider_score(referenceList, predictionList)
#print('helpCom_4o cider: ',cider,' cider: ',cider,' cider: ',cider)

#######self_codeLlama######################

self_codeLlama_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/self_codeLlama.csv'
self_codeLlama = []

with open(self_codeLlama_filePath, mode="r") as file:
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
        self_codeLlama.append(data)

predictionList = []

for item in gt:
    target_id = item['id']
    #referenceList.append(item['summary'])
    found = False
    for element in self_codeLlama:
        if(target_id==element['id']):
            found=True
            predictionList.append(element['summary'])
            break
    if found == False:
        predictionList.append('')

ciderself_codeLlama = cider_score(referenceList, predictionList)
#print('self_codeLlama cider: ',cider,' cider: ',cider,' cider: ',cider)


#######self_Llama######################

self_Llama_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/self_Llama.csv'
self_Llama = []

with open(self_Llama_filePath, mode="r") as file:
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
        self_Llama.append(data)

predictionList = []

for item in gt:
    target_id = item['id']
    #referenceList.append(item['summary'])
    found = False
    for element in self_Llama:
        if(target_id==element['id']):
            found=True
            predictionList.append(element['summary'])
            break
    if found == False:
        predictionList.append('')

ciderself_Llama = cider_score(referenceList, predictionList)
#print('self_Llama cider: ',cider,' cider: ',cider,' cider: ',cider)

print('-----------------------------------------------------------------')


# Perform the Wilcoxon Signed-Rank Test
stat, p_value = wilcoxon(ciderhelpCom_N_gpt4o, ciderCodebert, alternative='two-sided')
technique1= 'HelpComN_gpt4o'
technique2 = 'CodeBert'
metric='cider'
# Print results
#print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
#print(f"P-value: {p_value}")
print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# Interpretation
if p_value < 0.05:
    print("The difference between the two techniques is statistically significant (p < 0.05).")
else:
    print("No statistically significant difference between the techniques (p >= 0.05).")


# Perform the Wilcoxon Signed-Rank Test
stat, p_value = wilcoxon(ciderhelpCom_N_gpt4o, ciderCodeT5, alternative='two-sided')
technique1= 'HelpComN_gpt4o'
technique2 = 'CodeT5+'
metric='cider'
# Print results
#print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
#print(f"P-value: {p_value}")
print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# Interpretation
if p_value < 0.05:
    print("The difference between the two techniques is statistically significant (p < 0.05).")
else:
    print("No statistically significant difference between the techniques (p >= 0.05).")

# Perform the Wilcoxon Signed-Rank Test
stat, p_value = wilcoxon(ciderhelpCom_N_gpt4o, ciderAsap, alternative='two-sided')
technique1= 'HelpComN_gpt4o'
technique2 = 'ASAP_BASE'
metric='cider'
# Print results
#print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
#print(f"P-value: {p_value}")
print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# Interpretation
if p_value < 0.05:
    print("The difference between the two techniques is statistically significant (p < 0.05).")
else:
    print("No statistically significant difference between the techniques (p >= 0.05).")


# Perform the Wilcoxon Signed-Rank Test
stat, p_value = wilcoxon(ciderhelpCom_N_gpt4o, ciderAsap4, alternative='two-sided')
technique1= 'HelpComN_gpt4o'
technique2 = 'ASAP_GPT4o'
metric='cider'
# Print results
#print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
#print(f"P-value: {p_value}")
print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# Interpretation
if p_value < 0.05:
    print("The difference between the two techniques is statistically significant (p < 0.05).")
else:
    print("No statistically significant difference between the techniques (p >= 0.05).")

# Perform the Wilcoxon Signed-Rank Test
stat, p_value = wilcoxon(ciderhelpCom_N_gpt4o, ciderGPT4, alternative='two-sided')
technique1= 'HelpComN_gpt4o'
technique2 = 'GPT-4o'
metric='cider'
# Print results
#print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
#print(f"P-value: {p_value}")
print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# Interpretation
if p_value < 0.05:
    print("The difference between the two techniques is statistically significant (p < 0.05).")
else:
    print("No statistically significant difference between the techniques (p >= 0.05).")


# Perform the Wilcoxon Signed-Rank Test
stat, p_value = wilcoxon(ciderhelpCom_N_gpt4o, ciderself_Llama, alternative='two-sided')
technique1= 'HelpComN_gpt4o'
technique2 = 'Llama-3.3'
metric='cider'
# Print results
#print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
#print(f"P-value: {p_value}")
print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# Interpretation
if p_value < 0.05:
    print("The difference between the two techniques is statistically significant (p < 0.05).")
else:
    print("No statistically significant difference between the techniques (p >= 0.05).")

# Perform the Wilcoxon Signed-Rank Test
stat, p_value = wilcoxon(ciderhelpCom_N_gpt4o, ciderself_codeLlama, alternative='two-sided')
technique1= 'HelpComN_gpt4o'
technique2 = 'CodeLlama'
metric='cider'
# Print results
#print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
#print(f"P-value: {p_value}")
print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# Interpretation
if p_value < 0.05:
    print("The difference between the two techniques is statistically significant (p < 0.05).")
else:
    print("No statistically significant difference between the techniques (p >= 0.05).")


# Perform the Wilcoxon Signed-Rank Test
stat, p_value = wilcoxon(ciderhelpCom_N_gpt4o, ciderhelpCom_codeLlama, alternative='two-sided')
technique1= 'HelpComN_gpt4o'
technique2 = 'helpCom_codeLlama'
metric='cider'
# Print results
#print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
#print(f"P-value: {p_value}")
print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# Interpretation
if p_value < 0.05:
    print("The difference between the two techniques is statistically significant (p < 0.05).")
else:
    print("No statistically significant difference between the techniques (p >= 0.05).")

# Perform the Wilcoxon Signed-Rank Test
stat, p_value = wilcoxon(ciderhelpCom_N_gpt4o, ciderhelpCom_N_codellama, alternative='two-sided')
technique1= 'HelpComN_gpt4o'
technique2 = 'helpCom_N_codellama'
metric='cider'
# Print results
#print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
#print(f"P-value: {p_value}")
print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# Interpretation
if p_value < 0.05:
    print("The difference between the two techniques is statistically significant (p < 0.05).")
else:
    print("No statistically significant difference between the techniques (p >= 0.05).")


# Perform the Wilcoxon Signed-Rank Test
stat, p_value = wilcoxon(ciderhelpCom_N_gpt4o, ciderhelpCom_llama, alternative='two-sided')
technique1= 'HelpComN_gpt4o'
technique2 = 'CodeT5+'
metric='cider'
# Print results
#print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
#print(f"P-value: {p_value}")
print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# Interpretation
if p_value < 0.05:
    print("The difference between the two techniques is statistically significant (p < 0.05).")
else:
    print("No statistically significant difference between the techniques (p >= 0.05).")

# Perform the Wilcoxon Signed-Rank Test
stat, p_value = wilcoxon(ciderhelpCom_N_gpt4o, ciderhelpCom_N_llama, alternative='two-sided')
technique1= 'HelpComN_gpt4o'
technique2 = 'helpCom_N_llama'
metric='cider'
# Print results
#print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
#print(f"P-value: {p_value}")
print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# Interpretation
if p_value < 0.05:
    print("The difference between the two techniques is statistically significant (p < 0.05).")
else:
    print("No statistically significant difference between the techniques (p >= 0.05).")


# Perform the Wilcoxon Signed-Rank Test
stat, p_value = wilcoxon(ciderhelpCom_N_gpt4o, ciderhelpCom_4o, alternative='two-sided')
technique1= 'HelpComN_gpt4o'
technique2 = 'helpCom_4o'
metric='cider'
# Print results
#print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
#print(f"P-value: {p_value}")
print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# Interpretation
if p_value < 0.05:
    print("The difference between the two techniques is statistically significant (p < 0.05).")
else:
    print("No statistically significant difference between the techniques (p >= 0.05).")