# import sys
# import mysql.connector  # Importation pour la base de données MySQL
# from PySide6.QtGui import QIcon, QPixmap, QFont, QDesktopServices
# from PySide6.QtCore import QSize, QUrl, Qt
# from functools import partial
# from PySide6.QtWidgets import (
#     QApplication, QWidget, QLabel, QLineEdit, QPushButton, QCheckBox,
#     QFrame, QMessageBox, QComboBox  # Ajout de QComboBox pour la liste déroulante
# )






# class inscriptionWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Interface d'inscription")
#         self.setGeometry(100, 100, 700, 400)

#         # Mode sombre activé ou désactivé
#         self.dark_mode_enabled = False

#         # ------------------ SECTION droite ------------------ #
#         self.right_frame = QFrame(self)
#         self.right_frame.setGeometry(377, 10, 320, 350)
#         self.right_frame.setStyleSheet("border-radius: 30px;")

#         # Ajout d'une image dans la section right_frame
#         self.image_label = QLabel(self.right_frame)
#         self.image_label.setGeometry(0, 0, self.right_frame.width(), self.right_frame.height())
#         self.image_label.setPixmap(QPixmap("logo-SBT.png"))
#         self.image_label.setScaledContents(True)
#         self.image_label.setAlignment(Qt.AlignCenter)

#         # Label de bienvenue
#         self.welcome_label = QLabel("Bonjour, bienvenue!", self.right_frame)
#         self.welcome_label.setFont(QFont("Arial", 15, QFont.Bold))
#         self.welcome_label.setStyleSheet("color: #ffffff;")
#         self.welcome_label.setGeometry(50, 30, 200, 40)
#         self.welcome_label.setAlignment(Qt.AlignCenter)

#         # Description sous le titre
#         self.description_label = QLabel(
#             "Entrez vos coordonnées pour vous inscrire.", self.right_frame
#         )
#         self.description_label.setFont(QFont("Arial", 10))
#         self.description_label.setStyleSheet("color: #ffffff;")
#         self.description_label.setGeometry(20, 100, 260, 50)
#         self.description_label.setWordWrap(True)
#         self.description_label.setAlignment(Qt.AlignCenter)

#         # Bouton Sign Up
#         self.sign_up_button = QPushButton("Se Connecter", self.right_frame)
#         self.sign_up_button.setStyleSheet(""" 
#             QPushButton {
#                 background-color: #ffffff;
#                 color: #000000;
#                 border-radius: 15px;
#                 padding: 5px 8px;
#             }
#             QPushButton:hover {
#                 background-color: #cce7e5;
#             }
#         """)
#         self.sign_up_button.setFont(QFont("Arial", 12, QFont.Bold))
#         self.sign_up_button.setGeometry(90, 170, 120, 40)
#         self.sign_up_button.clicked.connect(self.bouton_seconnecter)

#         # ------------------ SECTION Gauche ------------------ #
#         self.left_frame = QFrame(self)
#         self.left_frame.setGeometry(-17, 10, 350, 380)
#         self.left_frame.setStyleSheet("background-color: #ffffff; border-radius: 20px;")

#         # Champ NomPersonne
#         self.NomPersonne_input = QLineEdit(self.left_frame)
#         self.NomPersonne_input.setPlaceholderText("Nom d'utilisateur")
#         self.NomPersonne_input.setGeometry(50, 30, 270, 40)
#         self.NomPersonne_input.setStyleSheet(""" 
#             QLineEdit {
#                 border: 2px solid #cccccc;
#                 border-radius: 10px;
#                 padding: 8px;
#                 background-color: #f9f9f9;
#             }
#         """)

#         # Champ MotDePasse
#         self.MotDePasse_input = QLineEdit(self.left_frame)
#         self.MotDePasse_input.setPlaceholderText("Mot de passe")
#         self.MotDePasse_input.setEchoMode(QLineEdit.Password)
#         self.MotDePasse_input.setGeometry(50, 80, 270, 40)
#         self.MotDePasse_input.setStyleSheet(""" 
#             QLineEdit {
#                 border: 2px solid #cccccc;
#                 border-radius: 10px;
#                 padding: 8px;
#                 background-color: #f9f9f9;
#             }
#         """)

