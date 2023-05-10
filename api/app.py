from flask import Flask
from flask import Response, stream_with_context
import os

app = Flask(__name__)
def make_file(template_name,uuid):
        bytes = b""
        placeholder = '~uuid'
        with open('templates/%s' % template_name,'r') as clashx_file:
            for line in clashx_file:
                if placeholder in line: line = line.replace(placeholder,uuid)
                bytes += line.encode("utf-8") 
        return bytes

def make_response(template_name,uuid):
    response = Response(make_file(template_name,uuid),content_type="application/octet-stream")
    response.headers['Content-Disposition'] = 'attachment; filename=%s' % template_name
    response.headers['Content-Length'] = len(bytes)
    return response

@app.route("/api/clashx/<uuid>")
def clashx_conf(uuid):
    template_name = "clashx.yaml"
    return make_response(template_name,uuid)

@app.route("/api/shadowrocket/<uuid>")
def shadowrocket_conf(uuid):
    return clashx_conf(uuid)

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5500)