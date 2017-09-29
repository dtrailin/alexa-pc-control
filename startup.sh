cd "$(dirname "$0")"
export FLASK_APP=app.py
flask run &
java -jar amazon-echo-bridge-*.jar --upnp.config.address=128.189.129.9 &
