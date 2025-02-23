def lcs_length(reference, prediction):
    """
    Calculate the length of the Longest Common Subsequence (LCS) between two strings.
    """
    ref_len = len(reference)
    pred_len = len(prediction)
    
    # Create a 2D table to store the LCS lengths
    lcs_table = [[0] * (pred_len + 1) for _ in range(ref_len + 1)]

    for i in range(1, ref_len + 1):
        for j in range(1, pred_len + 1):
            if reference[i - 1] == prediction[j - 1]:
                lcs_table[i][j] = lcs_table[i - 1][j - 1] + 1
            else:
                lcs_table[i][j] = max(lcs_table[i - 1][j], lcs_table[i][j - 1])

    # The LCS length for the entire strings is in the bottom-right cell
    return lcs_table[ref_len][pred_len]

def rouge_l(reference, prediction):
    """
    Calculate ROUGE-L score between a reference and a predicted string.
    """
    # Split reference and prediction into tokens
    ref_tokens = reference.split()
    pred_tokens = prediction.split()
    
    # Get LCS length
    lcs = lcs_length(ref_tokens, pred_tokens)
    
    # Calculate ROUGE-L precision, recall, and F1-score
    precision = lcs / len(pred_tokens) if pred_tokens else 0
    recall = lcs / len(ref_tokens) if ref_tokens else 0
    if precision + recall == 0:
        f1_score = 0
    else:
        f1_score = (2 * precision * recall) / (precision + recall)
    
    return f1_score

# Example usage
reference_text = "The quick brown fox jumps over the lazy dog"
prediction_text = "The fast brown fox jumps over a lazy dog"
rouge_l_score = rouge_l(reference_text, prediction_text)
print("ROUGE-L Score:", rouge_l_score)
