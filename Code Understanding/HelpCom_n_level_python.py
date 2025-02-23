from pymongo import MongoClient

from time import sleep
import csv
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

import sys

from openai import OpenAI
client_openAI = OpenAI(
    api_key = "sk-proj-dPQvN0GALJBgOPcFYYkWT3BlbkFJOMo2fRii5rMXSv7fxDEm"
)

sys.setrecursionlimit(10**6)

PY_LANGUAGE = Language(tspython.language(),'python')

parser = Parser()
parser.set_language(PY_LANGUAGE)

client = MongoClient('mongodb://localhost:27017/')
db = client.code_understanding    
       
sampleDB = db.samplePython
masterMethodDB = db.methodsPython

parentRepo = ''
methodSearchSpace = []

def generateSummary(method, helperMap):
    instruction =("""Write down only the summary part of the docstring that would have been written by a developer for the following function,\n\n""")
    prompt = instruction + "\"" + method + "\"\n\n"
    prompt+= "Where the implementations of the helper functions are as follows:\n"
    summary=''
    
    for key,valueList in helperMap.items():
        level = int(key) + 1
        prompt+='Level-'+ str(level) +' helpers:\n'
        prompt+='-------------------------------------------------------------------------------\n'
        helperBodies = set()

        for item in valueList:
            for element in item:
                bodyMethod = element['MethodBody']
                if len(bodyMethod)>0:
                    helperBodies.add(element['MethodBody'])
        
        for helperBody in helperBodies:
            prompt+= helperBody+"\n"
        prompt+='-------------------------------------------------------------------------------\n'
    
    completion = client_openAI.chat.completions.create(
        model="gpt-4o",
        temperature=0.2,
        messages=[
            {"role": "system", "content": "You are an expert Python developer."},
            {"role": "user", "content": prompt}
            ]
            )
    summary = completion.choices[0].message.content

    return summary

def traverse(node, results):
    if node is None:
        return results
    # Print node information.
    if(node.type=="call"):
        node_text = node.text.decode('utf-8')    
        #print('Called_Method: ',node_text)
        functionName = ''
        cnt = 0
        arg_string=''
        arg_list=[]
        for child in node.children:
            #print(child.type)
            if(child.type=="argument_list"):
                for args in child.children:
                    arg_string+=args.type
                    #print(arg_string)
                arg_string = arg_string.strip('()')
                arg_list = [item.strip() for item in arg_string.split(',')]
                cnt = len(arg_list)
                if(cnt==1 and len(arg_string)==0):
                    cnt=0
  
            if(child.type=="attribute"):
                functionName = (child.text.decode('utf-8'))
        
        fName = functionName.split('.').pop()
        #print('function name: ',fName)
        #print('argument count: ',cnt)
        helperInf = {
            "Syntax":node_text,
            "FunctionName":fName,
            "ArgsCount":cnt
        }
        results.append(helperInf)
    # Recursively traverse child nodes
    for child in node.children:
        traverse(child,results)
    return results



def extractHelpers(code):
    tree = parser.parse((code))
    root = tree.root_node
    helperInfo=[]
    return traverse(root,helperInfo)


results = []

def getMethodBody(repo,functionName,argsCount):
    methodBody=""
    fileName=""
    

    for item in methodSearchSpace:
        fileName = item.get('file')
        methods = item.get('methods')
        for method in methods:
            if(functionName == method.get('FunctionName') and argsCount == method.get('ArgsCount')):
                methodBody = method.get('Syntax')
                return methodBody,fileName
    return methodBody,fileName 

def explore_helper_tree(helperTree):
    current_node_number = 1  # Start numbering nodes from 1
    
    def visit_node(node):
        nonlocal current_node_number
        
        # Process the current node if it hasn't been visited
        if not node['visited']:
            node['visited'] = True  # Mark it as visited
            
            # Explore helperMethods and add them as new nodes
            new_nodes = []
            for method in node['helpers']:
                
                body = method.get('MethodBody') 

                if len(body)==0:
                    continue
                
                current_node_number += 1  # Increment node number
                #print("Calling extractHelpers")
                methodHelpers = extractHelpers(body.encode('utf-8'))

                helpersList = []
                ## todo: loop through methodHelpers and match from JavaCodeT5DB , find method boy and populate uniqueHelpers
                for element in methodHelpers:
                    functionName = element.get('FunctionName')
                    argsCount = element.get('ArgsCount')
                    #print("Calling getMethodBody")
                    matchedMethodBody, fileName = getMethodBody(parentRepo, functionName, argsCount)
                    
                    if len(matchedMethodBody)>0:
                        helpersList.append({
                            'Syntax': element.get('Syntax'),
                            'FunctionName': functionName,
                            'ArgsCount': argsCount,
                            'MethodBody': matchedMethodBody,
                            'FileName': fileName
                        })
                if(len(helpersList)>0):
                    new_nodes.append({
                        'node': current_node_number,
                        'parent': node['node'],
                        'helpers': helpersList,
                        'visited': False
                    })
            
            # Add new nodes to the helperTree
            if len(new_nodes)>0:
                helperTree.extend(new_nodes)

    def traverse_tree():
        # Check if any node is unvisited and process it
        for node in helperTree:
            if not node['visited']:
                visit_node(node)
                traverse_tree()  # Recursive call to handle all nodes
                break  # Restart the loop after processing a node

    # Start traversal
    traverse_tree()




def postProcessHelperLevel(helperChain):
    processedTree = {}
    prevParent = 0
    helperList=[]
    currParent = 0

    for item in helperChain:
        parent = item['parent']
        helperList = item['helpers']

        if parent not in processedTree:
            processedTree[parent] = []
        processedTree[parent].append(helperList)

    return processedTree




count = 0

for item in sampleDB.find():
    #print(item)
    parentRepo = item.get('repo')
    methodSearchSpace = masterMethodDB.find({'repo': parentRepo})
    helpers = item.get('helpers').get('helpers')
    method = item.get('Syntax')
    helperMethods = []
    helperTree = []
 
    for helper in helpers:
        helperBody = helper.get('MethodBody') 
        if(len(helperBody)==0):
            continue
        helperMethods.append(helper)

    helperTree.append({
        'node': 1,
        'parent': 0,
        'helpers':helperMethods,
        'visited': False
    })
    
    #######################Recursive till n-level######################
    #print("Calling explore_helper_tree")
    helperChain = explore_helper_tree(helperTree)
    ###################################################################
    #print("helperTree: ",json.dumps(helperTree,indent=2))
    #print("length of tree: ",len(helperTree) )
    processedTree=postProcessHelperLevel(helperTree)
    #print("processed helper tree: ",json.dumps(processedTree))
    print("##################")

    count+=1


    #Generate Summary Part
    try:
        HelpComSummary = generateSummary(method, processedTree)
        print(HelpComSummary)
        data = {
            '_id': item.get('_id'),
            'HelpComSummary': HelpComSummary
        }
        results.append(data)
    except Exception as e:
        print("Error generating summary: ",e)
        sleep(5)

    sleep(1)

    # if count == 1:
    #     break

#Write results to the csv
with open('helpCom_N_gpt4o_python.csv', mode='w', newline='') as file:
    # Get the headers from the dictionary keys
    fieldnames = results[0].keys()
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()  # Write headers
    writer.writerows(results) 

