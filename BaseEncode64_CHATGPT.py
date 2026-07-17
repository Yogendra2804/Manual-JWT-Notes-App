import base64
import json


def base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def encoded_make_header(header_dict):

    header_json = json.dumps(header_dict)

    header_bytes = header_json.encode()

    return base64url_encode(header_bytes)


def encoded_make_payload(payload_dict):

    payload_json = json.dumps(payload_dict)

    payload_bytes = payload_json.encode()

    return base64url_encode(payload_bytes)