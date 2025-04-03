from flask import Flask, request, jsonify
import gnupg
import os

app = Flask(__name__)
gpg = gnupg.GPG()

@app.route('/')
def hello_world():
    return "Hello, World"

@app.route('/encrypt', methods=['GET', 'POST'])
def encrypt():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files['file']
        key_data = file.read().decode()

        # Import public key
        import_result = gpg.import_keys(key_data)
        if not import_result.fingerprints:
            return jsonify({"error": "Invalid GPG key"}), 400

        fingerprint = import_result.fingerprints[0]
        message = "Hello, this is your encrypted message!"

        # Encrypt message
        encrypted_data = gpg.encrypt(message, fingerprint)

        if not encrypted_data.ok:
            return jsonify({"error": "Encryption failed"}), 500

        return '<pre>' +  str(encrypted_data) + '</pre>' 

    else:
        return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
            <input type=file name=file>
            <input type=submit value=Upload>
        </form>
        '''
