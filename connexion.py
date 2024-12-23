
import sys
import mysql.connector
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QSize, Qt, QUrl
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QCheckBox,
    QFrame, QMessageBox, QComboBox, QInputDialog, QDialog, QVBoxLayout
)
from PySide6.QtWebEngineWidgets import QWebEngineView  # Importer QWebEngineView pour afficher des pages web
from PySide6.QtGui import QFont
from functools import partial
from enregistrement import EnregistrementWindow  # Import de l'interface d'enregistrement
from liste import ListeFichiersWindow  # Import de l'interface utilisateur
from inscription import inscriptionWindow

# Classe de base pour les fenêtres des réseaux sociaux
class SocialMediaWindow(QDialog):
    def __init__(self, url):
        super().__init__()
        self.setWindowTitle("Réseau Social")
        self.setGeometry(100, 100, 800, 600)
        
        # QVBoxLayout pour gérer la disposition
        layout = QVBoxLayout(self)

        

        # QWebEngineView pour charger des pages web
        self.web_view = QWebEngineView(self)
        self.web_view.setUrl(QUrl(url))  # Charger l'URL passée
        layout.addWidget(self.web_view)

        self.setLayout(layout)

# Classes spécifiques pour chaque réseau social, passant l'URL correspondante
class GoogleWindow(SocialMediaWindow):
    def __init__(self):
        super().__init__("http://www.google.com")  # Remplacez par votre URL interne

class FacebookWindow(SocialMediaWindow):
    def __init__(self):
        super().__init__("http://www.facebook.com")  # Remplacez par votre URL interne

class InstagramWindow(SocialMediaWindow):
    def __init__(self):
        super().__init__("http://www.instagram.com")  # Remplacez par votre URL interne

