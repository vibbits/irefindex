-- Import data into the schema.

-- Copyright (C) 2011, 2012 Ian Donaldson <ian.donaldson@biotek.uio.no>
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

create temporary table tmp_athaliana_accessions (
    gene_stable_id varchar NOT NULL,
    transcript_stable_id varchar,
    protein_stable_id varchar, -- same as transcript_stable_ID
    xref varchar not null, -- Uniprot ID
    db_name varchar not null,
    info_type varchar,
    source_identity varchar,
    xref_identity varchar,
    linkage_type varchar
);

\copy tmp_athaliana_accessions from '<directory>/Arabidopsis_thaliana.TAIR10.<release>.uniprot.tsv'

-- Insert the _best_ row of a group of `gene_stable_id`:
-- info_type "DEPENDENT" is better than "SEQUENCE_MATCH" and "NONE"

insert into athaliana_accessions
  with ranked_athaliana_accessions as (
      select *,
        rank() over (partition by gene_stable_id order by
		          num_info_type, -- sort on the ordinal info_type
		          protein_stable_id desc,
		          transcript_stable_id desc,
		          xref)
      from (select *,
              case info_type  -- translate info_type into an ordinal
                when 'DEPENDENT' then 1
                when 'SEQUENCE_MATCH' then 2
                when 'NONE' then 3
                else 4
              end as num_info_type
            from tmp_athaliana_accessions) as q)
  select
      gene_stable_id,
      transcript_stable_id,
      protein_stable_id,
      xref,
      db_name,
      info_type,
      source_identity,
      xref_identity,
      linkage_type
  from ranked_athaliana_accessions
  where rank = 1; -- keep only the top row

analyze athaliana_accessions;

commit;
