def r_csv(filename):
    """CSV 파일을 읽어서 List 객체로 변환"""
    data = []
    try:
        with open(filename, 'r') as file:
            header = next(file)  # 첫째 줄 스킵
            for line in file:
                values = line.strip().split(',')
                if len(values) >= 5:
                    try:
                        values[4] = float(values[4])  # 인화성 지수 변환
                        data.append(values)
                    except ValueError:
                        print(f"숫자 변환 불가: {values}")
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {filename}")
    except Exception as e:
        print(f"파일을 읽는 중 오류 발생: {e}")
    return data


def w_csv(filename, data):
    """리스트 데이터를 CSV 파일로 저장"""
    try:
        with open(filename, 'w') as file:
            for item in data:
                file.write(f"{item[0]},{item[4]}\n")
    except Exception as e:
        print(f"파일 저장 실패: {e}")

# 보너스 과제
def w_binary(filename, data):
    """정렬된 데이터를 이진 파일로 저장"""
    try:
        with open(filename, 'wb') as file:
            for item in data:
                line = f"{item[0]},{item[4]}\n"
                file.write(line.encode())
    except Exception as e:
        print(f"이진 파일 저장 실패: {e}")


def r_binary(filename):
    """이진 파일을 읽어 출력"""
    try:
        with open(filename, 'rb') as file:
            content = file.read().decode()
            print(content)
    except Exception as e:
        print(f"이진 파일 읽기 실패: {e}")


def main():
    csv_filename = 'Mars_Base_Inventory_List.csv'
    danger_csv_filename = 'Mars_Base_Inventory_danger.csv'
    binary_filename = 'Mars_Base_Inventory_List.bin'

    inventory_data = r_csv(csv_filename)
    if not inventory_data:
        return

    inventory_data.sort(key=lambda x: x[4], reverse=True)

    danger_items = [item for item in inventory_data if item[4] >= 0.7]

    w_csv(danger_csv_filename, danger_items)

    # 보너스 과제
    w_binary(binary_filename, inventory_data)

    print("이진 파일에서 읽은 데이터:")
    r_binary(binary_filename)

    print("\n작업 완료")


if __name__ == "__main__":
    main()