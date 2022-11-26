from flask import Flask, render_template
import os

app = Flask(__name__)


#insertion de l'image
IMG_FOLDER = os.path.join('static', 'images')

app.config['UPLOAD_FOLDER'] = IMG_FOLDER
Flask_Logo = os.path.join(app.config['UPLOAD_FOLDER'], 'enedis3.png')


@app.route('/')
def home():
    return render_template('pages/home.html', user_image=Flask_Logo)


@app.route('/about')
def about():
    return render_template('pages/about.html', user_image=Flask_Logo)

@app.route('/contact')
def contact():
    return render_template('pages/contact.html', user_image=Flask_Logo)



@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html', user_image=Flask_Logo), 404



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5080)