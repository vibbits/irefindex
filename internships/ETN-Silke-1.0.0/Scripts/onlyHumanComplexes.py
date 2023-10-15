# Filter out complexes with 1,2,3 unique proteins per complex and make graphs.
import pickle
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
import collections

# Define the necessary variables
human_counts = {}
complex_one_interactor = []
complex_two_interactors = []
complex_three_interactors = []

# Load the file to use 
path = '/home/guest/VIB_Traineeship/HumanComplexes/onlyHumanComplexes_innatedb_nr.pickle'

onlyHumanComplexes = pickle.load(open(path,"rb"))
print(len(onlyHumanComplexes))

# Filter out complexes with 1, 2 or 3 interactors
counter = 0
for complex,ids in onlyHumanComplexes.items():
	nr_interactors = len(ids)
	#print(nr_interactors)
	human_counts[complex] = nr_interactors
	#print(human_counts)
	counter += 1
	if counter == 2:
		print("Complex id:{},\nInteractors:{}".format(complex, ids))
	if nr_interactors == 1:
		print("Complex id:{},\nInteractors:{}".format(complex, ids))
		complex_one_interactor.append(complex)
	elif nr_interactors == 2:
		complex_two_interactors.append(complex)
	elif nr_interactors == 3:
		complex_three_interactors.append(complex)
#print(len(complex_one_interactor))

#print("One interactor",complex_one_interactor)
print("Two interactors:", complex_two_interactors)
#print("Three interactors:",complex_three_interactors)
print(len(complex_two_interactors))


# Count the number of unique proteins per complex and the number of complexes with an equal number of interactors
count_dict = collections.Counter(human_counts.values())
#print(count_dict)
	
counts = []
frequencies = []
for key,value in count_dict.items():
	counts.append(key)
	frequencies.append(value)

# Plot this data
fig,ax = plt.subplots()
ax.bar(counts, frequencies)
ax.set(xlim=(0,50), ylim=(0,1000), xlabel="Unique proteins per complex", ylabel="Number of complexes",
title="Number of complexes with its corresponding \nnumber of unique proteins - bar")
plt.show()


