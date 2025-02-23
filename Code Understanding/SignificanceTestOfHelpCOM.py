from meteor import meteor_score
from rougeL import rouge_l
from emseBleu import nltk_bleu
import csv
from scipy.stats import wilcoxon

def calculateScores(refList,predList):
    totalBleu = []
    totalRouge = []
    totalMeteor = []

    for ref,pred in zip(refList,predList):
        totalBleu.append(nltk_bleu(pred, ref))
        totalRouge.append(rouge_l(ref, pred))
        totalMeteor.append(meteor_score(ref, pred))

    return totalBleu, totalRouge, totalMeteor


# start calculating for 380 dependent methods
print("Text similarity scores")
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

bleuCodeT5,rougeCodeT5,meteorCodeT5 = calculateScores(referenceList, predictionList)
#print('CodeT5 bleu: ',bleu,' rouge: ',rouge,' meteor: ',meteor)



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

bleuCodebert,rougeCodeBert,meteorCodeBert = calculateScores(referenceList, predictionList)
#print('CodeBert bleu: ',bleu,' rouge: ',rouge,' meteor: ',meteor)


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

bleuAsap,rougeAsap,meteorAsap = calculateScores(referenceList, predictionList)
#print('ASAP_Base bleu: ',bleu,' rouge: ',rouge,' meteor: ',meteor)




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

bleuAsap4,rougeAsap4,meteorAsap4 = calculateScores(referenceList, predictionList)
#print('ASAP_4o bleu: ',bleu,' rouge: ',rouge,' meteor: ',meteor)


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

bleuGPT4,rougeGPT4,meteorGPT4 = calculateScores(referenceList, predictionList)
#print('GPT_4o bleu: ',bleu,' rouge: ',rouge,' meteor: ',meteor)


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

bleuhelpCom_codeLlama,rougehelpCom_codeLlama,meteorhelpCom_codeLlama = calculateScores(referenceList, predictionList)
#print('helpCom_codeLlama bleu: ',bleu,' rouge: ',rouge,' meteor: ',meteor)


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

bleuhelpCom_llama,rougehelpCom_llama,meteorhelpCom_llama = calculateScores(referenceList, predictionList)
#print('helpCom_llama bleu: ',bleu,' rouge: ',rouge,' meteor: ',meteor)


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

bleuhelpCom_N_gpt4o,rougehelpCom_N_gpt4o,meteorhelpCom_N_gpt4o = calculateScores(referenceList, predictionList)
#print('helpCom_N_level_gpt4o bleu: ',bleu,' rouge: ',rouge,' meteor: ',meteor)

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

bleuhelpCom_N_codellama,rougehelpCom_N_codellama,meteorhelpCom_N_codellama = calculateScores(referenceList, predictionList)
#print('helpCom_N_level_codellama bleu: ',bleu,' rouge: ',rouge,' meteor: ',meteor)


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

bleuhelpCom_N_llama,rougehelpCom_N_llama,meteorhelpCom_N_llama = calculateScores(referenceList, predictionList)
#print('helpCom_N_level_llama bleu: ',bleu,' rouge: ',rouge,' meteor: ',meteor)


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

bleuhelpCom_4o,rougehelpCom_4o,meteorhelpCom_4o = calculateScores(referenceList, predictionList)
#print('helpCom_4o bleu: ',bleu,' rouge: ',rouge,' meteor: ',meteor)

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

bleuself_codeLlama,rougeself_codeLlama,meteorself_codeLlama = calculateScores(referenceList, predictionList)
#print('self_codeLlama bleu: ',bleu,' rouge: ',rouge,' meteor: ',meteor)


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

bleuself_Llama,rougeself_Llama,meteorself_Llama = calculateScores(referenceList, predictionList)
#print('self_Llama bleu: ',bleu,' rouge: ',rouge,' meteor: ',meteor)

print('-----------------------------------------------------------------')


#####Statistical Test Start######

# # Perform the Wilcoxon Signed-Rank Test
# stat, p_value = wilcoxon(bleuhelpCom_N_gpt4o, bleuCodebert, alternative='two-sided')
# technique1= 'HelpComN_gpt4o'
# technique2 = 'CodeBert'
# metric='Bleu'
# # Print results
# #print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
# #print(f"P-value: {p_value}")
# print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# # Interpretation
# if p_value < 0.05:
#     print("The difference between the two techniques is statistically significant (p < 0.05).")
# else:
#     print("No statistically significant difference between the techniques (p >= 0.05).")


