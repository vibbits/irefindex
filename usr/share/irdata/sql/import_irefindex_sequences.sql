-- Generate a mapping of identifiers to sequences for all known sequences in
-- sequence databases. Although many sequences will not be referenced by
-- interactors in the current releases or states of interaction databases, they
-- may have been referenced in previous iRefIndex releases or be referenced in
-- future releases. If a historical perspective is not required, processing can
-- be made much quicker by constraining sequence retrieval to identifiers used
-- by the current interaction database data.

-- Copyright (C) 2012, 2013 Ian Donaldson <ian.donaldson@biotek.uio.no>
-- Copyright (C) 2013 Paul Boddie <paul@boddie.org.uk>
-- Original author: Paul Boddie <paul.boddie@biotek.uio.no>
--
-- This program is free software; you can redistribute it and/or modify it under
-- the terms of the GNU General Public License as published by the Free Software
-- Foundation; either version 3 of the License, or (at your option) any later
-- version.
--
-- This program is distributed in the hope that it will be useful, but WITHOUT ANY
-- WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
-- PARTICULAR PURPOSE.  See the GNU General Public License for more details.
--
-- You should have received a copy of the GNU General Public License along
-- with this program.  If not, see <http://www.gnu.org/licenses/>.

begin;

-- UniProt accessions mapping directly and indirectly to proteins.

insert into irefindex_sequences

    -- Accessions are distinct in the proteins table.

    select 'uniprotkb' as dblabel, accession as refvalue,
        taxid as reftaxid, sequence as refsequence, sequencedate as refdate
    from uniprot_proteins;

-- RefSeq versions and accessions mapping directly to proteins.

insert into irefindex_sequences

    -- Versions and accessions are distinct in the proteins table.

    select 'refseq' as dblabel, version as refvalue,
        taxid as reftaxid, sequence as refsequence, null as refdate
    from refseq_proteins as P
    where version is not null
    union all
    select 'refseq' as dblabel, accession as refvalue,
        taxid as reftaxid, sequence as refsequence, null as refdate
    from refseq_proteins as P
    where accession is not null;

-- FlyBase accessions mapping directly and indirectly to proteins.

insert into irefindex_sequences
    select distinct 'flybase' as dblabel, flyaccession as refvalue,
        taxid as reftaxid, sequence as refsequence, sequencedate as refdate
    from fly_accessions as A
    inner join uniprot_proteins as P
        on A.accession = P.accession
    union all
    select distinct 'flybase' as dblabel, flyaccession as refvalue,
        P.taxid as reftaxid, P.sequence as refsequence, P.sequencedate as refdate
    from fly_accessions as A
    inner join uniprot_proteins as P
        on A.uniprotid = P.uniprotid

    -- Exclude previous matches.

    left outer join uniprot_proteins as P2
        on A.accession = P2.accession
    where P2.accession is null;

-- sam:  copied and adapted  above code block for athaliana
insert into irefindex_sequences
    select distinct 'athalianabase' as dblabel, gene_stable_id as refvalue,
        taxid as reftaxid, sequence as refsequence, sequencedate as refdate
    from athaliana_accessions as A
    inner join uniprot_proteins as P
        on A.xref = P.accession
    union all
    select distinct 'athalianabase' as dblabel, gene_stable_id as refvalue,
        P.taxid as reftaxid, P.sequence as refsequence, P.sequencedate as refdate
    from athaliana_accessions as A
    inner join uniprot_proteins as P
        on A.gene_stable_id = P.uniprotid

    -- Exclude previous matches.

    left outer join uniprot_proteins as P2
        on A.xref = P2.accession
    where P2.accession is null;



-- SGD accessions mapping directly and indirectly to proteins.

insert into irefindex_sequences
    select distinct 'sgd' as dblabel, sgdxref as refvalue,
        taxid as reftaxid, sequence as refsequence, sequencedate as refdate
    from yeast_accessions as A
    inner join uniprot_proteins as P
        on A.accession = P.accession
    union all
    select distinct 'sgd' as dblabel, sgdxref as refvalue,
        P.taxid as reftaxid, P.sequence as refsequence, P.sequencedate as refdate
    from yeast_accessions as A
    inner join uniprot_proteins as P
        on A.uniprotid = P.uniprotid

    -- Exclude previous matches.

    left outer join uniprot_proteins as P2
        on A.accession = P2.accession
    where P2.accession is null;

-- CYGD accessions mapping directly and indirectly to proteins.

insert into irefindex_sequences
    select distinct 'cygd' as dblabel, orderedlocus as refvalue,
        taxid as reftaxid, sequence as refsequence, sequencedate as refdate
    from yeast_accessions as A
    inner join uniprot_proteins as P
        on A.accession = P.accession
    union
    select distinct 'cygd' as dblabel, orderedlocus as refvalue,
        P.taxid as reftaxid, P.sequence as refsequence, P.sequencedate as refdate
    from yeast_accessions as A
    inner join uniprot_proteins as P
        on A.uniprotid = P.uniprotid

    -- Exclude previous matches.

    left outer join uniprot_proteins as P2
        on A.accession = P2.accession
    where P2.accession is null;

