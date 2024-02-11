import ssl
import socket

def convert_value(value):
    if isinstance(value, (tuple, list)):
        return [convert_value(item) for item in value]
    elif isinstance(value, dict):
        return {str(key): convert_value(item) for key, item in value.items()}
    return value

def get_certificate_info(url):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((url, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=url) as ssock:
                cert = ssock.getpeercert()
                certificate_info = {str(key): convert_value(value) for key, value in cert.items()}

                return certificate_info

    except Exception as e:
        return {"error": f"Error: {e}"}
