-- A simple schema purely for completing interactor data.

create table taxonomy_names (
    taxid integer not null,
    name varchar not null,
    uniquename varchar not null,
    nameclass varchar not null,
    primary key(taxid, name, nameclass)
);

create materialized view taxonomy_scientific_names as (
  select name, taxid from taxonomy_names
  where nameclass = 'scientific name'
);

create unique index taxonomy_scientific_names_index on taxonomy_scientific_names(name);
