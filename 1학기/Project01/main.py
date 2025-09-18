def read_log_file(file_path):
    try:
        with open(file_path, 'r', encoding = 'utf-8') as file:
            log_contents = file.readlines()
            for line in log_contents:
                print(line.strip())
            return log_contents
    except FileNotFoundError:
        print('\n오류 : ' + file_path + ' 파일 위치를 찾을 수 없습니다.')
        return None
    except Exception as e:
        print('\n오류 발생 : ' + str(e))
        return None

def generate_report(log_contents, report_path):
    with open(report_path, 'w', encoding='utf-8') as file:
        file.write('# 문제 로그 보고서\n\n')
        file.write('## 다음은 시스템에서 감지된 이상 로그입니다.\n\n')

        for line in log_contents:
            parts = line.strip().split(',', 2)
            if len(parts) == 3:
                log_time, log_event, log_message = parts

                if 'unstable' in log_message.lower() or 'explosion' in log_message.lower():
                    file.write(f'### 시간: {log_time}\n')
                    file.write(f'- 이벤트: {log_event}\n')
                    file.write(f'- 메시지: {log_message}\n\n')

    print('\n보고서가 생성 완료 : ', report_path)

def main():
    log_file = 'mission_computer_main.log'
    report_file = 'log_analysis.md'

    log_contents = read_log_file(log_file)

    print("\n\n")

    for line in reversed(log_contents):
        print(line.strip())

    if log_contents is not None:
        generate_report(log_contents, report_file)

main()