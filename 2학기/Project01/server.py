#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import threading
from typing import Dict, Tuple, TextIO

ENC = 'utf-8'


class ChatServer:
    '''
    TCP/IP 멀티스레드 채팅 서버.

    - 접속 시 닉네임을 입력받고, 중복이면 번호를 붙여 고유화한다.
    - 입장/퇴장 시 전체 브로드캐스트.
    - 일반 메시지는 '사용자> 메시지' 형식으로 전체 브로드캐스트.
    - '/종료' 입력 시 해당 클라이언트 연결 종료.
    - 귓속말: '@닉 메시지' 또는 '/w 닉 메시지'.
    '''

    def __init__(self, host: str = '0.0.0.0', port: int = 5000) -> None:
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock.bind((host, port))
        self.server_sock.listen()

        self.lock = threading.Lock()
        # name -> (conn, rfile, wfile)
        self.clients: Dict[str, Tuple[socket.socket, TextIO, TextIO]] = {}
        self.running = True

    def start(self) -> None:
        print('[*] listening...')
        try:
            while self.running:
                try:
                    conn, addr = self.server_sock.accept()
                except OSError:
                    # 소켓이 이미 닫힌 경우 루프 종료
                    break
                thread = threading.Thread(
                    target=self.handle,
                    args=(conn,),
                    daemon=True
                )
                thread.start()
        except KeyboardInterrupt:
            print('\n[*] shutdown requested (KeyboardInterrupt)')
        finally:
            self.shutdown()

    def shutdown(self) -> None:
        self.running = False
        # 먼저 모든 클라이언트 정리
        with self.lock:
            items = list(self.clients.items())
            self.clients.clear()

        for _, (conn, rfile, wfile) in items:
            try:
                rfile.close()
            except Exception:
                pass
            try:
                wfile.close()
            except Exception:
                pass
            try:
                conn.shutdown(socket.SHUT_RDWR)
            except Exception:
                pass
            try:
                conn.close()
            except Exception:
                pass

        try:
            self.server_sock.close()
        except Exception:
            pass

        print('[*] server closed')

    def handle(self, conn: socket.socket) -> None:
        with conn:
            rfile = conn.makefile('r', encoding=ENC, newline='\n')
            wfile = conn.makefile('w', encoding=ENC, newline='\n')

            self.send(wfile, '닉네임을 입력하세요: ')
            name = (rfile.readline() or '').strip() or 'user'

            # 닉네임 고유화
            with self.lock:
                unique = name
                i = 1
                while unique in self.clients:
                    i += 1
                    unique = f'{name}{i}'
                name = unique
                self.clients[name] = (conn, rfile, wfile)

            self.broadcast(f'{name}님이 입장하셨습니다.')

            try:
                for line in rfile:
                    msg = line.rstrip('\n')
                    if not msg:
                        continue

                    if msg == '/종료':
                        self.send(wfile, '연결을 종료합니다.')
                        break

                    # 귓속말이면 여기서 처리하고 다음 반복
                    if self.whisper(name, msg):
                        continue

                    # 일반 메시지 브로드캐스트
                    self.broadcast(f'{name}> {msg}')
            except Exception as exc:
                # 경고 메시지 대신 서버 표준 출력 로그
                print(f'[!] client handler error: {exc}')
            finally:
                # 클라이언트 제거 및 자원 정리
                with self.lock:
                    entry = self.clients.pop(name, None)

                if entry:
                    _, rf, wf = entry
                    try:
                        rf.close()
                    except Exception:
                        pass
                    try:
                        wf.close()
                    except Exception:
                        pass

                self.broadcast(f'{name}님이 퇴장하셨습니다.')

    def whisper(self, sender: str, msg: str) -> bool:
        '''
        귓속말 파싱/전송.
        - '@닉 메시지' 또는 '/w 닉 메시지'
        - 처리했으면 True, 아니면 False 반환.
        '''
        if not msg:
            return False

        if msg.startswith('@'):
            parts = msg.split(' ', 1)
            if len(parts) < 2:
                self.send_to(sender, '사용법: @닉 메시지')
                return True
            target = parts[0][1:]
            body = parts[1]
            return self._deliver_whisper(sender, target, body)

        if msg.startswith('/w '):
            parts = msg.split(' ', 2)
            if len(parts) < 3:
                self.send_to(sender, '사용법: /w 닉 메시지')
                return True
            _, target, body = parts
            return self._deliver_whisper(sender, target, body)

        return False

    def _deliver_whisper(self, sender: str, target: str, body: str) -> bool:
        if not target or not body:
            self.send_to(sender, '귓속말 형식 오류')
            return True
        if target == sender:
            self.send_to(sender, '본인에게는 보낼 수 없습니다.')
            return True

        with self.lock:
            entry = self.clients.get(target)

        if not entry:
            self.send_to(sender, f'[{target}] 없음')
            return True

        self.send(entry[2], f'(귓속말) {sender}> {body}')
        self.send_to(sender, f'(귓속말 전송됨) {sender} -> {target}: {body}')
        return True

    def broadcast(self, text: str) -> None:
        with self.lock:
            targets = [w for _, _, w in self.clients.values()]
        for wfile in targets:
            self.send(wfile, text)

    def send_to(self, name: str, text: str) -> None:
        with self.lock:
            entry = self.clients.get(name)
        if entry:
            self.send(entry[2], text)

    @staticmethod
    def send(wfile: TextIO, text: str) -> None:
        try:
            wfile.write(text + '\n')
            wfile.flush()
        except Exception:
            # 연결이 이미 닫혔을 수 있음
            pass


def main() -> None:
    ChatServer().start()


if __name__ == '__main__':
    main()
