import os
import csv
import datetime
import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr


class VoiceRecorder:
    def __init__(self, sample_rate=44100, duration=3): # duration초동안 녹음
        self.sample_rate = sample_rate
        self.duration = duration
        self.records_dir = 'records'

    # 저장 폴더 없으면 생성하기
    def ensure_records_dir_exists(self):
        if not os.path.exists(self.records_dir):
            os.makedirs(self.records_dir)

    # 녹음 파일명 생성
    def generate_filename(self):
        now = datetime.datetime.now()
        timestamp = now.strftime('%Y%m%d-%H%M%S')
        filename = f'{timestamp}.wav'
        return os.path.join(self.records_dir, filename)

    # 녹음
    def record_audio(self):
        print('녹음을 시작합니다...')
        audio_data = sd.rec(
            int(self.sample_rate * self.duration),
            samplerate=self.sample_rate,
            channels=1,
            dtype='int16'
        )
        sd.wait()
        print('녹음이 완료되었습니다.')
        return audio_data

    def save_audio(self, audio_data, filepath):
        write(filepath, self.sample_rate, audio_data)
        print(f'파일이 저장되었습니다: {filepath}')

    def run_recording(self):
        self.ensure_records_dir_exists()
        audio_data = self.record_audio()
        filename = self.generate_filename()
        self.save_audio(audio_data, filename)

    def list_recordings_in_range(self, start_date, end_date):
        self.ensure_records_dir_exists()

        try:
            start = datetime.datetime.strptime(start_date, '%Y%m%d')
            end = datetime.datetime.strptime(end_date, '%Y%m%d')
        except ValueError:
            print('날짜 형식이 잘못되었습니다. YYYYMMDD 형식으로 입력해주세요.')
            return

        print(f'\n📁 {start_date} ~ {end_date} 사이의 녹음 파일 목록:')
        file_list = []
        for filename in os.listdir(self.records_dir):
            if not filename.endswith('.wav'):
                continue

            file_date_str = filename[:8]
            try:
                file_date = datetime.datetime.strptime(file_date_str, '%Y%m%d')
            except ValueError:
                continue

            if start <= file_date <= end:
                file_list.append(filename)
                print(f' - {filename}')

        if not file_list:
            print('해당 날짜 범위의 파일이 없습니다.')
            return

        check_play = input('\n이 중에서 재생할 파일이 있습니까? (y/n): ').strip().lower()

        if check_play == 'y':
            for i, fname in enumerate(file_list, start=1):
                print(f' [{i}] {fname}')

            try:
                choice = int(input('재생할 파일의 번호를 입력하세요: '))
                if 1 <= choice <= len(file_list):
                    file_path = os.path.join(self.records_dir, file_list[choice - 1])
                    print(f'재생 중: {file_path}')
                    os.startfile(file_path)
                else:
                    print('잘못된 번호입니다.')
            except ValueError:
                print('숫자를 입력해주세요.')
        else:
            print('재생하지 않고 종료합니다.')


class VoiceProcessor:
    def __init__(self, records_dir='records'):
        self.records_dir = records_dir

    # 모든 녹음 파일을 STT로 변환
    def process_all_recordings(self):
        recognizer = sr.Recognizer()
        for filename in os.listdir(self.records_dir):
            if filename.endswith('.wav'):
                filepath = os.path.join(self.records_dir, filename)
                print(f'처리 중: {filename}')

                with sr.AudioFile(filepath) as source:
                    audio = recognizer.record(source)

                try:
                    text = recognizer.recognize_google(audio, language='ko-KR')
                    print(f'인식된 텍스트: {text}')
                except sr.UnknownValueError:
                    text = '[인식 실패]'
                    print('음성을 인식할 수 없습니다.')
                except sr.RequestError as e:
                    text = '[API 오류]'
                    print(f'STT 요청 실패: {e}')

                csv_filename = filename.replace('.wav', '.csv')
                csv_path = os.path.join(self.records_dir, csv_filename)
                with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['시간', '인식된 텍스트'])
                    writer.writerow(['00:00', text])
                print(f'CSV로 저장됨: {csv_path}')

    # 보너스 과제
    def search_keyword_in_csv(self, keyword):
        found = False
        for filename in os.listdir(self.records_dir):
            if filename.endswith('.csv'):
                filepath = os.path.join(self.records_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    next(reader)
                    for row in reader:
                        if keyword in row[1]:
                            print(f'[{filename}] {row[0]} - {row[1]}')
                            found = True
        if not found:
            print('해당 키워드가 포함된 텍스트를 찾을 수 없습니다.')


def main():
    recorder = VoiceRecorder()
    processor = VoiceProcessor()

    print('\n[1] 음성 녹음하기')
    print('[2] 녹음 파일 조회하기 (날짜 범위)')
    print('[3] 음성 파일 STT 처리 후 CSV 저장')
    print('[4] 키워드로 CSV 텍스트 검색')

    choice = input('원하는 작업을 선택하세요 (1 ~ 4): ')

    if choice == '1':
        recorder.run_recording()
    elif choice == '2':
        start = input('시작 날짜를 입력하세요 (YYYYMMDD): ')
        end = input('종료 날짜를 입력하세요 (YYYYMMDD): ')
        recorder.list_recordings_in_range(start, end)
    elif choice == '3':
        processor.process_all_recordings()
    elif choice == '4':
        keyword = input('검색할 키워드를 입력하세요: ')
        processor.search_keyword_in_csv(keyword)
    else:
        print('잘못된 선택입니다. 프로그램을 종료합니다.')


if __name__ == '__main__':
    main()
