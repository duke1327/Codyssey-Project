import time
import random

class DummySensor:
    # 사전 객체 추가
    def __init__(self):
        self.__env_values = {
            'mars_base_internal_temperature' : 0.0,
            'mars_base_external_temperature' : 0.0,
            'mars_base_internal_humidity' : 0.0,
            'mars_base_external_illuminance' : 0.0,
            'mars_base_internal_co2' : 0.0,
            'mars_base_internal_oxygen' : 0.0
        }

    # set_env() 메소드 추가
    def set_env(self):
        self.__env_values['mars_base_internal_temperature'] = round(random.uniform(18, 30), 2)
        self.__env_values['mars_base_external_temperature'] = round(random.uniform(0, 21), 2)
        self.__env_values['mars_base_internal_humidity'] = round(random.uniform(50, 60), 2)
        self.__env_values['mars_base_external_illuminance'] = round(random.uniform(500, 715), 2)
        self.__env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 2)
        self.__env_values['mars_base_internal_oxygen'] = round(random.uniform(4, 7), 2)

    # get_env() 메소드 추가
    def get_env(self):
        # 보너스 과제
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        log_line = (
            f'{now}, '
            f"{self.__env_values['mars_base_internal_temperature']}°C, "
            f"{self.__env_values['mars_base_external_temperature']}°C, "
            f"{self.__env_values['mars_base_internal_humidity']}%, "
            f"{self.__env_values['mars_base_external_illuminance']} W/m2, "
            f"{self.__env_values['mars_base_internal_co2']}%, "
            f"{self.__env_values['mars_base_internal_oxygen']}%\n"
        )
        # log 파일 작성
        try:
            with open('sensor_log.log', 'r', encoding='utf-8') as log_check:
                log_content = log_check.readlines()
        except FileNotFoundError as f:
            log_content = []
        try:
            with open('sensor_log.log', 'a', encoding='utf-8') as log_file:
                if not log_content:
                    log_file.write('Dummy Sensor 로그 파일입니다.\n')
                    log_file.write('날짜, 기지 내부 온도, 기지 외부 온도, 기지 내부 습도, ')
                    log_file.write('기지 외부 광량, 기지 내부 이산화탄소 농도, 기지 내부 산소 농도\n')

                log_file.write(log_line)
        except Exception as e:
            print(f"파일 작성 중 오류 발생: {e}")
        return self.__env_values

class MissionComputer:
    # 사전 객체 추가
    def __init__(self):
        self.__env_values = {
            'mars_base_internal_temperature' : 0.0,
            'mars_base_external_temperature' : 0.0,
            'mars_base_internal_humidity' : 0.0,
            'mars_base_external_illuminance' : 0.0,
            'mars_base_internal_co2' : 0.0,
            'mars_base_internal_oxygen' : 0.0
        }

        self.ds = DummySensor()

        # 보너스 과제
        # 5분동안 저장할 내역
        self.__history = {
            key: [] for key in self.__env_values
        }

    # get_sensor_data() 메소드 추가
    def get_sensor_data(self):
        # 5분을 셀 카운트 추가
        count = 0
        
        try:
            # 반복문 설정
            while True:
                # DummySensor에서 값을 가져와서 담기
                self.ds.set_env()
                self.__env_values = self.ds.get_env()

                # 평균 구할 값 저장
                for key in self.__env_values:
                    self.__history[key].append(self.__env_values[key])

                # json 형식로 화면에 출력 (json 메소드 안 쓰기)
                print('{')
                keys = list(self.__env_values.keys())
                for i, key in enumerate(keys):
                    value = self.__env_values[key]
                    comma = ',' if i < len(keys) - 1 else ''
                    print(f"  '{key}' : {value}{comma}")
                print('}\n')

                # 5초마다 카운트 1개씩 추가
                count += 1

                # 5분(300초) / 5초 =  60번 수행했을 시 평균 구함
                if count % 60 == 0:
                    print('5분 평균 환경 값 :')
                    print('{')
                    for i, key in enumerate(keys):
                        values = self.__history[key][-60:]
                        avg = sum(values) / len(values)
                        comma = ',' if i < len(keys) - 1 else ''
                        print(f"  '{key}_5min_avg' : {round(avg, 2)}{comma}")
                        self.__history[key] = []
                    print('}\n')

                # 5초마다 반복하게 설정
                time.sleep(5)
        # 특정 키 입력시 종료
        except KeyboardInterrupt:
            print('Sytem stoped….')

if __name__ == '__main__':
    # RunComputer로 인스턴스화
    RunComputer = MissionComputer()
    RunComputer.get_sensor_data()