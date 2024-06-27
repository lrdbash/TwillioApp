from flask import Flask, request, render_template, redirect, url_for, flash
from crypto import encrypt_message, decrypt_message
import os
from twilio.rest import Client

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'your_default_secret_key')

# Twilio configuration
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Load the encryption key from an environment variable
key = os.environ.get('ENCRYPTION_KEY')
if not key:
    raise ValueError("No encryption key set in environment variables")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_message():
    phone_number = request.form['phone_number']
    message = request.form['message']

    # Encrypt the message
    encrypted_message = encrypt_message(key, message)
    
    # Send the encrypted message via SMS
    client.messages.create(
        body=f"encry: {encrypted_message}",
        from_=TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    
    flash('Message sent successfully!')
    return redirect(url_for('index'))

@app.route('/decrypt', methods=['POST'])
def decrypt():
    encrypted_message = request.form['encrypted_message']
    
    try:
        # Decrypt the message
        decrypted_message = decrypt_message(key, encrypted_message)
        flash(f'Decrypted message: {decrypted_message}')
    except Exception as e:
        flash('Failed to decrypt message. Please check the encrypted text and try again.')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
