import json
import requests
import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QGridLayout,
                             QDesktopWidget, QPushButton, QAction, QLineEdit, QMessageBox)
from PyQt5.QtGui import QIcon

app_id = 'c12e32d2'
app_key = 'bb73cf8adadb2d0b1704ca43c2782fe0'

language = 'en'
word_id = 'Ace'

class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        # attributes
        self.textbox = None

        self.initUI()
        self.show()

    def initUI(self):

        # Main Window Init
        self.setWindowTitle('Dictionary')
        self.setWindowIcon(QIcon("icons/book.png"))
        self.resize(250, 150)
        self.center()

        # Window init
        window = QWidget()
        self.setCentralWidget(window)
        grid = QGridLayout()
        window.setLayout(grid)

        # Widgets Init
        self.textbox = QLineEdit(self)
        self.textbox.resize(self.sizeHint())
        self.textbox.returnPressed.connect(self.on_click)

        search_button = QPushButton("Search", self)
        search_button.clicked.connect(self.on_click)

        # Add to layout
        grid.addWidget(self.textbox, 1, 0)
        grid.addWidget(search_button, 1, 1)

    def on_click(self):
        url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + self.textbox.text().lower()
        data = requests.get(url, headers={'app_id': app_id, 'app_key': app_key}).json()
        defn = data['results'][0]['lexicalEntries']

        print(defn)


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