# # Perform the Wilcoxon Signed-Rank Test
# stat, p_value = wilcoxon(bleuhelpCom_N_gpt4o, bleuCodeT5, alternative='two-sided')
# technique1= 'HelpComN_gpt4o'
# technique2 = 'CodeT5+'
# metric='Bleu'
# # Print results
# #print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
# #print(f"P-value: {p_value}")
# print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# # Interpretation
# if p_value < 0.05:
#     print("The difference between the two techniques is statistically significant (p < 0.05).")
# else:
#     print("No statistically significant difference between the techniques (p >= 0.05).")

# # Perform the Wilcoxon Signed-Rank Test
# stat, p_value = wilcoxon(bleuhelpCom_N_gpt4o, bleuAsap, alternative='two-sided')
# technique1= 'HelpComN_gpt4o'
# technique2 = 'ASAP_BASE'
# metric='Bleu'
# # Print results
# #print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
# #print(f"P-value: {p_value}")
# print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# # Interpretation
# if p_value < 0.05:
#     print("The difference between the two techniques is statistically significant (p < 0.05).")
# else:
#     print("No statistically significant difference between the techniques (p >= 0.05).")


# # Perform the Wilcoxon Signed-Rank Test
# stat, p_value = wilcoxon(bleuhelpCom_N_gpt4o, bleuAsap4, alternative='two-sided')
# technique1= 'HelpComN_gpt4o'
# technique2 = 'ASAP_GPT4o'
# metric='Bleu'
# # Print results
# #print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
# #print(f"P-value: {p_value}")
# print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# # Interpretation
# if p_value < 0.05:
#     print("The difference between the two techniques is statistically significant (p < 0.05).")
# else:
#     print("No statistically significant difference between the techniques (p >= 0.05).")

# # Perform the Wilcoxon Signed-Rank Test
# stat, p_value = wilcoxon(bleuhelpCom_N_gpt4o, bleuGPT4, alternative='two-sided')
# technique1= 'HelpComN_gpt4o'
# technique2 = 'GPT-4o'
# metric='Bleu'
# # Print results
# #print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
# #print(f"P-value: {p_value}")
# print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# # Interpretation
# if p_value < 0.05:
#     print("The difference between the two techniques is statistically significant (p < 0.05).")
# else:
#     print("No statistically significant difference between the techniques (p >= 0.05).")


# # Perform the Wilcoxon Signed-Rank Test
# stat, p_value = wilcoxon(bleuhelpCom_N_gpt4o, bleuself_Llama, alternative='two-sided')
# technique1= 'HelpComN_gpt4o'
# technique2 = 'Llama-3.3'
# metric='Bleu'
# # Print results
# #print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
# #print(f"P-value: {p_value}")
# print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# # Interpretation
# if p_value < 0.05:
#     print("The difference between the two techniques is statistically significant (p < 0.05).")
# else:
#     print("No statistically significant difference between the techniques (p >= 0.05).")

# # Perform the Wilcoxon Signed-Rank Test
# stat, p_value = wilcoxon(bleuhelpCom_N_gpt4o, bleuself_codeLlama, alternative='two-sided')
# technique1= 'HelpComN_gpt4o'
# technique2 = 'CodeLlama'
# metric='Bleu'
# # Print results
# #print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
# #print(f"P-value: {p_value}")
# print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# # Interpretation
# if p_value < 0.05:
#     print("The difference between the two techniques is statistically significant (p < 0.05).")
# else:
#     print("No statistically significant difference between the techniques (p >= 0.05).")


# # Perform the Wilcoxon Signed-Rank Test
# stat, p_value = wilcoxon(bleuhelpCom_N_gpt4o, bleuhelpCom_codeLlama, alternative='two-sided')
# technique1= 'HelpComN_gpt4o'
# technique2 = 'helpCom_codeLlama'
# metric='Bleu'
# # Print results
# #print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
# #print(f"P-value: {p_value}")
# print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# # Interpretation
# if p_value < 0.05:
#     print("The difference between the two techniques is statistically significant (p < 0.05).")
# else:
#     print("No statistically significant difference between the techniques (p >= 0.05).")

