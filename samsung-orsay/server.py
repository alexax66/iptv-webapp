#!/usr/bin/env python3

# This server serves Samsung TV Orsay (pre-Tizen) applications ("widgets")
# without the need for the user to zip them manually.
# Just put each app in one directory each, and run the server.
# Then synchronize with the TV using the "develop" Samsung account.
# This allows for a rapid development and test cycle.
# Note that for a Samsung TV Orsay (pre-Tizen) application ("widget") to work
# properly, it needs to do certain things in onLoad() of its main html page.

import os
import socket
import shutil
import zipfile
from http.server import SimpleHTTPRequestHandler, HTTPServer
from io import BytesIO
import xml.etree.ElementTree as ET
import urllib.parse
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Get the server's IP address
def get_server_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.0.0.0', 1))
        ip = s.getsockname()[0]
    except Exception as e:
        logging.error(f"Failed to get server IP address: {e}")
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

# Get top-level directories containing config.xml
def get_top_level_directories_with_config():
    dirs = []
    try:
        for entry in os.scandir('.'):
            if entry.is_dir():
                config_path = os.path.join(entry.path, 'config.xml')
                if os.path.exists(config_path):
                    dirs.append(entry.path)
    except Exception as e:
        logging.error(f"Error scanning directories: {e}")
    return dirs

# Calculate the size of a directory
def get_directory_size(directory):
    total_size = 0
    try:
        for dirpath, _, filenames in os.walk(directory):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
    except Exception as e:
        logging.error(f"Error calculating directory size for {directory}: {e}")
    return total_size

# Parse the config.xml file to get widget details
def parse_config_xml(directory):
    config_path = os.path.join(directory, 'config.xml')
    try:
        tree = ET.parse(config_path)
        root = tree.getroot()

        # Attempt to find the widgetname element, ignoring namespaces
        widgetname = None
        for elem in root.iter():
            if 'widgetname' in elem.tag:
                widgetname = elem.text
                break

        if widgetname is None:
            raise ValueError("config.xml does not contain widgetname")

        return widgetname
    except ET.ParseError as e:
        logging.error(f"XML parsing error in {config_path}: {e}")
        raise
    except Exception as e:
        logging.error(f"Error reading config.xml in {directory}: {e}")
        raise

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)
        path = parsed_path.path

        if path == '/widgetlist.xml':
            try:
                dirs = get_top_level_directories_with_config()
                server_ip = get_server_ip()

                response = '<?xml version="1.0" encoding="UTF-8"?>\n<rsp stat="ok">\n<list>\n'
                for dir_path in dirs:
                    dir_name = os.path.basename(dir_path)
                    try:
                        widgetname = parse_config_xml(dir_path)
                        size = get_directory_size(dir_path)
                        download_url = f'http://{server_ip}/{dir_name}.zip'
                        response += f'<widget id="{widgetname}">\n'
                        response += f'<title>{widgetname}</title>\n'
                        response += f'<compression type="zip" size="{size}"/>\n'
                        response += f'<description/>\n'
                        response += f'<download>{download_url}</download>\n'
                        response += '</widget>\n'
                    except Exception as e:
                        logging.error(f"Error processing directory {dir_path}: {e}")
                        continue
                response += '</list>\n</rsp>'

                self.send_response(200)
                self.send_header('Content-type', 'application/xml')
                self.end_headers()
                self.wfile.write(response.encode('utf-8'))
            except Exception as e:
                logging.error(f"Error generating widget list: {e}")
                self.send_error(500, 'Internal Server Error')
        elif path.endswith('.zip'):
            dir_name = path.strip('/').replace('.zip', '')
            if os.path.isdir(dir_name):
                try:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/zip')
                    self.send_header('Content-Disposition', f'attachment; filename="{dir_name}.zip"')
                    self.end_headers()

                    with BytesIO() as byte_stream:
                        with zipfile.ZipFile(byte_stream, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                            for root, _, files in os.walk(dir_name):
                                for file in files:
                                    file_path = os.path.join(root, file)
                                    arcname = os.path.relpath(file_path, dir_name)
                                    zip_file.write(file_path, arcname)
                        byte_stream.seek(0)
                        shutil.copyfileobj(byte_stream, self.wfile)
                except Exception as e:
                    logging.error(f"Error creating zip for {dir_name}: {e}")
                    self.send_error(500, 'Internal Server Error')
            else:
                logging.error(f"Requested directory {dir_name} does not exist")
                self.send_error(404, 'File not found')
        else:
            super().do_GET()

if __name__ == '__main__':
    PORT = 80
    try:
        server = HTTPServer(('0.0.0.0', PORT), CustomHandler)
        logging.info(f'Server started at http://{get_server_ip()}:{PORT}')
        server.serve_forever()
    except Exception as e:
        logging.critical(f"Failed to start server: {e}")
