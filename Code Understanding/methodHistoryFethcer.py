from gitLogExecuter import git_log_executer
from pymongo import MongoClient
import time
from multiprocessing import Pool

repo_path = 'localDirectoryPath/JAVA_Projects/neo4j/'  # Change this to the path of the target repository
repo_prefix = "https://github.com/neo4j/neo4j/blob/5.20/"
currentRepo = 'neo4j/neo4j'

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.code_understanding

# Access the collection
methods = db.methods.find()

methodListTotal=[]
methodList=[]
duplicates = []
methodHistoryFileList=[]
#itemCount = 0

for item in methods:
    if(item.get("repo")==currentRepo):
        methodListTotal.append(item)

client.close()

client = MongoClient('mongodb://localhost:27017/')
db = client.code_understanding             

methodHistory = db.methodHistory.find()



count=0

for item in methodHistory:
    if(item.get("repo")==currentRepo):
        methodHistoryFileList.append(item.get("file"))

client.close()

for item in methodListTotal:
    if(item.get("file") in methodHistoryFileList):
        duplicates.append(item)
    else:
        count+=1

print("duplicates: ",len(duplicates))
print("unique: ",count)

methodList = [x for x in methodListTotal if x not in duplicates]


client = MongoClient('mongodb://localhost:27017/')
db = client.code_understanding             

methodHistoryDB = db.methodHistory


def fetchHistory(item):
    method=item.get("methods")
    file_path = item.get("file")
    file_path = file_path.replace(repo_prefix,"")

    for element in method:
        start_line = element.get("StartLine")
        end_line = element.get("EndLine")
        element["historyFetched"] = False
        try:
            nCommits, nDiffs, nAuthors, firstCommit, lastCommit, timeFrame = git_log_executer(repo_path, start_line, end_line, file_path)

            element["commits"] = nCommits
            element["authors"] = nAuthors
            element["diffs"] = nDiffs
            element["firstCommit"] = str(firstCommit)
            element["lastCommit"] = str(lastCommit)
            element["timeFrame"] = str(timeFrame)
            element["historyFetched"] = True
        
        except Exception as e:
            print("Exception in method history fetching", e)
            time.sleep(5)

    methodHistoryDB.insert_one(item)
    print("Added item: ", item.get('_id'))    


# Execute in multi thread
pool = Pool()
pool.map(fetchHistory, methodList)
pool.close()
pool.join()