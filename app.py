from flask import Flask, render_template, request, jsonify
import random
import base64

app = Flask(__name__)

def generate_key_stream(seed: int, length: int) -> bytes:
    """Generates a pseudo-random key stream of a given length from a seed."""
    random.seed(seed)
    key_stream = bytearray()
    for _ in range(length):
        key_stream.append(random.randint(0, 255))
    return bytes(key_stream)

def xor_bytes(data: bytes, key_stream: bytes) -> bytes:
    """Performs XOR operation between two byte streams."""
    return bytes([b ^ k for b, k in zip(data, key_stream)])

def encrypt(plaintext: str, seed: int) -> dict:
    """Encrypts a plaintext string and returns the result along with process steps."""
    steps = []
    
    steps.append(f"Original Text: '{plaintext}'")
    
    plaintext_bytes = plaintext.encode('utf-8')
    steps.append(f"1. Converted to bytes: {plaintext_bytes}")
    
    key_stream = generate_key_stream(seed, len(plaintext_bytes))
    steps.append(f"2. Generated key stream with seed {seed}: {key_stream}")
    
    ciphertext_bytes = xor_bytes(plaintext_bytes, key_stream)
    steps.append(f"3. Performed XOR operation: {ciphertext_bytes}")

    result_b64 = base64.b64encode(ciphertext_bytes).decode('utf-8')
    steps.append(f"4. Encoded result to Base64: {result_b64}")
    
    return {"result": result_b64, "steps": steps}

def decrypt(ciphertext_b64: str, seed: int) -> dict:
    """Decrypts a Base64 encoded string and returns the result along with process steps."""
    steps = []

    steps.append(f"Original Base64 Text: '{ciphertext_b64}'")

    try:
        ciphertext_bytes = base64.b64decode(ciphertext_b64)
        steps.append(f"1. Decoded from Base64: {ciphertext_bytes}")
    except Exception as e:
        # Stop and return error if Base64 is invalid
        return {"error": f"Invalid Base64 format: {e}"}

    key_stream = generate_key_stream(seed, len(ciphertext_bytes))
    steps.append(f"2. Generated key stream with seed {seed}: {key_stream}")

    plaintext_bytes = xor_bytes(ciphertext_bytes, key_stream)
    steps.append(f"3. Performed XOR operation: {plaintext_bytes}")

    try:
        result_text = plaintext_bytes.decode('utf-8')
        steps.append(f"4. Decoded bytes to text: '{result_text}'")
        return {"result": result_text, "steps": steps}
    except UnicodeDecodeError:
        # If decoding fails, it means the result is not valid text.
        # Return an error immediately instead of showing steps.
        error_message = "Decryption Failed: The output is not readable text. This commonly occurs if the wrong seed (key) is used or the encrypted text has been altered."
        return {"error": error_message}


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    text = data.get('text')
    seed_str = data.get('seed')
    operation = data.get('operation')
    response = {}

    if not text or not seed_str:
        response = {"error": "Please provide both text and a seed."}
    else:
        try:
            seed = int(seed_str)
            if operation == 'encrypt':
                response = encrypt(text, seed)
            elif operation == 'decrypt':
                response = decrypt(text, seed)
        except ValueError:
            response = {"error": "Seed must be an integer."}
        except Exception as e:
            response = {"error": f"An error occurred: {e}"}
            
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
