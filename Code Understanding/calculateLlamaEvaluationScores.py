import re
from collections import defaultdict
import csv
# File path
file_path = "/student/mjr175/method-level-comment-generation/Code Understanding/llamaEval.txt"

# Dictionary to store scores for each comment
scores = defaultdict(list)

# Regular expression to extract comment scores
pattern = r"Comment (\d+): (\d+)"

# Read and parse the file
with open(file_path, "r") as file:
    for line in file:
        match = re.findall(pattern, line)
        if match:
            for comment_id, score in match:
                scores[int(comment_id)].append(int(score))


print (scores)
# Calculate and print averages
print("Average Scores for Each Comment:")
for comment_id in sorted(scores.keys()):
    avg_score = sum(scores[comment_id]) / len(scores[comment_id])
    print(f"Comment {comment_id}: {avg_score:.2f}")

directoryPath = '/student/mjr175/method-level-comment-generation/Code Understanding/metricResults/'

with open(directoryPath+"codeT5_llamaEval.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    for item in scores[1]:
        writer.writerow([item])
print('-----------------------------------------------------------------')
with open(directoryPath+"codeBert_llamaEval.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    for item in scores[2]:
        writer.writerow([item])
print('-----------------------------------------------------------------')
with open(directoryPath+"asap_llamaEval.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    for item in scores[3]:
        writer.writerow([item])
print('-----------------------------------------------------------------')
with open(directoryPath+"asap4o_llamaEval.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    for item in scores[4]:
        writer.writerow([item])
print('-----------------------------------------------------------------')
with open(directoryPath+"gpt4o_llamaEval.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    for item in scores[5]:
        writer.writerow([item])
print('-----------------------------------------------------------------')
with open(directoryPath+"codeLlama_llamaEval.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    for item in scores[6]:
        writer.writerow([item])
print('-----------------------------------------------------------------')

with open(directoryPath+"Llama_llamaEval.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    for item in scores[7]:
        writer.writerow([item])
print('-----------------------------------------------------------------')
with open(directoryPath+"helpCom_Llama_llamaEval.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    for item in scores[8]:
        writer.writerow([item])
print('-----------------------------------------------------------------')
with open(directoryPath+"helpCom_4o_llamaEval.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    for item in scores[9]:
        writer.writerow([item])
print('-----------------------------------------------------------------')
with open(directoryPath+"helpCom_codeLlama_llamaEval.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    for item in scores[10]:
        writer.writerow([item])
print('-----------------------------------------------------------------')
with open(directoryPath+"helpCom_N_Llama_llamaEval.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    for item in scores[11]:
        writer.writerow([item])
print('-----------------------------------------------------------------')
with open(directoryPath+"helpCom_N_4o_llamaEval.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    for item in scores[12]:
        writer.writerow([item])
print('-----------------------------------------------------------------')
with open(directoryPath+"helpCom_N_codeLlama_llamaEval.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    for item in scores[13]:
        writer.writerow([item])
print('-----------------------------------------------------------------')