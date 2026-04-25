from flask import Flask, render_template, jsonify, request
import time

app = Flask(__name__)

# Estado dos dispositivos (persistido em memória - em produção use banco)
device_states = {
    "tv": {"on": True, "volume": 28, "channel": 7},
    "ac": {"on": True, "temp": 24, "mode": 0, "fan": 2},  # mode: 0=frio,1=quente,2=ventilar,3=secar,4=auto
    "garage": {"open": False}
}

@app.route("/")
def index():
    return render_template("index.html")

# ====================== API TV ======================
@app.route("/api/tv/status", methods=["GET"])
def tv_status():
    return jsonify({"success": True, "state": device_states["tv"]})

@app.route("/api/tv/power", methods=["POST"])
def tv_power():
    device_states["tv"]["on"] = not device_states["tv"]["on"]
    return jsonify({"success": True, "message": "TV alterada", "state": device_states["tv"]})

@app.route("/api/tv/volume", methods=["POST"])
def tv_volume():
    action = request.json.get("action")
    if action == "up" and device_states["tv"]["volume"] < 100:
        device_states["tv"]["volume"] += 2
    elif action == "down" and device_states["tv"]["volume"] > 0:
        device_states["tv"]["volume"] -= 2
    return jsonify({"success": True, "state": device_states["tv"]})

@app.route("/api/tv/mute", methods=["POST"])
def tv_mute():
    device_states["tv"]["volume"] = 0 if device_states["tv"]["volume"] > 0 else 28
    return jsonify({"success": True, "state": device_states["tv"]})

@app.route("/api/tv/channel", methods=["POST"])
def tv_channel():
    action = request.json.get("action")
    if action == "up":
        device_states["tv"]["channel"] = (device_states["tv"]["channel"] % 20) + 1
    elif action == "down":
        device_states["tv"]["channel"] = 20 if device_states["tv"]["channel"] == 1 else device_states["tv"]["channel"] - 1
    return jsonify({"success": True, "state": device_states["tv"]})

@app.route("/api/tv/input", methods=["POST"])
def tv_input():
    return jsonify({"success": True, "message": "Entrada alterada para HDMI 1"})

# ====================== API AR CONDICIONADO ======================
@app.route("/api/ac/status", methods=["GET"])
def ac_status():
    return jsonify({"success": True, "state": device_states["ac"]})

@app.route("/api/ac/power", methods=["POST"])
def ac_power():
    device_states["ac"]["on"] = not device_states["ac"]["on"]
    return jsonify({"success": True, "message": "Ar-condicionado alterado", "state": device_states["ac"]})

@app.route("/api/ac/temp", methods=["POST"])
def ac_temp():
    action = request.json.get("action")
    if action == "up" and device_states["ac"]["temp"] < 30:
        device_states["ac"]["temp"] += 1
    elif action == "down" and device_states["ac"]["temp"] > 16:
        device_states["ac"]["temp"] -= 1
    return jsonify({"success": True, "state": device_states["ac"]})

@app.route("/api/ac/mode", methods=["POST"])
def ac_mode():
    mode = request.json.get("mode")
    if 0 <= mode <= 4:
        device_states["ac"]["mode"] = mode
    return jsonify({"success": True, "state": device_states["ac"]})

@app.route("/api/ac/fan", methods=["POST"])
def ac_fan():
    device_states["ac"]["fan"] = (device_states["ac"]["fan"] % 3) + 1
    return jsonify({"success": True, "state": device_states["ac"]})

# ====================== API GARAGEM ======================
@app.route("/api/garage/status", methods=["GET"])
def garage_status():
    return jsonify({"success": True, "state": device_states["garage"]})

@app.route("/api/garage/toggle", methods=["POST"])
def garage_toggle():
    device_states["garage"]["open"] = not device_states["garage"]["open"]
    time.sleep(0.8)  # simula tempo real do motor
    return jsonify({"success": True, "message": "Portão em movimento", "state": device_states["garage"]})

@app.route("/api/garage/stop", methods=["POST"])
def garage_stop():
    return jsonify({"success": True, "message": "Movimento parado"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)