import http.server
import socketserver
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

PORT = 25532
httpd = None
observer = None

class ReloadHandler(FileSystemEventHandler):
    def __init__(self, server, root_path):
        self.server = server
        self.root_path = root_path
        self.ignore_dirs = {'.git'}

    def on_any_event(self, event):
        # Log events for debugging
        # print(f"Event type: {event.event_type} - Path: {event.src_path}")

        # Get the directory of the changed file
        dir_name = os.path.dirname(os.path.relpath(event.src_path, self.root_path))

        # Check if the directory is in the ignore list
        if dir_name in self.ignore_dirs:
            return

        # Check if the event is in the root directory or its subdirectories
        if event.event_type in ('modified', 'created', 'deleted'):
            # Convert the path to relative path
            relative_path = os.path.relpath(event.src_path, self.root_path)
            # Ensure that the event is for the root or its subdirectories
            if not os.path.isabs(relative_path):  # Ensure it's a relative path
                print("Change detected, restarting server...")
                self.restart_server()

    def restart_server(self):
        # Shutdown the current server
        if self.server:
            self.server.shutdown()
            self.server.server_close()

        # Brief delay to ensure the port is released
        time.sleep(1)
        
        # Restart the server
        start_server()

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)

    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def start_server():
    global httpd, observer
    root_path = os.getcwd()
    handler = MyHttpRequestHandler

    try:
        httpd = socketserver.TCPServer(("", PORT), handler)
        print(f"Serving on port {PORT}")

        # Set up the watchdog observer
        #event_handler = ReloadHandler(httpd, root_path)
        #observer = Observer()
        #observer.schedule(event_handler, path=root_path, recursive=True)
        #observer.start()

        httpd.serve_forever()
    except OSError as e:
        if e.errno == 98:  # Address already in use
            print("Address already in use. Retrying...")
            time.sleep(5)  # Wait before retrying
            start_server()
    except KeyboardInterrupt:
        print("Shutting down server...")
    finally:
        stop_server()

def stop_server():
    global httpd, observer
    if httpd:
        httpd.server_close()  # Ensure the server is properly closed
#    if observer:
#        observer.stop()
#        observer.join()

if __name__ == "__main__":
    start_server()
