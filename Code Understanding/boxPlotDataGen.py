from pymongo import MongoClient
import csv
client = MongoClient('mongodb://localhost:27017/')
db = client.code_understanding             
javaDBFinal = db.javaDBCodeT5p.find()
dataList = []


for file in javaDBFinal:
    methods = file.get('methods')
    for method in methods:
        isDependent = method.get('isDependent')
        commits = method.get('commits')
        authors = method.get('authors')
        diffs = method.get('diffs')
        if(commits==None):
            continue
        data ={
            'metric': 'commits_'+('dependent'if isDependent else'independent'),
            'count': commits
        }
        dataList.append(data)

        data ={
            'metric': 'engagement_'+('dependent'if isDependent else'independent'),
            'count': authors

        }
        dataList.append(data)




with open('boxPlot_horizontal.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["metric","count"])
    for data in dataList:
        writer.writerow([data.get('metric'),data.get('count')])

print("Data exported to CSV successfully!")