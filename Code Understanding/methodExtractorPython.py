import tree_sitter_python as tspython
from tree_sitter import Language, Parser
import os
from pymongo import MongoClient
import sys
import time

sys.setrecursionlimit(10**6)

PY_LANGUAGE = Language(tspython.language(),'python')

parser = Parser()
parser.set_language(PY_LANGUAGE)


def traverse(node, results):
    
    global isDoctring
    global blockComment

    if node is None:
        return results
    functionName = ''

    if node.type == "function_definition":
        node_text = node.text.decode('utf-8')  
        startLine = node.start_point[0] + 1
        endLine = node.end_point[0] + 1
        cnt = 0
        for child in node.children:
            if child.type == "parameters":
                for subchild in child.children:
                    if subchild.type in ('default_parameter', 'identifier', 'typed_parameter'):
                        cnt += 1
            if child.type == "identifier":
                functionName = child.text.decode('utf-8')
        
        methodInf = {
            "Docstring": blockComment,
            "Syntax": node_text,
            "FunctionName": functionName,
            "ArgsCount": cnt,
            "StartLine": startLine,
            "EndLine": endLine
        }
        results.append(methodInf)
    
    isDoctring = False
    blockComment = ''

    #fetch docstring -->do in another file
    # if(node.type=="expression_statement"):
    #     blockComment = node.text.decode('utf-8')
    #     isDoctring = True  

    # Recursively traverse child nodes
    for child in node.children:
        traverse(child, results)
    return results

def extractMethods(root):
    methodInfo = []
    return traverse(root, methodInfo)

def traverseTree(node, results):
    if node is None:
        return results
    if node.type == "import_statement" or node.type == "import_from_statement":
        node_text = node.text.decode('utf-8')
        results.append(node_text)

    # Recursively traverse child nodes
    for child in node.children:
        traverseTree(child, results)
    return results

def extractImports(root):
    importInfo = []
    return traverseTree(root, importInfo)

methodsFinal = []

def process_python_files(directory):
    # Traverse the directory tree recursively
    for root, dirs, files in os.walk(directory):
        # Iterate over all files in the current directory
        for file in files:
            # Check if the file has a .py extension
            if file.endswith(".py"):
                # Process the Python file
                process_python_file(os.path.join(root, file))
                

def process_python_file(file_path):
    # Process the Python file
    print("Processing Python file:", file_path)
    # Split the file path using the '/' delimiter
    file_path_fromDisk = file_path.replace(directory_to_process, "")
    # Extract the repository name (second-to-last element)
    print('repo_name:', repo_name)
    with open(file_path, "rb") as f:
        tree = parser.parse(f.read())
        root = tree.root_node
        methods = {
            "repo": repo_name,
            "file": file_prefix + file_path_fromDisk,
            "methods": extractMethods(root),
            "imports": extractImports(root),
            "language": "Python"
        }
        methodsFinal.append(methods)
        print("processed file: ", file_path_fromDisk)

# Specify the directory to process (change this to your desired directory)
directory_to_process = "/student/mjr175/python_project/celery"

#information about the GitHub Project
repo_name = "celery/celery"
branch_name = "main"
file_prefix = "https://github.com/"+repo_name+"/blob/"+branch_name

# Call the function to process Python files in the specified directory and its subdirectories
process_python_files(directory_to_process)



#save_methods_to_database
#client = MongoClient('mongodb+srv://mbillahmim:dmY5XMETcLbLSmF6@cluster0.h3plcij.mongodb.net/')
client = MongoClient('mongodb://localhost:27017/')
db = client.code_understanding
methods = db.methodsPython

for item in methodsFinal:
    try:
        methods.insert_one(item)
        print("processed")
    except Exception as e:
        print(f"Error inserting data: {e}")