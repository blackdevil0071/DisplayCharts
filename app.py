from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json

chart_type = None

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

        if parsed_path.path == '/chart-data':
            self.handle_chart_data_request()
        elif parsed_path.path == '/':
            self.serve_file('index.html', 'text/html')
        elif parsed_path.path == '/chart.html':
            self.serve_file('chart.html', 'text/html')
        elif parsed_path.path.startswith('/static/'):
            self.serve_static_file(parsed_path.path[1:])
        else:
            self.send_error(404, 'Not Found')

    def handle_chart_data_request(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = json.dumps(chart_data if chart_type in ['bar', 'line'] else {'error': 'Please select chart type from home page'})
        print(response)
        self.wfile.write(response.encode())

    def serve_file(self, filepath, content_type):
        try:
            with open(filepath, 'rb') as file:
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.end_headers()
                self.wfile.write(file.read())
        except FileNotFoundError:
            self.send_error(404, 'Not Found')

    def serve_static_file(self, filepath):
        content_type = 'text/css' if filepath.endswith('.css') else 'application/javascript'
        self.serve_file(filepath, content_type)

    def do_POST(self):
        if self.path == '/set-chart-type':
            self.handle_set_chart_type_request()
        else:
            self.send_error(404, 'Not Found')

    def handle_set_chart_type_request(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_params = json.loads(post_data.decode('utf-8'))
        global chart_type
        chart_type = post_params.get('chartType')

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = json.dumps({'success': 'Chart type set successfully'})
        self.wfile.write(response.encode())

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
