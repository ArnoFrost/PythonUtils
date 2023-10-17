import base64
import hashlib
import hmac
import struct
import time


def pad_output(i, code_length):
    num = str(i)
    while len(num) < code_length:
        num = '0' + num
    return num


def generate_response_code(signer, interval, code_length, pin_modulo):
    # Convert the interval to an 8-byte array
    interval_bytes = struct.pack(">Q", interval)

    # Calculate the HMAC-SHA1 of the interval using the signer
    hmac_result = signer(interval_bytes)

    # Extract the 4-byte dynamic binary code (DBC) from the HMAC result
    dbc = struct.unpack(">I", hmac_result[-4:])[0]

    # Calculate the final response code as an integer between 0 and 999999
    response_code = dbc & 0x7FFFFFFF % 1000000

    # Pad the response code with leading zeros to ensure it's code_length digits long
    response_code_str = pad_output(response_code, code_length)

    return response_code_str


def rc4_decrypt(ciphertext, key):
    key = key.encode('utf-8')
    s = list(range(256))
    j = 0
    for i in range(256):
        j = (j + s[i] + key[i % len(key)]) % 256
        s[i], s[j] = s[j], s[i]

    i = j = 0
    plaintext = bytearray(len(ciphertext))
    for char in ciphertext:
        i = (i + 1) % 256
        j = (j + s[i]) % 256
        s[i], s[j] = s[j], s[i]
        k = s[(s[i] + s[j]) % 256]
        char_int = char if isinstance(char, int) else ord(char)  # Convert char to int
        plaintext.append(char_int ^ k)

    return plaintext


def decode_and_decrypt(access_token, encoded_data):
    # 1. Calculate MD5 hash of access_token
    md5_hash = hashlib.md5(access_token.encode('utf-8')).hexdigest()

    # 2. Decode and replace characters for base64 decoding
    encoded_data = encoded_data.replace('_', '+').replace('/', '')

    # 2. Decode base64
    decoded_data = base64.b64decode(encoded_data)

    # 3. Decrypt with RC4
    decrypted_data = rc4_decrypt(decoded_data, md5_hash)

    # Convert to string and remove the first 18 characters
    result = decrypted_data[18:]

    return result


def get_seed():
    encoded_data = "djE9xPVNQrjx-0f00CgfyK-HG-icRg0HlsKpVIYDdIo48MrHQ99rC5JhKqGcaFziowXe450VZJJNsJ7Ov3JN6heoC6LyuoIIbJZZhaFNafXmsAeVEOAJZRQuiUY94T8Lli1LoXhm9CHlavp5nefLFfWSYGiQx83fs8ao2K6HTeJKhw="
    access_token = "v.:V1Udz;z*vKn0Q2EgUA5EDUd4HN8Bd"
    seed = decode_and_decrypt(access_token, encoded_data)
    return seed


# Example usage:
def custom_signer(data):
    # Replace this with your signing logic using HMAC-SHA1
    # The data parameter is a byte array that you need to sign
    secret_key = get_seed()  # Replace with your secret key (bytes)
    return hmac.new(secret_key, data, hashlib.sha1).digest()


if __name__ == '__main__':
    interval = int(time.timezone)  # Replace with the current interval
    code_length = 6  # Replace with the desired code length
    pin_modulo = 1000000  # Replace with the desired PIN modulo
    response_code = generate_response_code(custom_signer, interval, code_length, pin_modulo)
    print("Response Code:", response_code)
