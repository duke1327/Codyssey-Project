import os.path
import platform
import psutil

class MissionComputer:
    # 해당 문제에 필요없는 변수 메소드는 전부 지움
    def __init__(self):
        # 보너스 과제
        self.setting_file = 'setting.txt'
        self.default_options = {
            'os', 'os_version', 'cpu_type', 'cpu_core',
            'memory', 'cpu_usage', 'memory_usage'
        }
        self.settings = self.load_or_create_settings()

    # 보너스 과제
    def load_or_create_settings(self):
        # 파일이 없으면 기본 세팅으로 설정 후 생성, 후에 설정 항목 확인
        if not os.path.exists(self.setting_file):
            print(f"'{self.setting_file}' 파일이 없어 기본 설정으로 생성합니다.")
            with open(self.setting_file, 'w', encoding='utf-8') as f:
                f.write('os, os_version, cpu_type, cpu_core, memory, cpu_usage, memory_usage\n')
                f.write('\n'.join(self.default_options))
            return set(self.default_options)
        else:
            with open(self.setting_file, 'r', encoding='utf-8') as f:
                header = next(f)
                return set(line.strip() for line in f if line.strip())

    # get_mission_computer_info 메소드 추가
    def get_mission_computer_info(self):
        # 미션 컴퓨터의 시스템 정보
        # 보너스 과제 setting.txt 내용에 따라 선택적으로 출력
        try:
            print('Mission Computer Info')
            if "os" in self.settings:
                print("os : ", platform.system())
            if "os_version" in self.settings:
                print("os_version : ", platform.version())
            if "cpu_type" in self.settings:
                print("cpu_type : ", platform.processor())
            if "cpu_core" in self.settings:
                print("cpu_core : ", psutil.cpu_count(logical=False))
            # 메모리는 GB 단위로 출력하게
            if "memory" in self.settings:
                memory_gb = round(psutil.virtual_memory().total / (1024 ** 3), 2)
                print("memory(GB) : ", memory_gb)
        # 예외처리
        except Exception as e:
            print(f'시스템 정보 획득 실패 : {e}')
            return None

    # get_mission_computer_load 메소드 추가
    def get_mission_computer_load(self):
        # 미션 컴퓨터의 부하 정보
        try:
            load = {
                'cpu_usage' : psutil.cpu_percent(interval=1),
                'memory_usage' : psutil.virtual_memory().percent
            }
            print('\nMission Computer Load')
            if "cpu_usage" in self.settings:
                print("cpu_usage : ", psutil.cpu_percent(interval=1))
            if "memory_usage" in self.settings:
                print("memory_usage : ", psutil.virtual_memory().percent)
            return load
        # 예외처리
        except Exception as e:
            print(f'부하 정보 획득 실패 : {e}')
            return None

if __name__ == '__main__':
    # runComputer로 인스턴스화
    runComputer = MissionComputer()
    runComputer.get_mission_computer_info()
    runComputer.get_mission_computer_load()