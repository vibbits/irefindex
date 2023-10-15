/*

Experimental setup to optimize query (in `import_irefindex_sequences.sql`)

----
insert into irefindex_sequence_rogids
    select distinct refsequence || reftaxid as rogid
    from irefindex_sequences
    where reftaxid is not null;
----

To start from a clean slate:

-> Create synthetic dataset
* all of SWISS prot (incl splice var)
* 10'000'000 records from Trembl

-> Prepare the dataset
$ irparse UNIPROT

-> Prepare the database
$ dropdb irdata19
$ createdb irdata19
$ irinit --init
$ irimport UNIPROT


Test:

$ time psql -f opt_irefindex_sequences.sql irdata19

*/

begin;

/*
insert into irefindex_sequences
    select 'uniprotkb' as dblabel, accession as refvalue,
        taxid as reftaxid, sequence as refsequence, sequencedate as refdate
    from uniprot_proteins;

create index irefindex_sequences_index on irefindex_sequences(dblabel, refvalue);
commit;

--- The above takes bout 35 seconds
*/

/*
-- Original
insert into irefindex_sequence_rogids
    select distinct refsequence || reftaxid as rogid
    from irefindex_sequences
    where reftaxid is not null;

-- real	1m20.656s
-- user	0m0.007s
-- sys	0m0.007s
*/

-- Opt
create index irefindex_rogid_index on irefindex_sequences (refsequence, reftaxid);
analyze irefindex_sequences;

-- insert into irefindex_sequence_rogids

explain analyze insert into irefindex_sequence_rogids
    select refsequence || reftaxid as rogid
    from (
        select distinct refsequence, reftaxid
            from irefindex_sequences
            where reftaxid is not null
    ) as R;

-- real	0m43.535s
-- user	0m0.002s
-- sys	0m0.008s


-- Control
select * from irefindex_sequence_rogids limit 25;

rollback;
