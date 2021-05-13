from flask import Flask, render_template
from flask_socketio import SocketIO
import os
import sys

def init_webhooks(base_url):
    # Update inbound traffic via APIs to use the public-facing ngrok URL
    pass

def create_ngrok_app():
    app = Flask(__name__)
    # Initialize our ngrok settings into Flask
    app.config.from_mapping(
        BASE_URL="http://localhost:5000",
        USE_NGROK=os.environ.get("WERKZEUG_RUN_MAIN") != "true"
    )

    if app.config["USE_NGROK"]:
        # pyngrok will only be installed, and should only ever be initialized, in a dev environment
        from pyngrok import ngrok

        # Get the dev server port (defaults to 5000 for Flask, can be overridden with `--port`
        # when starting the server
        port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else 5000

        # Open a ngrok tunnel to the dev server
        public_url = ngrok.connect(port).public_url
        print(" * ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port))

        # Update any base URLs or webhooks to use the public ngrok URL
        app.config["BASE_URL"] = public_url
        init_webhooks(public_url)

    # ... Initialize Blueprints and the rest of our app

    return app
    
app = create_ngrok_app()
socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on('messages')
def handle_messages(json):
    print('received json: ' + str(json))
    for i in range(10):
        emit("messages","I am Alive")
    return 'hello'

def emit(event_name,data):
    socketio.emit(event_name, data)

if __name__ == '__main__':
    socketio.run(app)
