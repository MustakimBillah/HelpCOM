
import csv
from scipy.stats import wilcoxon

import csv

def read_csv_to_list(file_path):
    values = []
    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:  # Ensure the row is not empty
                values.append(float(row[0]))  # Convert the value to float

        

    return values

def make_lists_equal(list1, list2):
    # Find the difference in lengths
    len_diff = len(list1) - len(list2)
    
    # If list1 is shorter, add zeros to it
    if len_diff > 0:
        list2.extend([0] * len_diff)
    
    # If list2 is shorter, add zeros to it
    elif len_diff < 0:
        list1.extend([0] * (-len_diff))
    
    return list1, list2

def wilcoxonModified(list1, list2, alternative='two-sided'):
    list1, list2 = make_lists_equal(list1, list2)

    return wilcoxon(list1,list2,alternative='two-sided')


llamaEvalCodeT5 = read_csv_to_list('/student/mjr175/method-level-comment-generation/Code Understanding/metricResults/codeT5_llamaEval.csv')
#print('CodeT5 bleu: ',bleu,' rouge: ',rouge,' llamaEval: ',llamaEval)



#######CodeBert######################

llamaEvalCodeBert = read_csv_to_list('/student/mjr175/method-level-comment-generation/Code Understanding/metricResults/codeBert_llamaEval.csv')
#print('CodeBert bleu: ',bleu,' rouge: ',rouge,' llamaEval: ',llamaEval)


#######ASAP_Base######################

llamaEvalAsap = read_csv_to_list('/student/mjr175/method-level-comment-generation/Code Understanding/metricResults/asap_llamaEval.csv')
#print('ASAP_Base bleu: ',bleu,' rouge: ',rouge,' llamaEval: ',llamaEval)




#######ASAP_4o######################

llamaEvalAsap4 = read_csv_to_list('/student/mjr175/method-level-comment-generation/Code Understanding/metricResults/asap4o_llamaEval.csv')
#print('ASAP_4o bleu: ',bleu,' rouge: ',rouge,' llamaEval: ',llamaEval)


#######GPT_4o######################

llamaEvalGPT4 = read_csv_to_list('/student/mjr175/method-level-comment-generation/Code Understanding/metricResults/gpt4o_llamaEval.csv')
#print('GPT_4o bleu: ',bleu,' rouge: ',rouge,' llamaEval: ',llamaEval)


#######helpCom_CodeLlama######################

llamaEvalhelpCom_codeLlama = read_csv_to_list('/student/mjr175/method-level-comment-generation/Code Understanding/metricResults/helpCom_codeLlama_llamaEval.csv')
#print('helpCom_codeLlama bleu: ',bleu,' rouge: ',rouge,' llamaEval: ',llamaEval)


#######helpCom_llama######################

llamaEvalhelpCom_llama = read_csv_to_list("/student/mjr175/method-level-comment-generation/Code Understanding/metricResults/helpCom_Llama_llamaEval.csv")
#print('helpCom_llama bleu: ',bleu,' rouge: ',rouge,' llamaEval: ',llamaEval)


#######helpCom_N_gpt4o######################

llamaEvalhelpCom_N_gpt4o = read_csv_to_list('/student/mjr175/method-level-comment-generation/Code Understanding/metricResults/helpCom_N_4o_llamaEval.csv')
#print('helpCom_N_level_gpt4o bleu: ',bleu,' rouge: ',rouge,' llamaEval: ',llamaEval)

#######helpCom_N_codellama######################

llamaEvalhelpCom_N_codellama = read_csv_to_list('/student/mjr175/method-level-comment-generation/Code Understanding/metricResults/helpCom_N_codeLlama_llamaEval.csv')
#print('helpCom_N_level_codellama bleu: ',bleu,' rouge: ',rouge,' llamaEval: ',llamaEval)


#######helpCom_N_llama######################

llamaEvalhelpCom_N_llama = read_csv_to_list('/student/mjr175/method-level-comment-generation/Code Understanding/metricResults/helpCom_N_Llama_llamaEval.csv')
#print('helpCom_N_level_llama bleu: ',bleu,' rouge: ',rouge,' llamaEval: ',llamaEval)


