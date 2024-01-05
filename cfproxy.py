#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, request, redirect
from quickflare.quickflare import CloudflaredManager
import os

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

cf = CloudflaredManager(port=port, host = destination, path=cfbase)
cf.start()

@app.route('/')
def redirect_to_new_location():
    full_original_path = request.full_path
    print(full_original_path)
    return redirect(cf.tunnel_url + full_original_path, code=302)

if __name__ == '__main__':
    app.run(debug=True, port=5000)