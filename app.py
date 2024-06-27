from flask import Flask, request, render_template, redirect, url_for, flash
from crypto import generate_key, encrypt_message, decrypt_message
from twilio.rest import Client

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Twilio configuration (replace with your actual Twilio credentials)
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
    
    # Generate a new AES key for this request
    key = generate_key()
    
    # Encrypt the message
    encrypted_message = encrypt_message(key, message)
    
    # Send the encrypted message via SMS along with the key
    client.messages.create(
        body=f"encry: {encrypted_message};key: {key}",
        from_=TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    
    flash('Message sent successfully!')
    return redirect(url_for('index'))

@app.route('/decrypt', methods=['POST'])
def decrypt():
    encrypted_data = request.form['encrypted_data']
    
    try:
        # Extract encrypted message and key from the received data
        encrypted_message, key = parse_encrypted_data(encrypted_data)
        
        # Decrypt the message using the extracted key
        decrypted_message = decrypt_message(key, encrypted_message)
        
        # Flash decrypted message for visibility
        flash(f'Decrypted message: {decrypted_message}')
        return render_template('index.html', decrypted_message=decrypted_message)
    except Exception as e:
        flash('Failed to decrypt message. Please check the encrypted text and try again.')
    
    return redirect(url_for('index'))

def parse_encrypted_data(encrypted_data):
    # This function parses the encrypted data to extract message and key
    parts = encrypted_data.split(';')
    encrypted_message = None
    key = None
    
    for part in parts:
        if part.startswith('encry:'):
            encrypted_message = part.split(':')[1].strip()
        elif part.startswith('key:'):
            key = part.split(':')[1].strip()
    
    return encrypted_message, key

if __name__ == '__main__':
    app.run(debug=True)
