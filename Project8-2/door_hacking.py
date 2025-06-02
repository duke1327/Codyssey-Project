import zipfile
import itertools
import string
import time
from io import BytesIO
import multiprocessing
import os

def try_prefix_range(prefixes, zip_data, file_name, result_queue, stop_flag):
    zip_file = zipfile.ZipFile(BytesIO(zip_data))
    charset = string.ascii_lowercase + string.digits

    for prefix in prefixes:
        for suffix in itertools.product(charset, repeat=5):
            if stop_flag.is_set():
                return
            password = prefix + ''.join(suffix)
            try:
                zip_file.read(file_name, pwd=password.encode())
                result_queue.put(password)
                stop_flag.set()
                return
            except:
                continue
    result_queue.put(None)

def unlock_zip():
    zip_filename = "emergency_storage_key.zip"
    charset = string.ascii_lowercase + string.digits
    output_file = "password.txt"
    max_length = 6
    num_workers = multiprocessing.cpu_count()

    try:
        with open(zip_filename, "rb") as f:
            zip_data = f.read()
    except FileNotFoundError:
        print("ZIP 파일을 찾을 수 없습니다.")
        return

    try:
        zip_file = zipfile.ZipFile(BytesIO(zip_data))
        file_list = zip_file.namelist()
        if not file_list:
            print("ZIP 안에 파일이 없습니다.")
            return
        file_name = file_list[0]
    except Exception as e:
        print(f"ZIP 처리 중 오류 발생: {e}")
        return

    prefixes = list(charset)
    chunk_size = len(prefixes) // num_workers + (len(prefixes) % num_workers > 0)
    prefix_chunks = [prefixes[i:i+chunk_size] for i in range(0, len(prefixes), chunk_size)]

    print(f"{num_workers}개의 코어로 prefix 분할 병렬 해제를 시작합니다...")
    start_time = time.time()

    result_queue = multiprocessing.Queue()
    stop_flag = multiprocessing.Event()

    processes = []
    for chunk in prefix_chunks:
        p = multiprocessing.Process(
            target=try_prefix_range,
            args=(chunk, zip_data, file_name, result_queue, stop_flag)
        )
        p.start()
        processes.append(p)

    found_password = None
    while True:
        result = result_queue.get()
        if result:
            found_password = result
            break

    elapsed = time.time() - start_time

    if found_password:
        print(f"\n성공! 암호: {found_password}")
        print(f"걸린 시간: {elapsed:.2f}초")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(found_password)
        zip_file.extractall(pwd=found_password.encode())
    else:
        print("암호를 찾지 못했습니다.")

    for p in processes:
        if p.is_alive():
            p.terminate()

if __name__ == "__main__":
    unlock_zip()
