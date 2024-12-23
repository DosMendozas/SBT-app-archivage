import sys
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFrame
from PySide6.QtCore import Qt
from connexion import LoginWindow  # Importer la classe LoginWindow depuis connexion.py

class AccueilWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Titre de la fenêtre
        self.setWindowTitle("Interface d'accueil")
        self.setGeometry(100, 100, 700, 400)

        # SECTION droite
        self.right_frame = QFrame(self)
        self.right_frame.setGeometry(0, 0, 700, 400)
        self.right_frame.setStyleSheet("border-radius: 30px;")

        # Ajout d'une image
        self.image_label = QLabel(self.right_frame)
        self.image_label.setGeometry(0, 0, self.right_frame.width(), self.right_frame.height())
        self.image_label.setPixmap(QPixmap("logo-SBT.png"))
        self.image_label.setScaledContents(True)
        self.image_label.setAlignment(Qt.AlignCenter)

        # Bouton Suivant
        self.aller_button = QPushButton("Suivant...", self.right_frame)
        self.aller_button.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #000000;
                border-radius: 15px;
                padding: 5px 8px;
            }
            QPushButton:hover {
                background-color: #cce7e5;
            }
        """)
        self.aller_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.aller_button.setGeometry(290, 330, 120, 40)  
        self.aller_button.clicked.connect(self.bouton_suivant)

    def bouton_suivant(self):
        self.login_window = LoginWindow() 
        self.login_window.show()            
        self.hide()                        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AccueilWindow()
    window.show()
    sys.exit(app.exec())
