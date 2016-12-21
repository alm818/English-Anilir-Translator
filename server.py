from flask import Flask
import flask
from translator import Translator

app = Flask(__name__)

@app.route("/")
def index():
    return flask.render_template('index.html')

@app.route('/post', methods=['POST'])
def post():
	sentence = flask.request.form['text']
	trans = Translator(sentence)
	trans.translate()
	if trans.res == None:
		return flask.render_template('index.html')
	trans.finalize()
	print(trans.res)
	return flask.render_template('index.html', sentence=sentence, gloss=trans.gloss, res=trans.res, phono=trans.phonology)

if __name__ == "__main__":
    app.run()