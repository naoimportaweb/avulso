#script: /tmp/proxy.py
import socket
import threading

index = 1;

def handle_client_request(client_socket):
    global index;
    request = b''
    
    client_socket.setblocking(False)
    while True:
        try:
            data = client_socket.recv(1024)
            request = request + data
        except:
            break
    host_string_start = request.find(b'Host: ') + len(b'Host: ');
    host_string_end = request.find(b'\r\n', host_string_start);
    host_string = request[host_string_start:host_string_end].decode('utf-8').strip();
    if len(host_string.strip()) > 0:
        print( str(index), "\t", host_string.strip() );
        index += 1;
    client_socket.close()

def start_proxy_server():
    port = 8888
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', port))
    server.listen(10)
    print(f"Proxy server listening on port {port}...")
    while True:
        client_socket, addr = server.accept()
        client_handler = threading.Thread(target=handle_client_request, args=(client_socket,))
        client_handler.start()
if __name__ == "__main__":
    start_proxy_server()

#export http_proxy='http://127.0.0.1:8888'    
#export https_proxy='https://127.0.0.1:8888'
