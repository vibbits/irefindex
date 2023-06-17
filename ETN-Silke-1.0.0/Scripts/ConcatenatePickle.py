# Concatenate the files into one pickle file
import pickle5 as pickle

# Read in all the pickle files to use
with open('UniProtKB2GeneID_imex1.pickle','rb') as f1:
    result1 = pickle.load(f1)
with open('UniProtKB2GeneID_imex2.pickle','rb') as f2:
    result2 = pickle.load(f2)
with open('UniProtKB2GeneID_imex3.pickle','rb') as f3:
    result3 = pickle.load(f3)

# Combine the results in one dictionary and write it to a new pickle file
all_results = {}

all_results.update(result1)
all_results.update(result2)
all_results.update(result3)

with open('UniProtKB2GeneID_imex_no-isoforms.pickle', 'wb') as output:
	pickle.dump(all_results, output, pickle.HIGHEST_PROTOCOL)