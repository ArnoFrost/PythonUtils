import base64
import hashlib


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
        plaintext.append(char ^ k)

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
    result = decrypted_data.decode('utf-8')[18:]

    return result


if __name__ == '__main__':
    # 示例用法
    # secret = "6383hgdh56na4ff56786pkss"  # 替换为您的密钥
    # data_to_encrypt = "hello"  # 要加密的数据
    #
    # encryptor = LocalSeedEncrypt(secret)
    # encrypted_data = encryptor.get_enc_string(data_to_encrypt)
    # print("Encrypted Data:", encrypted_data)
    #
    # decrypted_data = encryptor.get_des_string(encrypted_data)
    # print("Decrypted Data:", decrypted_data)

    # Example usage:
    encoded_data = "djE9xPVNQrjx-0f00CgfyK-HG-icRg0HlsKpVIYDdIo48MrHQ99rC5JhKqGcaFziowXe450VZJJNsJ7Ov3JN6heoC6LyuoIIbJZZhaFNafXmsAeVEOAJZRQuiUY94T8Lli1LoXhm9CHlavp5nefLFfWSYGiQx83fs8ao2K6HTeJKhw="
    decode_data = "v1=C4F54D42B8F1D1FD340AF22871A27118341E5B0AA55218D228E3C32B1D0F7DAC2E494AAA8671A1738A8C17B78E7455924936C27B3AFDC937A85EA02E8BCAEA0821B2596616855A7D79AC001E544380259450BA2518F784FC58B52E85E19BD08795ABE9E6779F2C57D64981A2431F377ECF1AA362BA1D37892A1C"
    access_token = "v.:V1Udz;z*vKn0Q2EgUA5EDUd4HN8Bd"
    access_token_md5 = 'c9b18a994d47f7298af09bf3ceb72e1c'

    # result = decode_and_decrypt(access_token, encoded_data)

    result = rc4_decrypt(decode_data, access_token_md5)
    print(result)
