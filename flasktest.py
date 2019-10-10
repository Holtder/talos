from flask import Flask, render_template, url_for
app = Flask(__name__)

posts = [
    {
        'author' : 'Ender Holten',
        'title' : 'Might as well make it myself',
        'content' : 'Should bookstack fail me then there\'s always Flask',
        'date' : 'October 10, 2019'
    },
    {
        'author' : 'Ender Holten',
        'title' : 'Or I\'ll just leave it like this',
        'content' : 'Considering the fact that my time is limited as it is',
        'date' : 'October 11, 2019'
    }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts, title="home")

@app.route('/about')
def about():
    return render_template('about.html', title="about")


if __name__ == '__main__':
    # Turn debug off when used on server!
    app.run(debug=True)