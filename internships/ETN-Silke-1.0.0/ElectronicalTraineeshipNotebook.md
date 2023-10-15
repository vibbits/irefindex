<!--

author:   Silke Plas
email:    silke.plas@student.howest.be
version:  24.0.0
language: en
narrator: UK English Female

logo:     https://d39j63uul3zf0p.cloudfront.net/default/0006/31/thumb_530010_default_small.png

comment:  This document is the electronic traineeship notebook of Silke Plas. It consists of all useful information on the traineeship. 

script:   https://cdn.jsdelivr.net/chartist.js/latest/chartist.min.js
          https://felixhao28.github.io/JSCPP/dist/JSCPP.es5.min.js


-->

# Electronic traineeship notebook - Silke Plas

### A description/elaboration on the tasks performed

## Week 1
#### Monday 24/04/2023
###### Exploratory research on the topic:
- Read article about the iRefIndex (Razick, S., Magklaras, G., & Donaldson, I. M. (2008). iRefIndex: A consolidated protein interaction database with provenance. BMC Bioinformatics, 9(1), 405. https://doi.org/10.1186/1471-2105-9-405)
- Read documentation on the iRefIndex (https://irefindex.vib.be/wiki/index.php/iRefIndex)
- Explore the script to be used (parseIRefIndexComplexes_copy.py) 
###### Create TDP and ETN:
- Start working on TDP and ETN in Markdown


#### Tuesday 25/04/2023
###### Exploratory research on the topic:
- Further explore the scripts to be used (parseIRefIndexComplexes_copy.py, createIdMappings_copy.py, createPPIPartnerList_copy.py)
- Read documentation on the iRefIndex (https://irefindex.vib.be/wiki/index.php/iRefIndex)
###### Determination of the number of unique human complexes in the dataset:
- Try to get the number of unique human complexes in the dataset by writing a python script (NumberUniqueComplexes.py)

#### Wednesday 26/04/2023
###### Exploration of the dataset
- Install a software to visualize and analyse large datasets (TIBCO Spotfire)
- Explore the dataset
###### Determination of the number of unique human complexes in the dataset:
- Try to figure out why the number of unique complexes in human is so high 
- Try to solve the problem of the high number of unique complexes by grouping the complexes (test-pandas.py)
- Investigate a specific complex into more detail to find the link between ints subunits (Complexes_CommonInteractors.py)

#### Thursday 27/04/2023
###### Determination of the number of unique human complexes in the dataset:
- Proceed to try to solve the problem of the high number of unique complexes by filtering the complexes (FilterHuman.py)
- Make a dictionary with the complex ids as key and interactor ids as values (FilterHuman.py)
- Use these dictionaries to check the interactors and validate them via UniProt (onlyHumanComplexes.py)
###### Get to know the iRefIndex better:
- Look up some more information on the iRefIndex (https://irefindex.vib.be/wiki/index.php/iRefIndex)

#### Friday 28/04/2023
###### Exploration of the Complex Portal
- Follow a online tutorial concerning a quick tour in the Complex Portal (https://www.ebi.ac.uk/training/online/courses/complex-portal-quick-tour/)
- Look at a webinar about the Complex Portal (https://www.ebi.ac.uk/training/events/introduction-complex-portal/)
###### Visualize the number of unique proteins per complex:
- Make sure to only work with the non-redundant list of subunits in each complex (Human_NonRedundant.py)
- Make a plot visualizing the data in both Python and R (HumanComplexes.R, onlyHumanComplexes.py)

## Week 2
#### Monday 01/05/2023
Labour day

#### Tuesday 02/05/2023
###### Interpretation of the plot and the generated data:
- Check what the members of some complexes are to see if the high numbers could be correct (onlyHumanComplexes.py)
- Investigate a specific complex into more detail to find the link between ints subunits (complex:0+DjbQLowUB3/m529HKD7tkG29I with subunits P13612, Q99965, P05556-2)
###### Visualize the number of unique proteins per complex per source:
- Make plots to visualize the number of unique proteins per complex for each source seperately to check where the high numbers come from. (FilterHuman.py, Human_NonRedundant.py, onlyHumanComplexes.py)

#### Wednesday 03/05/2023
###### Visualize the number of unique proteins per complex per source:
- Make plots to visualize the number of unique proteins per complex for each source seperately to check where the high numbers come from. (FilterHuman.py, Human_NonRedundant.py, onlyHumanComplexes.py)
- Interpret the results of these plots
###### Check the origin of intact, imex and complex portal data:
- Look at documentation of these databases, because they have a very high number of complexes with 3 subunits (https://www.ebi.ac.uk/intact/about#overview, http://www.imexconsortium.org/about/, https://www.ebi.ac.uk/complexportal/about)
###### Check the human complex portal dataset into more detail:
- Download the tsv file and compare some content to the data of iRefIndex to get a general idea of similarities between both. (http://ftp.ebi.ac.uk/pub/databases/intact/complex/current/complextab/9606.tsv)

#### Thursday 04/05/2023
###### Look at data and documentation of Innatedb in detail:
- Try to find out why complexes with only 2 subunits are incorporated in iRefIndex (http://innatedb.ca/redirect.do?go=aboutIDB)
- Investigate the data to search for the distinction between complexes and binary interactions (https://storage.googleapis.com/vib-training-data/INNATEDB/innatedb_psicquic.txt, https://irefindex.vib.be/psicquic/webservices/current/search/query/source:psi-mi:%22MI:0974%22(innatedb))
###### Perform a gene ontology enrichment of the data for each source separately
- Find more information on how to perform this in Python (Klopfenstein, D.V., Zhang, L., Pedersen, B.S. et al. GOATOOLS: A Python library for Gene Ontology analyses. Sci Rep 8, 10872 (2018). https://doi.org/10.1038/s41598-018-28948-z, https://github.com/tanghaibao/goatools/blob/main/README.md)
- Start trying some things in a script (GO_Enrichment_Analysis.py)

##### Friday 05/05/2023
###### Perform a gene ontology enrichment of the data for each source separately:
- Keep on working on the script (GO_Enrichment_Analysis.py)
###### Community meeting with technologies core:
- Discuss what everyone is working on.

## Week 3
#### Monday 08/05/2023
###### Perform a gene ontology enrichment of the data for each source separately:
- Make a script to convert UniProt IDs into Gene IDs (UniProtID2GeneID.py)
- Keep on working on the script (GO_Enrichment_Analysis.py)

#### Tuesday 09/05/2023
###### Perform a gene ontology enrichment of the data for each source separately:
- Finish the script to perform GOEA (GO_Enrichment_Analysis.py)
###### Further process these GOEA results:
- Extract the biological processes from the GOEA results (GOEA_BiologicalProcesses.py)
- Convert ratios to percentages and sort by these percentages in descending order (GOEA_BiologicalProcesses_sorted.py)

#### Wednesday 10/05/2023
###### Apply the GOEA to the last sources:
- Apply GOEA_BiologicalProcesses.py and GOEA_BiologicalProcesses_sorted.py to the last sources, except two with too many items, they still need to be split up first.
###### Work on the documentation for the traineeship:
- Summarize everything that has been done so far and describe some results.
Visualize top 10 biological processes in cytoscape:
- Check the sorted BPs in the excel file generated with GOEA_BiologicalProcesses_sorted.py and filter on these GO_term ids in Cytoscape. 

#### Thursday 11/05/2023
###### Finish GOEA:
- Execute the conversion of UniProt id to Gene id on multiple subsets of genes, because in total there were too many items for 'imex' and 'intact' (UniProtID2GeneID.py)
- Concatenate the pickle files of the conversions (ConcatenatePickle.py)
- Perform the GOEA with GO_Enrichment_Analysis.py, GOEA_BiologicalProcesses.py and GOEA_BiologicalProcesses_sorted.py
###### Visualize top 10 biological processes in CytoScape:
- Check the sorted BPs in the excel file generated with GOEA_BiologicalProcesses_sorted.py and filter on these GO_term ids in Cytoscape.
###### Keep looking for a reason why innatedb has complexes with 2 subunits included in iRefIndex:
- Investigate the data to search for the distinction between complexes and binary interactions (https://storage.googleapis.com/vib-training-data/INNATEDB/innatedb_psicquic.txt, https://irefindex.vib.be/psicquic/webservices/current/search/query/source:psi-mi:%22MI:0974%22(innatedb))

#### Friday 12/05/2023
###### Visualize the GO-terms for each source in one network:
- Combine all the networks to get a clear overview of all GO-terms and all sources
- Adjust the styles for the representation of different variables
###### Review scripts made so far:
- Check the clarity and add comments where necessary
- Check for redundancy

## Week 4
#### Monday 15/05/2023
###### Review scripts made so far:
- Check the clarity and add comments where necessary
- Check for redundancy
###### Convert Complex Portal human data into MITAB2.6/MITAB2.7 format:
- Review tsv file Complex Portal and general content of MITAB2.6 to see which information is present and which information is needed. (https://psicquic.github.io/MITAB26Format.html,https://psicquic.github.io/MITAB27Format.html)
- Think about how I would do the transformation with the information that I have in the tsv file. 

#### Tuesday 16/05/2023
###### Visualize top 10 and top 5 GO-terms over all sources:
- Filter on each GO-term in the combined network with all sources to get the number of occurences
- Make a new network with only the top 10 GO-terms over all sources
- Make a new network with only the top 5 GO-terms over all sources
###### Convert Complex Portal human data into MITAB2.6/MITAB2.7 format:
- Extract necessary data from the file of Complex Portal (ComplexPortal_mitab.py) that will be used in the conversion

#### Wednesday 17/05/203
###### Convert Complex Portal human data into MITAB2.6/MITAB2.7 format:
- Investigation of the Complex Portal data to think about which data should be used and how it should be used
###### Investigate Innatedb data in detail and compare to iRefIndex data:
- Still look for a reason why complexes with 2 unique interactors are captured in iRefIndex
###### Summarize results of the visualization in Cytoscape:
- Make a summary table of the results from the top 10 visualization

#### Thursday 18/05/2023
Ascension day

#### Friday 19/05/2023
###### Learn how to work with Inkscape:
- Follow a training about Inkscape, organized by a collegue
###### Convert Complex Portal human data into MITAB2.6/MITAB2.7 format:
- Think about which data should be used and to which column it belongs

## Week 5
#### Monday 22/05/2023
###### Work on documentation for the traineeship:
- Review the roadmap for the traineeship and the documentation I have so far.
###### Intermediate evaluation traineeship:
- Meeting with internal and external supervisors about how I'm doing on the traineeship. 
###### Convert Complex Portal human data into MITAB2.6/MITAB2.7 format:
- Meeting with a co-worker from the technologies core who is very experienced in Python coding to get me started on the coding for this conversion. (parser.py, test_parsing.py)

#### Tuesday 23/05/2023
###### Convert Complex Portal human data into MITAB2.7 format:
- Continue working on script for the conversion (parser.py, test_parsing.py). Add the part to extract the pubmed identifiers and based on these pubmed identifiers get the first author and year of publication for each publication. Use parts of the ComplexPortal_mitab.py script that was made as a preparation.

#### Wednesday 24/05/2023
###### Convert Complex Portal human data into MITAB2.7 format:
- Continue working on script for the conversion (parser.py, test_parsing.py). 
- Get the sourcedb from the Complex Portal file.
- Try some things in a test script to check the output before adding it to the parser.py script (test_output.py). 
###### Reflect on the intermediate evaluation of the traineeship:
- Compare the results that I predicted to those of the evaluation by the supervisors and draw an intermediate conclusion.

#### Thursday 25/05/2023
###### Convert Complex Portal human data into MITAB2.7 format:
- Continue working on script for the conversion (parser.py, test_parsing.py). 
- Add new function to extract interactionIdentifiers
- Add new function to extract interactor_type_B
- Extract Host_organism_taxid, xrefs_Interaction, method, taxa, taxb, interactionType, expansion, biological_role_A, biological_role_B, experimental_role_A, experimental_role_B, interactor_type_A

#### Friday 26/05/2023
###### Convert Complex Portal human data into MITAB2.7 format:
- Continue working on script for the conversion (parser.py, test_parsing.py).
- Add new function to get the current date
- Add new function to extract the stoichiometry
- Extract xrefs_A,xrefs_B,Annotations_A,Annotations_B,Annotations_Interaction,parameters_Interaction,Creation_date,Update_date,Checksum_A,Checksum_B,Checksum_Interaction,Negative,Features_A,Features_B,Stoichiometry_A,Stoichiometry_B,Identification_method_A,Identification_method_B,altA,altB,aliasA,aliasB

## Week 6
#### Monday 29/05/2023
Whit monday

#### Tuesday 30/05/2023
###### Convert Complex Portal human data into MITAB2.7 format:
- Continue working on script for the conversion (parser.py, test_parsing.py).
- Modify the functions get_pubmedArticles() and extract_first_author() to get the pubmed xml for all pubmed ids at once, instead of looping over them one by one. Then use this pubmed xml to get the first author of every article. 
- Add new functions to get the taxonomy xml for all the taxids in the dataset and then use this xml to get the scientific names of the corresponding taxids.
###### Make a histogram to visualize the number of unique complexes for each organism in iRefIndex:
- Download the iRefIndex dataset of all organisms: wget https://storage.googleapis.com/irefindex-data/archive/release_19.0/psi_mitab/MITAB2.6/All.mitab.08-22-2022.txt 
- Start the script to make the visualization. Load in the data. (All-organisms.py)

#### Wednesday 31/05/2023
###### Convert Complex Portal human data into MITAB2.7 format:
- Test the script on the whole human dataset of Complex Portal (parser.py, test_parsing.py)
###### Make a histogram to visualize the number of unique complexes for each organism in iRefIndex:
- Continue working on the script (All-organisms.py). Add part to iterate over each row and filter out the data that is needed. Also add part to plot the data
- Add filter with pandas library to seperate the complexes with mixed organisms from the other data to plot this as a seperate bar. 

#### Thursday 01/06/2023
###### Make a histogram to visualize the number of unique complexes for each organism in iRefIndex, debug code for large input file:
- Continue working on the script (All-organisms.py). When executing it with large files (GB) Visual Studio Code crashes. Debug this.
- Get Visual Studio Code up and running on Windows to continue here with the script instead of Linux (with the idea of a memory problem in mind). Configure the Git repository with the script I'm working on. 

#### Friday 02/06/2023
###### Make a heatmap to visualize the number of complexes per source and per organism in iRefIndex:
- Add this part to the script All-organisms.py 
###### Look at the overlap of complexes in different sources:
- Make a script that counts the number of overlapping complexes between all the sources pairwise (Overlap_sources.py)
###### Discuss the plan for the coming two weeks:
- What has been done so far? What still needs to be done?

## Week 7
#### Monday 05/06/2023
###### Generate a matrix to summarize the overlap between sources and the number of complexes exclusively to each source (Overlap_sources_matrix.csv):
- Convert the pairwise comparison between to sources into a matrix, only show the upper triangle of the matrix to avoid redundant information (Overlap_sources.py)
- Calculate the number of complexes exclusively for each source and add this to the matrix as a last line (Overlap_sources.py)
- Get this script up and running for the human data so that it can also be applied to the other organisms (Overlap_sources.py)

#### Tuesday 06/06/2023
###### Generate a matrix to summarize the overlap between sources and the number of complexes exclusively to each source (Overlap_sources.py and Overlap_sources_Y.py):
- Do this for top 9 organisms (mixed_species excluded from top 10) with edgetype C
- Do this for top 10 organisms with edgetype Y
###### Make a histogram to visualize the number of unique complexes (now specifically multimers) for each organism in iRefIndex (All-organisms_Y.py):
- Only show the top 10 organisms to keep the graph clear
###### Make a heatmap to visualize the number of complexes (specifically multimers) per source and per organism in iRefIndex (All-organisms_Y.py)

#### Wednesday 07/06/2023
###### Make a pie chart to visualize the most occuring GO-terms in corum:
- Compare the top GO-terms of corum to those of Complex Portal to get an idea of how detailed the terms should be in the chart
- Add a column to add the ratio_pop as percentage in the GOEA result (GOEA_BiologicalProcesses_sorted.py)
- Use the visualization done earlier in Cytoscape to select the top GO-terms that will be in the pie chart
- Write a script to perform this plotting (Plotting_GOterms.py)
###### Perform some tasks on the generated overlap matrices (Overlap_sources.py):
- Exclude certain sources to look at the effect
- Get the complex_ids of the complexes unique for each source and write these to a new file

#### Tuesday 08/06/2023
###### Make histograms of the interaction types and detection methods for intact and corum and their overlap:
- Write a script to extract the complex ids that are exclusively in both sources and make a histogram representing the occurences of the methods and types to compare them (Interaction_Method.py and Interaction_Type.py). 
###### Discuss the progress of this week with my supervisor:
- Talk about my results of the histograms, matrices and pie chart

#### Friday 09/06/2023
###### Perform a Gene Ontology Enrichment Analysis on all human complexes:
- Go through the whole pipeline of the GOEA: FilterHuman.py, UniProtID2GeneID.py, ConcatenatePickle.py, GO_Enrichment_Analysis.py, GOEA_BiologicalProcesses.py and GOEA_BiologicalProcesses_sorted.py
- Take all human genes and use BiNGO in Cytoscape to perform a GOEA
- Select the top10 GO-terms from the result of GOEA_BiologicalProcesses_sorted.py and filter them out in the Cytoscape network.
- Select which terms to use for the visualization in the pie chart
###### Make a pie chart to visualize the most occuring GO-terms over all sources (Plotting_GOterms.py)
###### Write a first version of the abstract

## Week 8
#### Monday 12/06/2023
###### Make histograms of the interaction types and detection methods for overlapping complex ids in intact and corum:
- Write a script to extract the complex ids that are overlapping in both sources and make a histogram representing the occurences of the methods and types to compare them (Interaction_Method_Overlap.py and Interaction_Type_Overlap.py).
###### Work on the documentation for the traineeship
###### Work on the abstract

#### Tuesday 13/06/2023
###### Install LiaScript-Exporter to be able to convert Markdown into PDF:
- Installation based on https://github.com/LiaScript/LiaScript-Exporter 
###### Work on the abstract
###### Work on the presentation
###### Review scripts made so far:
- Check the clarity and add comments where necessary
- Check for redundancy

#### Wednesday 14/06/2023
###### Review scripts made so far:
- Check the clarity and add comments where necessary
- Check for redundancy
###### Finish the abstract
###### Work on the presentation

#### Thursday 15/06/2023
###### Work on the presentation

#### Friday 16/06/2023
###### Give a test presentation at the traineeship
<div style="page-break-after: always;"></div>

### Research, comparisons and background information on the traineeship topic
- https://irefindex.vib.be/ 
- https://www.ebi.ac.uk/training/search-results?query=complex%20portal&domain=ebiweb_training&page=1&facets= 
- https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-9-405 
- https://academic.oup.com/nar/article/50/D1/D578/6414048 
<div style="page-break-after: always;"></div>

### Problems and solutions
1. 
	- Problem: VisualStudio Code -> when adding a new line to an indentation, instead of inserting a tab it inserted spaces. Because of this I got the following error: 'TabError: inconsistent use of tabs and spaces in indentation' so the script didn't work. 
	- Solution: in settings, disable 'Editor: Insert Spaces'.
2. 
	- Problem: to be able to use pickle in a conda environment, I cannot just use pickle, but need to install pickle5
	- Solution: conda install -c conda-forge pickle5
2. 
	- Problem: for the GOEA a, ftp from NCBI is needed to download the gene2go file, but the VIB does not allow these ftp processes.
	- Solution: download the file manually using the url
3. 
	- Problem: for the Gene Ontology Enrichment Analysis, gene IDs are needed. Now I only have UniProt IDs.
	- Solution: convert them using a script (UniProtID2GeneID.py)
4. 
	- Problem: the original file is too large to test things on. The scripts take too long to run.
	- Solution: make a smaller file of this data using the 'head' command to test scripts.
5. 
	- Problem: the script (All-organisms.py) cannot be run on the whole dataset (All.mitab.08-22-2022.txt), because some characters could not be interpreted. 
	- Solution: add 'encoding="utf8"' to 'with open(irefIndexFile, 'r') as ppiFile:' --> 'with open(irefIndexFile, 'r',encoding="utf-8") as ppiFile:'
6. 
	- Problem: to convert the markdown ETN into a PDF, a tool needs to be installed.
	- Solution: install LiaScript-Exporter (https://github.com/LiaScript/LiaScript-Exporter)
<div style="page-break-after: always;"></div>

### Location of scripts and datasets
Git repository silkeplas/ETN-Silke (git@github.com:silkeplas/ETN-Silke.git)
Dataset iRefIndex: from 'https://irefindex.vib.be/wiki/index.php/iRefIndex', more specifically https://storage.googleapis.com/irefindex-data/archive/release_19.0/psi_mitab/MITAB2.6/9606.mitab.08-22-2022.txt for human data and https://storage.googleapis.com/irefindex-data/archive/release_19.0/psi_mitab/MITAB2.6/All.mitab.08-22-2022.txt for the data of all organisms
Complex Portal data: from http://ftp.ebi.ac.uk/pub/databases/intact/complex/current/complextab/9606.tsv
For the project of converting Complex Portal data into MITAB2.7 format a seperate repository is used: vibbits/protein-complex-converter (git@github.com:vibbits/protein-complex-converter.git)
<div style="page-break-after: always;"></div>

# Traineeship documentation plan

### Tentative planning 

- Extract list of complexes – list of subunits of complexes
- Determine overlap with dataset from complexPortal (e.g. via upset plots)
- Look at distrubutions per relevant species (reference are Complex portal’s major reference proteomes)
- Investigate the alternative irefindex parser psi2.5 using dataset from complexPortal (as to integrate in irefindex pipeline)
- Compare to huMap (bespoke parser)
- benchmark with the above – Corum/ComplexPortal/HuMap/iRefindex/ Tabloid proteome
There is no specific deadline for each task seperately, but they will be executed consecutively during the traineeship.

### Data management

- Findable: the data that will be used will come from the iRefIndex database. This can be found on 'https://irefindex.vib.be/wiki/index.php/iRefIndex'.
Each interactor in the database has a unique identifier and has metadata available like taxonomy identifiers for interactors, interaction types, source of the interaction. 
In the dataset, a key is generated for each protein interaction record and a key for each participant protein is generated as well. 
Next to the iRefIndex data, also Complex Portal data will be used which can be found on 'https://www.ebi.ac.uk/complexportal/download'. In this dataset, more specifically the  ComplexTab format, each complex has a complex identifier and has metadata available like interactor identifiers, GO Annotations, source of the interaction. 

- Accessible: the iRefIndex database can be accessed via the following link: 'https://irefindex.vib.be/wiki/index.php/iRefIndex'. This is open and free. Version 19.0 of iRefIndex in PSI-MITAB tab-delimited format is used: 'https://storage.googleapis.com/irefindex-data/archive/release_19.0/psi_mitab/MITAB2.6/irefindex-19.listing.txt' and more specifically the human MITAB taxon id:9606 is the downloaded dataset: 'https://storage.googleapis.com/irefindex-data/archive/release_19.0/psi_mitab/MITAB2.6/9606.mitab.08-22-2022.txt'. Also the dataset consisting of all organisms in iRefIndex is used, which was downloaded from: https://storage.googleapis.com/irefindex-data/archive/release_19.0/psi_mitab/MITAB2.6/All.mitab.08-22-2022.txt.
The human data that is used from Complex Portal is the ComplexTab format that can be accessed via: 'http://ftp.ebi.ac.uk/pub/databases/intact/complex/current/complextab/9606.tsv'. This is also open and free. 

- Interoperable: the iRefIndex data is available in PSI-MITAB 2.6 tab-delimited format. The Complex Portal data is available in multiple formats: PSI-MI XML, MI-JSON and ComplexTab format. 

- Reusable: the iRefIndex data could be replicated using the method described in the article with DOI:10.1186/1471-2105-9-405. How the curation of the Complex Portal data happens, is described in this document: https://raw.githubusercontent.com/Complex-Portal/complex-portal-documentation/master/assets/Manual_Complexes_curation.pdf.


### Traceability of steps and methods

To document the project steps and progression in a traceable manner, Markdown pages on Git will be used. (repositories: git@github.com:silkeplas/ETN-Silke.git and git@github.com/vibbits/protein-complex-converter.git)

### Version control of code

The Git repositories that will be used to store the code are called 'ETN-Silke' and 'protein-complex-converter'. This last one is only used for the project in which the Complex Portal data is converted from ComplexTab into MITAB2.7 
These repositories will be made available for the internal and external supervisors by adding them to the repositories.  
<div style="page-break-after: always;"></div>

# Personal development

### Development goal

Try to improve my Python coding skills in the conversion of one tabular format into another tabular format.

### Development activity

I'll be working with different tabular formats in Python during the whole traineeship. At a certain moment a dataset should be converted from one tabular format to another so I should do some more research on the internet on how to do this. Besides that I will meet someone from the technologies core who is very experienced with Python programming to help me with this conversion. 

### Desired results

At the end of the traineeship I would like to be able to write a Python script to convert one tabular format into another one. Based on a given dataset or other type of input in a certain tabular format I want to be able to get an idea of how I can process the data in a clear way to another tabular format.

### Schedule

I'll be working on the goal during the entire traineeship as I'll have to convert data from one tabular format to another tabular format using a Python script.

### Necessary support and facilities

In order to obtain my goal, I'll need my traineeship working hours and possibly also external working hours to review what I'm working on.
It would definitely also be interesting to gather information from videos or other sources.

### SMART-principle
**S**pecific: Python coding one tabular format into another tabular format 
**M**easurable: at the end of the traineeship I should be able to convert data from one tabular format into another tabular format using Python. 
**A**chievable: as such a conversion needs to be performed in Python during the traineeship, I should be able to achieve this skill.
**R**elevant: in the context of the traineeship, this learning outcome is a relevant one. 
**T**ime-bound: the objective should be met by the end of the traineeship.
<div style="page-break-after: always;"></div>

# Intermediate evaluation traineeship

### Feedback on the tasks provided by the traineeship supervisors
- Everyday I am able to perform some things which get me step by step closer to an intermediate solution. 
- Unless some unexpected difficulties that I've come across until now, I'm still on track to get everything done that was stated in the beginning.
- So far, the skills that I've shown are good. 
- I should suggest some ideas of my own more often.
- I can work quite independently without asking a lot of help. 

### Intermediate evaluation form
In general I could say that the intermediate evaluation was better than expected. Comparing the evaluation by the supervisors with the evaluation that I predicted for myself, I seem to have underestimated myself. 
For example the usage and learning of new techniques and programming is going better than expected. I did not have the idea that it was going so well, because it took a lot of time to get the right information about something new and to actually apply it. 
Also the combination of different skills and various knowledge is better than I expected. 
Something that was predicted quite good by myself is the organization of the code and the documentation of everything. 
Besides these evaluation, not everything could be evaluated yet, because it was still too early to do so.
After this intermediate evaluation I think I can say that I'm already happy with the progress that I've made so far. I'll definitely try to keep working like this and keep improving my skills.
<div style="page-break-after: always;"></div>

# Self assessment at the end of the traineeship
The self assessment at the end of the traineeship was filled in an uploaded seperately in the 'Electronic traineeship notebook' folder on OneDrive. 
<div style="page-break-after: always;"></div>

# Reflection on international/intercultural aspects
In the workplace company the collegues are both national and international so the communication happens in Dutch and English. To make sure that everyone can understand the communication, emails and chats are in English. Research, literature, reports, trainings are also in English.
