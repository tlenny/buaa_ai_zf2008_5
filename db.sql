create table t_code
(
    code integer primary key asc,
    name text
);

create table t_rule
(
    code     integer primary key asc,
    name     text,
    position integer,
    rule     text
);
