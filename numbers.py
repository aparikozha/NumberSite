"""საიტი, რომელზეც მომხმარებელს შეუძლია მიიღოს საინტერესო ფაქტი მისი დაბადების
დღის რიცხვზე. ფაქტები შენახულია ბაზაში.საიტი შედგება 5 ჩანართიდან, ეს არის: მთავარი გვერდი, ავტორიზაციის გვერდი,
 ფაქტების გვერდი, სურათების გვერდი და log out-ის გვერდი, სადაც ასევე არის განთავსებული კონტენტი."""
from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "gfryfgrfgrfgeu81763bfnvjkdo934ggjfgre"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///numbers.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Numbers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    fact = db.Column(db.Text, nullable=False)

    def __str__(self):
        return f'Your number is {self.number}. \nHere is an interesting fact about it: {self.fact}'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['user']
        session['username'] = user
        return redirect(url_for('user'))
    else:
        if "user" in request.args:
            user = request.args['user']
        return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('logout.html')


@app.route('/facts', methods=['GET', 'POST'])
def facts():
    if request.method == 'POST':
        try:
            numb = request.form['num']
            fact = Numbers.query.filter_by(number=numb).first()
            flash(fact.fact, 'info')
        except AttributeError:
            return redirect(url_for('facts'))

    return render_template('facts.html')


@app.route('/photos')
def photos():
    return render_template('photos.html')


if __name__ == '__main__':
    app.run(debug=True)
