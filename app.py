from flask import Flask, request, render_template, redirect, url_for, flash
from crypto import generate_key, load_key, encrypt_message, decrypt_message
import os
from twilio.rest import Client

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Twilio configuration
TWILIO_ACCOUNT_SID = 'AC4c8f8d846d39633fd21704a1fadcaf18'
TWILIO_AUTH_TOKEN = '902247870fbc0dbda9506a3a485462f3'
TWILIO_PHONE_NUMBER = '+17622206066'
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Generate and store encryption key if it doesn't exist
if not os.path.exists('aes_key.bin'):
    generate_key()

@app.route('/')
def index():
    print("Rendering index.html")
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_message():
    phone_number = request.form['phone_number']
    message = request.form['message']
    print(f"Received phone number: {phone_number}")
    print(f"Received message: {message}")

    # Load the key
    print("Loading encryption key...")
    key = load_key()


    # Encrypt the message
    print("Encrypting message...")
    encrypted_message = encrypt_message(key, message)
    print(f"Encrypted message: {encrypted_message}")

    # Send the encrypted message via SMS
    print("Sending encrypted message via SMS...")
    client.messages.create(
        body=f"encry: {encrypted_message}",
        from_=TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    print("Message sent successfully!")

    flash('Message sent successfully!')
    return redirect(url_for('index'))

@app.route('/decrypt', methods=['POST'])
def decrypt():
    encrypted_message = request.form['encrypted_message']
    print(f"Received encrypted message: {encrypted_message}")

    try:
        # Load the key
        print("Loading encryption key...")
        key = load_key()


        # Decrypt the message
        print("Decrypting message...")
        decrypted_message = decrypt_message(key, encrypted_message)
        print(f"Decrypted message: {decrypted_message}")

        flash(f'Decrypted message: {decrypted_message}')
    except Exception as e:
        print(f"Error during decryption: {e}")
        flash('Failed to decrypt message. Please check the encrypted text and try again.')

    return redirect(url_for('index'))

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(debug=True)
