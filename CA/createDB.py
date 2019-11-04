# file to create CA database using sqlite3

import sqlite3

DB_ADDRESS = "./gm_db.db"


def connect_db(db_address):
    gm_db = sqlite3.connect(db_address)
    cursor = gm_db.cursor()
    return cursor


def create_table():
    cursor = connect_db(DB_ADDRESS)
    # crate certification table
    sql = '''
    create table certification{
    id int,
    serial_number text,
    country text,
    province text
    city text,
    organization text,
    name text,
    email text,
    state int,
    create_date DATE,
    effective_time int,
    }
    '''

    cursor.execute(sql)

    # create destroy table
    sql = '''
    create table destroy_list{
    id int,
    serial_number text,
    country text,
    province text
    city text,
    organization text,
    state int,
    create_date DATE,
    effective_time int,
    destroy_date DATE
    }
    '''

    cursor.execute(sql)
