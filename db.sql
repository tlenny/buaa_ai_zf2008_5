create table t_code
(
    code integer primary key asc,
    name text,
    type integer
);

create table t_rule
(
    code     integer primary key asc,
    name     text,
    position integer,
    type     integer,
    rule     text
);
