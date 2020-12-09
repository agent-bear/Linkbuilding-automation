from flask import Flask, request, render_template, jsonify
import backend
import threading, webbrowser

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('main.html')


@app.route('/req', methods= ["POST"])
def responseFunc():
    req_data = request.get_json()
    backend.requestLinks(req_data)
    return "data received!"

if __name__ == "__main__":
    threading.Timer(1, lambda: backend.init()).start()
    app.run(debug=False, port="8080")