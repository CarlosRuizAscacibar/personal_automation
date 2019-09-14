import db
import datetime

def create_lend(external_id,creation_date=None):
    if creation_date == None:
        creation_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c = db.connect_db()
    
    c.execute(
        "INSERT INTO lend (cretion_date, external_id, id) values(?,?,?)",
        (creation_date, external_id, db.generate_uuid())
    )

    c.commit()
    c.close()

def get_lend(id):
    return db.connect_db().execute("SELECT * FROM lend WHERE id = ?",[id]).fetchone()

def get_lend_external_id(external_id):
    return db.connect_db().execute("SELECT * FROM lend WHERE external_id = ?",[external_id]).fetchone()
