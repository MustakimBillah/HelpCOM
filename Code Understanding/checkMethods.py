from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('mongodb://localhost:27017/')

db = client.code_understanding             
sampleDB = db.checkedDepSample.find()
#sample = db.depSample.find_one({'_id':ObjectId('67299dbda23f7e5639814e0e')})

#print(sample)


bleu = 0
total = 0

test = """protected boolean insert(T e) {
        int n = size;
        if (n >= heap.length) {
            grow(n + 1);
        }
        siftUp(n, e);
        size = n + 1;
        return true;
    }"""
bleuASAP =0
bleuHelpCom =0
totalBleu=0
for item in sampleDB:
    bleuASAP = item.get('bleuCodeBert')
    #bleuHelpCom =item.get('bleuHelpCom')
    #print(item)
    #break
    # if (item.get('Syntax') == test):
    #     print(item)
    #     break
    if(bleuASAP!=None):
        totalBleu+=bleuASAP
        total+=1

    else:
        print(item.get('_id'))
        


print(totalBleu/(total))
print(total)
#print(bleuHelpCom)

