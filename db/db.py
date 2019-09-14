import sqlite3
import os
import uuid
MIGRATION_PATH = './db/migrations/'
INTERNAL_TABLE_PREFIX = 'sys_'
DATABASE_FILENAME = 'example.db'

def generate_uuid():
    return str(uuid.uuid1())

def connect_db():
    connection = sqlite3.connect(DATABASE_FILENAME)
    return connection

def apply_migraton(filename,connection):
    print('Apply migration: ' + filename)
    with open(MIGRATION_PATH + filename, 'r') as sql_file:
        sql_script = sql_file.read()
    cursor = connection.cursor()
    cursor.executescript(sql_script)
    connection.commit()
    print('Migration commited: ' + filename)
    cursor = connection.cursor()
    cursor.execute('UPDATE sys_migration SET last_migration_file=? where id = 0',[filename])
    print('Migration log updated: ' + filename)
    connection.commit()

def query_tables():
    """
        Gets all tables from
    """
    connection = connect_db()
    tables = [x[1] for x in connect_db().execute("select * from sqlite_master").fetchall() if x[0]=='table']
    connection.close()
    return tables

def get_all_migrations():
    return sorted([x for x in os.listdir(MIGRATION_PATH)])

def init():
    """
        Connects to sql databases
        if it is a newly created database, it will apply the first migration
        which creates the migrations tables with the 000 migration
    """
    connection = connect_db()
    number_of_tables = connection.execute("SELECT name FROM sqlite_master").fetchall()
    if len(number_of_tables) == 0:
        print('Created database')
        apply_migraton(get_all_migrations()[0],connection)
    connection.close()

def run_pending_migrations():
    """
        Queries the database for last executed migration
    """
    all_migrations = get_all_migrations()
    connection = connect_db()
    r = connection.execute('select * from sys_migration').fetchone()
    last_migration_filename = r[1]
    index_last_migration_filename = all_migrations.index(last_migration_filename)
    migrations_to_apply = all_migrations[index_last_migration_filename+1:]
    connection = connect_db()
    for m in migrations_to_apply:
        apply_migraton(m,connection)
    connection.close()

init()
run_pending_migrations()