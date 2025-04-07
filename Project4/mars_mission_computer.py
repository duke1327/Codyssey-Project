import time
from dummy_sensor import DummySensor

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
                print('}\n')

            # 5초마다 반복하게 설정
            time.sleep(5)

if __name__ == '__main__':
    # RunComputer로 인스턴스화
    RunComputer = MissionComputer()
    RunComputer.get_sensor_data()