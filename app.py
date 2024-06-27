from flask import Flask, request, render_template, redirect, url_for, flash, session
from crypto import generate_key, encrypt_message, decrypt_message
from twilio.rest import Client
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Twilio configuration (replace with your actual credentials)
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
    
    # Generate a new AES key and store it in the session
    key = generate_key()
    session['encryption_key'] = key
    
    # Encrypt the message
    encrypted_message = encrypt_message(key, message)
    
    # Send the encrypted message via SMS
    client.messages.create(
        body=f"encry: {encrypted_message}",
        from_=TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    
    flash('Message sent successfully!', 'success')  # 'success' is a category for Bootstrap styling
    return redirect(url_for('index'))

@app.route('/decrypt', methods=['POST'])
def decrypt():
    encrypted_message = request.form['encrypted_message']
    
    try:
        # Retrieve the key from the session
        key = session.get('encryption_key')
        if not key:
            flash('No encryption key found in session. Cannot decrypt message.', 'danger')  # 'danger' for error messages
            return redirect(url_for('index'))
        
        # Decrypt the message
        decrypted_message = decrypt_message(key, encrypted_message)
        flash(f'Decrypted message: {decrypted_message}', 'info')  # 'info' for informational messages
        return render_template('index.html', decrypted_message=decrypted_message)
    except Exception as e:
        flash('Failed to decrypt message. Please check the encrypted text and try again.', 'danger')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