-- NOTE: gi not used anymore
-- GenBank identifiers mapping directly and indirectly to proteins for both
-- RefSeq and GenPept.

--insert into irefindex_sequences

  -- GenBank identifiers are distinct in RefSeq and GenPept.

--    select 'genbank_protein_gi' as dblabel, cast(gi as varchar) as refvalue,
--        taxid as reftaxid, sequence as refsequence, null as refdate
--    from refseq_proteins as P
--   union all
--    select 'genbank_protein_gi' as dblabel, cast(gi as varchar) as refvalue,
--        taxid as reftaxid, sequence as refsequence, null as refdate
--    from genpept_proteins as P
--    union all
--    select 'genbank_protein_gi' as dblabel, cast(gi as varchar) as refvalue,
--        P.taxid as reftaxid, P.sequence as refsequence, null as refdate
--    from genpept_accessions as A
--    inner join genpept_proteins as P
--        on A.accession = P.accession;

-- GenBank accessions mapping directly and indirectly to proteins.

insert into irefindex_sequences

    -- Accessions and the short forms are distinct in GenPept.

    select 'ddbj/embl/genbank' as dblabel, version as refvalue,
        taxid as reftaxid, sequence as refsequence, null as refdate
    from genpept_proteins as P
    union all
    select 'ddbj/embl/genbank' as dblabel, shortform as refvalue,
        taxid as reftaxid, sequence as refsequence, null as refdate
    from genpept_accessions as A
    inner join genpept_proteins as P
        on A.version = P.version;

-- IPI accessions mapping directly and indirectly to proteins.

insert into irefindex_sequences
    select distinct 'ipi' as dblabel, P.accession as refvalue,
        cast(T.refvalue as integer) as reftaxid, P.sequence as refsequence, null as refdate
    from ipi_proteins as P
    inner join ipi_identifiers as T
        on P.accession = T.accession
        and T.dblabel = 'Tax_Id'
    union all
    select distinct 'ipi' as dblabel, shortform as refvalue,
        cast(T.refvalue as integer) as reftaxid, P.sequence as refsequence, null as refdate
    from ipi_accessions as A
    inner join ipi_proteins as P
        on A.accession = P.accession
    inner join ipi_identifiers as T
        on P.accession = T.accession
        and T.dblabel = 'Tax_Id'

    -- Exclude previous matches.

    left outer join uniprot_proteins as P2
        on A.accession = P2.accession
    where P2.accession is null;

-- PDB accessions mapping directly and indirectly to proteins.

insert into irefindex_sequences
    select distinct 'pdb' as dblabel, M.accession || '|' || M.chain as refvalue,
        M.taxid as reftaxid, P.sequence as refsequence, null as refdate
    from mmdb_pdb_accessions as M
    inner join pdb_proteins as P
        on M.accession = P.accession
        and M.chain = substring(P.chain from 1 for 1)
--	and M.gi = P.gi
    union all
    select distinct 'pdb' as dblabel, P.accession || '|' || substring(P.chain from 1 for 1) as refvalue,
        M.taxid as reftaxid, P.sequence as refsequence, null as refdate
    from pdb_proteins as P
    left outer join mmdb_pdb_accessions as M
        on M.accession = P.accession
        and M.chain = substring(P.chain from 1 for 1)

    -- Exclude previous matches.

    where M.accession is null;

create index irefindex_sequences_index on irefindex_sequences(dblabel, refvalue);
create index irefindex_rogid_index on irefindex_sequences (refsequence, reftaxid);
analyze irefindex_sequences;


-- ROG identifiers for all sequences having a taxonomy identifier.

insert into irefindex_sequence_rogids
    select refsequence || reftaxid as rogid
    from (
        select distinct refsequence, reftaxid
            from irefindex_sequences
            where reftaxid is not null
    ) as R;

analyze irefindex_sequence_rogids;

drop index irefindex_rogid_index;

--till here no errors
-- Actual sequences for all known sequences.

insert into irefindex_sequences_original
    select distinct "sequence", actualsequence, 'uniprotkb' as dblabel
    from uniprot_sequences;
-- this already gives the disk space error
insert into irefindex_sequences_original
    select distinct "sequence", actualsequence, 'refseq' as dblabel
    from refseq_sequences;

insert into irefindex_sequences_original
    select distinct "sequence", actualsequence, 'ipi' as dblabel
    from ipi_sequences;

insert into irefindex_sequences_original
    select distinct "sequence", actualsequence, 'genpept' as dblabel
    from genpept_sequences;

insert into irefindex_sequences_original
    select distinct "sequence", actualsequence, 'pdb' as dblabel
    from pdb_sequences;

analyze irefindex_sequences_original;

commit;
