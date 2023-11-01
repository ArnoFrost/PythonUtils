import base64
import hashlib
import hmac
import json
import struct
import time
from io import BytesIO
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


class SeedInfo:

    def __init__(self):
        self.VSN = ""
        self.data = None
        self.tokenTime = 0

    @classmethod
    def create(cls, json_string):
        obj = cls()
        json_object = json.loads(json_string)
        obj.VSN = json_object["vsn"]
        obj.data = json_object["data"]
        return obj

    def get_otp(self):
        try:
            mac = hmac.new(self.data.encode(), digestmod=hashlib.sha1)
            passcode_gen = PasscodeGenerator(mac, 6, 60)
            return passcode_gen.generate_timeout_code(True, self.tokenTime)
        except Exception as e:
            print(e)
            return None


class PasscodeGenerator:
    INTERVAL = 30
    PASS_CODE_LENGTH = 6
    PIN_MODULO = 10 ** 6

    class IntervalClock:

        def __init__(self, generator):
            self.generator = generator

        def get_current_interval(self):
            current_time_seconds = (time.time() - self.generator.time_offset)
            interval_period_count = current_time_seconds // self.generator.interval_period

            if self.generator.is_created:
                remaining_time = self.generator.interval_period - (
                        current_time_seconds % self.generator.interval_period)
                print(f"Remaining Time: {remaining_time}")
                # Assuming a send method or similar mechanism in the handler
                # if self.generator.handler:
                #     message = {
                #         'what': 100,
                #         'arg1': int(remaining_time)
                #     }
                #     self.generator.handler.send(message)
            return int(interval_period_count)

        def get_interval_period(self):
            return self.generator.interval_period

    class Signer:

        def __init__(self, mac):
            self.mac = mac

        def sign(self, data):
            self.mac.update(data)
            return self.mac.digest()

    def __init__(self, mac, code_length=PASS_CODE_LENGTH, interval_period=INTERVAL, handler=None):
        self.signer = self.Signer(mac)
        self.code_length = code_length
        self.interval_period = interval_period
        self.clock = self.IntervalClock(self)
        self.handler = handler
        self.is_created = False
        self.time_offset = 0

    def pad_output(self, value):
        value_str = str(value)
        while len(value_str) < self.code_length:
            value_str = "0" + value_str
        print(f"pad out: {value_str}")
        return value_str

    def generate_timeout_code(self, is_created, time_offset):
        self.is_created = is_created
        self.time_offset = time_offset
        return self.generate_response_code(self.clock.get_current_interval())

    def generate_response_code(self, interval):
        data = struct.pack(">Q", interval)  # Convert the long to 8 bytes in big-endian format
        return self.generate_response_code_from_data(data)

    def generate_response_code_from_data(self, data):
        signature = self.signer.sign(data)
        truncated_hash = self.hash_to_int(signature, signature[-1] & 0x0F)
        pin_value = (truncated_hash & 0x7FFFFFFF) % self.PIN_MODULO
        return self.pad_output(pin_value)

    @staticmethod
    def hash_to_int(hash_data, offset):
        data_stream = BytesIO(hash_data[offset: offset + 4])
        return struct.unpack(">I", data_stream.read(4))[0]

    def verify_response_code(self, interval, response_code):
        return self.generate_response_code(interval) == response_code

    def verify_timeout_code(self, response_code, past_intervals=1, future_intervals=1):
        current_interval = self.clock.get_current_interval()
        for interval_index in range(-past_intervals, future_intervals + 1):
            if self.generate_response_code(current_interval + interval_index) == response_code:
                return True
        return False


class NetSeedEncrypt:
    def __init__(self, access_token=""):
        self.access_token = access_token
        self.PASSWORD = self.get_net_des_secret()
        self.key = self.set_key(self.PASSWORD)

    def get_net_des_secret(self):
        # Dummy implementation since the original method is missing
        return "default_secret"

    def set_key(self, key_str):
        # Convert string to bytes
        key_bytes = key_str.encode()

        # Truncate or pad key to make it 8 bytes long for DES
        if len(key_bytes) > 8:
            key_bytes = key_bytes[:8]
        elif len(key_bytes) < 8:
            key_bytes += b'0' * (8 - len(key_bytes))

        # Now we have the correct DES key length
        self.key = key_bytes

        # If you wish to generate random bytes for some reason (as with SecureRandom):
        # random_bytes = get_random_bytes(8)

    def get_enc_string(self, s):
        hexdigest = self.md5_hexdigest(self.access_token)
        current_time = int((time.time() + 300) * 1000)
        return base64.b64encode(
            self.rc4_enc(self.md5_hexdigest(s + hexdigest + str(current_time))[:8] + str(current_time) + s,
                         hexdigest)).decode().replace("+", "_").replace("/", "-").replace("=", "")

    def get_dec_string(self, s):
        return self.rc4_dec(base64.b64decode(s.replace("_", "+").replace("-", "/")),
                            self.md5_hexdigest(self.access_token))[18:].decode()

    def get_des_string(self, s):
        return self.get_des_code(self.hex2byte(s.encode()))

    def md5_hexdigest(self, s):
        m = hashlib.md5()
        m.update(s.encode())
        return m.hexdigest()

    def rc4_enc(self, data, key):
        s = list(range(256))
        j = 0
        out = bytearray()

        # Key-scheduling algorithm
        for i in range(256):
            j = (j + s[i] + ord(key[i % len(key)])) % 256
            s[i], s[j] = s[j], s[i]

        i = j = 0
        for char in data:
            i = (i + 1) % 256
            j = (j + s[i]) % 256
            s[i], s[j] = s[j], s[i]
            out.append(char ^ s[(s[i] + s[j]) % 256])

        return out

    def rc4_dec(self, data, key):
        return self.rc4_enc(data, key)  # RC4 encryption and decryption are the same

    def get_des_code(self, byte_array):
        # Placeholder for DES decryption
        return byte_array

    @staticmethod
    def hex2byte(hex_str):
        return bytes.fromhex(hex_str.decode())

    @staticmethod
    def byte2hex(byte_array):
        return byte_array.hex().upper()

    # Missing implementations: getPinEncString, getSign, and other related DES methods


if __name__ == '__main__':
    # passcode_generator = PasscodeGenerator(interval_period=60, code_length=6, is_created=True)
    # interval = passcode_generator.get_current_interval()
    # print(f"Interval: {interval}")
    token = "v.:V1Udz;z*vKn0Q2EgUA5EDUd4HN8Bd"
    json = {
        "vsn": "854299952",
        "data": "djE9xPVNQrjx-0f00CgfyK-HG-icRg0HlsKpVIYDdIo48MrHQ99rC5JhKqGcaFziowXe450VZJJNsJ7Ov3JN6heoC6LyuoIIbJZZhaFNafXmsAeVEOAJZRQuiUY94T8Lli1LoXhm9CHlavp5nefLFfWSYGiQx83fs8ao2K6HTeJKhw"
    }
    seed_info = SeedInfo.create(json.dumps(json))
    opt = seed_info.get_otp()
    print(f"OTP: {opt}")
