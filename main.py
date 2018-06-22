import json
import requests
import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QVBoxLayout, QLabel,
                             QDesktopWidget, QLineEdit)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

# API info
app_id = 'c12e32d2'
app_key = 'bb73cf8adadb2d0b1704ca43c2782fe0'
language = 'en'


class Dictionary(QMainWindow):

    def __init__(self):
        super().__init__()

        # attributes
        self.win_width = 480
        self.win_height = 720
        self.vbox = QVBoxLayout()
        self.textbox = []
        self.display_labels = []

        # methods
        self.initUI()
        self.show()

    def initUI(self):

        # Main Window Init
        self.setWindowTitle('Dictionary')
        self.setWindowIcon(QIcon("icons/book.png"))
        self.setFixedSize(self.win_width, self.win_height)
        self.center()

        # Window init
        window = QWidget()
        self.setCentralWidget(window)
        window.setLayout(self.vbox)

        # Widgets Init
        self.init_dynamic_widgets()

    def init_dynamic_widgets(self):

        for x in range(0, 5):

            # TextBox
            temp = QLineEdit()
            font = QFont('PT Sans', 18)  # Textbox font
            temp.setFont(font)
            temp.index = x  # index of textbox
            temp.returnPressed.connect(self.on_returnPressed)
            self.textbox.append(temp)

            # Label
            temp = QLabel()
            temp.setTextInteractionFlags(Qt.TextSelectableByMouse)  # Enables text select
            font = QFont('PT Sans', 11)  # label font
            temp.setFont(font)
            self.display_labels.append(temp)

            # Add to VBox Layout
            self.vbox.addWidget(self.textbox[x])
            self.vbox.addWidget(self.display_labels[x])

    def on_returnPressed(self):

        word_id = self.sender().text()
        index = self.sender().index

        url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + word_id.lower()
        r = requests.get(url, headers={'app_id': app_id, 'app_key': app_key})

        # Handles definition not found
        if r.status_code == 404:
            self.display_labels[index].setText("Definition not found.")
            return

        json_data = json.dumps(r.json())
        self.display_labels[index].setText(self.json_definition(json_data))

    def json_definition(self, json_data):
        return json_data


    # Centers window
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Dictionary = Dictionary()
    sys.exit(app.exec_())
