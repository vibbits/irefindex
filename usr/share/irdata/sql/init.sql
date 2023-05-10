-- Utilities.

create aggregate array_accum (
    sfunc = array_append,
    basetype = anycompatible,
    stype = anycompatiblearray,
    initcond = '{}'
);

create aggregate array_array_accum (
    sfunc = array_cat,
    basetype = anycompatiblearray,
    stype = anycompatiblearray,
    initcond = '{}'
);
