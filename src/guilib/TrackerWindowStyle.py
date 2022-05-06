tracker_window_style = """
#TrackerWindow {
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
  background-color: black;
  font-size: 10pt;
  font-weight: bold;
}

QPushButton:pressed {
  border-style: solid;
  border-color: black;
  border-width: 2px;
  border-radius: 6px;
  color: black;
  background-color: white;
  font-size: 10pt;
  font-weight: bold;
}

QLabel {
  background-color: black;
  color: white;
  padding: 20 20 20 20;
  font-size: 12pt;
  font-weight: bold;
}

QLabel#devinfo {
  background-color: black;
  color: white;
  padding: 2 2 2 2;
  font-size: 9pt;
  font-weight: bold;
}

QHBoxLayout#actionButtonLayout {
  background-color: black;
  color: white;
  padding: 40 40 40 40;
}

QToaster {
    border: 1px solid gray;
    border-radius: 4px;
    background-color: black;
    color: white;
}
"""