# # Perform the Wilcoxon Signed-Rank Test
# stat, p_value = wilcoxon(bleuhelpCom_N_gpt4o, bleuhelpCom_N_codellama, alternative='two-sided')
# technique1= 'HelpComN_gpt4o'
# technique2 = 'helpCom_N_codellama'
# metric='Bleu'
# # Print results
# #print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
# #print(f"P-value: {p_value}")
# print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# # Interpretation
# if p_value < 0.05:
#     print("The difference between the two techniques is statistically significant (p < 0.05).")
# else:
#     print("No statistically significant difference between the techniques (p >= 0.05).")


# # Perform the Wilcoxon Signed-Rank Test
# stat, p_value = wilcoxon(bleuhelpCom_N_gpt4o, bleuhelpCom_llama, alternative='two-sided')
# technique1= 'HelpComN_gpt4o'
# technique2 = 'CodeT5+'
# metric='helpCom_llama'
# # Print results
# #print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
# #print(f"P-value: {p_value}")
# print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# # Interpretation
# if p_value < 0.05:
#     print("The difference between the two techniques is statistically significant (p < 0.05).")
# else:
#     print("No statistically significant difference between the techniques (p >= 0.05).")

# # Perform the Wilcoxon Signed-Rank Test
# stat, p_value = wilcoxon(bleuhelpCom_N_gpt4o, bleuhelpCom_N_llama, alternative='two-sided')
# technique1= 'HelpComN_gpt4o'
# technique2 = 'helpCom_N_llama'
# metric='Bleu'
# # Print results
# #print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
# #print(f"P-value: {p_value}")
# print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# # Interpretation
# if p_value < 0.05:
#     print("The difference between the two techniques is statistically significant (p < 0.05).")
# else:
#     print("No statistically significant difference between the techniques (p >= 0.05).")


# # Perform the Wilcoxon Signed-Rank Test
# stat, p_value = wilcoxon(bleuhelpCom_N_gpt4o, bleuhelpCom_4o, alternative='two-sided')
# technique1= 'HelpComN_gpt4o'
# technique2 = 'helpCom_4o'
# metric='Bleu'
# # Print results
# #print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
# #print(f"P-value: {p_value}")
# print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# # Interpretation
# if p_value < 0.05:
#     print("The difference between the two techniques is statistically significant (p < 0.05).")
# else:
#     print("No statistically significant difference between the techniques (p >= 0.05).")


# # Perform the Wilcoxon Signed-Rank Test
# stat, p_value = wilcoxon(rougehelpCom_N_gpt4o, rougeCodeBert, alternative='two-sided')
# technique1= 'HelpComN_gpt4o'
# technique2 = 'CodeBert'
# metric='Rouge'
# # Print results
# #print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
# #print(f"P-value: {p_value}")
# print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# # Interpretation
# if p_value < 0.05:
#     print("The difference between the two techniques is statistically significant (p < 0.05).")
# else:
#     print("No statistically significant difference between the techniques (p >= 0.05).")


# # Perform the Wilcoxon Signed-Rank Test
# stat, p_value = wilcoxon(rougehelpCom_N_gpt4o, rougeCodeT5, alternative='two-sided')
# technique1= 'HelpComN_gpt4o'
# technique2 = 'CodeT5+'
# metric='Rouge'
# # Print results
# #print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
# #print(f"P-value: {p_value}")
# print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# # Interpretation
# if p_value < 0.05:
#     print("The difference between the two techniques is statistically significant (p < 0.05).")
# else:
#     print("No statistically significant difference between the techniques (p >= 0.05).")

# # Perform the Wilcoxon Signed-Rank Test
# stat, p_value = wilcoxon(rougehelpCom_N_gpt4o, rougeAsap, alternative='two-sided')
# technique1= 'HelpComN_gpt4o'
# technique2 = 'ASAP_BASE'
# metric='Rouge'
# # Print results
# #print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
# #print(f"P-value: {p_value}")
# print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# # Interpretation
# if p_value < 0.05:
#     print("The difference between the two techniques is statistically significant (p < 0.05).")
# else:
#     print("No statistically significant difference between the techniques (p >= 0.05).")