#         # Champ Rôle (Utilisateur ou Administrateur)
#         self.role_input = QComboBox(self.left_frame)
#         self.role_input.setGeometry(50, 130, 270, 40)
#         self.role_input.addItems(["Utilisateur", "Administrateur"])
#         self.role_input.setStyleSheet(""" 
#             QComboBox {
#                 border: 2px solid #cccccc;
#                 border-radius: 10px;
#                 padding: 8px;
#                 background-color: #f9f9f9;
#             }
#         """)

#         # Bouton Sign In
#         self.sign_in_button = QPushButton("S'inscrire", self.left_frame)
#         self.sign_in_button.setGeometry(50, 200, 270, 40)
#         self.sign_in_button.clicked.connect(self.bouton_inscrire)
#         self.sign_in_button.setStyleSheet(""" 
#             QPushButton {
#                 background-color: #0d615e;
#                 color: #ffffff;
#                 border-radius: 10px;
#                 padding: 10px 0;
#             }
#             QPushButton:hover {
#                 background-color: #0a4f4c;
#             }
#         """)

#         # Ajouter les boutons de réseaux sociaux avec des images
#         social_media_icons = {
#             "google_icon.jpg": ("#DB4437", "https://plus.google.com"),
#             "facebook_icon.png": ("#3B5998", "https://www.facebook.com"),
#             "instagram_icon.jpg": ("#E4405F", "https://www.instagram.com"),
#             "twitter_icon.png": ("#1DA1F2", "https://www.twitter.com")
#         }

#         x_offset = 70
#         for icon_path, (color, url) in social_media_icons.items():
#             button = QPushButton(self.left_frame)
#             button.setGeometry(x_offset, 250, 40, 40)
#             icon = QIcon(icon_path)
#             button.setIcon(icon)
#             button.setIconSize(QSize(30, 30))
#             button.setStyleSheet(f"""
#                 QPushButton {{
#                     background-color: {color};
#                     border-radius: 5px;
#                 }}
#                 QPushButton:hover {{
#                     background-color: #cccccc;
#                 }}
#             """)
#             button.clicked.connect(partial(QDesktopServices.openUrl, QUrl(url)))
#             x_offset += 60

#         # Case à cocher Remember me
#         self.remember_me_checkbox = QCheckBox("Souviens-toi de moi", self.left_frame)
#         self.remember_me_checkbox.setGeometry(140, 300, 100, 20)

#         # Commutateur pour le mode sombre en dehors de la section gauche
#         self.dark_mode_label = QLabel("Mode Sombre", self)
#         self.dark_mode_label.setGeometry(600, 370, 100, 20)
#         self.dark_mode_toggle = QCheckBox(self)
#         self.dark_mode_toggle.setGeometry(580, 370, 50, 20)
#         self.dark_mode_toggle.stateChanged.connect(self.toggle_dark_mode)

#         # Centrer la fenêtre
#         self.center()

#     def center(self):
#         """Centre la fenêtre sur l'écran."""
#         frame = self.frameGeometry()
#         screen_center = QApplication.primaryScreen().availableGeometry().center()
#         frame.moveCenter(screen_center)
#         self.move(frame.topLeft())

#     def bouton_seconnecter(self):
#         from connexion import LoginWindow
#         self.connexion_window = LoginWindow()
#         self.connexion_window.show()
#         self.hide()

#     def bouton_inscrire(self):
#         from enregistrement import EnregistrementWindow
        
        
        
#         NomPersonne = self.NomPersonne_input.text()
#         MotDePasse = self.MotDePasse_input.text()
#         Role = self.role_input.currentText()  # Récupérer le rôle sélectionné

#         if not NomPersonne or not MotDePasse:
#             QMessageBox.warning(self, "Erreur", "Veuillez entrer un nom d'utilisateur et un mot de passe.")
#             return

#         conn = None  # Définir conn à None pour l'utiliser dans le bloc finally
#         try:
#             # Connexion à la base de données MySQL
#             conn = mysql.connector.connect(
#                 host="localhost",
#                 user="root",           # Remplacez par votre nom d'utilisateur MySQL
#                 password="",           # Remplacez par votre mot de passe MySQL
#                 database="sbt_base"    # Remplacez par le nom de votre base de données
#             )
#             cursor = conn.cursor()

