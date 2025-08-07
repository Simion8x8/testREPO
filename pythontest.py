from flask import Flask,request,render_template,jsonify
import platform
import psutil
import time
import configparser
import os
import requests

def elapsed_time():
    return ((time.time() - psutil.boot_time())/60.0)

def percentage_memory():
    return psutil.virtual_memory().available *100 / (psutil.virtual_memory().total)

def cpu_available():
    return 100-psutil.cpu_percent()

app = Flask(__name__)

@app.route('/system')
def hello_world():
    return jsonify(processor = platform.processor(),
		architecture = platform.architecture(), 
		system = platform.system(), 
		av_mem = percentage_memory(),
		cpu_av = cpu_available(),
		elapsed_time=elapsed_time())

@app.route('/health',methods=['GET'])
def health_status():
    headers = {'Content-Type': 'application/json'}
    response = requests.get("http://localhost:5000/system", headers = headers)
    if response.status_code == 200:
	    return jsonify(health = "OK")
    else:
	    return jsonify(health = "BAD") 


@app.route('/calculate/<int:n>')
def calculate(n):
    fib0 = 0
    fib1 = 1
    while n > 0:
        temp = fib0 + fib1
        fib0 = fib1
        fib1 = temp
        n = n - 1
    return jsonify(fibo=fib0)


@app.route('/config/<value>')
def config(value):
	config = configparser.ConfigParser()
	ini_path = os.path.join(os.getcwd(),'config.ini')
	config.read(ini_path)
	ch0_before = config.get('ABC','ch0')
	config.set('ABC','ch0',value)
	ch0 = config.get('ABC','ch0')
	return jsonify(before=ch0_before,result=ch0)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
