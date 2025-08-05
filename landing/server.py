#!/usr/bin/env python3
"""
MSProject2 SAJU 랜딩 페이지 서버
포트 4000에서 간단한 HTML 랜딩 페이지를 제공합니다.
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path

# 포트 설정
PORT = 4000

# 현재 스크립트가 있는 디렉토리로 변경
script_dir = Path(__file__).parent
os.chdir(script_dir)

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # CORS 헤더 추가 (다른 포트의 서비스들과 연동 위해)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_GET(self):
        # 루트 경로로 접근시 index.html 반환
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()

def main():
    try:
        with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
            print("🔮 MSProject2 SAJU 랜딩 페이지 서버 시작")
            print(f"📍 서버 주소: http://localhost:{PORT}")
            print("🛑 종료하려면 Ctrl+C를 누르세요")
            print("-" * 50)
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n✅ 서버가 정상적으로 종료되었습니다.")
        sys.exit(0)
    except OSError as e:
        if e.errno == 98 or "already in use" in str(e).lower():
            print(f"❌ 포트 {PORT}이 이미 사용 중입니다.")
            print("다른 프로세스를 종료하거나 다른 포트를 사용하세요.")
        else:
            print(f"❌ 서버 시작 실패: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
