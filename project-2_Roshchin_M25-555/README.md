# project-2_Roshchin_M25-555

To install this package run:

```bash
make install
```

To run this package use:

```bash
make project
```

Examples:

```bash
create_database DB /Users/phil/GitHub/masters_degree_Roshchin_M25-555/db

load_database /Users/phil/GitHub/masters_degree_Roshchin_M25-555/db.json

create_table table_1 /Users/phil/GitHub/masters_degree_Roshchin_M25-555/table_1.csv name:str ID:int is_active:bool is_superuser:bool

list_tables

info table_1

select from table_1

select from table_1 where is_active=1 AND is_superuser=1
```
