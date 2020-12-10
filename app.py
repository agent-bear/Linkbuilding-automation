from flask import Flask, request, render_template, jsonify
import backend
import threading

app = Flask(__name__)

#renders the main webpage for your browser
@app.route('/')
def index():
    return render_template('main.html')

#gets the post request and starts the link requesting with the received data
@app.route('/req', methods= ["POST"])
def responseFunc():
    req_data = request.get_json()
    backend.requestLinks(req_data)
    return "data received!"

#starts the webpage and loads the webpage in the automated browser
if __name__ == "__main__":
    threading.Timer(1, lambda: backend.init()).start()
    app.run(debug=False, port="8080")