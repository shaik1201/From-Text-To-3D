from flask import Flask, render_template, request, session
import subprocess
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_model', methods=['POST'])
def generate_model():
    # ********* TO DO: Get user input from the form ***********
    # data = request.form['user_input']

    # run create_obj_file.py and present the object
    result = subprocess.run(["python", "create_obj_file.py"], capture_output=True, text=True)
    if result.returncode == 0:
        output = result.stdout  # captured output from the subprocess
        result_data = json.loads(output)
        params = result_data['params']
        num_of_params = result_data['num_of_params']
        session['params'] = params
        session['num_of_params'] = num_of_params
    else:
        error = result.stderr 
        print(error)
    return render_template('show_obj.html')

@app.route('/modify_model', methods=['POST'])
def modify_model():
    params = session.get('params')
    num_of_params = session.get('num_of_params')
    return render_template('modify_model.html', params=params, num_of_params=num_of_params)

@app.route('/modified_model', methods=['POST'])
def modified_model():
    sliders_values = {}
    params = session.get('params')
    for param in params:
        sliders_values[param] = request.form.get(f"{param}_value")
    
    print(sliders_values)
    subprocess.run(["python", "create_obj_file.py", json.dumps(sliders_values)], capture_output=True, text=True)

    return render_template('show_obj.html')

@app.route('/generate_gcode', methods=['POST'])
def generate_gcode():

    # receive the gcode and send it to the template
    return render_template('gcode.html')

@app.route('/object', methods=['GET'])
def present_obj():

    return render_template('present_obj.html')

if __name__ == '__main__':
    app.run(debug=True)
