#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, request, redirect
from quickflare.quickflare import CloudflaredManager
import os
from dbmanager import *

db_manager = DatabaseManager(db_path = 'data/data.db')
db_manager.get_redirect_statistics()

port = os.environ.get("CFPROXY_PORT")
if isinstance(port,type(None)):
    port = 8096
else:
    port = int(port)
    
destination = os.environ.get("CFPROXY_DEST")
if isinstance(destination,type(None)):
    destination = '192.168.1.168'

cfbase = os.environ.get("CFPROXY_CFBASE")
if isinstance(cfbase,type(None)):
    cfbase = '/tmp'

app = Flask(__name__)

ignored_user_agents = [
    'curl',
    'wget',
    'python-requests',
    'httpie',
]

cf = CloudflaredManager(port=port, host = destination, path=cfbase, keep_alive=True)
cf.start()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def redirect_to_new_location(path):
    full_original_path = request.full_path
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    user_agent = request.headers.get('User-Agent', '').lower()
    if any(agent in user_agent for agent in ignored_user_agents):
        return '', 204 
    
    db_manager.add_event(source=client_ip, to=cf.tunnel_url)

    return redirect(cf.tunnel_url + full_original_path, code=302)

if __name__ == '__main__':
    app.run(debug=True, port=5000)