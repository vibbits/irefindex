cleaning steps

# change date
sed -e "s_\([0-9][0-9][0-9][0-9]\)\-\([0-9][0-9]\)\-\([0-9][0-9]\)_\1/\2/\3_" All.mitab.txt.out > All.mitab.txt.o2
#
cut -f1-36 -d"   " All.mitab.txt > All.mitab.psicquic.txt
#
#e.g.
#hgnc:Su(var)3-7|uniprotkb:SUV37_DROME|crogid:RoAuo6NH8jq8dliHvYA1PY/HYtI7227|icrogid:3904603    -       -
#text needs to be converted to
#hgnc:"Su(var)3-7"
#
perl -pi.bak -e 's/(\b\S+?:)(\S+?\(\S+?\)[^\s\|]+?)(?=\|)/$1"$2"/g;' All.mitab.PSICQUIC.09-18-2017.txt
#
# issues with 'taxid:11689(Human immunodeficiency virus type 1 (ELI ISOLATE))'
# the brackets should be in quotes
#perl -pi.bak -e 's/(taxid:[^\t]+?\()([^\t]+?[^\)]\){1})(\){1})(?=\t)/$1"$2"$3/g;' All.mitab.PSICQUIC.09-18-2017.txt
perl -pi.bak -e 's/(taxid:[^\t]+?\()([^\t]+?[^\)]\){1})(\){1})(?=\t)/$1"$2"$3/g;' All.mitab.psicquic.01-22-2018.txt
#
perl -pi.bak -e 's/(taxid:[^\t]+?\()([^\t]+?[^\)]\){1}\){1})(\){1})(?=\t)/$1"$2"$3/g;' All.mitab.PSICQUIC.09-18-201
7.txt
# issues with open brackets of proteinchip(r)
perl -pi.bak -e  's/proteinchip(r)/proteinchip)/g;' All.mitab.PSICQUIC.09-18-2017.txt
# issues with taxid where a colon is used 'taxid:83334(Escherichia coli O157:H7)
perl -pi.bak -e 's/(taxid:[\d]+?\()([^\t]+?[:\|][^\t]+?)(\){1})(?=\t)/$1"$2"$3/g;' All.mitab.PSICQUIC.09-18-2017.tx
t
# issues with brackets in the taxid 'taxid:8364(Xenopus (Silurana) tropicalis)'
perl -pi.bak -e 's/(taxid:[\d]+?\()([^"][^\t]+?\([^\t]+?\)[^\t]+?[^"])(\){1})(?=\t)/$1"$2"$3/g;' All.mitab.PSICQUIC
.09-18-2017.txt
# [taxid, 456481, Leptospira biflexa serovar Patoc strain 'Patoc 1 , Paris, ']
perl -pi.bak -e 's/(taxid:[\d]+?\()([^"][^\t]+?\047[^\t]+?\([^\t]+?\)\047)(\){1})(?=\t)/$1"$2"$3/g;' All.mitab.psicquic.txt


#!/bin/bash

sed -i 's/MI:0000(psi-mi:"MI:0407")/psi-mi:"MI:0407"(direct interaction)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:0915")/psi-mi:"MI:0915"(physical association)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:0403")/psi-mi:"MI:0403"(colocalization)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:0217")/psi-mi:"MI:0217"(phosphorylation reaction)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:0203")/psi-mi:"MI:0203"(dephosphorylation reaction)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:0194")/psi-mi:"MI:0194"(cleavage reaction)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:0220")/psi-mi:"MI:0220"(ubiquitination reaction)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:0570")/psi-mi:"MI:0570"(protein cleavage)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:0871")/psi-mi:"MI:0871"(demethylation reaction)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:0566")/psi-mi:"MI:0566"(sumoylation reaction)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:0844")/psi-mi:"MI:0844"(phosphotransfer reaction)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:0567")/psi-mi:"MI:0567"(neddylation reaction)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:0414")/psi-mi:"MI:0414"(enzymatic reaction)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:0192")/psi-mi:"MI:0192"(acetylation reaction)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:0218")/psi-mi:"MI:0218"(undefined)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:0179")/psi-mi:"MI:0179"(undefined)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:0208")/psi-mi:"MI:0208"(genetic interaction)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:0216")/psi-mi:"MI:0216"(palmitoylation reaction)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:0213")/psi-mi:"MI:0213"(methylation reaction)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:0213")//g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:0204")/psi-mi:"MI:0204"(deubiquitination reaction)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:1110")/psi-mi:"MI:1110"(predicted interaction)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:0195")/psi-mi:"MI:0195"(covalent binding)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:0195")/psi-mi:"MI:0945"(oxidoreductase activity electron transfer reaction)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:0945")/psi-mi:"MI:0945"(oxidoreductase activity electron transfer reaction)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:1126")/psi-mi:"MI:1126"(self interaction)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:1148")/psi-mi:"MI:1148"(ampylation reaction)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:0408")/psi-mi:"MI:0408"(disulfide bond)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:0557")/psi-mi:"MI:0557"(adp ribosylation reaction)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:1143")/psi-mi:"MI:1143"(aminoacylation reaction)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:0197")/psi-mi:"MI:0197"(deacetylation reaction)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:0212")/psi-mi:"MI:0212"(lipoprotein cleavage reaction)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:1127")/psi-mi:"MI:1127"(putative self interaction)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:0199")/psi-mi:"MI:0199"(deformylation reaction)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:0210")/psi-mi:"MI:0210"(hydroxylation reaction)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:0254")/psi-mi:"MI:0254"(genetic interference)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:0556")/psi-mi:"MI:0556"(transglutamination reaction)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:0883")/psi-mi:"MI:0883"(gtpase reaction)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:0559")/psi-mi:"MI:0559"(glycosylation reaction)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:1355")/psi-mi:"MI:1355"(lipid cleavage)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:2280")/psi-mi:"MI:2280"(deamidation reaction)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:0401")/psi-mi:"MI:0401"(biochemical)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:0985")/psi-mi:"MI:0985"(deamination reaction)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:1237")/psi-mi:"MI:1237"(proline isomerization reaction)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:0193")/psi-mi:"MI:0193"(amidation reaction)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:0902")/psi-mi:"MI:0902"(rna cleavage)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:0701")/psi-mi:"MI:0701"(dna strand elongation)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:1250")/psi-mi:"MI:1250"(isomerase reaction)/g' All.mitab.psicquic.01-22-2018.txt
sed -i 's/MI:0000(psi-mi:"MI:0569")/psi-mi:"MI:0569"(deneddylation reaction)/g' All.mitab.psicquic.01-22-2018.txt

