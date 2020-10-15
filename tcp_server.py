import socket

from parser import parse_data, select_from_file

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ('127.0.0.1', 7777)
print('Getting data from server...')
server_socket.bind(server_address)
parse_data()
print('Done!')

while True:
    server_socket.listen(4)
    print('Server is waiting for connections...')
    (connection, server_address) = server_socket.accept()

    while True:
        data = connection.recv(2048).decode()
        print("Server recieved data: ", data)
        if data == 'exit':
            connection.close()
            break
        elif 'select' not in data:
            continue
        result = select_from_file(data)
        print('Sending to client result: ', result)
        connection.sendall(result.encode())
        connection.send(b"#yepyep")
