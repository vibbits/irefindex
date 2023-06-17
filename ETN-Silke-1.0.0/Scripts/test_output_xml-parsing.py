# utility functions for pubmed xml parsing
import requests as req
import xml.etree.ElementTree as et
from bs4 import BeautifulSoup
import csv,re

'''
pubmed_base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&rettype=abstract"
batchsize = 500

def get_pubmedArticles(pubmed_ids):
    response = req.get(pubmed_base_url+'&id='+str(pubmed_ids))
    xml = response.text
    #print(xml)
    pubmedArticleSet = et.fromstring(xml)
    return xml

#output = get_pubmedArticles(23661758)
#print(output)
xml_data = get_pubmedArticles(pubmed_ids)

soup = BeautifulSoup(output, 'xml')
author_list = soup.find_all('Author')
first_author = author_list[0]
last_name = first_author.find('LastName').text
publication_year = soup.find('PubDate').find('Year').text
last_name_with_year = last_name + " " + "et al. " + "(" + publication_year + ")"
print(last_name)
print(publication_year)
print(last_name_with_year)
'''


ComplexPortalfile = "9606_ComplexPortal_10lines.txt"
with open(ComplexPortalfile,'r') as ppiFile:
	csvreader = csv.reader(ppiFile, delimiter='\t')
	header = next(csvreader)
	for row in csvreader:
		interactor_list_stoichiometry = row[4].split('|')
		interactor_list = [interactor.split('(')[0] for interactor in interactor_list_stoichiometry]
		print(interactor_list)
		types_b = []
		for interactor in interactor_list:
			#print(interactor)
			if re.search("^CHEBI",interactor):
				#print("chemical entity:",interactor)
				types_b.append('psi-mi:"MI:0328"(small molecule)')
			elif re.search("^URS",interactor):
				#print("RNA:",interactor)
				types_b.append('psi-mi:"MI:0320"(RNA)')
			elif re.search("^CPX",interactor):
				#print("protein complex:",interactor)
				types_b.append('psi-mi:"MI:0315"(protein complex)')
			else:
				#print("protein:",interactor)
				types_b.append('psi-mi:"MI:0326"(protein)')
		print(types_b)

		# Get interactionIdentifier
		part1 = row[6] 
		part2 = list(row[8].split('|'))
		interaction_identifier = []
		if part1 != '-':
			interaction_identifier.append(part1)
		for ref in part2:
			ref = ref.split('(')[0]
			#print(ref)
			if not ref.startswith('pubmed'):
				interaction_identifier.append(ref)
		print(interaction_identifier)
		#print(part1)
		#print(part2)