# # Perform the Wilcoxon Signed-Rank Test
# stat, p_value = wilcoxon(rougehelpCom_N_gpt4o, rougeAsap4, alternative='two-sided')
# technique1= 'HelpComN_gpt4o'
# technique2 = 'ASAP_GPT4o'
# metric='Rouge'
# # Print results
# #print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
# #print(f"P-value: {p_value}")
# print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# # Interpretation
# if p_value < 0.05:
#     print("The difference between the two techniques is statistically significant (p < 0.05).")
# else:
#     print("No statistically significant difference between the techniques (p >= 0.05).")

# # Perform the Wilcoxon Signed-Rank Test
# stat, p_value = wilcoxon(rougehelpCom_N_gpt4o, rougeGPT4, alternative='two-sided')
# technique1= 'HelpComN_gpt4o'
# technique2 = 'GPT-4o'
# metric='Rouge'
# # Print results
# #print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
# #print(f"P-value: {p_value}")
# print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# # Interpretation
# if p_value < 0.05:
#     print("The difference between the two techniques is statistically significant (p < 0.05).")
# else:
#     print("No statistically significant difference between the techniques (p >= 0.05).")


# # Perform the Wilcoxon Signed-Rank Test
# stat, p_value = wilcoxon(rougehelpCom_N_gpt4o, rougeself_Llama, alternative='two-sided')
# technique1= 'HelpComN_gpt4o'
# technique2 = 'Llama-3.3'
# metric='Rouge'
# # Print results
# #print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
# #print(f"P-value: {p_value}")
# print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# # Interpretation
# if p_value < 0.05:
#     print("The difference between the two techniques is statistically significant (p < 0.05).")
# else:
#     print("No statistically significant difference between the techniques (p >= 0.05).")

# # Perform the Wilcoxon Signed-Rank Test
# stat, p_value = wilcoxon(rougehelpCom_N_gpt4o, rougeself_codeLlama, alternative='two-sided')
# technique1= 'HelpComN_gpt4o'
# technique2 = 'CodeLlama'
# metric='Rouge'
# # Print results
# #print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
# #print(f"P-value: {p_value}")
# print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# # Interpretation
# if p_value < 0.05:
#     print("The difference between the two techniques is statistically significant (p < 0.05).")
# else:
#     print("No statistically significant difference between the techniques (p >= 0.05).")


# # Perform the Wilcoxon Signed-Rank Test
# stat, p_value = wilcoxon(rougehelpCom_N_gpt4o, rougehelpCom_codeLlama, alternative='two-sided')
# technique1= 'HelpComN_gpt4o'
# technique2 = 'helpCom_codeLlama'
# metric='Rouge'
# # Print results
# #print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
# #print(f"P-value: {p_value}")
# print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# # Interpretation
# if p_value < 0.05:
#     print("The difference between the two techniques is statistically significant (p < 0.05).")
# else:
#     print("No statistically significant difference between the techniques (p >= 0.05).")

# # Perform the Wilcoxon Signed-Rank Test
# stat, p_value = wilcoxon(rougehelpCom_N_gpt4o, rougehelpCom_N_codellama, alternative='two-sided')
# technique1= 'HelpComN_gpt4o'
# technique2 = 'helpCom_N_codellama'
# metric='Rouge'
# # Print results
# #print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
# #print(f"P-value: {p_value}")
# print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# # Interpretation
# if p_value < 0.05:
#     print("The difference between the two techniques is statistically significant (p < 0.05).")
# else:
#     print("No statistically significant difference between the techniques (p >= 0.05).")


# # Perform the Wilcoxon Signed-Rank Test
# stat, p_value = wilcoxon(rougehelpCom_N_gpt4o, rougehelpCom_llama, alternative='two-sided')
# technique1= 'HelpComN_gpt4o'
# technique2 = 'CodeT5+'
# metric='helpCom_llama'
# # Print results
# #print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
# #print(f"P-value: {p_value}")
# print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# # Interpretation
# if p_value < 0.05:
#     print("The difference between the two techniques is statistically significant (p < 0.05).")
# else:
#     print("No statistically significant difference between the techniques (p >= 0.05).")

