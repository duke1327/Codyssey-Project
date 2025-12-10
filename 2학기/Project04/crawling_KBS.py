import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


# --- 전역 상수 ---
NAVER_LOGIN_URL = 'https://nid.naver.com/nidlogin.login'
NAVER_MAIL_URL = 'https://mail.naver.com/'


class NaverCrawlHelper:
    def __init__(self):
        try:
            options = Options()
            # 불필요한 로그 출력 방지
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_experimental_option('detach', True)  # 브라우저 꺼짐 방지

            self.driver = webdriver.Chrome(options=options)
            self.wait = WebDriverWait(self.driver, 10)
        except Exception as e:
            print(f'크롬 드라이버 실행 오류: {e}')
            sys.exit(1)

    def naver_login(self, user_id, user_pw):
        """
        자바스크립트로 ID/PW를 입력하여 자동 로그인 (CAPTCHA 우회 시도)
        """
        print('1. 로그인 페이지 접속')
        self.driver.get(NAVER_LOGIN_URL)
        time.sleep(1)

        try:
            # JS로 아이디/비밀번호 입력
            script_id = f"document.getElementById('id').value = '{user_id}';"
            script_pw = f"document.getElementById('pw').value = '{user_pw}';"

            self.driver.execute_script(script_id)
            self.driver.execute_script(script_pw)
            time.sleep(0.5)

            # 로그인 버튼 클릭
            btn = self.driver.find_element(By.ID, 'log.login')
            btn.click()

            # 페이지 이동 대기
            time.sleep(3)

            # URL 변경 여부로 성공 판단
            if 'nid.naver.com' not in self.driver.current_url:
                print('>> 로그인 성공!')
                return True
            else:
                print('>> 로그인 실패 (캡차 발생 가능성)')
                return False

        except Exception as e:
            print(f'로그인 중 오류: {e}')
            return False

    def get_mail_titles(self):
        print('2. 메일함 이동 및 목록 로딩 대기...')
        self.driver.get(NAVER_MAIL_URL)

        titles_list = []

        try:
            # [핵심 수정] 이미지 분석 결과 반영: a.mail_title_link 아래의 span.text
            target_selector = "a.mail_title_link span.text"

            # 해당 요소가 뜰 때까지 최대 10초 대기
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, target_selector)))

            # 요소들 찾기
            mail_elements = self.driver.find_elements(By.CSS_SELECTOR, target_selector)

            for index, element in enumerate(mail_elements):
                # 텍스트 추출
                title = element.text.strip()
                if title:
                    titles_list.append(f'{index + 1}. {title}')

            return titles_list

        except Exception as e:
            return [f'메일 리스트 파싱 실패: {e}']

    def quit(self):
        print('브라우저 종료')
        self.driver.quit()


def main():
    # ---------------------------------------------------------
    # 실행 전 본인의 아이디/비밀번호 입력
    # ---------------------------------------------------------
    my_id = 'YOUR_ID'
    my_pw = 'YOUR_PW'

    crawler = NaverCrawlHelper()

    if crawler.naver_login(my_id, my_pw):
        # 메일 제목 가져오기
        titles = crawler.get_mail_titles()

        print('\n' + '=' * 40)
        print(f'   [내 메일함 최근 메일 {len(titles)}개]')
        print('=' * 40)

        if titles:
            for t in titles:
                print(t)
        else:
            print('메일을 찾을 수 없습니다.')
        print('=' * 40)

    # 확인을 위해 5초 대기 후 종료
    time.sleep(5)
    crawler.quit()


if __name__ == '__main__':
    main()
