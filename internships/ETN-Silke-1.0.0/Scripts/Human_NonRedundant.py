#Filter out the redundant interactors onlyhumancomplexes dictionary
import pickle

# Load the file containing the redundant interactors  
onlyHumanComplexes = pickle.load(open("onlyHumanComplexes_bar.pickle","rb"))
print(len(onlyHumanComplexes))

# Check each interactor id in each complex and make the list of interactors unique
for entryType in onlyHumanComplexes:
	onlyHumanComplexes[entryType] = list(set(onlyHumanComplexes[entryType]))
#print(onlyHumanComplexes)

# Write the new dictionary with non-redundant interactors to a new pickle file
with open('onlyHumanComplexes_bar_nr.pickle', 'wb') as output:
	pickle.dump(onlyHumanComplexes, output, pickle.HIGHEST_PROTOCOL)