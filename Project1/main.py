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
        file.write('# 보고서\n')

        file.write('## 로그 기록\n')
        for line in log_contents:
            parts = line.strip().split(',', 2)
            if len(parts) == 3:
                log_time, log_event, log_message = parts
                file.write(f'시간 : {log_time}\n')
                file.write(f'이벤트 : {log_event}\n')
                file.write(f'메시지 : {log_message}\n\n')

    print('\n보고서가 생성 완료 : ', report_path)

def main():
    log_file = 'mission_computer_main.log'
    report_file = 'log_analysis.md'

    log_contents = read_log_file(log_file)

    if log_contents is not None:
        generate_report(log_contents, report_file)

main()