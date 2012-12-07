#!/usr/bin/env python

import string
import random
import shelve
from subprocess import check_output
import flask
from flask import request
from os import environ
import os
import Cookie
import datetime
import json
import subprocess

app = flask.Flask(__name__)
app.debug = True


dbS = shelve.open("shorten.db")
dbC = shelve.open("count.db")
dbCookie = shelve.open("cookie.db")
#logfile = open("logfile","a")


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
# Now we'd like to do this generally:
# <short> will match any word and put it into the variable =short= Your task is
# to store the POST information in =db=, and then later redirect a GET request
# for that same word to the URL provided.  If there is no association between a
# =short= word and a URL, then return a 404
##/
@app.route("/", methods=['GET'])
def inputpage():
    #app.logger.debug( dbCookie.keys() )

    cookieId = checkCookie()
    if cookieId == "":
	#app.logger.debug("home-cookieNotSet"+cookieId)
	Ary = setCookie()

	response = flask.make_response(flask.render_template('index.html'))
	response.headers['Set-Cookie'] = Ary[1]
	currentTime = datetime.datetime.now().strftime("%a, %d-%b-%Y %H:%M:%S PST")
	userAgent = flask.request.headers["User-Agent"]

	logline = json.dumps({'id':Ary[0], 'datetime':currentTime, 'action':'load', 'user-agent':userAgent})
	logfile = open("logfile","a")
	logfile.write(logline+"\n")
	logfile.close()
        return response
    else:
	#app.logger.debug("home-cookieSet"+cookieId)
	currentTime = datetime.datetime.now().strftime("%a, %d-%b-%Y %H:%M:%S PST")
	userAgent = flask.request.headers["User-Agent"]

	logline = json.dumps({'id':cookieId, 'datetime':currentTime, 'action':'load homepage', 'user-agent':userAgent})
        logfile = open("logfile","a")
	logfile.write(logline+"\n")
	logfile.close()
	return flask.render_template('index.html')


@app.route("/create", methods=['PUT', 'POST'])
def create():
    #"""Create an association of =short= with the POST arguement =url="""
    origin = request.form.get('origin','DEFAULT')
    custom = request.form.get('custom','DEFAULT')
    custom = custom.encode('utf-8')    

    # handle url that doesn't start with "http"
    if origin[:4]!="http":
	origin = "http://"+origin

    duplicate_msg = ""
    originurl = origin
    custom = custom.encode('utf-8')

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
    
    # check cookieId
    cookieId = checkCookie()
    if cookieId == "":
        #app.logger.debug("create-cookieNotSet"+cookieId)
        Ary = setCookie()

	response = flask.make_response(flask.render_template(
        'index.html',
        afterurl = "http://people.ischool.berkeley.edu/~katehsiao/server/" + custom,
        duplicate_msg = duplicate_msg,
        originurl = originurl ))
        response.headers['Set-Cookie'] = Ary[1]
        currentTime = datetime.datetime.now().strftime("%a, %d-%b-%Y %H:%M:%S PST")
	userAgent = flask.request.headers["User-Agent"]

        logline = json.dumps({'id':Ary[0], 'datetime':currentTime, 'action':'save URL', 'user-agent':userAgent, 'short':custom, 'long':origin})
        logfile = open("logfile","a")
        logfile.write(logline+"\n")
        logfile.close()

        return response
    else:
        #app.logger.debug("create-cookieSet"+cookieId)
        currentTime = datetime.datetime.now().strftime("%a, %d-%b-%Y %H:%M:%S PST")
	userAgent = flask.request.headers["User-Agent"]

        logline = json.dumps({'id':cookieId, 'datetime':currentTime, 'action':'save URL', 'user-agent':userAgent, 'short':custom, 'long':origin})
        logfile = open("logfile","a")
        logfile.write(logline+"\n")
        logfile.close()

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

	cookieId = checkCookie()
	if cookieId == "":
            #app.logger.debug("redirect-cookieNotSet"+cookieId)
            Ary = setCookie()
	    
	    response = flask.make_response(flask.redirect(destination))
            response.headers['Set-Cookie'] = Ary[1]
            currentTime = datetime.datetime.now().strftime("%a, %d-%b-%Y %H:%M:%S PST")
	    userAgent = flask.request.headers["User-Agent"]

            logline = json.dumps({'id':Ary[0], 'datetime':currentTime, 'action':'redirect', 'user-agent':userAgent, 'short':short, 'long':destination})
            logfile = open("logfile","a")
            logfile.write(logline+"\n")
            logfile.close()
            return response
        else:
            #app.logger.debug("redirect-cookieSet"+cookieId)
            currentTime = datetime.datetime.now().strftime("%a, %d-%b-%Y %H:%M:%S PST")
	    userAgent = flask.request.headers["User-Agent"]

            logline = json.dumps({'id':cookieId, 'datetime':currentTime, 'action':'redirect', 'user-agent':userAgent, 'short':short,'long':destination})
            logfile = open("logfile","a")
            logfile.write(logline+"\n")
            logfile.close()
	    return flask.redirect(destination)

    else:
	return "404 Not Found"

@app.errorhandler(404)
def page_not_found(error):
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

#-----------------------------------------

def setCookie():
    # Set the cookie exiration time = 30 days
    expiration = datetime.datetime.now() + datetime.timedelta(days=30)
    cookie = Cookie.SimpleCookie()

    # Check if sessionId already exists in database
    tempKey = str(random.randint(0,10000000))
    while dbCookie.has_key(tempKey):
	tempKey = str(random.randint(0,10000000))
    
    cookie["session"] = tempKey
    #cookie["session"]["domain"] = ".people.ischool.berkeley.edu/~katehsiao/server/"
    #cookie["session"]["path"] = "/"
    cookie["session"]["expires"] = expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST")

    dbCookie[tempKey] = cookie["session"]["expires"]

    #print "Set cookie with: " + cookie.output()
    # Ary[0]: tempKey
    # Ary[1]: cookie.output()[12:]
    Ary = [ tempKey, cookie.output()[12:] ]
    return Ary

def checkCookie():
    header = flask.request.headers
    
    try:
	cookie = Cookie.SimpleCookie(header['Cookie'])
	print "session = " + cookie["session"].value
	return cookie["session"].value
    except(Cookie.CookieError, KeyError):
	print "Session cookie not set!"
	return ""

#--------------------------------------------------------
def execute(cmd):
	devnull = open('/dev/null', 'w')
	fd = subprocess.Popen(cmd,
				stdout=subprocess.PIPE,
				stderr=devnull)
	while True:
		retcode = fd.poll() #returns None while subprocess is running
		line = fd.stdout.readline()
		yield line
		if(retcode is not None):
			break
	

@app.route("/analyze", methods=['GET'])
def analyze():
	p_file = "top_browser.py"
	command_line = ["python",p_file,"logfile"]
	li =[]
	#execute(command_line)
	for line in execute(command_line):
		if line != "":  #not empty then store it
			item, count = line.split('\t')
			#log(item,count)
			li.append((item,count))
#		print item, count
	return flask.render_template(
        'analyze.html',
	li = li,
	delmsg = "" )

if __name__ == "__main__":
    app.run(port=int(environ['FLASK_PORT']))
