from flask import Flask
from flask import Response, stream_with_context
import base64
app = Flask(__name__)
def make_file(template_name,uuid):
        string = ""
        placeholder = '~uuid'
        with open('templates/%s' % template_name,'r') as template_file:
            for line in template_file:
                if placeholder in line: line = line.replace(placeholder,uuid)
                string += line
        return string

def make_response(template_name,uuid):
    file_bytes = make_file(template_name,uuid)
    response = Response(file_bytes,content_type="application/octet-stream")
    response.headers['Content-Disposition'] = 'attachment; filename=%s' % template_name
    response.headers['Content-Length'] = len(file_bytes)
    return response

@app.route("/api/clashx/<uuid>")
def clashx_conf(uuid):
    template_name = "clashx.yaml"
    return make_response(template_name,uuid)

@app.route("/api/shadowrocket/<uuid>")
@app.route("/api/v2ray/<uuid>")
def shadowrocket_conf(uuid):
    template_name = "vmess.json"
    file = make_file(template_name,uuid)
    file_encoded = base64.b64encode(file.encode('utf-8')).decode('utf-8')
    vmess_url = 'vmess://' + file_encoded
    return base64.b64encode(vmess_url.encode('utf-8')).decode('utf-8')



if __name__=="__main__":
    app.run(host="0.0.0.0",port=5500)