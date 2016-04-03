def application(enc, start_response):
	start_response('200 OK', [('Content-Type', 'text/html')])
	return "Hello World!"
