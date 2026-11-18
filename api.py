from flask import Flask, render_template, request
from netmiko import ConnectHandler


app = Flask(__name__)


ROUTER = {
    "device_type": "cisco_ios_telnet",
    "host": "192.168.10.235",
    "port": 32770,
    "username": "admin",
    "password": "eve123",
    "secret": "eve123",
}


COMMANDS = [
    "show version",
    "show ip interface brief",
    "show running-config",
]




@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", results={}, error=None)




@app.route("/connect", methods=["POST"])
def connect():
    results = {}
    error = None
    net_connect = None


    try:
        net_connect = ConnectHandler(**ROUTER)
        net_connect.enable()
        for cmd in COMMANDS:
            results[cmd] = net_connect.send_command(cmd)
    except Exception as e:
        error = f"Connection failed: {e}"
    finally:
        if net_connect:
            net_connect.disconnect()


    return render_template("index.html", results=results, error=error)




if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)