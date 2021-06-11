-- A simple schema purely for completing interactor data.

create table athaliana_accessions (
    gene_stable_id varchar NOT NULL,
    transcript_stable_id varchar,
    protein_stable_id varchar, -- same as transcript_stable_ID
    xref varchar not null, -- Uniprot ID
    db_name varchar not null,
    info_type varchar,
    source_identity varchar,
    xref_identity varchar,
    linkage_type varchar,
    primary key(xref)
);
