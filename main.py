import socket
from typing import Tuple
from urllib.parse import urlparse, parse_qs, ParseResult

from views import *

URLS = {
    '/': index,
}


def parse_request(request: str) -> Tuple[str, ParseResult]:
    parsed = request.split(" ")
    method = parsed[0]
    url_parsed = urlparse(parsed[1])
    return method, url_parsed


def generate_headers(method: str, url: str) -> Tuple[str, int]:
    if not method == 'GET':
        return 'HTTP/1.1 405 Method not allowed\n\n', 405

    if url not in URLS:
        return 'HTTP/1.1 404 Not found\n\n', 404

    return 'HTTP/1.1 200 OK\nContent-Type: application/json \n\n', 200


def generate_content(code: int, url_parsed: ParseResult) -> str:
    if code == 404:
        return '<h1>404</h1><p>Not found</p>'
    if code == 405:
        return '<h1>405</h1><p>Method not allowed</p>'
    return URLS[url_parsed.path](**parse_qs(url_parsed.query))


def generare_response(request: str) -> bytes:
    method, url_parsed = parse_request(request)
    headers, code = generate_headers(method, url_parsed.path)
    body = generate_content(code, url_parsed)
    return (headers + body).encode()


def run() -> None:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5000))
    print('Ready')
    server_socket.listen()

    while True:
        client_socket, addr = server_socket.accept()
        request = client_socket.recv(1024)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        response = generare_response(request.decode('utf-8'))

        client_socket.sendall(response)
        client_socket.close()


if __name__ == '__main__':
    run()