#######helpCom_4o######################

llamaEvalhelpCom_4o = read_csv_to_list('/student/mjr175/method-level-comment-generation/Code Understanding/metricResults/helpCom_4o_llamaEval.csv')
#print('helpCom_4o bleu: ',bleu,' rouge: ',rouge,' llamaEval: ',llamaEval)

#######self_codeLlama######################

llamaEvalself_codeLlama = read_csv_to_list('/student/mjr175/method-level-comment-generation/Code Understanding/metricResults/codeLlama_llamaEval.csv')
#print('self_codeLlama bleu: ',bleu,' rouge: ',rouge,' llamaEval: ',llamaEval)


#######self_Llama######################

llamaEvalself_Llama = read_csv_to_list('/student/mjr175/method-level-comment-generation/Code Understanding/metricResults/Llama_llamaEval.csv')
#print('self_Llama bleu: ',bleu,' rouge: ',rouge,' llamaEval: ',llamaEval)

print('-----------------------------------------------------------------')


#####Statistical Test Start######



# Perform the Wilcoxon Signed-Rank Test
stat, p_value = wilcoxonModified(llamaEvalhelpCom_N_gpt4o, llamaEvalCodeBert, alternative='two-sided')
technique1= 'HelpComN_gpt4o'
technique2 = 'CodeBert'
metric='llamaEval'
# Print results
#print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
#print(f"P-value: {p_value}")
print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# Interpretation
if p_value < 0.05:
    print("The difference between the two techniques is statistically significant (p < 0.05).")
else:
    print("No statistically significant difference between the techniques (p >= 0.05).")


# Perform the Wilcoxon Signed-Rank Test
stat, p_value = wilcoxonModified(llamaEvalhelpCom_N_gpt4o, llamaEvalCodeT5, alternative='two-sided')
technique1= 'HelpComN_gpt4o'
technique2 = 'CodeT5+'
metric='llamaEval'
# Print results
#print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
#print(f"P-value: {p_value}")
print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# Interpretation
if p_value < 0.05:
    print("The difference between the two techniques is statistically significant (p < 0.05).")
else:
    print("No statistically significant difference between the techniques (p >= 0.05).")

# Perform the Wilcoxon Signed-Rank Test
stat, p_value = wilcoxonModified(llamaEvalhelpCom_N_gpt4o, llamaEvalAsap, alternative='two-sided')
technique1= 'HelpComN_gpt4o'
technique2 = 'ASAP_BASE'
metric='llamaEval'
# Print results
#print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
#print(f"P-value: {p_value}")
print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# Interpretation
if p_value < 0.05:
    print("The difference between the two techniques is statistically significant (p < 0.05).")
else:
    print("No statistically significant difference between the techniques (p >= 0.05).")


# Perform the Wilcoxon Signed-Rank Test
stat, p_value = wilcoxonModified(llamaEvalhelpCom_N_gpt4o, llamaEvalAsap4, alternative='two-sided')
technique1= 'HelpComN_gpt4o'
technique2 = 'ASAP_GPT4o'
metric='llamaEval'
# Print results
#print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
#print(f"P-value: {p_value}")
print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# Interpretation
if p_value < 0.05:
    print("The difference between the two techniques is statistically significant (p < 0.05).")
else:
    print("No statistically significant difference between the techniques (p >= 0.05).")

# Perform the Wilcoxon Signed-Rank Test
stat, p_value = wilcoxonModified(llamaEvalhelpCom_N_gpt4o, llamaEvalGPT4, alternative='two-sided')
technique1= 'HelpComN_gpt4o'
technique2 = 'GPT-4o'
metric='llamaEval'
# Print results
#print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
#print(f"P-value: {p_value}")
print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# Interpretation
if p_value < 0.05:
    print("The difference between the two techniques is statistically significant (p < 0.05).")
else:
    print("No statistically significant difference between the techniques (p >= 0.05).")


