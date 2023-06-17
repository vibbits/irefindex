# 15 Nov 2021. Parse the UniProt ID mapping data file and create a dictionary of RefSeq protein ids mapped to their corresponding UniProt ids.
# 14 Dec 2021. Updated to convert all UniProt ID isoforms to wt (i.e., '-n' info is now removed).
# 15 Dec 2021. Updated to add a UniProt ID to ENSG and ENST (Ensemble gene/transcript) ID conversion (mapping) dictionary.
# Mainak Guharoy. VIB Bioinformatics Core.

import csv,sys,pickle

# The id mapping file was downloaded from https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/idmapping/by_organism/
idMappingFile = "HUMAN_9606_idmapping.dat"

RefSeq2UniProtDict = {}
UniProt2ENSGDict = {}
UniProt2ENSTDict = {}

if __name__ == "__main__":

	# Open and parse the ID mapping file.
	with open(idMappingFile, 'r') as idsFile:
		csvreader = csv.reader(idsFile, delimiter='\t')
		for row in csvreader:
			uniprot_id = row[0]
			mappedDB = row[1]
			mappedDB_id = row[2]

			# For now treat all isoforms as wild type, i.e., remove "-n" at the end of the UniProt id, if present.
			if len(uniprot_id) > 6 and uniprot_id[6] == "-":
				uniprot_id = uniprot_id[:6]

			if mappedDB in ["RefSeq"]:
				RefSeq_id = mappedDB_id
				#RefSeq2UniProtDict[RefSeq_id] = UniProt_id # May not be a unique correspondence?
				if RefSeq_id not in RefSeq2UniProtDict:
					RefSeq2UniProtDict[RefSeq_id] = [uniprot_id]
				else:
					RefSeq2UniProtDict[RefSeq_id].append(uniprot_id)

			elif mappedDB in ["Ensembl"]:
				Ens_Gene_id = mappedDB_id

				if uniprot_id not in UniProt2ENSGDict:
					UniProt2ENSGDict[uniprot_id] = [Ens_Gene_id]
				else:
					UniProt2ENSGDict[uniprot_id].append(Ens_Gene_id)

			elif mappedDB in ["Ensembl_TRS"]:
				Ens_Transcript_id = mappedDB_id

				if uniprot_id not in UniProt2ENSTDict:
					UniProt2ENSTDict[uniprot_id] = [Ens_Transcript_id]
				else:
					UniProt2ENSTDict[uniprot_id].append(Ens_Transcript_id)

	print("Number of RefSeq protein IDs mapped to UniProt IDs:",len(RefSeq2UniProtDict))
	print("Number of UniProt IDs mapped to Ensembl genes:",len(UniProt2ENSGDict))
	print("Number of UniProt IDs mapped to Ensembl transcripts:",len(UniProt2ENSTDict))
	#print(UniProt2ENSTDict)

	# Save dictionary containing the mapped id info as pickle objects.
	with open("RefSeq2UniProtIDs.pickle","wb") as output1:
		pickle.dump(RefSeq2UniProtDict,output1,pickle.HIGHEST_PROTOCOL)

	with open("UniProt2EnsemblGeneIDs.pickle","wb") as output2:
		pickle.dump(UniProt2ENSGDict,output2,pickle.HIGHEST_PROTOCOL)

	with open("UniProt2EnsemblTranscriptIDs.pickle","wb") as output3:
		pickle.dump(UniProt2ENSTDict,output3,pickle.HIGHEST_PROTOCOL)
