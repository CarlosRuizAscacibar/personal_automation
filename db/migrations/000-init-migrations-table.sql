
CREATE TABLE IF NOT EXISTS sys_migration (
    id INT PRIMARY KEY,
    last_migration_file VARCHAR(255)
);

insert into sys_migration
(id,last_migration_file)
values
(0,'INITIAL');