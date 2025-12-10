import requests
from bs4 import BeautifulSoup


def get_kbs_headlines():
    """
    KBS 뉴스 홈페이지에 접속하여 주요 헤드라인 뉴스를 가져와 화면에 출력합니다.
    """
    # 1. KBS 뉴스 메인 페이지 접속
    url = 'https://news.kbs.co.kr/news/pc/main/main.html'

    # 로봇(크롤러)으로 오인받지 않도록 User-Agent 설정
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        # requests를 사용하여 웹 페이지 정보 요청
        response = requests.get(url, headers=headers)

        # 응답 코드가 200(성공)이 아닌 경우 예외 발생
        response.raise_for_status()

        # 2. BeautifulSoup을 사용하여 HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')

        # 3. 개발자 도구로 찾아낸 헤드라인 뉴스 가져오기
        # 사용자 발견: .txt-wrapper 안의 .title (가장 큰 메인 헤드라인)
        # 추가: 일반 리스트 기사의 제목인 .tit 클래스도 함께 포함하여 풍부한 리스트 구성
        headlines = soup.select('.txt-wrapper .title, .tit')

        print(f"=== KBS 뉴스 헤드라인 ({len(headlines)}건) ===")
        print("-" * 60)

        # 4. List 객체(headlines)를 순회하며 텍스트 출력
        count = 1
        for tag in headlines:
            # 태그 내의 텍스트만 추출하고 앞뒤 공백 제거
            title = tag.get_text().strip()

            # 빈 제목이 아닌 경우에만 출력
            if title:
                print(f"{count}. {title}")
                count += 1

        print("-" * 60)

    except requests.exceptions.RequestException as e:
        print(f"웹 페이지 요청 중 오류가 발생했습니다: {e}")
    except Exception as e:
        print(f"알 수 없는 오류가 발생했습니다: {e}")


if __name__ == '__main__':
    # 메인 함수 실행
    get_kbs_headlines()
