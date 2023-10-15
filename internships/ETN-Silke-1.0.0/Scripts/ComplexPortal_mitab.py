# This script was used to try some exraction of data before implementing these things in the real conversion script (git@github.com:vibbits/protein-complex-converter/protein_complex_converter/parser.py)
import csv
import pandas as pd
from metapub import PubMedFetcher
import re
from eutils import Client
from Bio import Entrez
import sys

eclient = Client(api_key="807e845f52fba7d9ff68c0f6a00a5daa0c09")

pubmed_ids = []

ComplexPortalfile = "9606_ComplexPortal.txt"
with open(ComplexPortalfile,'r') as ppiFile:
	csvreader = csv.reader(ppiFile, delimiter='\t')
	header = next(csvreader)
	for row in csvreader:
		# Get complex id
		complexid = row[0]

		# Get list of interactors without stoichiometry
		interactors = row[18].split('|')
		interactor_list = [interactor.split('(')[0] for interactor in interactors]
		#print(interactor_list)

		# Get pubmed ids 
		crossreferences = row[8].split('|')
		references = [ref.split('(')[0] for ref in crossreferences]
		for reference in references:
			if 'pubmed:' in reference:
				pubmed_ids.append(reference)
				pmids = [reference.split('pubmed:')[1]]
		print(pubmed_ids)
		

		# Extract the first author using BeautifulSoup
		from bs4 import BeautifulSoup
		pmid_esearch = Entrez.efetch(db='pubmed', id='16322555', retmode='xml')
		xml_data = pmid_esearch.read()
		soup = BeautifulSoup(xml_data, 'xml')

		author_list = soup.find_all('Author')
		first_author = author_list[0]
		last_name = first_author.find('LastName').text

		publication_year = soup.find('PubDate').find('Year').text

		last_name_with_year = last_name + " " + "et al." + " " + "(" + publication_year + ")"
		

'''
		authors = {}
		fetch = PubMedFetcher()
		for pmid in pmids:
			authors[pmid] = fetch.article_by_pmid(pmid).authors
		Author = pd.DataFrame(list(authors.items()), columns=['pmid','Author'])
		firstAuthor = Author['Author'].str[0]
		print(firstAuthor)

		# Get source database
		source = row[17]
		#print(source)

		# Get interaction identfier
		interactionid = row[6]

		# Get interactor types
		interactors_id = row[18].split('|')
		interactor_id_list = [interactor.split('(')[0] for interactor in interactors_id]
		#print(interactor_id_list)
		types = []
		for id in interactor_id_list:
			#print(id)
			if re.search("^CHEBI:",id):
				print("chemical entity")
				print(id)
				type = "chemical entity"
			elif re.match("^CPX-",id):
				type = "complex"
			elif re.match("^URS",id):
				type = "RNA"
			else:
				type = "UniProtKB"
			types.append(type)
		types_list = "|".join(types)
		#print(types_list)
'''		

'''
with open('ComplexPortal_mitab.csv', mode='w') as mitab_file:
	csvwriter = csv.writer(mitab_file, delimiter="\t")
	csvwriter.writerow("UidA","UidB","AltA","AltB","AliasA","AliasB")
mitab_file.close()
'''