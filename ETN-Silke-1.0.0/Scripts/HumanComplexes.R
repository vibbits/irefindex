#install.packages('reticulate')

library('reticulate')
py_data = py_load_object("/home/guest/VIB_Traineeship/HumanComplexes/onlyHumanComplexes.pickle")

#for (value in py_data){
#  counts <- length(value)
#  print(counts)
#}

human_counts <- list()
for (complex in names(py_data)){
  nr_interactors <- length(py_data[[complex]])
  human_counts[[complex]] <- nr_interactors
}

count_dict <- table(unlist(human_counts))
counts <- as.numeric(names(count_dict))
frequencies <- as.numeric(count_dict)

layout(matrix(c(1), 1,1, byrow = TRUE))
barplot(frequencies, names.arg=counts,
        xlim=c(0,1200), ylim=c(0,5500),
        xlab="Unique proteins per complex",
        ylab="Number of complexes",
        main="Number of complexes with its corresponding \nnumber of unique proteins")
