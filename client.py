import json
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('127.0.0.1', 7777)

print(f'Connecting to {server_address[0]} port {server_address[1]} ...')
print('- Print \'exit\' to quit')
print("- Query example: select first_name email ip_address")

client_socket.connect(server_address)

while True:
    message = input("~$ query: ")
    print('Please wait for response, sending: {}'.format(message))
    client_socket.sendall(message.encode())
    if message == 'exit':
        print('Exiting...')
        client_socket.send(b"exit")
        client_socket.close()
        break
    received_value = ''
    while True:
        data = client_socket.recv(1024)
        data_received = data.decode()
        if "#done" in data_received:
            received_value = received_value + data_received.replace('#done', '')
            break
        received_value = received_value + data_received
    datas = json.loads(received_value)
    for element in datas:
        print(element)