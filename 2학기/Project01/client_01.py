#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import threading

ENC = 'utf-8'
HOST = '127.0.0.1'  # 필요시 여기만 수정
PORT = 5000         # 필요시 여기만 수정


class ChatClient:
    def __init__(self, username: str) -> None:
        self.host = HOST
        self.port = PORT
        self.username = username or '사용자'
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = False

    def start(self) -> None:
        self.sock.connect((self.host, self.port))
        self.running = True

        # 서버의 닉네임 프롬프트 1줄 수신 후 닉네임 전송
        _ = self.sock.recv(4096)
        self.sock.sendall((self.username + '\n').encode(ENC))

        threading.Thread(target=self._recv_loop, daemon=True).start()
        print('[*] 채팅을 시작합니다. 종료하려면 /종료 를 입력하세요.')

        try:
            while self.running:
                msg = input()
                self.sock.sendall((msg + '\n').encode(ENC))
                if msg.strip() == '/종료':
                    self.running = False
                    break
        finally:
            self._close()

    def _recv_loop(self) -> None:
        try:
            rfile = self.sock.makefile('r', encoding=ENC, newline='\n')
            for line in rfile:
                print(line.rstrip('\n'))
        except Exception as exc:
            print(f'[!] 수신 중 예외: {exc}')
        finally:
            self.running = False

    def _close(self) -> None:
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
        except Exception:
            pass
        try:
            self.sock.close()
        except Exception:
            pass
        print('[*] 연결이 종료되었습니다.')


def main() -> None:
    username = input('사용자 이름: ').strip()
    client = ChatClient(username=username)
    client.start()


if __name__ == '__main__':
    main()
