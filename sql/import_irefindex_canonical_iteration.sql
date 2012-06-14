-- Update the "active" mapping from genes to related genes.

-- Copyright (C) 2012 Ian Donaldson <ian.donaldson@biotek.uio.no>
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

-- Connect the active genes to related genes via the full mapping.

create temporary table tmp_gene2related as
    select distinct A.geneid, B.related
    from irefindex_gene2related_active as A
    inner join irefindex_gene2related as B
        on A.related = B.geneid;

alter table tmp_gene2related add primary key(geneid, related);
analyze tmp_gene2related;

-- Check the distribution of groups and write out how many genes have been
-- moved to larger groups.

create temporary table tmp_updated as
    select count(X.geneid)
    from (
        select geneid, count(related) as n
        from tmp_gene2related
        group by geneid
        ) as X
    left outer join (
        select geneid, count(related) as n
        from irefindex_gene2related_active
        group by geneid
        ) as Y
        on X.geneid = Y.geneid
        and X.n = Y.n
    where Y.geneid is null;

\copy tmp_updated to '<directory>/canonical_updates'

-- Update the active genes mapping.

truncate table irefindex_gene2related_active;
insert into irefindex_gene2related_active select * from tmp_gene2related;

commit;