# Perform the Wilcoxon Signed-Rank Test
stat, p_value = wilcoxonModified(llamaEvalhelpCom_N_gpt4o, llamaEvalself_Llama, alternative='two-sided')
technique1= 'HelpComN_gpt4o'
technique2 = 'Llama-3.3'
metric='llamaEval'
# Print results
#print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
#print(f"P-value: {p_value}")
print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# Interpretation
if p_value < 0.05:
    print("The difference between the two techniques is statistically significant (p < 0.05).")
else:
    print("No statistically significant difference between the techniques (p >= 0.05).")

# Perform the Wilcoxon Signed-Rank Test
stat, p_value = wilcoxonModified(llamaEvalhelpCom_N_gpt4o, llamaEvalself_codeLlama, alternative='two-sided')
technique1= 'HelpComN_gpt4o'
technique2 = 'CodeLlama'
metric='llamaEval'
# Print results
#print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
#print(f"P-value: {p_value}")
print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# Interpretation
if p_value < 0.05:
    print("The difference between the two techniques is statistically significant (p < 0.05).")
else:
    print("No statistically significant difference between the techniques (p >= 0.05).")


# Perform the Wilcoxon Signed-Rank Test
stat, p_value = wilcoxonModified(llamaEvalhelpCom_N_gpt4o, llamaEvalhelpCom_codeLlama, alternative='two-sided')
technique1= 'HelpComN_gpt4o'
technique2 = 'helpCom_codeLlama'
metric='llamaEval'
# Print results
#print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
#print(f"P-value: {p_value}")
print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# Interpretation
if p_value < 0.05:
    print("The difference between the two techniques is statistically significant (p < 0.05).")
else:
    print("No statistically significant difference between the techniques (p >= 0.05).")

# Perform the Wilcoxon Signed-Rank Test
stat, p_value = wilcoxonModified(llamaEvalhelpCom_N_gpt4o, llamaEvalhelpCom_N_codellama, alternative='two-sided')
technique1= 'HelpComN_gpt4o'
technique2 = 'helpCom_N_codellama'
metric='llamaEval'
# Print results
#print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
#print(f"P-value: {p_value}")
print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# Interpretation
if p_value < 0.05:
    print("The difference between the two techniques is statistically significant (p < 0.05).")
else:
    print("No statistically significant difference between the techniques (p >= 0.05).")


# Perform the Wilcoxon Signed-Rank Test
stat, p_value = wilcoxonModified(llamaEvalhelpCom_N_gpt4o, llamaEvalhelpCom_llama, alternative='two-sided')
technique1= 'HelpComN_gpt4o'
technique2 = 'helpCom_llama'
metric='llamaEval'
# Print results
#print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
#print(f"P-value: {p_value}")
print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# Interpretation
if p_value < 0.05:
    print("The difference between the two techniques is statistically significant (p < 0.05).")
else:
    print("No statistically significant difference between the techniques (p >= 0.05).")

# Perform the Wilcoxon Signed-Rank Test
stat, p_value = wilcoxonModified(llamaEvalhelpCom_N_gpt4o, llamaEvalhelpCom_N_llama, alternative='two-sided')
technique1= 'HelpComN_gpt4o'
technique2 = 'helpCom_N_llama'
metric='llamaEval'
# Print results
#print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
#print(f"P-value: {p_value}")
print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# Interpretation
if p_value < 0.05:
    print("The difference between the two techniques is statistically significant (p < 0.05).")
else:
    print("No statistically significant difference between the techniques (p >= 0.05).")


# Perform the Wilcoxon Signed-Rank Test
stat, p_value = wilcoxonModified(llamaEvalhelpCom_N_gpt4o, llamaEvalhelpCom_4o, alternative='two-sided')
technique1= 'HelpComN_gpt4o'
technique2 = 'helpCom_4o'
metric='llamaEval'
# Print results
#print(f"Wilcoxon Signed-Rank Test statistic: {stat}")
#print(f"P-value: {p_value}")
print("Wilcoxon Signed-Rank On ",metric," with ",technique2)
# Interpretation
if p_value < 0.05:
    print("The difference between the two techniques is statistically significant (p < 0.05).")
else:
    print("No statistically significant difference between the techniques (p >= 0.05).")