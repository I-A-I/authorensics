from flask import Flask,render_template,request
import scap
import vea
from profile import Profile
import re

app = Flask(__name__)

MIN_CHARACTERS = 140

@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")

@app.route("/", methods=["GET","POST"])
def index():
    if request.method=="GET":
        return render_template("index.html")

    algorithm = request.form["algorithm"]

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
            text = text.strip()
        else:
            break

        candidates_raw.append({"name":name, "text":text})
        counter = counter + 1

    candidate_profiles = {}
    split_regex = re.compile("(?:([^:]+): (.+))")
    for candidate in candidates_raw:
        # Is plaintext, not FB chat
        if candidate["name"]:
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
    # Check length
    if len([1 for profile in candidate_profiles.values() if len(profile.single_text) < MIN_CHARACTERS]) > 0:
        return render_template("index.html", error = "You cannot have any candidate texts shorter than %d characters." % (MIN_CHARACTERS), anon_text = anon_text)


    if algorithm == "scap":
        results = scap.analyze(anon_profile, candidate_profiles)
    elif algorithm == "vea":
        results = vea.analyze(anon_profile, candidate_profiles)

    return render_template("results.html", results=results, algorithm=algorithm)

if __name__=="__main__":
    app.debug=True
    app.run(host="0.0.0.0",port=5000)