# # Perform the Wilcoxon Signed-Rank Test
# stat, p_value = wilcoxon(rougehelpCom_N_gpt4o, rougehelpCom_N_llama, alternative='two-sided')
# technique1= 'HelpComN_gpt4o'
# technique2 = 'helpCom_N_llama'
# metric='Rouge'
# # Print results
# #print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
# #print(f"P-value: {p_value}")
# print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# # Interpretation
# if p_value < 0.05:
#     print("The difference between the two techniques is statistically significant (p < 0.05).")
# else:
#     print("No statistically significant difference between the techniques (p >= 0.05).")


# # Perform the Wilcoxon Signed-Rank Test
# stat, p_value = wilcoxon(rougehelpCom_N_gpt4o, rougehelpCom_4o, alternative='two-sided')
# technique1= 'HelpComN_gpt4o'
# technique2 = 'helpCom_4o'
# metric='Rouge'
# # Print results
# #print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
# #print(f"P-value: {p_value}")
# print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# # Interpretation
# if p_value < 0.05:
#     print("The difference between the two techniques is statistically significant (p < 0.05).")
# else:
#     print("No statistically significant difference between the techniques (p >= 0.05).")



# Perform the Wilcoxon Signed-Rank Test
stat, p_value = wilcoxon(meteorhelpCom_N_gpt4o, meteorCodeBert, alternative='two-sided')
technique1= 'HelpComN_gpt4o'
technique2 = 'CodeBert'
metric='METEOR'
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
stat, p_value = wilcoxon(meteorhelpCom_N_gpt4o, meteorCodeT5, alternative='two-sided')
technique1= 'HelpComN_gpt4o'
technique2 = 'CodeT5+'
metric='METEOR'
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
stat, p_value = wilcoxon(meteorhelpCom_N_gpt4o, meteorAsap, alternative='two-sided')
technique1= 'HelpComN_gpt4o'
technique2 = 'ASAP_BASE'
metric='METEOR'
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
stat, p_value = wilcoxon(meteorhelpCom_N_gpt4o, meteorAsap4, alternative='two-sided')
technique1= 'HelpComN_gpt4o'
technique2 = 'ASAP_GPT4o'
metric='METEOR'
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
stat, p_value = wilcoxon(meteorhelpCom_N_gpt4o, meteorGPT4, alternative='two-sided')
technique1= 'HelpComN_gpt4o'
technique2 = 'GPT-4o'
metric='METEOR'
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
stat, p_value = wilcoxon(meteorhelpCom_N_gpt4o, meteorself_Llama, alternative='two-sided')
technique1= 'HelpComN_gpt4o'
technique2 = 'Llama-3.3'
metric='METEOR'
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
stat, p_value = wilcoxon(meteorhelpCom_N_gpt4o, meteorself_codeLlama, alternative='two-sided')
technique1= 'HelpComN_gpt4o'
technique2 = 'CodeLlama'
metric='METEOR'
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
stat, p_value = wilcoxon(meteorhelpCom_N_gpt4o, meteorhelpCom_codeLlama, alternative='two-sided')
technique1= 'HelpComN_gpt4o'
technique2 = 'helpCom_codeLlama'
metric='METEOR'
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
stat, p_value = wilcoxon(meteorhelpCom_N_gpt4o, meteorhelpCom_N_codellama, alternative='two-sided')
technique1= 'HelpComN_gpt4o'
technique2 = 'helpCom_N_codellama'
metric='METEOR'
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
stat, p_value = wilcoxon(meteorhelpCom_N_gpt4o, meteorhelpCom_llama, alternative='two-sided')
technique1= 'HelpComN_gpt4o'
technique2 = 'CodeT5+'
metric='METEOR'
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
stat, p_value = wilcoxon(meteorhelpCom_N_gpt4o, meteorhelpCom_N_llama, alternative='two-sided')
technique1= 'HelpComN_gpt4o'
technique2 = 'helpCom_N_llama'
metric='METEOR'
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
stat, p_value = wilcoxon(meteorhelpCom_N_gpt4o, meteorhelpCom_4o, alternative='two-sided')
technique1= 'HelpComN_gpt4o'
technique2 = 'helpCom_4o'
metric='METEOR'
# Print results
#print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
#print(f"P-value: {p_value}")
print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# Interpretation
if p_value < 0.05:
    print("The difference between the two techniques is statistically significant (p < 0.05).")
else:
    print("No statistically significant difference between the techniques (p >= 0.05).")