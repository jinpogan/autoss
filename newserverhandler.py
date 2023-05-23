from flask import Flask
from flask import request
from flask import send_file
from flask import redirect
import json
import time
app = Flask(__name__)

from waitress import serve

pcon=False
@app.route('/', methods = ['GET'])
def a():
    return redirect("https://www.bilibili.com/video/BV1MY4119713/", code=302)

@app.route('/getscript', methods = ['GET'])
def getscript():
    return send_file("shadow.sh")

@app.route('/getlink', methods = ['GET'])
def getlink():
    return send_file("genlink.py")


@app.route('/newserver',methods = ['POST'])
def newserver():
    if request.method == 'POST':
        with open("servers/"+str(time.time())+".txt","wb") as f:
            f.write(request.data)
        return "ok"
    else:
        return  redirect("https://www.bilibili.com/video/BV1MY4119713/", code=302)

#app.run(port=3939)
serve(app,port=3939)


