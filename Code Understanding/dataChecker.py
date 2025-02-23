from emseBleu import nltk_bleu
from rougeL import rouge_l
import csv

groundTruth_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/gtSummaryChecked.csv'
codeT5_filePath = '/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/ASAPresultsBase.csv'

gt=[]
asap=[]

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

with open(codeT5_filePath, mode="r") as file:
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
        asap.append(data)

for ref,pred in zip(gt,asap):
    id = ref['id']
    bleu = nltk_bleu(pred['summary'],ref['summary'])
    rouge = rouge_l(ref['summary'],pred['summary'])
    if(rouge>0.8):
        print(id,rouge)