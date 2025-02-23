from pymongo import MongoClient
from scipy.stats import mannwhitneyu

client = MongoClient('mongodb://localhost:27017/')
db = client.code_understanding      


sampleDep = db.depSample.find()
sampleIndep = db.indepSample.find()


indepSideCbert = []
indepSideCodeT5p = []
depSideCbert = []
depSideCodeT5p = []

for item in sampleIndep:
    sideCbert = item.get('sideCodeBert')
    sideCodeT5p = item.get('sideCodeT5p')

    indepSideCbert.append(sideCbert)
    indepSideCodeT5p.append(sideCodeT5p)

for item in sampleDep:
    sideCbert = item.get('sideCodeBert')
    sideCodeT5p = item.get('sideCodeT5p')

    depSideCbert.append(sideCbert)
    depSideCodeT5p.append(sideCodeT5p)

stat, p_value = mannwhitneyu(indepSideCbert, depSideCbert, alternative='two-sided')

# Output the results
print("Mann-Whitney U Test Statistic:", stat)
print("p-value:", p_value)

# Interpretation
alpha = 0.05  # Significance level
if p_value < alpha:
    print("There is a statistically significant difference")
else:
    print("There is no statistically significant difference")


stat, p_value = mannwhitneyu(indepSideCodeT5p, depSideCodeT5p, alternative='two-sided')

# Output the results
print("Mann-Whitney U Test Statistic:", stat)
print("p-value:", p_value)

# Interpretation
alpha = 0.05  # Significance level
if p_value < alpha:
    print("There is a statistically significant difference")
else:
    print("There is no statistically significant difference")
                







