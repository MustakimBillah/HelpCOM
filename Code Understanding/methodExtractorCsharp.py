
from tree_sitter import Language, Parser
import os
import csv
from pymongo import MongoClient
import sys
 
sys.setrecursionlimit(10**6)

def instantiate_language(name):
    Language.build_library(f"libtree-sitter-c-sharp.so", ["/student/mjr175/method-level-comment-generation/tree-sitter-c-sharp"])
    return Language(f"/student/mjr175/method-level-comment-generation/tree-sitter-c-sharp/libtree-sitter-c-sharp.so", name)


# instantiate language
C_SHARP = instantiate_language("c_sharp") 

# instantiate parser
parser = Parser()
parser.set_language(C_SHARP)

tree = parser.parse(
    bytes(
        """
static int CalculateFactorial(int n)
{
    if (n == 0 || n == 1)
    {
        return 1; // Base case: factorial of 0 or 1 is 1
    }

    return n * CalculateFactorial(n - 1); // Recursive call
}
""",
        "utf8",
    )
)

print(tree.root_node)

# def traverse(node, results):
#     global isDoctring
#     global blockComment

#     if node is None:
#         return results
#     # Print node information
#     functionName = ''

#     if(node.type == "method_declaration"):
#         declaredMethod = node.text.decode('utf-8')    
#         startLine = node.start_point[0] + 1
#         endLine = node.end_point[0] + 1
#         #print("start line: ", startLine)
#         #print("end line: ", endLine)
#         cnt = 0
#         for child in node.children:
#             if(child.type=="formal_parameters"):
#                 for subchild in child.children:
#                     if ('parameter' in subchild.type):
#                         cnt = cnt + 1
#             if (child.type=="identifier"):
#                 functionName = child.text.decode('utf-8')
#                 #print('functionName',functionName)
        
#         methodInf = {
#             "Docstring": blockComment,
#             "Syntax": declaredMethod,
#             "FunctionName": functionName,
#             "ArgsCount": cnt,
#             "StartLine": startLine,
#             "EndLine": endLine
#         }
#         results.append(methodInf)


#     isDoctring = False
#     blockComment = ''

#     #fetch docstring
#     if(node.type=="block_comment"):
#         blockComment = node.text.decode('utf-8')
#         isDoctring = True   

#     # Recursively traverse child nodes
#     for child in node.children:
#         traverse(child,results)
#     return results


# def extractMethods(root):
#     methodInfo=[]
#     return traverse(root,methodInfo)


# def traverseTree(node, results):
#     if node is None:
#         return results
#     if(node.type == "import_declaration"):
#         node_text = node.text.decode('utf-8')
#         results.append(node_text)

#     # Recursively traverse child nodes
#     for child in node.children:
#         traverseTree(child,results)
#     return results



# def extractImports(root):
#     importInfo=[]
#     return traverseTree(root,importInfo)



# methodsFinal = [] 



# def process_java_files(directory):
#     # Traverse the directory tree recursively
#     for root, dirs, files in os.walk(directory):
#         # Iterate over all files in the current directory
#         for file in files:
#             # Check if the file has a .java extension
#             if file.endswith(".java"):
#                 # Process the Java file
#                 process_java_file(os.path.join(root, file))

# def process_java_file(file_path):
#     # Process the Java file
#     print("Processing Java file:", file_path)
#     # Split the file path using the '/' delimiter
#     file_path_fromDisk = file_path.replace(directory_to_process, "")
#     # Extract the repository name (second-to-last element)
#     #print('repo_name:',repo_name)
#     with open(file_path, "rb") as f:
#         tree = parser.parse(f.read())
#         root = tree.root_node
#         methods = {
#             "repo": repo_name,
#             "file": file_prefix + file_path_fromDisk,
#             "methods": extractMethods(root),
#             "imports": extractImports(root),
#             "language": "JAVA"
#         }
#         methodsFinal.append(methods)
#         #print("processed file: ",file_path_fromDisk)

        

# # Specify the directory to process (change this to your desired directory)
# directory_to_process = "/student/mjr175/JAVA_Projects/neo4j"

# #information about the GitHub Project
# repo_name = "neo4j/neo4j"
# branch_name = "5.20"
# file_prefix = "https://github.com/"+repo_name+"/blob/"+branch_name


# #Global variables to fetch docstrings with methods
# blockComment = ''
# isDoctring = False

# # Call the function to process Java files in the specified directory and its subdirectories
# process_java_files(directory_to_process)


# #save_methods_to_database
# #client = MongoClient('mongodb+srv://mbillahmim:dmY5XMETcLbLSmF6@cluster0.h3plcij.mongodb.net/')
# client = MongoClient('mongodb://localhost:27017/')
# db = client.code_understanding
# methods = db.methods

# for item in methodsFinal:
#     try:
#         methods.insert_one(item)
#         print("processed")
#     except Exception as e:
#         print(f"Error inserting data: {e}")