#             # Créer la table si elle n'existe pas déjà
#             cursor.execute(""" 
#                 CREATE TABLE IF NOT EXISTS Personne (
#                     IdPersonne INT AUTO_INCREMENT PRIMARY KEY,
#                     NomPersonne VARCHAR(50) NOT NULL UNIQUE,
#                     MotDePasse VARCHAR(50) NOT NULL,
#                     Role ENUM('Utilisateur', 'Administrateur') NOT NULL
#                 )
#             """)

#             # Insérer dans la table Personne
#             cursor.execute("INSERT INTO Personne (NomPersonne, MotDePasse, Role) VALUES (%s, %s, %s)", 
#                            (NomPersonne, MotDePasse, Role))

#             conn.commit()
#             QMessageBox.information(self, "Succès", f"Inscription réussie en tant que {Role}!")

#             # Rediriger vers la fenêtre appropriée
#             if Role == "Administrateur":
#                 # from enregistrement import EnregistrementWindow
#                 self.enregistrement_window = EnregistrementWindow()
#                 self.enregistrement_window.show()
#                 self.hide()
#             else:
#                 from liste import ListeFichiersWindow
#                 self.liste_fichiers_window = ListeFichiersWindow()
#                 self.liste_fichiers_window.show()

#                 self.hide()  # Cacher la fenêtre d'inscription

#         except mysql.connector.IntegrityError:
#             QMessageBox.warning(self, "Erreur", "Le nom d'utilisateur existe déjà.")
#         except Exception as e:
#             QMessageBox.critical(self, "Erreur", f"Une erreur s'est produite : {str(e)}")
#         finally:
#             if conn is not None and conn.is_connected():
#                 cursor.close()
#                 conn.close()

#     def toggle_dark_mode(self):
#         """Basculer entre le mode sombre et le mode clair."""
#         if self.dark_mode_toggle.isChecked():
#             self.left_frame.setStyleSheet("background-color: #333333; border-radius: 20px;")
#             self.right_frame.setStyleSheet("background-color: #222222; border-radius: 20px;")
#             self.welcome_label.setStyleSheet("color: #ffffff;")
#             self.description_label.setStyleSheet("color: #cccccc;")
#             self.NomPersonne_input.setStyleSheet(""" 
#                 QLineEdit {
#                     border: 2px solid #555555;
#                     border-radius: 10px;
#                     padding: 8px;
#                     background-color: #444444;
#                     color: #ffffff;
#                 }
#             """)
#             self.MotDePasse_input.setStyleSheet(""" 
#                 QLineEdit {
#                     border: 2px solid #555555;
#                     border-radius: 10px;
#                     padding: 8px;
#                     background-color: #444444;
#                     color: #ffffff;
#                 }
#             """)

#             self.sign_in_button.setStyleSheet(""" 
#                 QPushButton {
#                     background-color: #444444;
#                     color: #ffffff;
#                     border-radius: 10px;
#                     padding: 10px 0;
#                 }
#                 QPushButton:hover {
#                     background-color: #666666;
#                 }
#             """)
#         else:
#             self.left_frame.setStyleSheet("border-radius: 20px;")
#             self.right_frame.setStyleSheet("background-color: #ffffff; border-radius: 20px;")
#             self.welcome_label.setStyleSheet("color: #ffffff;")
#             self.description_label.setStyleSheet("color: #ffffff;")
#             self.NomPersonne_input.setStyleSheet(""" 
#                 QLineEdit {
#                     border: 2px solid #cccccc;
#                     border-radius: 10px;
#                     padding: 8px;
#                     background-color: #f9f9f9;
#                 }
#             """)
#             self.MotDePasse_input.setStyleSheet(""" 
#                 QLineEdit {
#                     border: 2px solid #cccccc;
#                     border-radius: 10px;
#                     padding: 8px;
#                     background-color: #f9f9f9;
#                 }
#             """)

#             self.sign_in_button.setStyleSheet(""" 
#                 QPushButton {
#                     background-color: #0d615e;
#                     color: #ffffff;
#                     border-radius: 10px;
#                     padding: 10px 0;
#                 }
#                 QPushButton:hover {
#                     background-color: #0a4f4c;
#                 }
#             """)

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = inscriptionWindow()
#     window.show()
#     sys.exit(app.exec())





