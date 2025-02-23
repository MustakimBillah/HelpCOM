BLEU = 2.8
METEOR = 20.4
ROUGE = 17.6
CIDERr = 8.0
sBERT = 49.8
USEnc = 39.6
SIDE = 85.0

gptEval = 0
llamaEval =0 

Syn_avg = (BLEU+ROUGE+METEOR)/3
Sem_avg = (CIDERr+SIDE+sBERT+USEnc)/4
LLM_avg = (gptEval+llamaEval)/2

OMS_ss = (0.46 * Syn_avg) + (0.54 * Sem_avg)

print("OMS_ss: ",OMS_ss)

OMS_ssl = (0.30 * Syn_avg + 0.35 * Sem_avg + 0.35 * LLM_avg)
print("OMS_ssl: ",OMS_ssl)