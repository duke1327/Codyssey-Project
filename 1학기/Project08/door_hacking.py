import zipfile
import itertools
import string
import time
from io import BytesIO

def unlock_zip():
    zip_filename = "emergency_storage_key.zip"
    charset = string.ascii_lowercase + string.digits
    max_length = 6

    try:
        with open(zip_filename, "rb") as f:
            zip_data = f.read()
    except FileNotFoundError:
        print("ZIP 파일을 찾을 수 없습니다.")
        return
    except Exception as e:
        print(f"ZIP 파일을 읽는 중 오류 발생: {e}")
        return

    try:
        zip_file = zipfile.ZipFile(BytesIO(zip_data))
        file_list = zip_file.namelist()  # 내부 파일 목록
        if not file_list:
            print("ZIP 안에 파일이 없습니다.")
            return

        start_time = time.time()
        attempt_count = 0
        print("암호 대입을 시작합니다...")

        for attempt in itertools.product(charset, repeat=max_length):
            password = ''.join(attempt)
            attempt_count += 1
            try:
                # 내부 파일 하나만 시도
                zip_file.read(file_list[0], pwd=password.encode())
                elapsed = time.time() - start_time
                print(f"\n[성공] 암호: {password}")
                print(f"시도 횟수: {attempt_count}")
                print(f"총 소요 시간: {elapsed:.2f}초")

                # 정상이라면 실제 압축 해제
                zip_file.extractall(pwd=password.encode())
                with open("password.txt", "w") as pw_file:
                    pw_file.write(password)
                break
            except RuntimeError:
                # 암호 오류
                if attempt_count % 100000 == 0:
                    print(f"{attempt_count}회 시도 중... (진행 시간: {time.time() - start_time:.2f}초)")
                    print(f"현재 시도 암호 : {password}")
                continue
            except Exception as e:
                continue  # 압축 오류는 무시하고 다음 시도

        else:
            print("모든 조합을 시도했으나 암호를 찾지 못했습니다.")

    except Exception as e:
        print(f"ZIP 처리 중 오류 발생: {e}")

if __name__ == "__main__":
    unlock_zip()