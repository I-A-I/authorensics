from flask import Flask,render_template,request

app = Flask(__name__)

@app.route("/results",methods=["GET","POST"])
def login():
    if request.method=="GET":
        return render_template("results.html")
    else:
        counter = request.form["counter"]
        a = request.form["a"]
        i = 1
        t = []
        while i <= counter:
            t.append(request.form[str(i)])
            i = i + 1
        print(t)
        print(a)
        #Stuff goes here
        return render_template("results.html", a = a, t = t)
                               
@app.route("/")
def index():
    return render_template("index.html")

if __name__=="__main__":
    app.debug=True
    app.run(host="0.0.0.0",port=5000)
