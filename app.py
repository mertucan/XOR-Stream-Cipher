from flask import Flask, render_template, request, jsonify
import random
import base64
import hashlib
import secrets

app = Flask(__name__)

def generate_key_stream(seed: str, length: int) -> bytes:
    """Generates a pseudo-random key stream of a given length from a string seed."""
    # Use SHA-256 to create a deterministic seed integer from the string
    hasher = hashlib.sha256(seed.encode('utf-8'))
    seed_int = int.from_bytes(hasher.digest(), 'big')
    
    random.seed(seed_int)
    key_stream = bytearray()
    for _ in range(length):
        key_stream.append(random.randint(0, 255))
    return bytes(key_stream)

def xor_bytes(data: bytes, key_stream: bytes) -> bytes:
    """Performs XOR operation between two byte streams."""
    return bytes([b ^ k for b, k in zip(data, key_stream)])

def encrypt(plaintext: str, seed: str) -> dict:
    """Encrypts a plaintext string and returns the result along with process steps."""
    steps = []
    
    steps.append(f"Orijinal Metin: '{plaintext}'")
    
    plaintext_bytes = plaintext.encode('utf-8')
    steps.append(f"1. Metin baytlara dönüştürüldü: {plaintext_bytes.hex()}")
    
    key_stream = generate_key_stream(seed, len(plaintext_bytes))
    steps.append(f"2. '{seed}' anahtarı kullanılarak anahtar akışı oluşturuldu: {key_stream.hex()}")
    
    ciphertext_bytes = xor_bytes(plaintext_bytes, key_stream)
    steps.append(f"3. XOR işlemi uygulandı: {ciphertext_bytes.hex()}")

    result_b64 = base64.b64encode(ciphertext_bytes).decode('utf-8')
    steps.append(f"4. Sonuç Base64 formatına kodlandı: {result_b64}")
    
    return {"result": result_b64, "steps": steps}

def decrypt(ciphertext_b64: str, seed: str) -> dict:
    """Decrypts a Base64 encoded string and returns the result along with process steps."""
    steps = []

    steps.append(f"Orijinal Base64 Metin: '{ciphertext_b64}'")

    try:
        ciphertext_bytes = base64.b64decode(ciphertext_b64)
        steps.append(f"1. Base64 formatından çözüldü: {ciphertext_bytes.hex()}")
    except Exception as e:
        # Stop and return error if Base64 is invalid
        return {"error": f"Geçersiz Base64 formatı: {e}"}

    key_stream = generate_key_stream(seed, len(ciphertext_bytes))
    steps.append(f"2. '{seed}' anahtarı kullanılarak anahtar akışı oluşturuldu: {key_stream.hex()}")

    plaintext_bytes = xor_bytes(ciphertext_bytes, key_stream)
    steps.append(f"3. XOR işlemi uygulandı: {plaintext_bytes.hex()}")

    try:
        result_text = plaintext_bytes.decode('utf-8')
        steps.append(f"4. Baytlar metne dönüştürüldü: '{result_text}'")
        return {"result": result_text, "steps": steps}
    except UnicodeDecodeError:
        # If decoding fails, it means the result is not valid text.
        # Return an error immediately instead of showing steps.
        error_message = "Şifre Çözme Başarısız: Çıktı okunabilir bir metin değil. Bu genellikle yanlış anahtar (seed) kullanıldığında veya şifreli metin değiştirildiğinde meydana gelir."
        return {"error": error_message}


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate-seed', methods=['GET'])
def generate_seed():
    """Generates a cryptographically secure random seed."""
    return jsonify({"seed": secrets.token_hex(16)})

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    text = data.get('text')
    seed = data.get('seed')
    operation = data.get('operation')
    response = {}

    if not text or not seed:
        response = {"error": "Lütfen hem metni hem de anahtarı girin."}
    else:
        try:
            if operation == 'encrypt':
                response = encrypt(text, seed)
            elif operation == 'decrypt':
                response = decrypt(text, seed)
        except Exception as e:
            response = {"error": f"Bir hata oluştu: {e}"}
            
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
