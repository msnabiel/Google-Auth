import os
import pathlib
import requests
from flask import Flask, session, abort, redirect, request
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

app = Flask("Google Login App")
app.secret_key = "YOUR_KEY" # make sure this matches with that's in client_secret.json

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" # to allow Http traffic for local dev

GOOGLE_CLIENT_ID = "YOUR_CLIENT_ID"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://localhost:8501/auth"
)


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper


@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url(prompt='consent')    # Remove prompt='consent' for autologin
    session["state"] = state
    return redirect(authorization_url)


@app.route("/auth")
def auth():
    try:
        print(f"Request URL: {request.url}")
        print(f"Session State: {session.get('state')}, Received State: {request.args.get('state')}")

        flow.fetch_token(authorization_response=request.url)

        # Verify the state parameter
        if session.get("state") != request.args.get("state"):
            print(f"State mismatch: expected {session.get('state')}, got {request.args.get('state')}")
            abort(500)  # State does not match!

        credentials = flow.credentials
        request_session = requests.session()
        cached_session = cachecontrol.CacheControl(request_session)
        token_request = google.auth.transport.requests.Request(session=cached_session)

        id_info = id_token.verify_oauth2_token(
            id_token=credentials._id_token,
            request=token_request,
            audience=GOOGLE_CLIENT_ID
        )

        print(f"ID Info: {id_info}")  # Debugging output

        session["google_id"] = id_info.get("sub")
        session["name"] = id_info.get("name")
        return redirect("/protected_area")
    except Exception as e:
        print(f"Error in /auth route: {e}")
        abort(500)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/")
def index():
    return "Hello World <a href='/login'><button>Login</button></a>"


@app.route("/protected_area")
@login_is_required
def protected_area():
    return f"Hello {session['name']}! <br/> <a href='/logout'><button>Logout</button></a>"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8501, debug=True)
