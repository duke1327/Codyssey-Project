import os
import datetime
import sounddevice as sd
from scipy.io.wavfile import write


class VoiceRecorder:
    def __init__(self, sample_rate=44100, duration=3): # 3초만 녹음되게
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

    # 보너스 과제
    def list_recordings_in_range(self, start_date, end_date):
        # start_date, end_date: 문자열 'YYYYMMDD' 형식
        self.ensure_records_dir_exists() # 폴더 있는지부터 검사

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

            file_date_str = filename[:8]  # 'YYYYMMDD'
            try:
                file_date = datetime.datetime.strptime(file_date_str, '%Y%m%d')
            except ValueError:
                continue

            if start <= file_date <= end:
                file_list.append(filename)
                print(f' - {filename}')
                found = True

        if not file_list:
            print('해당 날짜 범위의 파일이 없습니다.')
            return


        check_play = input('\n이 중에서 재생할 파일이 있습니까? (y/n): ').strip().lower()

        if check_play == 'y':
            # 해당 범위 리스트 보여주기
            for i, fname in enumerate(file_list, start=1):
                print(f' [{i}] {fname}')

            try:
                choice = int(input('재생할 파일의 번호를 입력하세요: '))
                if 1 <= choice <= len(file_list):
                    file_path = os.path.join(self.records_dir, file_list[choice - 1])
                    print(f'재생 중: {file_path}')
                    os.startfile(file_path)  # Windows 전용
                else:
                    print('잘못된 번호입니다.')
            except ValueError:
                print('숫자를 입력해주세요.')
        else:
            print('재생하지 않고 종료합니다.')

def main():
    recorder = VoiceRecorder()

    print('\n[1] 음성 녹음하기')
    print('[2] 녹음 파일 조회하기 (날짜 범위)')
    choice = input('원하는 작업을 선택하세요 (1 또는 2): ')

    if choice == '1':
        recorder.run_recording()
    elif choice == '2':
        start = input('시작 날짜를 입력하세요 (YYYYMMDD): ')
        end = input('종료 날짜를 입력하세요 (YYYYMMDD): ')
        recorder.list_recordings_in_range(start, end)
    else:
        print('잘못된 선택입니다. 프로그램을 종료합니다.')

if __name__ == '__main__':
    main()
