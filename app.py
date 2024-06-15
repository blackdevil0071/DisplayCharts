from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json
import os

# Simple in-memory storage for chart type
chart_type = None

# Sample chart data
chart_data = {
    "labels": [
        "1999", "2000", "2001", "2002", "2003", "2004", "2005", "2006",
        "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014",
        "2015", "2016", "2017", "2018", "2019"
    ],
    "data": [50, 40, 70, 20, 90, 10, 60, 30, 80, 40]
}

class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        if parsed_path.path == '/chart-data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            if chart_type in ['bar', 'line']:
                response = json.dumps(chart_data)
            else:
                response = json.dumps({'error': 'Please select chart type from home page'})

            self.wfile.write(response.encode())

        elif parsed_path.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as file:
                self.wfile.write(file.read())

        elif parsed_path.path == '/chart.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('chart.html', 'rb') as file:
                self.wfile.write(file.read())

        elif parsed_path.path.startswith('/static/'):
            self.serve_static_file(parsed_path.path)

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    def serve_static_file(self, path):
        try:
            with open(path[1:], 'rb') as file:
                self.send_response(200)
                if path.endswith('.css'):
                    self.send_header('Content-type', 'text/css')
                elif path.endswith('.js'):
                    self.send_header('Content-type', 'application/javascript')
                self.end_headers()
                self.wfile.write(file.read())
        except FileNotFoundError:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    def do_POST(self):
        if self.path == '/set-chart-type':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_params = json.loads(post_data.decode('utf-8'))
            chart_type_selected = post_params.get('chartType')

            global chart_type
            chart_type = chart_type_selected

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            response = json.dumps({'success': 'Chart type set successfully'})
            self.wfile.write(response.encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
