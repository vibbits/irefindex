-- Import PSI-MI data.

-- Copyright (C) 2012, 2013 Ian Donaldson <ian.donaldson@biotek.uio.no>
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

\copy psicv_terms from '<directory>/terms'

create index psicv_terms_index on psicv_terms(code, name, nametype);

ALTER TABLE psicv_terms ADD COLUMN codepsi varchar;

UPDATE psicv_terms SET codepsi = code WHERE code like 'psi-mi:%';
UPDATE psicv_terms SET codepsi = 'psi-mi:"' || code ||'"' WHERE code not like 'psi-mi:%';
UPDATE psicv_terms SET name='proteinchip on a surface-enhanced laser desorption/ionization'  WHERE name='proteinchip(r) on a surface-enhanced laser desorption/ionization';
UPDATE psicv_terms SET name='genetic interaction'  WHERE name='genetic interaction (sensu unexpected)';
--UPDATE psicv_terms SET name=''  WHERE name='';

analyze psicv_terms;

commit;
