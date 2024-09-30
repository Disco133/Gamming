import sys
from qtpy.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
import pandas as pd
import numpy as np

def convert_to_char(x):
    return chr(x + 1040)

gamma_key = []
def encrypt(string: str) -> str:
    global gamma_key
    data0 = pd.Series(list(string))

    # Фильтрация символов
    filtered_chars = [char for char in data0 if char.isalpha() and (1103 >= ord(char) >= 1040)]

    # Нормализация значений
    normalized_values = [ord(char) - 1040 for char in filtered_chars]

    # Создание Series
    data = pd.Series(normalized_values, dtype='int8')

    # Генерация Гамма-шифра по зерну
    np.random.seed(42)
    gamma_key = np.random.randint(0, 64, size=data.size, dtype='int8')

    # Побитовая операция XOR
    cypher = (data ^ gamma_key)

    # Возвращение закодированных символов в виде строки
    return ''.join(cypher.apply(convert_to_char))

class EncryptionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Шифрование и Дешифрование')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.input_label = QLabel('Введите строку:')
        layout.addWidget(self.input_label)

        self.input_text = QLineEdit(self)
        layout.addWidget(self.input_text)

        self.encrypt_button = QPushButton('Зашифровать', self)
        self.encrypt_button.clicked.connect(self.encrypt_text)
        layout.addWidget(self.encrypt_button)

        self.decrypt_button = QPushButton('Дешифровать', self)
        self.decrypt_button.clicked.connect(self.decrypt_text)
        layout.addWidget(self.decrypt_button)

        self.setLayout(layout)

    def encrypt_text(self):
        input_string = self.input_text.text()
        encrypted_string = encrypt(input_string)
        self.input_text.setText(encrypted_string)

    def decrypt_text(self):
        input_string = self.input_text.text()
        decrypted_string = encrypt(input_string)
        self.input_text.setText(decrypted_string)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EncryptionApp()
    ex.show()
    sys.exit(app.exec_())

