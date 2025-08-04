import http.server
import socketserver
import socket
import threading
import json
import urllib.parse
import mimetypes
from datetime import datetime
from pymongo import MongoClient
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration
HTTP_PORT = 3000
SOCKET_PORT = 5000
SOCKET_HOST = '0.0.0.0'
BUFFER_SIZE = 1024

# MongoDB configuration
MONGO_HOST = os.environ.get('MONGO_HOST', 'localhost')
MONGO_PORT = 27017
DB_NAME = 'messages_db'
COLLECTION_NAME = 'messages'


class HTTPHandler(http.server.BaseHTTPRequestHandler):
    """Custom HTTP request handler"""

    def do_GET(self):
        """Handle GET requests"""
        try:
            # Route mapping
            routes = {
                '/': 'templates/index.html',
                '/message': 'templates/message.html',                '/test': 'templates/test.html',
            }

            # Check if it's a route
            if self.path in routes:
                self.send_html(routes[self.path])
            # Check if it's a static file
            elif self.path.startswith('/static/'):
                file_path = self.path[1:]  # Remove leading slash
                self.send_static(file_path)
            else:
                self.send_error_404()

        except Exception as e:
            logger.error(f"Error in GET request: {e}")
            self.send_error(500, "Internal Server Error")

    def do_POST(self):
        """Handle POST requests"""
        try:
            if self.path == '/message':
                # Read form data
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)

                # Parse form data
                parsed_data = urllib.parse.parse_qs(post_data.decode('utf-8'))

                # Extract username and message
                username = parsed_data.get('username', [''])[0]
                message = parsed_data.get('message', [''])[0]

                if username and message:
                    # Prepare data for socket
                    data = {
                        'username': username,
                        'message': message
                    }

                    # Send to socket server
                    self.send_to_socket(data)

                    # Redirect to home page
                    self.send_response(302)
                    self.send_header('Location', '/')
                    self.end_headers()
                else:
                    self.send_error(400, "Bad Request: Missing username or message")
            else:
                self.send_error_404()

        except Exception as e:
            logger.error(f"Error in POST request: {e}")
            self.send_error(500, "Internal Server Error")

    def send_html(self, filepath):
        """Send HTML file"""
        try:
            with open(filepath, 'rb') as file:
                content = file.read()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error_404()

    def send_static(self, filepath):
        """Send static files"""
        try:
            # Determine content type
            mime_type, _ = mimetypes.guess_type(filepath)
            if not mime_type:
                mime_type = 'application/octet-stream'

            with open(filepath, 'rb') as file:
                content = file.read()

            self.send_response(200)
            self.send_header('Content-type', mime_type)
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error_404()

    def send_error_404(self):
        """Send 404 error page"""
        try:
            with open('templates/error.html', 'rb') as file:
                content = file.read()
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, "Not Found")

    def send_to_socket(self, data):
        """Send data to socket server"""
        try:
            # Create UDP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            # Serialize data
            message = json.dumps(data).encode('utf-8')

            # Send to socket server
            sock.sendto(message, (SOCKET_HOST, SOCKET_PORT))
            sock.close()

            logger.info(f"Sent data to socket server: {data}")
        except Exception as e:
            logger.error(f"Error sending to socket server: {e}")


def run_http_server():
    """Run HTTP server"""
    with socketserver.TCPServer(("0.0.0.0", HTTP_PORT), HTTPHandler) as httpd:
        logger.info(f"HTTP Server running on port {HTTP_PORT}")
        httpd.serve_forever()


def run_socket_server():
    """Run UDP socket server"""
    # Connect to MongoDB
    client = MongoClient(MONGO_HOST, MONGO_PORT)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((SOCKET_HOST, SOCKET_PORT))

    logger.info(f"Socket Server running on port {SOCKET_PORT}")

    while True:
        try:
            # Receive data
            data, addr = sock.recvfrom(BUFFER_SIZE)
            logger.info(f"Received data from {addr}")

            # Parse JSON data
            message_data = json.loads(data.decode('utf-8'))

            # Add timestamp
            message_data['date'] = str(datetime.now())

            # Save to MongoDB
            collection.insert_one(message_data)
            logger.info(f"Saved to MongoDB: {message_data}")

        except Exception as e:
            logger.error(f"Error in socket server: {e}")


def main():
    """Main function to start both servers"""
    # Create threads for both servers
    http_thread = threading.Thread(target=run_http_server, daemon=True)
    socket_thread = threading.Thread(target=run_socket_server, daemon=True)

    # Start both threads
    http_thread.start()
    socket_thread.start()

    logger.info("Both servers started successfully")

    # Keep the main thread alive
    try:
        http_thread.join()
        socket_thread.join()
    except KeyboardInterrupt:
        logger.info("Shutting down servers...")


if __name__ == "__main__":
    main()
