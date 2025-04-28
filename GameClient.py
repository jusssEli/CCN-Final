import keyboard
import socket
import time

def client_program():
    print("Select player:")
    print("1 - Player 1 (WASD)")
    print("2 - Player 2 (Arrow Keys)")
    choice = input("Enter 1 or 2: ")

    host = "10.22.9.83" 
    port = 5000 if choice == "1" else 5001

    client_socket = socket.socket()
    try:
        client_socket.connect((host, port))
        print(f"Connected to server as Player {choice}.")
    except Exception as e:
        print(f"Failed to connect to server: {e}")
        return

    startPressed = False

    def get_movement_keys():
        keys = []
        if choice == "1":
            if keyboard.is_pressed('w'):
                keys.append('w')
            if keyboard.is_pressed('a'):
                keys.append('a')
            if keyboard.is_pressed('s'):
                keys.append('s')
            if keyboard.is_pressed('d'):
                keys.append('d')
        elif choice == "2":
            if keyboard.is_pressed('up'):
                keys.append('w')
            if keyboard.is_pressed('left'):
                keys.append('a')
            if keyboard.is_pressed('down'):
                keys.append('s')
            if keyboard.is_pressed('right'):
                keys.append('d')
        return keys

    try:
        while True:
            if keyboard.is_pressed('space') and not startPressed:
                client_socket.send('space'.encode())
                startPressed = True

            movement_keys = get_movement_keys()
            if movement_keys:
                client_socket.send(''.join(movement_keys).encode())

            time.sleep(0.01)

    except KeyboardInterrupt:
        print("Disconnecting...")
        client_socket.close()

if __name__ == "__main__":
    client_program()