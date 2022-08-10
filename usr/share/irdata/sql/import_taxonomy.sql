-- Import data into the schema.

-- Copyright (C) 2011 Ian Donaldson <ian.donaldson@biotek.uio.no>
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

\copy taxonomy_names from '<directory>/names.txt'

UPDATE taxonomy_names SET name='Escherichia coli O127/H6 str. E2348/69' WHERE name= 'Escherichia coli O127:H6 str. E2348/69';
UPDATE taxonomy_names SET name='Escherichia coli BL21 DE3' WHERE name= 'Escherichia coli BL21(DE3)';
UPDATE taxonomy_names SET name='Desulfovibrio vulgaris str. Miyazaki F' WHERE name like 'Desulfovibrio vulgaris str. ''Miyazaki F''';
UPDATE taxonomy_names SET name='HIV-1 M/B_HXB2R' WHERE name='HIV-1 M:B_HXB2R';
UPDATE taxonomy_names SET name='Influenza A virus A/Aichi/2/1968/H3N2' WHERE name='Influenza A virus (A/Aichi/2/1968(H3N2))';
--UPDATE taxonomy_names SET name='' WHERE name=''
--UPDATE taxonomy_names SET name='' WHERE name=''

analyze taxonomy_names;

commit;
