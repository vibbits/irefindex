# general quoting of taxid needed instead of two steps
perl -pi.bak -e 's/(taxid:[^\t"]+?\()([^\t"]+?[^\)])(\))(?=\t)/$1"$2"$3/g;' All.mitab.08-22-2022.txt
perl -pi.bak -e 's/(taxid:[^\t]+?\()([^\t]+?[^\)]\){1})(\){1})(?=\t)/$1"$2"$3/g;' All.mitab.08-22-2022.txt
perl -pi.bak -e 's/(taxid:[^\t]+?\()([^\t]+?[^\)]\){1}\){1})(\){1})(?=\t)/$1"$2"$3/g;' All.mitab.08-22-2022.txt
# correct method description
perl -pi.bak -e 's/psi-mi:MI:1112(-)/psi-mi:"MI-1112"(two hybrid prey pooling approach)/g' All.mitab.08-22-2022.txt
perl -pi.bak -e 's/psi-mi:MI:0397(-)/psi-mi:"MI-0397"(two hybrid assay)/g' All.mitab.08-22-2022.txt
perl -pi.bak -e 's/psi-mi:MI:1356(-)/psi-mi:"MI-1356"(validated two hybrid)/g' All.mitab.08-22-2022.txt
perl -pi.bak -e 's/psi-mi:"MI:0809,"(-)/psi-mi:"MI-0809"(bimolecular fluorescence complementation)/g' All.mitab.08-22-2022.txt
perl -pi.bak -e 's/psi-mi:"MI:0000"(psi-mi:MI:0915)/psi-mi:"MI-0915"(physical association)/g' All.mitab.08-22-2022.txt
#sed -i 's/taxid:83334(Escherichia coli O157:H7)/taxid:83334("Escherichia coli O157:H7")/g' ~/All.mitab.psicquic.06-11-2021.txt
# correct source DB
perl -pi.bak -e 's/psi-mi:"MI:0000"(bhf_ucl)/psi-mi:"MI:1332"(bhf-ucl)/g' All.mitab.08-22-2022.txt
# correct hgnc special characters
perl -pi.bak -e 's/(hgnc:)([^\t]+?)(\|)(\w+?:.*)(?=\t)/$1"$2"$3$4/g;' All.mitab.08-22-2022.txt
#perl -pi.bak -e 's/(taxid:[^\t]+?\()([^\t]+?:[^\t]+?)(\))(?=\t)/$1"$2"$3/g;' ~/All.mitab.psicquic.06-11-2021.txt
#perl -pi.bak -e 's/(taxid:[^\t]+?\()([^\t]+?:[^\t]+?)(\))(?=\t)/$1"$2"$3/g;' ~/All.mitab.psicquic.06-11-2021.txt
#sed -i "s/taxid:456481(Leptospira biflexa serovar Patoc strain 'Patoc 1 (Paris)')/taxid:456481(Leptospira biflexa serovar Patoc strain Patoc 1 Paris)/g" ~/All.mitab.psicquic.06-11-2021.txt
#Caused by: org.hupo.psi.calimocho.io.IllegalFieldException: Incorrect number of groups found (4): [hgnc, Su, z, 12], in field 'hgnc:Su(z)12' / Is this a xref field?
perl -pi.bak -e 's/(\t)(hgnc:)([^\t"]+?)(\|)(\w+?:.*)(?=\t)/$1$2"$3"$4$5/g;' All.mitab.08-22-2022.txt
perl -pi.bak -e 's/(hgnc:)([^\t"]+?)(\|)(\w+?:.*)(?=\t)/$1$2"$3"$4$5/g;' All.mitab.08-22-2022.txt
