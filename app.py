from flask import Flask, render_template, request, jsonify
import random
import time

app = Flask(__name__)

current_otp = None
otp_expiry = None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate_otp():
    global current_otp, otp_expiry

    current_otp = str(random.randint(100000, 999999))
    otp_expiry = time.time() + 60

    return jsonify({
        "success": True,
        "otp": current_otp,
        "expires_in": 60
    })


@app.route("/verify", methods=["POST"])
def verify_otp():
    global current_otp, otp_expiry

    data = request.get_json()
    entered_otp = data.get("otp", "")

    if current_otp is None:
        return jsonify({
            "success": False,
            "message": "Generate an OTP first."
        })

    if time.time() > otp_expiry:
        current_otp = None
        return jsonify({
            "success": False,
            "message": "OTP expired."
        })

    if entered_otp == current_otp:
        current_otp = None
        return jsonify({
            "success": True,
            "message": "OTP verified successfully!"
        })

    return jsonify({
        "success": False,
        "message": "Invalid OTP."
    })


import os

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )