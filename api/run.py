from src import app, socket

if __name__ == '__main__':
    socket.run(app, debug = True, host = '127.0.0.1')