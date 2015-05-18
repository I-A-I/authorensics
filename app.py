from flask import Flask,render_template,request
#import parse
app = Flask(__name__)

#@app.route("/results",methods=["GET","POST"])
#def results():
#    return render_template()


                               
@app.route("/", methods=["GET","POST"])
def index():
    if request.method=="GET":
        return render_template("index.html")
    else:
        a = []
        i = 1
        t = {}
        try:
            while(1):
                a.append(request.form["a" + str(i)])
                i = i + 1
        except:
            pass
        i = 1
        try:
            while(1):
                t[request.form["n" + str(i)]] = request.form[str(i)]
                i = i + 1
        except:
            pass
        print(a)
        print(t)
       # d = parse.ChatParser(a)
        #print d.parseParser()
        #Stuff goes here
        return render_template("results.html", a = a, t = t)

if __name__=="__main__":
    app.debug=True
    app.run(host="0.0.0.0",port=5000)
