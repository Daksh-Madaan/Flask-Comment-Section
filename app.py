from flask import Flask, app, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comments.db'

db = SQLAlchemy(app)

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Comment %r' % self.id

@app.route('/', methods=['GET', 'POST'])
def comments():
    if request.method == 'POST':
        name = request.form['name']
        comment = request.form['comment']

        new_comment = Comments(name=name, comment=comment)
        db.session.add(new_comment)
        db.session.commit()
        return redirect('/')


    else:
        comments = Comments.query.order_by(Comments.date_created)
        return render_template('index.html', comments=comments)

if __name__ == '__main__':
    app.run(debug=True)