from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testdb'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Task %r>" % self.id

@app.route("/", methods = ["POST", "GET"])
def hello():
    if request.method == "GET":
        tasks = Todo.query.order_by(Todo.date).all()
        return render_template('index.html', tasks=tasks)
    else:
        new_task = Todo(content=request.form['content'])

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except:
            return "There was an error adding your task"

@app.route("/delete/<int:id>")
def delete(id):
    delete_task = Todo.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except:
        return "There was an issure deleting the task"

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == "GET":
        return render_template("update.html", task=task)
    else:
        task.content = request.form['updater']
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "Had an issue updating your task"

if __name__ == "__main__":
    app.run(debug=True)