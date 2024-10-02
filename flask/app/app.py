from flask import Flask, render_template, redirect, request, jsonify
from recommender import recommend

# Create an instance of Flask
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    # Return template and data
    return render_template("index.html")

@app.route("/works_cited")
def work_cited():
    # Return template and data
    return render_template("works_cited.html")

@app.route("/about_us")
def about_us():
    # Return template and data
    return render_template("about_us.html")

@app.route("/tableau")
def tableau():
    # Return template and data
    return render_template("tableau.html")
    
@app.route("/report")
def report():
    return render_template("report.html")

@app.route("/recommendation")
def recommendation():
    return render_template("recommendation.html")

#############################################################

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r

@app.route("/makePredictions", methods=["POST"])
def make_predictions():
    content = request.json["data"]
    print(content)

    # Make the recommendation given the data.
    result = recommend(int(content['list_length']), content['movie'])
    print(result)

    return(jsonify(result))

# Main.
if __name__ == "__main__":
    app.run(debug=True)