import sys
import mysql.connector  # Importation pour la base de données MySQL
from PySide6.QtGui import QIcon, QPixmap, QFont, QDesktopServices
from PySide6.QtCore import QSize, QUrl, Qt
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QCheckBox,
    QFrame, QMessageBox, QComboBox, QVBoxLayout, QDialog  # Assurez-vous que QDialog est ici
)

from PySide6.QtWebEngineWidgets import QWebEngineView  # Ajout de QWebEngineView
from functools import partial

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

class inscriptionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interface d'inscription")
        self.setGeometry(100, 100, 700, 400)

        # Mode sombre activé ou désactivé
        self.dark_mode_enabled = False

        # ------------------ SECTION droite ------------------ #
        self.right_frame = QFrame(self)
        self.right_frame.setGeometry(377, 10, 320, 350)
        self.right_frame.setStyleSheet("border-radius: 30px;")

        # Ajout d'une image dans la section right_frame
        self.image_label = QLabel(self.right_frame)
        self.image_label.setGeometry(0, 0, self.right_frame.width(), self.right_frame.height())
        self.image_label.setPixmap(QPixmap("logo-SBT.png"))
        self.image_label.setScaledContents(True)
        self.image_label.setAlignment(Qt.AlignCenter)

        # Label de bienvenue
        self.welcome_label = QLabel("Bonjour, bienvenue!", self.right_frame)
        self.welcome_label.setFont(QFont("Arial", 15, QFont.Bold))
        self.welcome_label.setStyleSheet("color: #ffffff;")
        self.welcome_label.setGeometry(50, 30, 200, 40)
        self.welcome_label.setAlignment(Qt.AlignCenter)

        # Description sous le titre
        self.description_label = QLabel(
            "Entrez vos coordonnées pour vous inscrire.", self.right_frame
        )
        self.description_label.setFont(QFont("Arial", 10))
        self.description_label.setStyleSheet("color: #ffffff;")
        self.description_label.setGeometry(20, 100, 260, 50)
        self.description_label.setWordWrap(True)
        self.description_label.setAlignment(Qt.AlignCenter)

        # Bouton Sign Up
        self.sign_up_button = QPushButton("Se Connecter", self.right_frame)
        self.sign_up_button.setStyleSheet(""" 
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
        self.sign_up_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.sign_up_button.setGeometry(90, 170, 120, 40)
        self.sign_up_button.clicked.connect(self.bouton_seconnecter)

        # ------------------ SECTION Gauche ------------------ #
        self.left_frame = QFrame(self)
        self.left_frame.setGeometry(-17, 10, 350, 380)
        self.left_frame.setStyleSheet("background-color: #ffffff; border-radius: 20px;")

        # Champ NomPersonne
        self.NomPersonne_input = QLineEdit(self.left_frame)
        self.NomPersonne_input.setPlaceholderText("Nom d'utilisateur")
        self.NomPersonne_input.setGeometry(50, 30, 270, 40)
        self.NomPersonne_input.setStyleSheet(""" 
            QLineEdit {
                border: 2px solid #cccccc;
                border-radius: 10px;
                padding: 8px;
                background-color: #f9f9f9;
            }
        """)

        # Champ MotDePasse
        self.MotDePasse_input = QLineEdit(self.left_frame)
        self.MotDePasse_input.setPlaceholderText("Mot de passe")
        self.MotDePasse_input.setEchoMode(QLineEdit.Password)
        self.MotDePasse_input.setGeometry(50, 80, 270, 40)
        self.MotDePasse_input.setStyleSheet(""" 
            QLineEdit {
                border: 2px solid #cccccc;
                border-radius: 10px;
                padding: 8px;
                background-color: #f9f9f9;
            }
        """)

        # Champ Rôle (Utilisateur ou Administrateur)
        self.role_input = QComboBox(self.left_frame)
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

        # Bouton Sign In
        self.sign_in_button = QPushButton("S'inscrire", self.left_frame)
        self.sign_in_button.setGeometry(50, 200, 270, 40)
        self.sign_in_button.clicked.connect(self.bouton_inscrire)
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
            button = QPushButton(self.left_frame)
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

        # Case à cocher Remember me
        self.remember_me_checkbox = QCheckBox("Souviens-toi de moi", self.left_frame)
        self.remember_me_checkbox.setGeometry(140, 300, 100, 20)

        # Commutateur pour le mode sombre
        self.dark_mode_label = QLabel("Mode Sombre", self)
        self.dark_mode_label.setGeometry(600, 370, 100, 20)
        self.dark_mode_toggle = QCheckBox(self)
        self.dark_mode_toggle.setGeometry(580, 370, 50, 20)
        self.dark_mode_toggle.stateChanged.connect(self.toggle_dark_mode)


    def center(self):
        """Centre la fenêtre sur l'écran."""
        frame = self.frameGeometry()
        screen_center = QApplication.primaryScreen().availableGeometry().center()
        frame.moveCenter(screen_center)
        self.move(frame.topLeft())

    def bouton_seconnecter(self):
        from connexion import LoginWindow
        self.connexion_window = LoginWindow()
        self.connexion_window.show()
        self.hide()

    def bouton_inscrire(self):
        from enregistrement import EnregistrementWindow
        
    
        
        NomPersonne = self.NomPersonne_input.text()
        MotDePasse = self.MotDePasse_input.text()
        Role = self.role_input.currentText()  # Récupérer le rôle sélectionné

        if not NomPersonne or not MotDePasse:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer un nom d'utilisateur et un mot de passe.")
            return

        conn = None  # Définir conn à None pour l'utiliser dans le bloc finally
        try:
            # Connexion à la base de données MySQL
            conn = mysql.connector.connect(
                host="localhost",
                user="root",           # Remplacez par votre nom d'utilisateur MySQL
                password="",           # Remplacez par votre mot de passe MySQL
                database="sbt_base"    # Remplacez par le nom de votre base de données
            )
            cursor = conn.cursor()

            # Créer la table si elle n'existe pas déjà
            cursor.execute(""" 
                CREATE TABLE IF NOT EXISTS Personne (
                    IdPersonne INT AUTO_INCREMENT PRIMARY KEY,
                    NomPersonne VARCHAR(50) NOT NULL UNIQUE,
                    MotDePasse VARCHAR(50) NOT NULL,
                    Role ENUM('Utilisateur', 'Administrateur') NOT NULL
                )
            """)

            # Insérer dans la table Personne
            cursor.execute("INSERT INTO Personne (NomPersonne, MotDePasse, Role) VALUES (%s, %s, %s)", 
                           (NomPersonne, MotDePasse, Role))

            conn.commit()
            QMessageBox.information(self, "Succès", f"Inscription réussie en tant que {Role}!")

            # Rediriger vers la fenêtre appropriée
            if Role == "Administrateur":
                # from enregistrement import EnregistrementWindow
                self.enregistrement_window = EnregistrementWindow()
                self.enregistrement_window.show()
                self.hide()
            else:
                from liste import ListeFichiersWindow
                self.liste_fichiers_window = ListeFichiersWindow()
                self.liste_fichiers_window.show()

                self.hide()  # Cacher la fenêtre d'inscription

        except mysql.connector.IntegrityError:
            QMessageBox.warning(self, "Erreur", "Le nom d'utilisateur existe déjà.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur s'est produite : {str(e)}")
        finally:
            if conn is not None and conn.is_connected():
                cursor.close()
                conn.close()    

    def toggle_dark_mode(self):
        # Change the style of the application based on the dark mode
        if self.dark_mode_toggle.isChecked():
            self.setStyleSheet("background-color: #1e1e1e; color: #000000;")
            self.right_frame.setStyleSheet("background-color: rgba(46, 46, 46, 0); border-radius: 30px;")  # Make left frame transparent
            self.left_frame.setStyleSheet("background-color: #3e3e3e; border-radius: 20px;")
            
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
            self.left_frame.setStyleSheet("background-color: #ffffff; border-radius: 20px;")
            
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

    
    # Méthodes pour ouvrir les fenêtres des réseaux sociaux
    def open_google_window(self):
        self.google_window = GoogleWindow()
        self.google_window.show()

    def open_facebook_window(self):
        self.facebook_window = FacebookWindow()
        self.facebook_window.show()

    def open_instagram_window(self):
        self.instagram_window = InstagramWindow()
        self.instagram_window.show()

    def open_twitter_window(self):
        self.twitter_window = TwitterWindow()
        self.twitter_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = inscriptionWindow()
    window.show()
    sys.exit(app.exec())
