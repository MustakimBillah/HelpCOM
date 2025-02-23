from pymongo import MongoClient
import csv

client = MongoClient('mongodb://localhost:27017/')
db = client.code_understanding    
       
sampleDB = db.samplePHP


gtSummary = []
codeT5Summary = []
cBertSummary = []
asapSummary = []
codeList = []
counter=0

for item in sampleDB.find():
    code = item.get('Syntax')
    # gt = item.get('methodLevelComment')
    # cT5 = item.get('codeT5p_Summary')
    # cBert = item.get('codeBert_Summary')
    # asap = item.get('summaryASAP')

    dataCode = {
        '_id': item.get('_id'),
        'Summary': code
    }

    codeList.append(dataCode)

    # dataGT = {
    #     '_id': item.get('_id'),
    #     'Summary': gt
    # }

    # gtSummary.append(dataGT)

    # dataCT5 = {
    #     '_id': item.get('_id'),
    #     'Summary': cT5
    # }

    # codeT5Summary.append(dataCT5)

    # dataCBert = {
    #     '_id': item.get('_id'),
    #     'Summary': cBert
    # }

    # cBertSummary.append(dataCBert)

    # dataAsap = {
    #     '_id': item.get('_id'),
    #     'Summary': asap
    # }

    # asapSummary.append(dataAsap)
    print('processed')




with open('/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/codePHP.csv', mode='w', newline='') as file:
    # Get the headers from the dictionary keys
    fieldnames = codeList[0].keys()
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()  # Write headers
    writer.writerows(codeList)  # Write each dictionary as a r 


# with open('/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/codeT5Summarydep.csv', mode='w', newline='') as file:
#     # Get the headers from the dictionary keys
#     fieldnames = codeT5Summary[0].keys()
#     writer = csv.DictWriter(file, fieldnames=fieldnames)

#     writer.writeheader()  # Write headers
#     writer.writerows(codeT5Summary)  # Write each dictionary as a r 

# with open('/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/codeBertSummarydep.csv', mode='w', newline='') as file:
#     # Get the headers from the dictionary keys
#     fieldnames = cBertSummary[0].keys()
#     writer = csv.DictWriter(file, fieldnames=fieldnames)

#     writer.writeheader()  # Write headers
#     writer.writerows(cBertSummary)  # Write each dictionary as a r 

# with open('/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/asapSummarydep.csv', mode='w', newline='') as file:
#     # Get the headers from the dictionary keys
#     fieldnames = asapSummary[0].keys()
#     writer = csv.DictWriter(file, fieldnames=fieldnames)

#     writer.writeheader()  # Write headers
#     writer.writerows(asapSummary)  # Write each dictionary as a r 


