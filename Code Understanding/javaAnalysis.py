from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.code_understanding             
javaDBFinal = db.javaDBCodeT5p.find()


dependentMethods = 0
independentMethods = 0

depCommitTotal = 0
indepCommitTotal = 0
depDiffTotal = 0 
indepDiffTotal = 0
depAuthorsTotal = 0
indepAuthorsTotal = 0
depDaysTotal = 0
indepDaysTotal = 0
totalFiles = 0

for element in javaDBFinal:
    totalFiles+=1
    methods = element.get('methods')
    for item in methods:
        if (item.get('isDependent')==True):
            dependentMethods+=1
            
            if (item.get('commits') != None):
                depCommitTotal += item.get('commits')
                depDiffTotal += item.get('diffs')
                depAuthorsTotal += item.get('authors')
                timeFrame = item.get('timeFrame')
                days = timeFrame.split(" ")
                if(len(days) < 2):
                    days[0] = 0

                depDaysTotal += int(days[0])

        else:
            independentMethods+=1
            
            if (item.get('commits') != None):
                indepCommitTotal += item.get('commits',0)
                indepDiffTotal += item.get('diffs',0)
                indepAuthorsTotal += item.get('authors',0)
                timeFrame = item.get('timeFrame',0)
                days = timeFrame.split(" ")
                if(len(days) < 2):
                    days[0] = 0

                indepDaysTotal += int(days[0])

print("Total Java Files : ", totalFiles)

print("Total Java Methods: ",dependentMethods+independentMethods)
print("Total dependent Methods: ",dependentMethods," Percentage: ",(dependentMethods/(dependentMethods+independentMethods))*100)
print("Total independent Methods: ",independentMethods," Percentage: ",(independentMethods/(dependentMethods+independentMethods))*100)

print("Total commit: ",indepCommitTotal+depCommitTotal)
print("Total independent commits: ", indepCommitTotal)
print("Total dependent commits: ", depCommitTotal)

print("Avg. Commits per method: ",(indepCommitTotal+depCommitTotal)/(dependentMethods+independentMethods))
print("Avg. Commits per independent method: ",(indepCommitTotal)/(independentMethods))
print("Avg. Commits per dependent method: ",(depCommitTotal)/(dependentMethods))

print("Total diffs: ",indepDiffTotal+depDiffTotal)
print("Total independent diffs: ", indepDiffTotal)
print("Total dependent diffs: ", depDiffTotal)

print("Avg. Diffs per method: ",(indepDiffTotal+depDiffTotal)/(dependentMethods+independentMethods))
print("Avg. Diffs per independent method: ",(indepDiffTotal)/(independentMethods))
print("Avg. Diffs per dependent method: ",(depDiffTotal)/(dependentMethods))


print("Total authors: ",indepAuthorsTotal+depAuthorsTotal)
print("Total independent authors: ", indepAuthorsTotal)
print("Total dependent authors: ", depAuthorsTotal)

print("Avg. Authors per method: ",(indepAuthorsTotal+depAuthorsTotal)/(dependentMethods+independentMethods))
print("Avg. Authors per independent method: ",(indepAuthorsTotal)/(independentMethods))
print("Avg. Authors per dependent method: ",(depAuthorsTotal)/(dependentMethods))

print("Avg. TimeFrame(days) of Commits per method: ",(indepDaysTotal+depDaysTotal)/(dependentMethods+independentMethods))
print("Avg. TimeFrame(days) of Commits per independent method: ",(indepDaysTotal)/(independentMethods))
print("Avg. TimeFrame(days) of Commits per dependent method: ",(depDaysTotal)/(dependentMethods))






            



