from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy # ORM istifade etmek ucun bunu install edib,sonra import etmek lazimdi

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Dell/Desktop/Flask todo/todo.db' # sonluga bizim db path-ni yaziriq
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)

@app.route('/')
def index():
    todos=Todo.query.all()
    return render_template('index.html',todos=todos)

@app.route('/add',methods=['POST'])
def addTodo():
    title=request.form.get('title') #'title' bize formdan gelen title-di
    newTodo=Todo(title=title,complete=False)
    db.session.add(newTodo)
    db.session.commit()# deyiklikler bas verdiyi ucun
    return redirect(url_for('index'))

@app.route("/complete/<string:id>")
def completeTodo(id):
    todo=Todo.query.filter_by(id = id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/delete/<string:id>")
def delete(id):
    todo=Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))




if __name__=="__main__":
    db.create_all() # burda olan butun classlar db bir table kimi yazilacaq bu kodun komeyi ile
    app.run(debug=True)


