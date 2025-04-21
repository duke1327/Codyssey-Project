import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('iPhone Calculator')
        self.setFixedSize(320, 480)
        self.setStyleSheet('background-color : black;')

        # 입력 문자열
        self.current_expression = ''

        # 계산 후 숫자 입력시 초기화용
        self.just_cal = False

        self.initUI()

    def initUI(self):
        # 수직 박스 레이아웃 (수평 박스 레이아웃은 QHBoxLayout())
        main_layout = QVBoxLayout()
        # 입력창
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        # 입력창 스타일
        self.display.setStyleSheet(
            "font-size: 32px; background: black; color: white; padding: 20px; border: none;"
        )
        main_layout.addWidget(self.display)

        # 그리드 레이아웃
        button_layout = QGridLayout()
        buttons = [
            ['AC', '±', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '−'],
            ['1', '2', '3', '+'],
            ['0', '', '.', '=']
        ]

        for row, row_values in enumerate(buttons):
            for col, text in enumerate(row_values):
                if text == '':
                    continue  # 빈 버튼은 스킵

                btn = QPushButton(text)
                btn.clicked.connect(self.on_button_click)
                btn.setFixedHeight(60)

                # 0번은 가로 두 칸 차지
                if text == '0':
                    btn.setFixedWidth(140)
                    btn_layout = button_layout.addWidget(btn, row, col, 1, 2)
                else:
                    btn.setFixedWidth(60)
                    btn_layout = button_layout.addWidget(btn, row, col)

                # 버튼 스타일
                if text in ['AC', '±', '%']:
                    btn.setStyleSheet("background-color : lightgray; font-size : 20px; border-radius : 30px;")
                elif text in ['÷', '×', '−', '+', '=']:
                    btn.setStyleSheet("background-color : orange; color : white; font-size : 20px; border-radius : 30px;")
                else:
                    btn.setStyleSheet("background-color : #333333; color : white; font-size : 20px; border-radius : 30px;")

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    # 버튼 클릭시 발동
    def on_button_click(self):
        # 클릭 버튼 객체 가져오기
        sender = self.sender()
        text = sender.text()

        if text == 'AC':
            self.current_expression = ''
            self.just_cal = False
        # 보너스 과제
        elif text == '=':
            try:
                expression = self.current_expression.replace('×', '*').replace('÷', '/').replace('−', '-')
                result = str(eval(expression))
                self.current_expression = result
                self.just_cal = True
            except Exception:
                self.current_expression = 'Error'
                self.just_cal = True
        elif text == '±':
            if self.current_expression and self.current_expression[0] == '-':
                self.current_expression = self.current_expression[1:]
            elif self.current_expression:
                self.current_expression = '-' + self.current_expression
        elif text == '%':
            try:
                value = str(eval(self.current_expression + "/100"))
                self.current_expression = value
                self.just_cal = True
            except Exception:
                self.current_expression = 'Error'
                self.just_cal = False
        else:
            # 계산 후 바로 숫자가 입력되면 기존 문자열 없애고 새로 만들기
            if self.just_cal and text.isdigit():
                self.current_expression = text
                # 후에 문자열이 이어지도록 설정
                self.just_cal = False
            # 사칙연산이나 기타 부호일 경우엔 그 뒤에 붙이기
            else:
                self.current_expression += text
                self.just_cal = False

        self.display.setText(self.current_expression)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())