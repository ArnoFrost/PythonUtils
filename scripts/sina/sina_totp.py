import base64
import datetime
import time

import pyotp


def generate_passcode(timestamp, vsn, data):
    try:
        # Base64解码data
        decoded_data = base64.b64decode(data)

        # 创建PyOTP TOTP实例，使用HMAC-SHA1算法
        totp = pyotp.TOTP(decoded_data, interval=60)  # 60秒的时间间隔

        # 计算时间偏移量
        current_time = int(timestamp)
        delta = (current_time - datetime.datetime.now().timestamp()) // 60

        # 生成passcode
        passcode = totp.at(counter=delta)

        return passcode
    except Exception as e:
        print(e)
        return None


if __name__ == '__main__':
    # 生成一个新的随机秘密密钥
    # secret = pyotp.random_base32()
    # 从环境变量中获取秘密密钥
    # secret = os.environ.get("TOTP_SECRET", pyotp.random_base32())
    # secret = "D2KEPOSJUSJU7QJOETEDSQVAJBBAGGEK"
    # secret = "a13b4dcb20721b8d47cfaaee816c65dd2017b6af"
    # secret = "1C891D80A7660BD1409452442F7E5CF1"
    # # secret = "k:jk6e5FsLaNAu9O,Y43wyhArQABajCu"
    # print(f"Secret Key: {secret}")
    #
    # # 使用该秘密密钥初始化 TOTP 对象
    # totp = pyotp.TOTP(secret)
    #
    # # 生成当前的 TOTP 令牌
    # token = totp.now()
    # print(f"Generated Token: {token}")
    #
    # # 验证 TOTP 令牌
    # is_valid = totp.verify(token)
    # if is_valid:
    #     print("Token is valid!")
    # else:
    #     print("Token is invalid!")

    # 示例用法
    timestamp = time.time()  # 替换为您的时间戳
    vsn = "854299952"  # 替换为您的VSN
    data = "djE9xPVNQrjx-0f00CgfyK-HG-icRg0HlsKpVIYDdIo48MrHQ99rC5JhKqGcaFziowXe450VZJJNsJ7Ov3JN6heoC6LyuoIIbJZZhaFNafXmsAeVEOAJZRQuiUY94T8Lli1LoXhm9CHlavp5nefLFfWSYGiQx83fs8ao2K6HTeJKhw"  # 替换为您的Base64编码的data

    passcode = generate_passcode(timestamp, vsn, data)
    if passcode is not None:
        print("Generated Passcode:", passcode)
    else:
        print("Passcode generation failed.")
