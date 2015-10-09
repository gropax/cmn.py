# -*- coding: utf-8 -*-

import sys
import cedict
import sqlite3


def setup_db():
    conn = sqlite3.connect('cmn/cedict.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

    if cursor.fetchall() == []:  # db is empty
        sys.stdout.write("Initializing Database\n")

        sys.stdout.write("    reading dictionary data\n")
        dictfile = open('cmn/cedict_ts.u8')

        # Create db and load data
        sys.stdout.write("    creating table\n")
        cursor.execute('''CREATE TABLE entries (traditional text,
                                                simplified text,
                                                pinyin text,
                                                definitions text,
                                                variants text,
                                                measure_word text)''')
        sys.stdout.write("    loading data into the database...\n")
        for ch, chs, py, ds, vs, mws in cedict.iter_cedict(dictfile):
            _py = py.replace(' ', '')
            _ds = "|".join(ds)
            _vs = "|".join([k + ":" + v for d in vs for k, v in d.items()])
            _mws = "|".join([";".join(mw) for mw in mws])
            entry = (ch, chs, _py, _ds, _vs, _mws)
            cursor.execute("INSERT INTO entries VALUES (?,?,?,?,?,?)", entry)

        conn.commit()
        sys.stdout.write("DONE\n")

    conn.close()

setup_db()

#sys.stdout.write("EMPTY? " + str(db_is_empty()))


def search_pinyin(word):
    dictfile = open('cmn/cedict_ts.u8')
    uword = word.decode('utf-8')
    match = set()
    for ch, chs, py, _, _, _ in cedict.iter_cedict(dictfile):
        if uword == ch or uword == chs:
            match.add(py)
    return match

def search_pinyin(word):
    w = word.decode('utf-8')
    conn = sqlite3.connect('cmn/cedict.db')
    cursor = conn.cursor()
    cursor.execute('SELECT pinyin FROM entries WHERE traditional=? OR simplified=?', (w,w))
    return set(s for t in cursor.fetchall() for s in t)
