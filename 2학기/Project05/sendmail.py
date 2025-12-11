import smtplib
import os
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class GmailSender:
    """
    Gmail SMTP 서버를 이용해 메일을 전송하는 클래스입니다.
    기본 텍스트 메일 및 파일 첨부 기능을 지원합니다.
    """

    def __init__(self, sender_email, app_password):
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587
        self.sender_email = sender_email
        self.password = app_password

    def send_email(self, receiver_email, subject, body, attachment_path=None):
        """
        메일을 구성하고 SMTP 서버를 통해 전송합니다.

        Args:
            receiver_email (str): 받는 사람 이메일 주소
            subject (str): 메일 제목
            body (str): 메일 본문 내용
            attachment_path (str, optional): 첨부할 파일의 경로. 기본값은 None.
        """
        # 메일 객체 생성 및 기본 헤더 설정
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        # 본문 추가
        msg.attach(MIMEText(body, 'plain'))

        # 첨부 파일이 있는 경우 처리 (보너스 과제)
        if attachment_path:
            self._attach_file(msg, attachment_path)

        # SMTP 서버 연결 및 메일 발송
        try:
            # SMTP 서버 연결
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.ehlo()  # 서버에 인사 (Identify)

            # 보안 연결(TLS) 시작
            server.starttls()
            server.ehlo()

            # 로그인
            server.login(self.sender_email, self.password)

            # 메일 전송
            server.sendmail(self.sender_email, receiver_email, msg.as_string())

            print(f'이메일 전송 성공: {receiver_email}')

        except smtplib.SMTPAuthenticationError:
            print('로그인 실패: 이메일 주소나 앱 비밀번호를 확인하세요.')
        except smtplib.SMTPException as e:
            print(f'SMTP 오류 발생: {e}')
        except Exception as e:
            print(f'예상치 못한 오류 발생: {e}')
        finally:
            # 연결 종료
            try:
                server.quit()
            except NameError:
                pass  # server 변수가 정의되지 않은 경우 무시

    def _attach_file(self, msg, file_path):
        """
        메일 메시지에 파일을 첨부하는 내부 메서드입니다.
        """
        if not os.path.isfile(file_path):
            print(f'파일을 찾을 수 없음: {file_path}')
            return

        filename = os.path.basename(file_path)

        # 파일 타입 추측
        ctype, encoding = mimetypes.guess_type(file_path)
        if ctype is None or encoding is not None:
            # 타입을 알 수 없는 경우 일반 바이너리로 처리
            ctype = 'application/octet-stream'

        maintype, subtype = ctype.split('/', 1)

        try:
            with open(file_path, 'rb') as f:
                part = MIMEBase(maintype, subtype)
                part.set_payload(f.read())

            # 파일을 base64로 인코딩
            encoders.encode_base64(part)

            # 헤더 추가
            part.add_header(
                'Content-Disposition',
                f'attachment; filename="{filename}"'
            )
            msg.attach(part)

        except IOError as e:
            print(f'파일 첨부 중 오류 발생: {e}')


if __name__ == '__main__':
    # ---------------------------------------------------------
    # 사용자 설정 영역
    # 주의: 실제 코드에 비밀번호를 하드코딩하는 것은 보안상 위험할 수 있습니다.
    # 환경 변수 사용을 권장하지만, 과제 수행을 위해 변수로 설정합니다.
    # ---------------------------------------------------------

    # 보내는 사람 계정 정보 (앱 비밀번호 사용 필수)
    SENDER_ACCOUNT = 'your_email@gmail.com'
    APP_PASSWORD = 'your_app_password_here'  # 16자리 앱 비밀번호

    # 받는 사람 정보
    RECEIVER_ACCOUNT = 'receiver_email@example.com'

    # 메일 내용
    EMAIL_SUBJECT = '웹 크롤링 테스트 메일'
    EMAIL_BODY = '이 메일은 Python을 통해 자동으로 발송되었습니다.'

    # 첨부 파일 경로 (없으면 None 혹은 빈 문자열)
    # 예: ATTACHMENT_FILE = 'report.txt'
    ATTACHMENT_FILE = None

    # ---------------------------------------------------------
    # 메일 전송 실행
    # ---------------------------------------------------------
    mailer = GmailSender(SENDER_ACCOUNT, APP_PASSWORD)
    mailer.send_email(RECEIVER_ACCOUNT, EMAIL_SUBJECT, EMAIL_BODY, ATTACHMENT_FILE)