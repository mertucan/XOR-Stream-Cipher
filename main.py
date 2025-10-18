import random
import base64

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

def encrypt(plaintext: str, seed: int) -> str:
    """Encrypts a plaintext string using a seed."""
    plaintext_bytes = plaintext.encode('utf-8')
    key_stream = generate_key_stream(seed, len(plaintext_bytes))
    ciphertext_bytes = xor_bytes(plaintext_bytes, key_stream)
    # Encode the result in Base64 to make it a printable string
    return base64.b64encode(ciphertext_bytes).decode('utf-8')

def decrypt(ciphertext_b64: str, seed: int) -> str:
    """Decrypts a Base64 encoded ciphertext string using a seed."""
    ciphertext_bytes = base64.b64decode(ciphertext_b64)
    key_stream = generate_key_stream(seed, len(ciphertext_bytes))
    plaintext_bytes = xor_bytes(ciphertext_bytes, key_stream)
    return plaintext_bytes.decode('utf-8')

def main():
    """Main function to run the command-line interface for the cipher."""
    while True:
        print("\n--- XOR Stream Cipher ---")
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            text = input("Enter the text to encrypt: ")
            try:
                seed = int(input("Enter the seed (integer key): "))
                encrypted = encrypt(text, seed)
                print(f"\nEncrypted text (Base64): {encrypted}")
            except ValueError:
                print("Invalid seed. Please enter an integer.")
        elif choice == '2':
            text = input("Enter the Base64 text to decrypt: ")
            try:
                seed = int(input("Enter the seed (integer key): "))
                decrypted = decrypt(text, seed)
                print(f"\nDecrypted text: {decrypted}")
            except ValueError:
                print("Invalid seed. Please enter an integer.")
            except Exception as e:
                print(f"An error occurred during decryption: {e}")
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please choose 1, 2, or 3.")

if __name__ == "__main__":
    main()
