from cryptolib import pkcs_strip

if __name__ == '__main__':
    pkcs_strip(b"ICE ICE BABY\x04\x04\x04\x04")
    try:
        pkcs_strip(b"ICE ICE BABY")
    except ValueError:
        print("Yeah!")