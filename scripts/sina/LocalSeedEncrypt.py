import base64
import hashlib
import hmac
import time


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


class SeedInfo:
    def __init__(self, seed, secret_key):
        self.seed = seed
        self.secret_key = secret_key

    def get_otp(self, is_create):
        if is_create:
            # Generate a new OTP
            timestamp = int(time.time())
            message = f"{self.seed}-{timestamp}"
            hmac_result = hmac.new(self.secret_key.encode(), message.encode(), hashlib.sha256).hexdigest()
            otp = hmac_result[-6:]  # Take the last 6 characters of the HMAC result
            return otp
        else:
            # Retrieve the previously generated OTP (if stored)
            # Implement your logic to retrieve the OTP here
            return None


class PasscodeGenerator:
    def __init__(self, seed_info):
        self.seed_info = seed_info

    def generate_otp(self, is_create):
        return self.seed_info.get_otp(is_create)


if __name__ == '__main__':
    # Example usage:
    encoded_data = "djE9xPVNQrjx-0f00CgfyK-HG-icRg0HlsKpVIYDdIo48MrHQ99rC5JhKqGcaFziowXe450VZJJNsJ7Ov3JN6heoC6LyuoIIbJZZhaFNafXmsAeVEOAJZRQuiUY94T8Lli1LoXhm9CHlavp5nefLFfWSYGiQx83fs8ao2K6HTeJKhw="
    access_token = "v.:V1Udz;z*vKn0Q2EgUA5EDUd4HN8Bd"
    seed = decode_and_decrypt(access_token, encoded_data)
    secret_key = "854299952"
    print(seed)

    # decode_data = "v1=C4F54D42B8F1D1FD340AF22871A27118341E5B0AA55218D228E3C32B1D0F7DAC2E494AAA8671A1738A8C17B78E7455924936C27B3AFDC937A85EA02E8BCAEA0821B2596616855A7D79AC001E544380259450BA2518F784FC58B52E85E19BD08795ABE9E6779F2C57D64981A2431F377ECF1AA362BA1D37892A1C"
    # access_token_md5 = 'c9b18a994d47f7298af09bf3ceb72e1c'
    # result = rc4_decrypt(decode_data, access_token_md5)

    seed_info = SeedInfo(seed=seed, secret_key=secret_key)
    passcode_generator = PasscodeGenerator(seed_info)

    # Generate a new OTP
    otp = passcode_generator.generate_otp(is_create=True)
    print("Generated OTP:", otp)

    # Retrieve the previously generated OTP
    otp = passcode_generator.generate_otp(is_create=False)
    print("Retrieved OTP:", otp)


