from flask import Flask,render_template,request
from scap import compare_profiles_scap
from profile import Profile
import re

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
    if request.method=="GET":
        return render_template("index.html")

    # Get anon text
    anon_text = request.form["anon"]
    anon_profile = Profile(anon_text)

    # Get candidates 
    candidates_raw = []
    counter  = 1
    while True:
        if "n" + str(counter) in request.form.keys():
            name = request.form["n" + str(counter)]
        else:
            name = False

        if str(counter) in request.form.keys():
            text = request.form[str(counter)]
        else:
            break

        candidates_raw.append({"name":name, "text":text})
        counter = counter + 1

    candidate_profiles = {}
    split_regex = re.compile("(?:(.+): (.+))")
    for candidate in candidates_raw:
        # Is plaintext, not FB chat
        if candidate["name"]:
            profile = Profile(candidate["text"])
            if candidate["name"] in candidate_profiles:
                candidate_profiles[candidate["name"]].add_text(candidate["text"])
            else:
                candidate_profiles[candidate["name"]] = Profile(candidate["text"])

        # Is FB chat
        else:
            lines = candidate["text"].split("\r\n")
            for line in lines:
                 match = re.match(split_regex, line)
                 if match:
                     chat_name = match.group(1)
                     chat_text = match.group(2)
                     if chat_name in candidate_profiles:
                         candidate_profiles[chat_name].add_text(chat_text)
                     else:
                         candidate_profiles[chat_name] = Profile(chat_text)

    results = {}
    for candidate_name, candidate_profile in candidate_profiles.iteritems():
        result = compare_profiles_scap(anon_profile, candidate_profile)
        results[candidate_name] = result

    print results
    return render_template("results.html", results=results)

if __name__=="__main__":
    app.debug=True
    app.run(host="0.0.0.0",port=5000)
