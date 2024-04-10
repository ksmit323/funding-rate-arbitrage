from base58 import b58encode


def encode_key(key: bytes):
    return "ed25519:%s" % b58encode(key).decode("utf-8")
