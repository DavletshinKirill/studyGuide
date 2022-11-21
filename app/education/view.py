from flask import render_template
from . import education
from ..model import TopicNames, Notes
from flask_login import login_required


@education.route("/main_page")
def get_topic_names():
    topic_names = TopicNames.query.filter_by().all()
    return render_template("main_menu.html", topic_names=topic_names, title="Main")


@education.route("/main_page/<topic_name>")
def get_notes(topic_name):
    topic_names = TopicNames.query.filter_by(topic_name=topic_name).first()
    notes = Notes.query.filter_by(topic_names=topic_names.id).all()
    return render_template("main_menu.html", notes=notes, title=topic_names.topic_name)


@education.route("/main_page/<topic_name>/<title>")
@login_required
def get_note(topic_name, title):
    note = Notes.query.filter_by(title=title).first()
    return render_template("note.html", title=note.title, tutorial=note.tutorial)
