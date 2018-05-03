from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__, template_folder="templates")
socketio = SocketIO(app, async_mode=None)  # Async mode will be handled automatically

# Load configuration from config.cfg
app.config.from_pyfile('config.cfg')
# Push the app configuration to the app context for it to be available to the submodules.
app.app_context().push()

if __name__ == "__main__":
    app.debug = True
    socketio.run(app)
