from flask import Flask, request, render_template, redirect, url_for, flash
from crypto import generate_key, encrypt_message, decrypt_message
import os
from twilio.rest import Client

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Twilio configuration
TWILIO_ACCOUNT_SID = 'AC4c8f8d846d39633fd21704a1fadcaf18'
TWILIO_AUTH_TOKEN = 'b6fbd0661e7b58425108043682039514'
TWILIO_PHONE_NUMBER = '+17622206066'
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_message():
    phone_number = request.form['phone_number']
    message = request.form['message']
    
    # Generate a new AES key
    key = generate_key()
    
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
        # Normally we would need the same key used for encryption to decrypt.
        # As we're generating a new key for each encryption, we cannot decrypt previously sent messages.
        flash('Decryption is not supported as keys are not stored.')
    except Exception as e:
        flash('Failed to decrypt message. Please check the encrypted text and try again.')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
