import random
import time

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
            with open('sensor_log.log', 'a', encoding='utf-8') as log_file:
                """
                with open ('sensor_log.log', 'r', encoding='utf-8') as log_check:
                    log_content = log_check.readlines()
                if log_content is None:
                    log_file.write('Dummy Sensor 로그 파일입니다.\n')
                    log_file.write('날짜, 기지 내부 온도, 기지 외부 온도, 기지 내부 습도, ')
                    log_file.write('기지 외부 광량, 기지 내부 이산화탄소 농도, 기지 내부 산소 농도')
                """
            log_file.write(log_line)
        except Exception as e:
            print(f"파일 작성 중 오류 발생: {e}")
        return self.__env_values

def main():
    ds = DummySensor()
    ds.set_env()
    values = ds.get_env()

    # 단위 정보를 사전 정의
    units = {
        'mars_base_internal_temperature': '°C',
        'mars_base_external_temperature': '°C',
        'mars_base_internal_humidity': '%',
        'mars_base_external_illuminance': 'W/m2',
        'mars_base_internal_co2': '%',
        'mars_base_internal_oxygen': '%'
    }

    print('더미 센서 환경 값 출력')
    for key, value in values.items():
        unit = units.get(key, '')
        print(f'{key} : {value}{unit}')

if __name__ == '__main__':
    main()