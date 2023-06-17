
pdf("rplot19.pdf")

library(readr) # for read_delim()
library(dplyr) # for distinct()
library(ggplot2)
library(RColorBrewer)
library(doMC)
registerDoMC(cores = 2)

iref_path = "/dataext/irdata19"
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
nrow(iref)


## finding duplicate rows
mitab=as_tibble(iref[,1:14])


duplicated_rows=duplicated(mitab)
duplicated_iref=mitab[duplicated_rows,]

table_count <- table(duplicated_iref[13])


barplot_data<- data.frame(name=names(table_count),value=table_count)
ggplot(barplot_data,aes(x=name,y=value.Freq)) +
  geom_bar(stat="identity") +
  scale_fill_brewer(palette = "Set1") +
  theme(legend.position="none")+
  coord_flip()+
  ggtitle("amount of duplicated")



#!!too intensive

##all unique values of columns

unique_columns=sapply(mitab,n_distinct)

barplot_data<- data.frame(name=mitab_header[1:14],value=unique_columns)
ggplot(barplot_data,aes(x=name,y=value)) +
  geom_bar(stat="identity") +
  scale_fill_brewer(palette = "Set1") +
  theme(legend.position="none")+
  coord_flip()+
  ggtitle("amount of unique values in all columns")

## make list of columns with a low amount of unique values

table_count <- table(mitab[12])


barplot_data<- data.frame(name=names(table_count),value=table_count)
ggplot(barplot_data,aes(x=name,y=value.Freq)) +
  geom_bar(stat="identity") +
  scale_fill_brewer(palette = "Set1") +
  theme(legend.position="none")+
  coord_flip()+
  ggtitle(mitab_header[12])

table_count <- table(mitab[13])



barplot_data<- data.frame(name=names(table_count),value=table_count)
ggplot(barplot_data,aes(x=name,y=value.Freq)) +
  geom_bar(stat="identity") +
  scale_fill_brewer(palette = "Set1") +
  theme(legend.position="none")+
  coord_flip()+
  ggtitle(mitab_header[13])

dev.off()
