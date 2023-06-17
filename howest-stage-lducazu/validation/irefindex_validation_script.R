#####################################################################
# iRefIndex data validation Andrei Turinsky <turinsky@wodaklab.org> Oct 13, 2017
#####################################################################
library(readr) # for read_delim()
library(dplyr) # for distinct()

# WARNING: Your path and MITAB names may differ
iref_path = "/dataext/irdata19/"
mitab_file_name = "mitab_all"
setwd(iref_path)

#####################################################################
# Load the MITAB data
iref <- read_delim( file.path(iref_path, mitab_file_name), "\t",
                    escape_double = FALSE, col_names = FALSE, trim_ws = TRUE)

mitab_header =
c("ID_Interactor_A",
           "ID_Interactor_B",
           "Alt_IDs_Interactor_A",
           "Alt_IDs_Interactor_B",
           "Aliases_Interactor_A",
           "Aliases_Interactor_B",
           "Interaction_Detection_Method",
           "Publication_1st_Author",
           "Publication_Identifiers",
           "Taxid_Interactor_A",
           "Taxid_Interactor_B",
           "Interaction_Types",
           "Source_Database",
           "Interaction_Identifiers",
           "Confidence_Values",
           "Expansion",
           "Biological_role_A",
           "Biological_role_B",
           "Experimental_role_A",
           "Experimental_role_B",
           "Interactor_type_A",
           "Interactor_type_B",
           "Xref_for_interactor_A",
           "Xref_for_interactor_B",
           "Xref_for_the_interaction",
           "Annotations_for_interactor_A",
           "Annotations_for_interactor_B",
           "Annotations_for_the_interaction",
           "NCBI_Taxonomy_identifier_for_the_host_organism",
           "Parameters_of_the_interaction",
           "Creation_date",
           "Update_date",
           "Checksum_for_interactor_A",
           "Checksum_for_interactor_B",
           "Checksum_for_interaction",
           "negative",
           "OriginalReferenceA",
           "OriginalReferenceB",
           "FinalReferenceA",
           "FinalReferenceB")

colnames(iref) = mitab_header
#####################################################################
# Extract interactors: concatenate A and B columns, remove redundancies
interactors = distinct( data.frame(
        ID = c(iref$ID_Interactor_A, iref$ID_Interactor_B),
        Alt_IDs = c(iref$Alt_IDs_Interactor_A, iref$Alt_IDs_Interactor_B),
        Aliases = c(iref$Aliases_Interactor_A, iref$Aliases_Interactor_B),
        Taxid = c(iref$Taxid_Interactor_A, iref$Taxid_Interactor_B),
        OrgReferences = c(iref$OriginalReferenceA, iref$OriginalReferenceB),
        FinReferences = c(iref$FinalReferenceA, iref$FinalReferenceB)
        ))
# remove complexes & sort by ID
interactors = interactors[!grepl("^complex", interactors$ID),]
interactors = interactors[order(interactors$ID), ]
#####################################################################
# Examine organisms
ORG_DELIM = '____'
# Extract & merge Uniprot organism suffix: e.g. "HUMAN", "DROME", "BOVIN____HUMAN____RAT"
uniprotOrgs = sapply(
    as.character(interactors$Aliases),
    function(x) {
        uniprotIDs = grep("uniprot", unlist(strsplit(x, '\\|')), val=T)
        organismSuffixList = unique(gsub("^.+_", "", uniprotIDs))
        paste(organismSuffixList, collapse = ORG_DELIM)
    } )
# Merge Uniprot organism suffix with Taxon info: e.g. "HUMAN taxid:9606(Homo sapiens)"
uniprotOrgs_taxon = paste(uniprotOrgs, interactors$Taxid)


#####################################################################
# Find strange interactors Multiple uniprot organisms
write.table(
    interactors[ grepl(ORG_DELIM, uniprotOrgs_taxon),],
    "strange_interactors.multiple_uniprot_organisms3.txt",
    sep = "\t", quote = F, row.names = FALSE)
# Wrong taxonomy number
write.table(
  interactors[grepl("\\(-\\)", uniprotOrgs_taxon),],
  "strange_interactors.wrong_taxid_number3.txt",
  sep = "\t", quote = F, row.names = FALSE)
# No taxonomy info
write.table(
    interactors[!grepl("taxid:", uniprotOrgs_taxon),],
    "strange_interactors.no_taxid3.txt",
    sep = "\t", quote = F, row.names = FALSE)
# No Uniprot aliases
write.table(
    interactors[grepl('^ taxid:', uniprotOrgs_taxon),],
    "strange_interactors.no_uniprot_alias3.txt",
    sep = "\t", quote = F, row.names = FALSE)
