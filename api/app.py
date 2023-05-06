from flask import Flask
from flask import Response, stream_with_context
import os

app = Flask(__name__)
def make_file(template_name,uuid):
        placeholder = '~uuid'
        with open('templates/%s' % template_name,'r') as clashx_file:
            for line in clashx_file:
                if placeholder in line: line = line.replace(placeholder,uuid)
                yield line 
                    

def make_response(template_name,uuid):
    response = Response(stream_with_context(make_file(template_name,uuid)),content_type="application/octet-stream")
    response.headers['Content-Disposition'] = 'attachment; filename=%s' % template_name
    response.headers['content-length'] = os.stat("templates/%s" % template_name).st_size
    return response

@app.route("/clashx/<uuid>")
def clashx_conf(uuid):
    template_name = "clashx.yaml"
    return make_response(template_name,uuid)

@app.route("/shadowrocket/<uuid>")
def shadowrocket_conf(uuid):
    return clashx_conf(uuid)

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5500)