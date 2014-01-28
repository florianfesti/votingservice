#!/usr/bin/python
# -*- coding: utf-8 -*-

from wsgiref.simple_server import make_server
from cgi import parse_qs, escape
import re, hashlib

html = u"""
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>Abstimmung Missionstatement</title>
</head>
<body>
<h1>Abstimmung Missionstatement</h1>

Die verschiedenen Entwürfe können in eine Reihenfolge gebracht werden.
"1" für den bevorzugten Entwurf. "-" gilt als nicht gewählt und entspricht rechnerisch dem letzten Platz. Es ist erlaubt mehrere Entwürfe auf den selben Platz zu stellen. Da Wahlverfahren beruht auf der paarweisen Zählung wie viele Stimmen einen Entwurf einem anderen vorziehen.
 

<form action="/" method="post">
<input type="hidden" name="key" value="%%s">
<ul>
%s
</ul>
<input type="submit" value="Abstimmen">
</form>

<body>
</html>
"""

class VotingApp:
    def __init__(self, optionsfile, hashfile, resultfile):
        self.hashes = set()
        self.options = []
        for line in open(hashfile):
            self.hashes.add(line[:-1])
        try:
            for line in open(resultfile):
                pass
                #self.hashes.discard(line.split()[0])
        except IOError:
            pass
        for line in open(optionsfile):
            self.options.append(line[:-1])

        self.resultfile = open(resultfile, "a")

        self.keyre = re.compile(r'^[a-zA-Z]+$')
        self.html = html % (
            "\n".join([self.select(name, i, len(self.options))
                                   for i, name in enumerate(self.options)]))

    def select(self, name, num, numoptions):
        return "\n".join(["<li>",
                          '<select name="%s" size="1">' % num] +
                         ['  <option>%s</option>' % (i+1)
                          for i in range(numoptions)] +
                         ['  <option selected>-</option>', '</select>',
                          str(name), "</li>"])

    def savevote(self, hash, d):
        vote = []
        votere = re.compile(r"^\d+|-$")
        for i in range(len(self.options)):
            place = d.get(str(i), [""])[0]
            if not votere.match(place):
                return "Invalid vote!"
            vote.append(place)
        self.resultfile.write("%s %s\n" % (hash, " ".join(vote)))
        self.resultfile.flush()
        #self.hashes.discard(hash)
        return "Vote saved!"

    def handler(self, environ, start_response):
        # the environment variable CONTENT_LENGTH may be empty or missing
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except (ValueError):
            # get request
            request_body_size = 0

        # When the method is POST the query string will be sent
        # in the HTTP request body which is passed by the WSGI server
        # in the file like wsgi.input environment variable.
        if request_body_size:
            request_body = environ['wsgi.input'].read(request_body_size)
            d = parse_qs(request_body)
        else:
            # Returns a dictionary containing lists as values.
            d = parse_qs(environ['QUERY_STRING'])

        key = d.get("key", [""])[0]
        if not self.keyre.match(key):
            key = None
        if key:
            hash = hashlib.sha1(key).hexdigest()
        else:
            hash = None

        status = '200 OK' # HTTP Status

        if key and hash in self.hashes:
            headers = [('Content-type', 'text/html')] # HTTP Headers
            start_response(status, headers)
            if request_body_size:
                return [self.savevote(hash, d)]

            return [(self.html % key).encode("utf-8")]

        # The returned object is going to be printed

        headers = [('Content-type', 'text/plain')] # HTTP Headers
        start_response(status, headers)

        return ["Go away!"]

app = VotingApp("options.txt", "hashes.txt", "votes.txt")

httpd = make_server('', 8000, app.handler)
print "Serving on port 8000..."

# Serve until process is killed
httpd.serve_forever()
