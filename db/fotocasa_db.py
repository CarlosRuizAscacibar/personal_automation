import db
import datetime

def get_existing_ad_ids():
    con = db.connect_db()
    res = [x[0] for x in con.execute("SELECT id FROM fotocasa").fetchall()]
    res = set(res)
    con.close()
    return res

def exsists_id(id):
    con = db.connect_db()
    res = con.execute("SELECT count(*) FROM fotocasa where id=?",[id]).fetchone()
    con.close()
    return res[0] > 0

def update_ad(dic):
    db.generic_update(dic, 'fotocasa')
    
def insert_ad(dic):
    if exsists_id(dic['id']):
        return False
    else:
        db.generic_insert(dic, 'fotocasa')
        return True

def get_existing_ads_url():
    con = db.connect_db()
    res = [x[0] for x in con.execute("SELECT url FROM fotocasa").fetchall()]
    con.close()
    return res