#!/usr/bin/env python3
"""Central Avatar Coin allocator. Python stdlib + SQLite only."""
import argparse, datetime as dt, hashlib, json, sqlite3, uuid
from pathlib import Path

HERE=Path(__file__).resolve().parent
SCHEMA=(HERE/'avatar_coin_schema.sql').read_text()

def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def day(): return dt.datetime.now(dt.timezone.utc).date().isoformat()
def h(obj): return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def connect(path):
    db=sqlite3.connect(path); db.executescript(SCHEMA); return db

def create(db, account, repo, page, anchor, payload, parent=None):
    created=now(); account_day=day()
    canonical={'creator':account,'repo':repo,'page':page,'anchor':anchor,'payload':payload,'parent':parent,'created_at':created}
    content_hash=h(canonical); coin='avatar:'+content_hash
    with db:
        row=db.execute('SELECT avatar_coin_id,allocation_state,daily_creator_ordinal FROM avatar_coins WHERE content_hash=?',(content_hash,)).fetchone()
        if row: return {'avatar_coin_id':row[0],'allocation_state':row[1],'daily_ordinal':row[2],'duplicate':True}
        ordinal=db.execute('SELECT COUNT(*)+1 FROM avatar_coins WHERE creator_account_id=? AND account_day=?',(account,account_day)).fetchone()[0]
        state='CREATOR_WALLET' if ordinal<=10 else 'PROJECT_MATCH_POOL'
        db.execute('INSERT INTO avatar_coins VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',(coin,content_hash,account,repo,page,anchor,parent,created,account_day,ordinal,state,json.dumps(canonical)))
        holder=account if state=='CREATOR_WALLET' else None
        holder_state='CREATOR_WALLET' if holder else 'UNALLOCATED_POOL'
        db.execute('INSERT INTO avatar_coin_holdings VALUES (?,?,?,?,?)',(coin,holder,holder_state,created,None))
        event={'coin':coin,'actor':account,'type':'CREATE','state':state,'ordinal':ordinal,'at':created}
        db.execute('INSERT INTO avatar_coin_events VALUES (?,?,?,?,?,?)',(str(uuid.uuid4()),coin,account,'CREATE',h(event),json.dumps(event),created))
    return {'avatar_coin_id':coin,'allocation_state':state,'daily_ordinal':ordinal,'duplicate':False}

def transfer(db, coin, to_account, kind, txref=None):
    created=now()
    with db:
        row=db.execute('SELECT holder_account_id FROM avatar_coin_holdings WHERE avatar_coin_id=?',(coin,)).fetchone()
        if not row: raise SystemExit('unknown avatar coin')
        from_account=row[0]
        tid=str(uuid.uuid4())
        db.execute('INSERT INTO avatar_transfers VALUES (?,?,?,?,?,?,?)',(tid,coin,from_account,to_account,kind,txref,created))
        db.execute("UPDATE avatar_coin_holdings SET holder_account_id=?,holder_state=?,changed_at=?,transaction_ref=? WHERE avatar_coin_id=?",(to_account,'PURCHASED' if kind=='PURCHASE' else 'TRANSFERRED',created,txref,coin))
        db.execute("UPDATE avatar_coins SET allocation_state='PURCHASED_TRANSFERRED' WHERE avatar_coin_id=?",(coin,))
    return {'transfer_id':tid,'avatar_coin_id':coin,'holder_account_id':to_account}

def main():
    p=argparse.ArgumentParser(); p.add_argument('--db',default='avatar-coins.db'); sp=p.add_subparsers(dest='cmd',required=True)
    c=sp.add_parser('create'); c.add_argument('--account',required=True); c.add_argument('--repo',required=True); c.add_argument('--page',default=''); c.add_argument('--anchor',default=''); c.add_argument('--payload',required=True); c.add_argument('--parent')
    t=sp.add_parser('transfer'); t.add_argument('--coin',required=True); t.add_argument('--to',required=True); t.add_argument('--kind',choices=['PURCHASE','GIFT','ASSIGNMENT'],required=True); t.add_argument('--txref')
    a=p.parse_args(); db=connect(a.db)
    if a.cmd=='create': out=create(db,a.account,a.repo,a.page,a.anchor,json.loads(a.payload),a.parent)
    else: out=transfer(db,a.coin,a.to,a.kind,a.txref)
    print(json.dumps(out,indent=2))
if __name__=='__main__': main()
