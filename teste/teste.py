from PyQt5.QtWidgets import QLineEdit, QApplication, QWidget

class Teste(QWidget):
    def __init__(self):
        super().__init__()

        self.lnEdit = QLineEdit(self)
        self.lnEdit.setPlaceholderText("Teste")

        self.lnEdit.mousePressEvent = self.clique()

        self