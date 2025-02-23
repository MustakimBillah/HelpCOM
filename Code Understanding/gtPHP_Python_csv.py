from pymongo import MongoClient
import csv

client = MongoClient('mongodb://localhost:27017/')
db = client.code_understanding             
samplePython = db.samplePython
samplePHP = db.samplePHP

gtPHP=[]
gtPython=[]


for item in samplePython.find():
    id=item.get('_id')
    groundTruth=item.get('Docstring')
    data={
        'id':id,
        'groundTruth':groundTruth
    }
    gtPython.append(data)


for item in samplePHP.find():
    id=item.get('_id')
    groundTruth=item.get('Docstring')
    data={
        'id':id,
        'groundTruth':groundTruth
    }
    gtPHP.append(data)


with open('/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/gtSummaryPython.csv', mode='w', newline='') as file:
    # Get the headers from the dictionary keys
    fieldnames = gtPython[0].keys()
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()  # Write headers
    writer.writerows(gtPython)  # Write each dictionary as a r 


with open('/student/mjr175/method-level-comment-generation/Code Understanding/Summary_Files/gtSummaryPHP.csv', mode='w', newline='') as file:
    # Get the headers from the dictionary keys
    fieldnames = gtPHP[0].keys()
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()  # Write headers
    writer.writerows(gtPHP)  # Write each dictionary as a r 

print("done processing")
