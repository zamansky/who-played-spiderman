from flask import Flask,request,url_for,redirect,render_template
import nifty
import json
import random


app=Flask(__name__)

@app.route("/",methods=['GET','POST'])
def index():
    if request.method=="GET":
        return render_template("index.html",guesses=None,ans=None,q=None)
    else:
        print("MAKING THE CALL")
        q=request.form['q']
        retval = nifty.getAnswers(q)
        guesses = [ "%s: %d"%(x,y) for (x,y) in retval]
        ans = retval[0][0]
        print( ans )
        return render_template("index.html",guesses=guesses,ans=ans,q=q)
        

if __name__=="__main__":
   app.debug=True
   app.run(host="0.0.0.0",port=8000)

