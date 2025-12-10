import requests
from bs4 import BeautifulSoup


def get_current_weather():
    """
    기상청 '도시별 관측' 페이지에서 주요 도시의 현재 기온을 가져와 출력합니다.
    """
    # 1. 기상청 도시별 관측 페이지 URL
    url = 'https://www.weather.go.kr/w/obs-climate/land/city-obs.do'

    # 봇 탐지 방지용 User-Agent 설정
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        # 2. 웹 페이지 요청
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # 3. HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')

        # 4. 날씨 데이터가 담긴 테이블의 행(tr)들을 선택
        # class가 'table-col'인 테이블의 tbody 안에 있는 모든 tr 태그 가져오기
        rows = soup.select('.table-col tbody tr')

        print(f"=== 기상청 도시별 현재 기온 ({len(rows)}개 지점) ===")
        print(f"{'도시명':<10} | {'현재기온':<10}")
        print("-" * 30)

        # 5. 각 행을 순회하며 데이터 추출
        for row in rows:
            # 한 행에 있는 모든 칸(td) 가져오기
            cols = row.select('td')

            # 데이터가 충분한지 확인 (유효한 행인지 체크)
            if len(cols) > 5:
                # 첫 번째 칸(인덱스 0): 도시 이름 (종종 a 태그 안에 있음)
                city = cols[0].get_text().strip()

                # 여섯 번째 칸(인덱스 5): 현재 기온
                temp = cols[5].get_text().strip()

                # 데이터가 비어있지 않은 경우 출력
                if city and temp:
                    print(f"{city:<10} | {temp}℃")

        print("-" * 30)

    except requests.exceptions.RequestException as e:
        print(f"네트워크 오류가 발생했습니다: {e}")
    except Exception as e:
        print(f"알 수 없는 오류가 발생했습니다: {e}")


if __name__ == '__main__':
    get_current_weather()
