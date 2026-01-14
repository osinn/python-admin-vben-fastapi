from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import base64
from typing import Tuple, Optional
import re


def generate_rsa_keypair_b64() -> Tuple[str, str]:
    """
    生成 2048 位 RSA 密钥对
    :return: (公钥base64, 私钥base64)
    """
    rsa_private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    rsa_public_key = rsa_private_key.public_key()

    # 公钥：DER 格式 → Base64
    public_der = rsa_public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # 私钥：PKCS#8 (DER) → Base64（无加密）
    private_der = rsa_private_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_b64 = base64.b64encode(public_der).decode('ascii')
    private_b64 = base64.b64encode(private_der).decode('ascii')

    return public_b64, private_b64


def encrypt_with_public_b64(plaintext: str, public_b64: str,
                            padding_scheme: str = 'OAEP') -> str:
    """
    公钥加密
    Args:
        plaintext: 明文文本
        public_b64: 公钥Base64字符串
        padding_scheme: 填充方案 'OAEP' 或 'PKCS1v15'
    Returns:
        Base64编码的密文
    """
    public_der = base64.b64decode(public_b64)
    public_key = serialization.load_der_public_key(public_der)

    if padding_scheme.upper() == 'PKCS1V15':
        # 使用 PKCS1 v1.5（兼容 jsencrypt）
        encrypted = public_key.encrypt(
            plaintext.encode('utf-8'),
            padding.PKCS1v15()
        )
    else:
        # 默认使用 OAEP
        encrypted = public_key.encrypt(
            plaintext.encode('utf-8'),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    return base64.b64encode(encrypted).decode('ascii')


def decrypt_with_private_b64(ciphertext: str, private_b64: str,
                             padding_scheme: str = 'AUTO') -> str:
    """
    私钥解密
    Args:
        ciphertext: 加密字符串（Base64格式）
        private_b64: 私钥Base64字符串
        padding_scheme:
            'AUTO' - 自动尝试两种填充方案
            'PKCS1v15' - 使用 PKCS1 v1.5（jsencrypt 默认）
            'OAEP' - 使用 OAEP 填充
    Returns:
        解密后的明文

    Raises:
        ValueError: 解密失败
    """
    # 清理可能的空白字符和换行
    ciphertext = clean_base64_string(ciphertext)
    private_b64 = clean_base64_string(private_b64)

    # 加载私钥
    private_der = base64.b64decode(private_b64)
    private_key = serialization.load_der_private_key(
        private_der,
        password=None
    )

    # 解码密文
    try:
        cipher_bytes = base64.b64decode(ciphertext)
    except Exception as e:
        cipher_bytes = base64.b64decode(ciphertext + '=' * (4 - len(ciphertext) % 4))

    if padding_scheme.upper() == 'AUTO':
        # 自动检测：先尝试 PKCS1 v1.5，再尝试 OAEP
        try:
            # 先尝试 PKCS1 v1.5（jsencrypt 默认）
            plaintext = private_key.decrypt(
                cipher_bytes,
                padding.PKCS1v15()
            ).decode('utf-8')
            return plaintext
        except Exception:
            # 再尝试 OAEP
            try:
                plaintext = private_key.decrypt(
                    cipher_bytes,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                ).decode('utf-8')
                return plaintext
            except Exception as e2:
                raise ValueError(f"解密失败（两种填充方案都失败）: {str(e2)}")

    elif padding_scheme.upper() == 'PKCS1V15':
        # 使用 PKCS1 v1.5 填充
        plaintext = private_key.decrypt(
            cipher_bytes,
            padding.PKCS1v15()
        ).decode('utf-8')
        return plaintext

    else:
        # 使用 OAEP 填充
        plaintext = private_key.decrypt(
            cipher_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        ).decode('utf-8')
        return plaintext


def clean_base64_string(b64_str: str) -> str:
    """
    清理 Base64 字符串，移除所有非 Base64 字符
    Args:
        b64_str: 原始Base64字符串
    Returns:
        清理后的Base64字符串
    """
    # 移除所有空白字符
    b64_str = re.sub(r'\s', '', b64_str)

    # 移除可能的URL前缀
    if b64_str.startswith('data:application/octet-stream;base64,'):
        b64_str = b64_str[len('data:application/octet-stream;base64,'):]

    # 补全等号
    padding_needed = 4 - (len(b64_str) % 4)
    if padding_needed < 4:
        b64_str += '=' * padding_needed

    return b64_str


def convert_pem_to_b64(pem_str: str) -> str:
    """
    将PEM格式的密钥转换为Base64格式
    Args:
        pem_str: PEM格式的密钥字符串
    Returns:
        Base64格式的密钥
    """
    # 移除PEM头尾和换行
    lines = pem_str.strip().split('\n')

    # 提取Base64内容部分
    b64_lines = []
    in_body = False
    for line in lines:
        line = line.strip()
        if line.startswith('-----BEGIN'):
            in_body = True
            continue
        elif line.startswith('-----END'):
            break
        elif in_body and line:
            b64_lines.append(line)

    b64_content = ''.join(b64_lines)

    try:
        return b64_content
    except:
        # 如果是纯Base64，直接返回
        return base64.b64encode(b64_content.encode()).decode('ascii')


def b64_to_pem(b64_str: str, key_type: str = "PUBLIC") -> str:
    """
    将Base64格式的密钥转换为PEM格式

    Args:
        b64_str: Base64格式的密钥
        key_type: "PUBLIC" 或 "PRIVATE"

    Returns:
        PEM格式的密钥字符串
    """
    # 每64个字符换行
    chunks = [b64_str[i:i + 64] for i in range(0, len(b64_str), 64)]

    if key_type.upper() == "PUBLIC":
        header = "-----BEGIN PUBLIC KEY-----\n"
        footer = "\n-----END PUBLIC KEY-----\n"
    else:
        header = "-----BEGIN PRIVATE KEY-----\n"
        footer = "\n-----END PRIVATE KEY-----\n"

    return header + '\n'.join(chunks) + footer


# === 测试加解密 ===
if __name__ == "__main__":
    # public_key_str = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA01HjqKEK52Amex1bRc7UcCpnzx4NJ8cwn+XBNgHh1y0rYv9IbLDAXNek6XilUNXRXekpE7Q7x/K1/px06bjvaAUbouy2iNhuqxK0z9YYrYHFsbF8t4m8IcyuMl0tA4DEBd7PrAR+VETkZfefIItf/81s4XZJ+qXPK3IBFJLmPuXW6LLk09f/ps2HXKdPi52iO1KI9mqDp7xD+hKMUrnJg/zdymKbq3r4BSivYNBhaprl3i4Z/gPgHhG1CBbHwg1IbaB+t6Me6KThjMvqpx/uf+bIOg9X5QptcKyMlpYbF52bLm4H/05chP0dUQVu9pUHxyK5ZC9KXfyIh7VRCg1NewIDAQAB"
    # private_key_str = "MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDTUeOooQrnYCZ7HVtFztRwKmfPHg0nxzCf5cE2AeHXLSti/0hssMBc16TpeKVQ1dFd6SkTtDvH8rX+nHTpuO9oBRui7LaI2G6rErTP1hitgcWxsXy3ibwhzK4yXS0DgMQF3s+sBH5URORl958gi1//zWzhdkn6pc8rcgEUkuY+5dbosuTT1/+mzYdcp0+LnaI7Uoj2aoOnvEP6EoxSucmD/N3KYpurevgFKK9g0GFqmuXeLhn+A+AeEbUIFsfCDUhtoH63ox7opOGMy+qnH+5/5sg6D1flCm1wrIyWlhsXnZsubgf/TlyE/R1RBW72lQfHIrlkL0pd/IiHtVEKDU17AgMBAAECggEAH8OzmAbxEnuE/UTvPIHiXqPj1ncax3ZtFt6chDI/O4QqJ+eIqvHcpc1dGCJ5nbouOP1nHnOdTX5sde5tsoOJKmvOI4I3zpUopCVxMWaUxLajkVoaYvpctwCYf1s7J3IlGl7LfPzF7S6CiINIE5vFB+Nd8PwXaF+hJv4sLxFac8H8cf/0VmV7m7PXv2HQa3ebrhXDzAU2Awbf3lwMMFrvX7HIEDQcvuTJWn0lBsO8ei1nCiDrg1g/PBq68LVJQKDIQu+isL0o/ZWfkiZWd1Hr31MOzhAw4d2HJ99tUYpXuLS1vBTANj8IrfFuKCnlxEGcYIhapilTuzHrKVV39hHqjQKBgQDuP+k8PWwBvoARYSaa2BgKb27J2gp327Rm7m5N6vwpjt+dfyT1rdnFOjtlwim23ulYa440bmy9XUHMSYqyFsVPfmXXOlDgd0EY2zj5EOVUNAYjLUp1RUw7q5aiVixfDso8rL9mnsZCeb9PcYfn65nJE7GmoAcWV48T/yZcRYlhTwKBgQDjEFoY5K5sLFMAbgVAkDson9W3fCdOtgkuzogSpn7cX5P5QmwivpFPSwLr0YoPvG9UCa/OPDfSqDrFGcoe08oObtBX6r8sq5fFUj5wvGpB6LSFKTUWwIKgu0uL+PMVyYTziHt+aXXbS40uuSdz1a1VR5ugUfIgpsH45RKAjKoOFQKBgQDMRDV3NX4tvKPWwsGzjsSF5eZJ38yL2O3CNniSC39pLhrg0MribMzCQVv9scvMAzBzY7vHjklizdsFCKSGbel7b3ZnYpNG8Ff6tLITMP4+BGCitkkZZHGo00PSKSnf0jFodf+gP07iXbm9piwMlr4CXQU6RAfviuCcF21PPTs9FwKBgQC8WmgiljAKE4qWpK0+rWYlgNDr79U7ec2MQk6mCe7aJ368GdlRyPsI55R4wczg2NMQxyhKz7EO0fZOYeJESDMoXcv94gDLsVuol1ysb99E5SA6BcDAKtkxM6yrY8thm1TqH6Exb5IQY0+uHnEXqXyrbUcvakqLw0jMilkawZSfMQKBgAas0T/N6NfL2JCh7f444gdQHctL2XFSNMvzgFMUV4Ehd71Yb8+Icpnu/PMp0+XV+Go12bB/v2+7QGEy7GLrTQJVvfQtpxLVl5lnfBVBPPiMCqeumItYKDrY7UzGGz/yTqjlnoP53VJQKpby+TnBAXYWpe7M2BWmVCsp/5qANRiY"
    public_key, private_key = generate_rsa_keypair_b64()

    msg = "hello Python RSA 加解密工具 !"
    encrypted = encrypt_with_public_b64(msg, public_key)
    decrypted = decrypt_with_private_b64(encrypted, private_key)

    print("原始:", msg)
    print("解密:", decrypted)
    print("成功?", msg == decrypted)
