from src import app, socket, scheduler

if __name__ == '__main__':
    scheduler.init_app(app)
    scheduler.start()
    socket.run(app, debug = True, host = '0.0.0.0', use_reloader = False, port = 8001)
    # use_reloader to False prevents double app initialization of debug mode (that causes issues with the scheduler).