#!/usr/bin/env python3
"""
Simple JSON-RPC Server for PDF Form Filling
This server can be called by OpenRPC MCP
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from enhanced_pdf_filler_v2 import handle_pdf_request

class JSONRPCHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Read the request
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            # Parse JSON-RPC request
            request = json.loads(post_data.decode('utf-8'))
            
            # Log the request
            print(f"Received request: {json.dumps(request, indent=2)}", file=sys.stderr)
            
            # Handle the method
            if request.get('method') == 'fillPharmaCareForm':
                # Extract parameters
                params = request.get('params', {})
                
                # Call the PDF filler
                result = handle_pdf_request(params)
                
                # Send JSON-RPC response
                response = {
                    "jsonrpc": "2.0",
                    "result": result,
                    "id": request.get('id')
                }
            else:
                # Method not found
                response = {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32601,
                        "message": "Method not found"
                    },
                    "id": request.get('id')
                }
                
        except Exception as e:
            # Error response
            response = {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32603,
                    "message": str(e)
                },
                "id": request.get('id', None)
            }
        
        # Send response
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def log_message(self, format, *args):
        # Log to stderr
        sys.stderr.write("%s - - [%s] %s\n" %
                         (self.address_string(),
                          self.log_date_time_string(),
                          format%args))

def run_server(port=8080):
    server_address = ('localhost', port)
    httpd = HTTPServer(server_address, JSONRPCHandler)
    print(f"JSON-RPC Server running on http://localhost:{port}", file=sys.stderr)
    print(f"Method: fillPharmaCareForm", file=sys.stderr)
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()