from datetime import date, datetime
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for

from core import Config, Data, Grade

app = Flask(__name__)


@app.route("/")
def index():
    data = (
        Data.load_from_file("data.json")
        if Path("data.json").exists()
        else Data(subjects=[])
    )
    config = Config.load("config.json")
    return render_template("index.html", data=data, config=config)


@app.route("/add_grade", methods=["GET", "POST"])
def add_grade():
    data = (
        Data.load_from_file("data.json")
        if Path("data.json").exists()
        else Data(subjects=[])
    )
    config = Config.load("config.json")
    if request.method == "POST":
        subject_name = request.form["subject"]
        grade = int(request.form["grade"])
        date_str = request.form.get("date")
        grade_date = (
            datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else date.today()
        )

        subject = next(s for s in data.subjects if s.name == subject_name)
        subject.grades.append(
            Grade(grade=grade, date=grade_date, semester=config.get_semester())
        )
        data.save("data.json")
        return redirect(url_for("index"))
    return render_template("add_grade.html", data=data)


@app.route("/settings", methods=["GET", "POST"])
def settings():
    config = Config.load("config.json")
    if request.method == "POST":
        config.semester = int(request.form["semester"])
        config.save("config.json")
        return redirect(url_for("index"))
    return render_template("settings.html", config=config)


if __name__ == "__main__":
    app.run(debug=True)
