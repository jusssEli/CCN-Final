import keyboard
import socket
import time

def client_program():
    print("Trying to connect to server...")
    host = "192.168.1.164"
    port = 5000

    client_socket = socket.socket()
    client_socket.connect((host, port))
    print("Connected.")

    startPressed = False

    try:
        while True:
            keys = []

            if keyboard.is_pressed('space') and not startPressed:
                client_socket.send('space'.encode())
                startPressed = True

            # Collect all pressed movement keys
            if keyboard.is_pressed('w'):
                keys.append('w')
            if keyboard.is_pressed('a'):
                keys.append('a')
            if keyboard.is_pressed('s'):
                keys.append('s')
            if keyboard.is_pressed('d'):
                keys.append('d')

            if keys:
                # Send combined input like "ws" or "ad"
                movement = ''.join(keys)
                client_socket.send(movement.encode())

            time.sleep(0.01)  # 10ms loop delay for smooth input

    except KeyboardInterrupt:
        client_socket.close()

client_program()
