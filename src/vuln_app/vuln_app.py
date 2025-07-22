from flask import Flask, render_template, request, redirect, render_template_string, Response
import base64
import logging
import csv
import os


logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CSV_FILE = 'submissions.csv'

@app.route('/', methods=['GET', 'POST'])
def signup():

    ip = request.remote_addr
    logging.info(f"Access to / from {ip} with Method: {request.method}")

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')

        if name and email:
            if not phone:
                phone = ""
            write_to_csv(name, email, phone)
            return redirect('/preview?name=' + name)
        else:
            return "Missing name and email. Please fill out all mandatory fields.", 400

    return render_template('form.html')

@app.route('/preview')
def preview():
    # Here is the vulnerable use of render_template_string
    ip = request.remote_addr
    logging.info(f"Access to /preview from {ip}")
    
    user_input = request.args.get('name', '')
    template = f"Thanks for signing up {user_input}! We'll contact you soon."
    return render_template_string(template) # SSTI Vulnerability

# https://owasp.org/www-project-web-security-testing-guide/v41/4-Web_Application_Security_Testing/07-Input_Validation_Testing/18-Testing_for_Server_Side_Template_Injection

# You can read files in this folder with this route:
# http://localhost:5000/preview?name={{config.__class__.__init__.__globals__[%27os%27].popen(%27ls%27).read()}}
# Or read the contents of submissions.csv with this route:
# http://localhost:5000/preview?name={{config.__class__.__init__.__globals__[%27os%27].popen(%27cat%20submissions.csv%27).read()}}

def write_to_csv(name, email, phone):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Name', 'Email', 'Phone'])
        writer.writerow([name, email, phone])


API_CREDENTIAL_USER = "Administrator"
API_CREDENTIAL_PASSWORD="Z76E5Q;|AhM6U>kR"
API_CREDENTIAL = f"{API_CREDENTIAL_USER}:{API_CREDENTIAL_PASSWORD}".encode("utf-8")
EXPECTED_AUTH_HEADER = "Basic " + base64.b64encode(API_CREDENTIAL).decode("utf-8")

@app.route('/csv')
def download_csv():
    ip = request.remote_addr
    logging.info(f"Access to /csv from {ip} with Authorization: {request.headers.get('Authorization', 'None')}")

    auth = request.headers.get("Authorization", "")

    if auth != EXPECTED_AUTH_HEADER:
        return Response("Unauthorized", status=401, headers={
            "WWW-Authenticate": 'Basic realm="Lab CSV Download - Authentication Required"'
        })

    try:
        with open(CSV_FILE, 'r') as f:
            return Response(f.read(), mimetype='text/plain')
    except FileNotFoundError:
        return Response("No CSV file found", status=404)
    
    


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