class TwitterWindow(SocialMediaWindow):
    def __init__(self):
        super().__init__("http://www.twitter.com")  # Remplacez par votre URL interne

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Interface de connexion")
        self.setGeometry(100, 100, 700, 400)

        # Connexion à la base de données
        self.db_conn = self.connect_to_db()

        # SECTION GAUCHE
        self.left_frame = QFrame(self)
        self.left_frame.setGeometry(-17, 10, 300, 350)
        self.left_frame.setStyleSheet("border-radius: 30px;")

        self.image_label = QLabel(self.left_frame)
        self.image_label.setGeometry(0, 0, self.left_frame.width(), self.left_frame.height())
        self.image_label.setPixmap(QPixmap("logo-SBT.png"))
        self.image_label.setScaledContents(True)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.welcome_label = QLabel("Bonjour, bienvenue!", self.left_frame)
        self.welcome_label.setFont(QFont("Arial", 15, QFont.Bold))
        self.welcome_label.setStyleSheet("color: #ffffff;")
        self.welcome_label.setGeometry(50, 30, 200, 40)
        self.welcome_label.setAlignment(Qt.AlignCenter)

        self.description_label = QLabel(
            "Entrez vos coordonnées pour vous connecter ou vous connecter avec les applications de médias sociaux.", self.left_frame
        )
        self.description_label.setFont(QFont("Arial", 10))
        self.description_label.setStyleSheet("color: #ffffff;")
        self.description_label.setGeometry(20, 100, 260, 50)
        self.description_label.setWordWrap(True)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.sign_up_button = QPushButton("S'inscrire", self.left_frame)
        self.sign_up_button.setStyleSheet(""" 
            QPushButton {
                background-color: #ffffff;
                color: #000000;
                border-radius: 15px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #cce7e5;
            }
        """)
        self.sign_up_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.sign_up_button.setGeometry(90, 170, 120, 40)
        self.sign_up_button.clicked.connect(self.bouton_inscrire)

        # SECTION DROITE
        self.right_frame = QFrame(self)
        self.right_frame.setGeometry(320, 10, 370, 380)
        self.right_frame.setStyleSheet("background-color: #ffffff; border-radius: 20px;")

        self.username_input = QLineEdit(self.right_frame)
        self.username_input.setPlaceholderText("Nom d'utilisateur")
        self.username_input.setGeometry(50, 30, 270, 40)
        self.username_input.setStyleSheet(""" 
            QLineEdit {
                border: 2px solid #cccccc;
                border-radius: 10px;
                padding: 8px;
                background-color: #f9f9f9;
            }
        """)

        self.password_input = QLineEdit(self.right_frame)
        self.password_input.setPlaceholderText("Mot de passe")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setGeometry(50, 80, 270, 40)
        self.password_input.setStyleSheet(""" 
            QLineEdit {
                border: 2px solid #cccccc;
                border-radius: 10px;
                padding: 8px;
                background-color: #f9f9f9;
            }
        """)

        # Champ Rôle (Utilisateur ou Administrateur)
        self.role_input = QComboBox(self.right_frame)
        self.role_input.setGeometry(50, 130, 270, 40)
        self.role_input.addItems(["Utilisateur", "Administrateur"])
        self.role_input.setStyleSheet(""" 
            QComboBox {
                border: 2px solid #cccccc;
                border-radius: 10px;
                padding: 8px;
                background-color: #f9f9f9;
            }
        """)

        self.forgot_password_link = QLabel("<a href='#'>Mot de passe oublié?</a>", self.right_frame)
        self.forgot_password_link.setGeometry(210, 180, 120, 20)
        self.forgot_password_link.setStyleSheet("color: #00aaff;")
        self.forgot_password_link.setAlignment(Qt.AlignRight)
        self.forgot_password_link.mousePressEvent = self.show_forgot_password_dialog  # Connecter le clic

        self.sign_in_button = QPushButton("Se connecter", self.right_frame)
        self.sign_in_button.setGeometry(50, 200, 270, 40)
        self.sign_in_button.clicked.connect(self.bouton_seconnecter)
        self.sign_in_button.setStyleSheet(""" 
            QPushButton {
                background-color: #0d615e;
                color: #ffffff;
                border-radius: 10px;
                padding: 10px 0;
            }
            QPushButton:hover {
                background-color: #0a4f4c;
            }
        """)

        # Icônes de médias sociaux
        social_media_icons = {
            "google_icon.jpg": ("#DB4437", self.open_google_window),
            "facebook_icon.png": ("#3B5998", self.open_facebook_window),
            "instagram_icon.jpg": ("#E4405F", self.open_instagram_window),
            "twitter_icon.png": ("#1DA1F2", self.open_twitter_window)
        }

        x_offset = 70
        for icon_path, (color, action) in social_media_icons.items():
            button = QPushButton(self.right_frame)
            button.setGeometry(x_offset, 250, 40, 40)
            icon = QIcon(icon_path)
            button.setIcon(icon)
            button.setIconSize(QSize(30, 30))
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    border-radius: 5px;
                }}
                QPushButton:hover {{
                    background-color: #cccccc;
                }}
            """)
            button.clicked.connect(action)  # Connecter le bouton à l'action correspondante
            x_offset += 60

        self.remember_me_checkbox = QCheckBox("Souviens-toi de moi", self.right_frame)
        self.remember_me_checkbox.setGeometry(140, 300, 100, 20)

        self.dark_mode_label = QLabel("Mode Sombre", self)
        self.dark_mode_label.setGeometry(10, 370, 100, 20)
        self.dark_mode_toggle = QCheckBox(self)
        self.dark_mode_toggle.setGeometry(100, 370, 50, 20)
        self.dark_mode_toggle.stateChanged.connect(self.toggle_dark_mode)

    def toggle_dark_mode(self):
        # Change the style of the application based on the dark mode
        if self.dark_mode_toggle.isChecked():
            self.setStyleSheet("background-color: #1e1e1e; color: #ffffff;")
            self.left_frame.setStyleSheet("background-color: rgba(46, 46, 46, 0); border-radius: 30px;")  # Make left frame transparent
            self.right_frame.setStyleSheet("background-color: #3e3e3e; border-radius: 20px;")
            
            self.image_label.setStyleSheet("color: #ffffff;")
            self.welcome_label.setStyleSheet("color: #ffffff;")
            self.description_label.setStyleSheet("color: #ffffff;")
            
            self.sign_up_button.setStyleSheet("""
                QPushButton {
                    background-color: #444444;
                    color: #ffffff;
                    border-radius: 15px;
                    padding: 10px 20px;
                }
                QPushButton:hover {
                    background-color: #555555;
                }
            """)

            # Update the styles for other widgets accordingly
            self.username_input.setStyleSheet("""
                QLineEdit {
                    border: 2px solid #888888;
                    border-radius: 10px;
                    padding: 8px;
                    background-color: #444444;
                    color: #ffffff;
                }
            """)
            self.password_input.setStyleSheet("""
                QLineEdit {
                    border: 2px solid #888888;
                    border-radius: 10px;
                    padding: 8px;
                    background-color: #444444;
                    color: #ffffff;
                }
            """)
            self.role_input.setStyleSheet("""
                QComboBox {
                    border: 2px solid #888888;
                    border-radius: 10px;
                    padding: 8px;
                    background-color: #444444;
                    color: #ffffff;
                }
            """)
            self.sign_in_button.setStyleSheet("""
                QPushButton {
                    background-color: #007ACC;
                    color: #ffffff;
                    border-radius: 10px;
                    padding: 10px 0;
                }
                QPushButton:hover {
                    background-color: #005F9C;
                }
            """)
            self.forgot_password_link.setStyleSheet("color: #007ACC;")
        else:
            self.setStyleSheet("background-color: #ffffff; color: #000000;")
            self.right_frame.setStyleSheet("background-color: #ffffff; border-radius: 20px;")
            
            self.image_label.setStyleSheet("color: #ffffff;")
            self.welcome_label.setStyleSheet("color: #ffffff;")
            self.description_label.setStyleSheet("color: #ffffff;")
            
            self.sign_up_button.setStyleSheet("""
                QPushButton {
                    background-color: #ffffff;
                    color: #000000;
                    border-radius: 15px;
                    padding: 10px 20px;
                }
                QPushButton:hover {
                    background-color: #cce7e5;
                }
            """)

            # Update the styles for other widgets accordingly
            self.username_input.setStyleSheet("""
                QLineEdit {
                    border: 2px solid #cccccc;
                    border-radius: 10px;
                    padding: 8px;
                    background-color: #f9f9f9;
                }
            """)
            self.password_input.setStyleSheet("""
                QLineEdit {
                    border: 2px solid #cccccc;
                    border-radius: 10px;
                    padding: 8px;
                    background-color: #f9f9f9;
                }
            """)
            self.role_input.setStyleSheet("""
                QComboBox {
                    border: 2px solid #cccccc;
                    border-radius: 10px;
                    padding: 8px;
                    background-color: #f9f9f9;
                }
            """)
            self.sign_in_button.setStyleSheet("""
                QPushButton {
                    background-color: #0d615e;
                    color: #ffffff;
                    border-radius: 10px;
                    padding: 10px 0;
                }
                QPushButton:hover {
                    background-color: #0a4f4c;
                }
            """)
            self.forgot_password_link.setStyleSheet("color: #00aaff;")


    def connect_to_db(self):
        """Méthode pour connecter à la base de données MySQL"""
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="sbt_base"
            )
            return connection
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la connexion à la base de données: {err}")
            return None

    def bouton_inscrire(self):
        self.inscription_window = inscriptionWindow()  # Interface d'enregistrement pour les admins
        self.inscription_window.show()
        self.hide()

    def bouton_seconnecter(self):
        """Vérification des informations d'identification et redirection"""
        username = self.username_input.text()
        password = self.password_input.text()
        role = self.role_input.currentText()

        if not username or not password:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer votre nom d'utilisateur et votre mot de passe.")
            return

        try:
            cursor = self.db_conn.cursor()
            query = "SELECT Role FROM Personne WHERE NomPersonne = %s AND MotDePasse = %s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()

            if result:
                db_role = result[0]
                if db_role == "Administrateur" and role == "Administrateur":
                    self.open_enregistrement_window()
                elif db_role == "Utilisateur" and role == "Utilisateur":
                    self.open_liste_fichiers_window()
                else:
                    QMessageBox.warning(self, "Erreur", "Le rôle sélectionné ne correspond pas à celui enregistré.")
            else:
                QMessageBox.warning(self, "Erreur", "Nom d'utilisateur ou mot de passe incorrect.")
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la vérification des informations d'identification: {err}")
        finally:
            cursor.close()

    def open_enregistrement_window(self):
        """Ouvrir la fenêtre Enregistrement pour les administrateurs"""
        self.enregistrement_window = EnregistrementWindow()  # Interface d'enregistrement pour les admins
        self.enregistrement_window.show()
        self.hide()

    def open_liste_fichiers_window(self):
        """Ouvrir la fenêtre ListeFichier pour les utilisateurs"""
        self.liste_fichiers_window = ListeFichiersWindow()  # Interface liste des fichiers pour les utilisateurs
        self.liste_fichiers_window.show()
        self.hide()


    def center(self):
        frame = self.frameGeometry()
        screen_center = QApplication.primaryScreen().availableGeometry().center()
        frame.moveCenter(screen_center)
        self.move(frame.topLeft())

    def show_forgot_password_dialog(self, event):
        """Afficher une boîte de dialogue pour récupérer le mot de passe"""
        username, ok = QInputDialog.getText(self, "Mot de passe oublié", "Entrez votre nom d'utilisateur:")
        if ok and username:
            self.retrieve_password(username)

    def retrieve_password(self, username):
        """Vérifier si le nom d'utilisateur existe et récupérer le mot de passe"""
        try:
            cursor = self.db_conn.cursor()
            query = "SELECT MotDePasse FROM Personne WHERE NomPersonne = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()

            if result:
                password = result[0]
                QMessageBox.information(self, "Mot de passe récupéré", f"Votre mot de passe est: {password}")
            else:
                QMessageBox.warning(self, "Erreur", "Nom d'utilisateur non trouvé.")
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la récupération du mot de passe: {err}")
        finally:
            cursor.close()


    def open_google_window(self):
        self.google_window = GoogleWindow()
        self.google_window.exec()

    def open_facebook_window(self):
        self.facebook_window = FacebookWindow()
        self.facebook_window.exec()

    def open_instagram_window(self):
        self.instagram_window = InstagramWindow()
        self.instagram_window.exec()

    def open_twitter_window(self):
        self.twitter_window = TwitterWindow()
        self.twitter_window.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())

