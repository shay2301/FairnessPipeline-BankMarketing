import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        data = request.form
        json_data = json.dumps(data)
        print(json_data)
        return json_data  # Return JSON data directly
    return render_template('form.html')

@app.route('/formdata', methods=['GET'])
def form_data():
    data = request.args.to_dict()
    return data


@app.route('/success')
def success():
    return "Form submitted successfully!"

if __name__ == '__main__':
    app.run(debug=True)
