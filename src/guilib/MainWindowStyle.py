main_window_style = """
#MainWindow {
  background-color: black;
}

QMenuBar {
  background-color: black;
  color: white;
}

QMenuBar::item {
  background-color: black;
  color: white;
}

QMenuBar::item::selected {
  background-color: lightgray;
  color: black;
}

QMenu {
  background-color: black;
  color: white;
  border: 1px solid #fff;
}

QMenu::item::selected {
  background-color: lightgray;
  color: black;
}

QPushButton {
  border-style: solid;
  border-color: grey;
  border-width: 2px;
  border-radius: 6px;
  color: white;
  font-size: 10pt;
  font-weight: bold;
}

QPushButton:Pressed {
  border-style: solid;
  border-color: black;
  border-width: 2px;
  border-radius: 6px;
  color: black;
  font-size: 10pt;
  font-weight: bold;
}

QLabel#TitleLabel {
  background-color: black;
  color: white;
  padding: 20 20 20 20;
  font-size: 20pt;
  font-weight: bold;
}

QLabel#StatusLabel {
  background-color: black;
  color: white;
  padding: 20 20 20 20;
  font-size: 14pt;
  font-weight: bold;
}

QTableWidget#DeviceTable {
  background-color: black;
  color: white;
  font-size: 12pt;
  font-weight: medium;
}
"""
