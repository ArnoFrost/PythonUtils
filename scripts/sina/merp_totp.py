import base64
import hashlib
import hmac
import struct


def generate_response_code(secret_key, interval):
    # Convert the interval to an 8-byte array
    interval_bytes = struct.pack(">Q", interval)

    # Calculate the HMAC-SHA1 of the interval using the secret key
    hmac_result = hmac.new(secret_key, interval_bytes, hashlib.sha1).digest()

    # Extract the 4-byte dynamic binary code (DBC) from the HMAC result
    dbc = struct.unpack(">I", hmac_result[-4:])[0]

    # Calculate the final response code as an integer between 0 and 999999
    response_code = dbc & 0x7FFFFFFF % 1000000

    # Pad the response code with leading zeros to ensure it's 6 digits long
    response_code_str = str(response_code).zfill(6)

    return response_code_str





if __name__ == '__main__':
    # Example usage:
    encoded_data = "djE9xPVNQrjx-0f00CgfyK-HG-icRg0HlsKpVIYDdIo48MrHQ99rC5JhKqGcaFziowXe450VZJJNsJ7Ov3JN6heoC6LyuoIIbJZZhaFNafXmsAeVEOAJZRQuiUY94T8Lli1LoXhm9CHlavp5nefLFfWSYGiQx83fs8ao2K6HTeJKhw="
    access_token = "v.:V1Udz;z*vKn0Q2EgUA5EDUd4HN8Bd"
    seed = decode_and_decrypt(access_token, encoded_data)
    # secret_key = "854299952"
    print(seed)
    # Example usage:
    secret_key = seed  # Replace with your secret key (bytes)
    current_interval = 61  # Replace with the current interval
    response_code = generate_response_code(secret_key, current_interval)
    print("Response Code:", response_code)
