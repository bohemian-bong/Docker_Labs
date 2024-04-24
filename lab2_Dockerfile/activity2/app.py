from flask import Flask
import uuid

app = Flask(__name__)

def generate_ctf_flag():
    # Generate a random UUID
    flag_uuid = str(uuid.uuid4())
    
    # Format the UUID as a CTF flag
    ctf_flag = f"CTF{{{flag_uuid}}}"
    
    return ctf_flag
flag = generate_ctf_flag()
@app.route('/')

def hello():
    return flag

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

