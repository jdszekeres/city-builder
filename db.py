import imp
import re
import sqlite3
import json
import helper
import random
user_structure = {'money':50,"buildings":[], "day": 1, "population":1}
# building_structre is {'name':name, 'coordinates':(x,y)}
conn = sqlite3.connect('database.db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS users(name text, password text,city json)')
cur.execute('CREATE TABLE IF NOT EXISTS settings(uname text, mode text)')
conn.commit()
def get_info(id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT city, name FROM users WHERE rowid='{}'".format(id))
    return json.loads(cur.fetchone()[0])
def create_user(name, password):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, password, city) values ('{0}', '{1}', '{2}')".format(name, password,json.dumps(user_structure)))
    cur.execute("INSERT INTO settings (uname, mode) values ('{0}', '{1}')".format(name, "light"))
    conn.commit()
def get_rowid(name):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT rowid FROM users where name='{}'".format(name))
    return cur.fetchone()[0]
def getalldata(id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * from users where rowid='{}'".format(id))
    return cur.fetchone()
def buy(price, building, id, coordinates):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT city FROM users WHERE rowid ='{}'".format(id))
    data = json.loads(cur.fetchone()[0])
    if  data["money"] >= price:
        data["money"] -= price
        data["buildings"].append({"name":building, "coordinates": coordinates})
        pop = 0
        for i in data["buildings"]:
            if i["name"] == "house":
                pop += 2
            elif i["name"] == "apartment":
                pop += 10
            elif i["name"] == "skyscraper":
                pop += 50
            elif i["name"] == "airport":
                pop += random.randint(1, 75)
            elif i["name"] == "bunker":
                pop += 200
        data["population"] = pop
        cur.execute("UPDATE users set city='{0}' where rowid='{1}'".format(json.dumps(data), id))
        conn.commit()

        if pop == 100:
            return "Population 100"
        else:
            return
    else:
        return '500'
def add_day(id, pb):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT city FROM users WHERE rowid ='{}'".format(id))
    data = json.loads(cur.fetchone()[0])
    data["day"] += 1
    wage = 0
    data["money"] = round(data["money"])
    for i in data["buildings"]:
        wage += helper.get_building(pb, i["name"])[1]/random.randint(2, 20)
    data["money"] += round(wage, 2)
    cur.execute("UPDATE users set city='{0}' where rowid='{1}'".format(json.dumps(data), id))
    conn.commit()
    if data["day"] == 50:
        return "This just in town is 50 days old"
def sell(id, coordinates, pb):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT city FROM users WHERE rowid ='{}'".format(id))
    data = json.loads(cur.fetchone()[0])
    refund = 0
    for v, i in enumerate(data["buildings"]):
        if i["coordinates"] == list(coordinates):
            refund =  helper.get_building(pb, i['name'])[1]/2
            del data["buildings"][v]
    data["money"] += refund
    cur.execute("UPDATE users set city='{0}' where rowid='{1}'".format(json.dumps(data), id))
    conn.commit()
def set_mode(id, mode):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("UPDATE settings SET mode='{0}' WHERE uname='{1}'".format(mode, id))
    conn.commit()
def get_mode(id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT mode from settings where uname='{}'".format(id))
    try:
        return cur.fetchone()[0]
    except:
        return None
def set_modex(id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO settings (uname,mode) values ('{0}', '{1}')".format(id, "light"))
    conn.commit()