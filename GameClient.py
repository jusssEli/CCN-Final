from pynput import keyboard
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

    pressed_keys = set()
    startPressed = False

    def on_press(key):
        nonlocal startPressed
        try:
            k = key.char
        except AttributeError:
            k = key.name  # Special keys (like arrows)

        if k == 'space' and not startPressed:
            client_socket.send('space'.encode())
            startPressed = True

        pressed_keys.add(k)

    def on_release(key):
        try:
            k = key.char
        except AttributeError:
            k = key.name
        if k in pressed_keys:
            pressed_keys.remove(k)

    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    listener.start()

    try:
        while True:
            movement_keys = []
            if choice == "1":
                if 'w' in pressed_keys:
                    movement_keys.append('w')
                if 'a' in pressed_keys:
                    movement_keys.append('a')
                if 's' in pressed_keys:
                    movement_keys.append('s')
                if 'd' in pressed_keys:
                    movement_keys.append('d')
            elif choice == "2":
                if 'up' in pressed_keys:
                    movement_keys.append('w')
                if 'left' in pressed_keys:
                    movement_keys.append('a')
                if 'down' in pressed_keys:
                    movement_keys.append('s')
                if 'right' in pressed_keys:
                    movement_keys.append('d')

            if movement_keys:
                client_socket.send(''.join(movement_keys).encode())

            time.sleep(0.001)

    except KeyboardInterrupt:
        print("Disconnecting...")
        client_socket.close()
        listener.stop()

if __name__ == "__main__":
    client_program()
