from flask import Flask,render_template,request
from scap import compare_profiles_scap
from profile import Profile
import re

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
    if request.method=="GET":
        return render_template("index.html")
    else:
        print request.form["algorithm"]
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
        person_profiles = {}
        split_regex = re.compile("(?:(.+): (.+))")
        for chats in a:
            temp = chats.split("\r\n")
            for sentence in temp:
                match = re.match(split_regex, sentence)
                if match:
                    chatlog_name = match.group(1)
                    chatlog_text = match.group(2)
                    if chatlog_name in person_profiles.keys():
                        person_profiles[chatlog_name].add_text(chatlog_text)
                    else:
                        person_profiles[chatlog_name] = Profile(chatlog_text)

        anon_profiles = {name : Profile(texts) for name, texts in t.iteritems()}
        anon_list = []
        for name, anon_profile in anon_profiles.iteritems():
            anon_result = {name : compare_profiles_scap(anon_profile, profile) for name, profile in person_profiles.iteritems()}
            anon_list.append(anon_result)

        return render_template("results.html", anon_list = anon_list)

if __name__=="__main__":
    app.debug=True
    app.run(host="0.0.0.0",port=5000)