# No Entrez Gene
write.table(
    interactors[!grepl('entrezgene', interactors$Alt_IDs),],
    "strange_interactors.no_entrezgene3.txt",
    sep = "\t", quote = F, row.names = FALSE)
#####################################################################
# Find strange publications
authors = iref$Publication_1st_Author
pubmeds = iref$Publication_Identifiers
pubmedTable =
iref[, c('Publication_1st_Author', 'Publication_Identifiers')]

isMissingPubmed = !grepl('pubmed:', pubmedTable$Publication_Identifiers)
isMissingAuthor = (pubmedTable$Publication_1st_Author == '-')
isMissingPubmedImex = !grepl(pattern='pubmed:|imex:', pubmedTable$Publication_Identifiers)

# Missing Pubmed ID
strangeTable = pubmedTable[!isMissingAuthor & isMissingPubmed,]

write.table(
    strangeTable[order(strangeTable$Publication_1st_Author),],
    "strange_publications.no_pubmed_IDs3.txt", sep = "\t", quote = F, row.names = FALSE)
# Missing Pubmed ID
strangeTable = pubmedTable[!isMissingAuthor & isMissingPubmedImex,]

write.table(
    strangeTable[order(strangeTable$Publication_1st_Author),],
    "strange_publications.no_pubmed_IDs_Imex3.txt", sep = "\t", quote = F, row.names = FALSE)
# Missing 1st author
strangeTable = pubmedTable[isMissingAuthor & !isMissingPubmed,]
write.table(
    strangeTable[order(strangeTable$Publication_Identifiers),],
    "strange_publications.no_1st_author3.txt", sep = "\t", quote = F, row.names = FALSE)
#####################################################################
# Find strange interactions: missing Pubmed ID and 1st authors
isStrange = (iref$Publication_1st_Author == '-') & (iref$Publication_Identifiers == '-')
strangeTable = distinct(iref[isStrange, c("ID_Interactor_A",
                                          "ID_Interactor_B",
                                          "Alt_IDs_Interactor_A",
                                          "Alt_IDs_Interactor_B",
                                          "Aliases_Interactor_A",
                                          "Aliases_Interactor_B",
                                          "Interaction_Detection_Method",
                                          "Publication_1st_Author",
                                          "Publication_Identifiers",
                                          "Taxid_Interactor_A",
                                          "Taxid_Interactor_B",
                                          "Interaction_Types",
                                          "Source_Database",
                                          "Interaction_Identifiers",
                                          "Confidence_Values",
                                          "Expansion",
                                          "Biological_role_A",
                                          "Biological_role_B",
                                          "Experimental_role_A",
                                          "Experimental_role_B",
                                          "Interactor_type_A",
                                          "Interactor_type_B",
                                          "Xref_for_interactor_A",
                                          "Xref_for_interactor_B",
                                          "Xref_for_the_interaction",
                                          "Annotations_for_interactor_A",
                                          "Annotations_for_interactor_B",
                                          "Annotations_for_the_interaction",
                                          "NCBI_Taxonomy_identifier_for_the_host_organism",
                                          "Parameters_of_the_interaction",
                                          "Creation_date",
                                          "Update_date",
                                          "Checksum_for_interactor_A",
                                          "Checksum_for_interactor_B",
                                          "Checksum_for_interaction",
                                          "negative")])
write.table(
    strangeTable[order(strangeTable$Interaction_Identifiers),],
    "strange_interactions.no_publication_info3.txt", sep = "\t", quote = F, row.names = FALSE)
#####################################################################
# Additional organism check: find multiple organism-taxon pairings
clean_organisms = sort(unique(uniprotOrgs_taxon))

clean_organisms = clean_organisms[ !grepl("^ ", clean_organisms) ]
clean_organisms = clean_organisms[ !grepl(ORG_DELIM, clean_organisms) ]

for(uniOrg in sort(unique(gsub(" .+", "", clean_organisms)))) {
    if(sum(grepl(paste0('^', uniOrg, ' '), clean_organisms)) > 1) {
	        cat("WARNING: multiple organism listings for Uniprot organism tag ", uniOrg, "\n\t",
            paste0(grep(uniOrg, clean_organisms, val=T), collapse = '\n\t'), '\n', sep = '')
    }
}
#####################################################################
# Additional HUMAN check: uniprots with "_HUMAN" but non-human taxons
isMismatchedHuman =
    (grepl("^HUMAN ", uniprotOrgs_taxon)) &
    (uniprotOrgs_taxon != "HUMAN taxid:9606(Homo sapiens)")

write.table(
    interactors[isMismatchedHuman,],
    "strange_interactors.mismatched_human_taxon3.txt",
    sep = "\t", quote = F, row.names = FALSE)
# END OF SCRIPT
