#!/usr/bin/env python

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
import curlconverter
# import pprint, uncurl

def dict_printer(d):
    s = ""
    for k,v in d.items():
        if isinstance(v,dict):
            s = s + dict_printer(v)
        else:
            s = s + f"{k} -> {v}" + "\n"
    return s

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Please 🙏")

        container = QWidget()
        self.layout: QVBoxLayout = QVBoxLayout()
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Paste Curl Here")

        submit_button = QPushButton("Submit")
        submit_button.pressed.connect(self.on_submit)
        clear_button = QPushButton("Clear")
        clear_button.pressed.connect(self.on_clear)

        self.result_label = QLabel("")
        self.result_label.setWordWrap(True)

        self.layout.addWidget(self.input_box)
        self.layout.addWidget(submit_button)
        self.layout.addWidget(clear_button)
        self.layout.addWidget(self.result_label)

        container.setLayout(self.layout)
        self.setCentralWidget(container)
        self.show()

    def on_clear(self):
        self.input_box.clear()
        self.input_box.setFocus()
        self.result_label.clear()

    def on_submit(self):
        text = self.input_box.text()
        if text.strip() == "":
            return

        parsed, res = self.parse_curl(text)
        if not parsed:
            self.result_label.setText(f"Error parsing curl... please check your curl..\n Error::{res}")
        else:
            self.input_box.clear()
            self.input_box.setFocus()
            self.result_label.setText(dict_printer(res))

    def clean_curl_text(self, text:str):
        text = text.replace("--location","")
        text = text.replace("--header", "-H")
        return text

    def parse_curl(self,text):
        try:
            p = curlconverter.CurlConverter(self.clean_curl_text(text))
            parsed = p.convert()
            # parsed = uncurl.parse_context(self.clean_curl_text(text))
            # pprint.pprint(parsed,indent=4)
            return True, parsed
        except Exception as e:
            return False, e.__str__()

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    app.exec()
