#!/usr/bin/python

from wsgiref.simple_server import make_server
from cgi import parse_qs, escape
import re

html = """
<html>
<head>
<title>Abstimmung Missionstatement</title>
</head>
<body>
<h1>Abstimmung Missionstatement</h1>
<form action="/" method="post">
<input type="hidden" name="key" value="%%s">
%s
<input type="submit" value="Abstimmen">
</form>

<body>
</html>
"""

class VotingApp:
    def __init__(self, keyfile):
        self.keys = set()
        for line in open(keyfile):
            self.keys.add(line[:-1])
        print self.keys
        self.keyre = re.compile(r'^[a-zA-Z]{16}$')
        self.html = html % (
            "\n".join([self.select(i, 5) for i in range(5)]))

    def select(self, name, numoptions):
        return "\n".join(['<select name="%s" size="1">' % name] +
                         ['  <option>%s</option>' % (i+1)
                          for i in range(numoptions)] +
                         ['  <option selected>-</option>', '</select>'])



    def handler(self, environ, start_response):
        # the environment variable CONTENT_LENGTH may be empty or missing
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except (ValueError):
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


        status = '200 OK' # HTTP Status

        if key and key in self.keys:
            headers = [('Content-type', 'text/html')] # HTTP Headers
            start_response(status, headers)
            return [self.html % key]

        # The returned object is going to be printed

        headers = [('Content-type', 'text/plain')] # HTTP Headers
        start_response(status, headers)

        return ["Go away!"]


app = VotingApp("keys.txt")

httpd = make_server('', 8000, app.handler)
print "Serving on port 8000..."

# Serve until process is killed
httpd.serve_forever()
