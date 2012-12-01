#!/usr/bin/env python

import string
import random
import shelve
from subprocess import check_output
import flask
from flask import request
from os import environ

app = flask.Flask(__name__)
app.debug = True


dbS = shelve.open("shorten.db")
dbC = shelve.open("count.db")

#@app.route('/')
#def index():
#    """Builds a template based on a GET request, with some default
#    arguements"""
#    index_title = request.args.get("title", "i253")
#    hello_name = request.args.get("name", "Jim")
#    return flask.render_template(
#            'index.html',
#            title=index_title,
#            name=hello_name)


@app.route('/static/js/<filename>')
def js(filename):
    response = flask.make_response(flask.render_template(filename))
    response.headers['Content-type'] = 'text/javascript'
    return response
    
@app.route('/static/css/<filename>')
def css(filename):
    response = flask.make_response(flask.render_template(filename))
    response.headers['Content-type'] = 'text/css'
    return response

@app.route('/img/<filename>')
def img(filename):
    return flask.send_file(filename, mimetype='image/png')

###
# This function is not working properly because the Content-Type is not set.
# Set the correct MIME type to be able to view the image in your browser
##/

###
#@app.route('/image')
#def image():
#    """Returns a PNG image of madlibs text"""
#    relationship = request.args.get("relationship", "friend")
#    name = request.args.get("name", "Jim")
#    adjective = request.args.get("adjective", "fun")

#    resp = flask.make_response(
#            check_output(['convert', '-size', '600x400', 'xc:transparent',
#                '-font', '/usr/share/fonts/thai-scalable/Waree-BoldOblique.ttf',
#                '-fill', 'black', '-pointsize', '32', '-draw',
#                "text 10,30 'My %s %s said i253 was %s'" % (relationship, name, adjective),
#                'png:-']), 200);
#    # Comment in to set header below
#    resp.headers['Content-Type'] = 'image/png'
#    
#    #
#    hrs = flask.request.headers
#    if hrs['Accept'].find('text/html')!= -1 or hrs['Accept'].find('image/png')!= -1 :
#        return resp
#    else:
#	return "My %s %s said this can only return text. :) " % (relationship, name)
###

###
# Below is an example of a shortened URL
# We can set where /wiki redirects to with a PUT or POST command
# and when we GET /wiki it will redirect to the specified Location
##/

###
#@app.route("/wiki", methods=['PUT', 'POST'])
#def install_wiki_redirect():
#    wikipedia = request.form.get('url', "http://en.wikipedia.org")
#    db['wiki'] = wikipedia
#    return "Stored wiki => " + wikipedia

#@app.route("/wiki", methods=["GET"])
#def redirect_wiki():
#    destination = db.get('wiki', '/')
#    app.logger.debug("Redirecting to " + destination)
#    return flask.redirect(destination)


###
# Now we'd like to do this generally:
# <short> will match any word and put it into the variable =short= Your task is
# to store the POST information in =db=, and then later redirect a GET request
# for that same word to the URL provided.  If there is no association between a
# =short= word and a URL, then return a 404
##/
@app.route("/", methods=['GET'])
def inputpage():
    return flask.render_template(
	'index.html')

@app.route("/create", methods=['PUT', 'POST'])
def create():
    #app.logger.debug(dbS.keys())
    #"""Create an association of =short= with the POST arguement =url="""
    origin = request.form.get('origin','DEFAULT')
    custom = request.form.get('custom','DEFAULT')
    custom = custom.encode('utf-8')    

    # handle url that doesn't start with "http"
    if origin[:4]!="http":
	origin = "http://"+origin

    duplicate_msg = ""
    originurl = origin

    #origin = origin.encode('utf-8')
    custom = custom.encode('utf-8')

    #app.logger.debug(origin)

    # if the same url is entered
    for v in dbS.keys():
	if dbS[v][7:]==origin[7:] or dbS[v][7:]==origin[8:] or dbS[v][8:]==origin[7:] or dbS[v][8:]==origin[8:] :
		duplicate_msg = "Your long URL already exists."
		return flask.render_template(
			'index.html',
			afterurl = "http://people.ischool.berkeley.edu/~katehsiao/server/" + v,
			duplicate_msg = duplicate_msg,
			originurl = originurl )
    
    # randomly generate 6-digit url if user doesn't input customize
    if dbS.has_key(custom) or custom == "" or custom=="listurl":
	if custom != "":
		duplicate_msg = "Your customize string is already in use, thus we generate a random shorten url for you. :)"

	custom = "".join(random.sample(string.letters, 6))
        while dbS.has_key(custom):
		custom = "".join(random.sample(string.letters, 6))
    
    #save to db
    dbS[custom] = origin
    dbC[custom] = 0
    return flask.render_template(
	'index.html',
	afterurl = "http://people.ischool.berkeley.edu/~katehsiao/server/" + custom,
	duplicate_msg = duplicate_msg,
	originurl = originurl ) 
    


@app.route("/<short>", methods=['GET'])
def redirect(short):
    #"""Redirect the request to the URL associated =short=, otherwise return 404
    #NOT FOUND"""
    short = short.encode('utf-8')
    if dbS.has_key(short) :
	destination = dbS.get(short,'/')
	dbC[short] = str( int(dbC[short]) + 1 )
	return flask.redirect(destination)
    else:
	return "404 Not Found"

#@app.route("/<short>", methods=['DELETE'])
@app.route("/listurl", methods=['POST'])
def destroy():
    """Remove the association between =short= and it's URL"""
    #app.logger.debug(db.keys())
    short = request.form.get('de','DEFAULT')
    short = short.encode('utf-8')
    delmsg = ""

    if dbS.has_key(short) :
	del dbS[short]
	del dbC[short]
	delmsg = "Successfully delete: "+short
    else:
	delmsg = "The key "+short+" doesn't exist, please try it again."    

    # re-render this page
    li = []

    for v in dbC.keys():
        li.append((v,dbC[v],dbS[v]))

    return flask.render_template(
        'listurl.html',
        li = li, 
        delmsg = delmsg )


@app.route("/listurl", methods=['GET'])
def listurl():
    li = []
   
    for v in dbC.keys():
	li.append((v,dbC[v],dbS[v]))

    return flask.render_template(
        'listurl.html',
	li = li,
	delmsg = "" )


if __name__ == "__main__":
    app.run(port=int(environ['FLASK_PORT']))
