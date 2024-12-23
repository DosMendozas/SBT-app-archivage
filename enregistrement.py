from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QFrame, QComboBox, QDateEdit,
    QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem, QVBoxLayout, QScrollArea
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont
import sys
import mysql.connector
import os  # Importer le module os pour extraire le nom de fichier

class EnregistrementWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Interface d'enregistrement de fichier")
        self.setGeometry(100, 100, 900, 500)
        self.setStyleSheet("background-color: lightblue;")

        # Connexion à la base de données
        self.db_conn = self.connect_to_db()
        self.ensure_categories_exist()

        # SECTION GAUCHE (left_frame)
        self.left_frame = QFrame(self)
        self.left_frame.setGeometry(10, 10, 380, 480)
        self.left_frame.setStyleSheet("background-color: #ffffff; border-radius: 20px;")

        self.scroll_area = QScrollArea(self.left_frame)
        self.scroll_area.setGeometry(10, 10, 280, 460)
        self.scroll_area.setWidgetResizable(True)

        self.table = QTableWidget()
        self.table.setColumnCount(5)  # On ajoute une colonne pour le titre
        self.table.setHorizontalHeaderLabels(["ID", "Nom", "Date", "Titre", "Catégorie"])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        self.table.itemSelectionChanged.connect(self.load_selected_file)
        self.scroll_area.setWidget(self.table)

        # SECTION DROITE (right_frame)
        self.right_frame = QFrame(self)
        self.right_frame.setGeometry(410, 10, 480, 480)
        self.right_frame.setStyleSheet("background-color: #ffffff; border-radius: 20px;")

        # ID du fichier
        self.file_id_label = QLabel("ID du Fichier", self.right_frame)
        self.file_id_label.setFont(QFont("Arial", 12))
        self.file_id_label.setGeometry(30, 20, 120, 30)

        self.file_id_input = QLineEdit(self.right_frame)
        self.file_id_input.setGeometry(160, 20, 180, 30)
        self.file_id_input.setStyleSheet("border: 1px solid #000000; background-color: #f0f0f0; padding: 5px;")

        # Nom du fichier
        self.file_name_label = QLabel("Nom du fichier", self.right_frame)
        self.file_name_label.setFont(QFont("Arial", 12))
        self.file_name_label.setGeometry(30, 70, 120, 30)

        self.file_name_input = QLineEdit(self.right_frame)
        self.file_name_input.setGeometry(160, 70, 180, 30)
        self.file_name_input.setStyleSheet("border: 1px solid #000000; background-color: #f0f0f0; padding: 5px;")
        
        # Importer un fichier
        self.import_button = QPushButton("Importer un Fichier", self.right_frame)
        self.import_button.setGeometry(160, 120, 180, 30)
        self.import_button.clicked.connect(self.import_file)
        
        # Titre
        self.titre_label = QLabel("Titre", self.right_frame)
        self.titre_label.setFont(QFont("Arial", 12))
        self.titre_label.setGeometry(30, 170, 120, 30)

        self.titre_input = QLineEdit(self.right_frame)
        self.titre_input.setGeometry(160, 170, 180, 30)
        self.titre_input.setStyleSheet("border: 1px solid #000000; background-color: #f0f0f0; padding: 5px;")

        # Date
        self.date_label = QLabel("Date", self.right_frame)
        self.date_label.setFont(QFont("Arial", 12))
        self.date_label.setGeometry(30, 220, 120, 30)

        self.date_input = QDateEdit(self.right_frame)
        self.date_input.setGeometry(160, 220, 180, 30)
        self.date_input.setStyleSheet("border: 1px solid #000000; background-color: #f0f0f0; padding: 5px;")
        self.date_input.setCalendarPopup(True)

        # Sélectionner la catégorie
        self.category_combo = QComboBox(self.right_frame)
        self.category_combo.setGeometry(160, 270, 180, 30)
        self.category_combo.addItem("Sélectionner la catégorie")

        predefined_categories = ["Sport", "Musique", "Informations"]
        self.category_combo.addItems(predefined_categories)
        self.category_combo.setStyleSheet("border: 1px solid #000000; background-color: #f0f0f0; padding: 5px;")

        # Bouton Modifier
        self.cancel_button = QPushButton("Modifier", self.right_frame)
        self.cancel_button.setGeometry(50, 320, 120, 40)
        self.cancel_button.setStyleSheet("background-color: #FF0000; color: #FFFFFF;")
        self.cancel_button.clicked.connect(self.update_file)

        # Bouton Enregistrer
        self.save_button = QPushButton("Enregistrer", self.right_frame)
        self.save_button.setGeometry(200, 320, 120, 40)
        self.save_button.setStyleSheet("background-color: #333333; color: #FFFFFF;")
        self.save_button.clicked.connect(self.save_to_db)

        # Boutons de gestion de la table
        self.update_button = QPushButton("Réinitialiser", self.right_frame)
        self.update_button.setGeometry(350, 320, 120, 40)
        self.update_button.setStyleSheet("background-color: #008CBA; color: #FFFFFF;")
        self.update_button.clicked.connect(self.clear_inputs)

        self.delete_button = QPushButton("Supprimer", self.right_frame)
        self.delete_button.setGeometry(50, 380, 120, 40)
        self.delete_button.setStyleSheet("background-color: #0000FF; color: #FFFFFF;")
        self.delete_button.clicked.connect(self.delete_file)

        # Bouton Sortir
        self.exit_button = QPushButton("Sortir", self.right_frame)
        self.exit_button.setGeometry(350, 380, 120, 40)
        self.exit_button.setStyleSheet("background-color: #FF5733; color: #FFFFFF;")
        self.exit_button.clicked.connect(self.aller_connexion)
        
        # Bouton Lister
        self.lister_button = QPushButton("Voir Liste", self.right_frame)
        self.lister_button.setGeometry(200, 380, 120, 40)
        self.lister_button.setStyleSheet("background-color: #FF5733; color: #FFFFFF;")
        self.lister_button.clicked.connect(self.Lister)

        self.load_files()

        self.center()

    def center(self):
        frame = self.frameGeometry()
        screen_center = QApplication.primaryScreen().availableGeometry().center()
        frame.moveCenter(screen_center)
        self.move(frame.topLeft())

    def import_file(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "Sélectionner un fichier", "", "Tous les fichiers (*)")
        if file_path:
            # Ne conserver que le nom du fichier sans le chemin
            file_name = os.path.basename(file_path)
            self.file_name_input.setText(file_name)

    def connect_to_db(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="sbt_base"
            )
            return connection
        except mysql.connector.Error as err:
            print(f"Erreur: {err}")
            return None

    def ensure_categories_exist(self):
        predefined_categories = ["Sport", "Musique", "Informations"]
        cursor = self.db_conn.cursor()

        for category in predefined_categories:
            cursor.execute("SELECT COUNT(*) FROM Categorie WHERE NomCategorie = %s", (category,))
            count = cursor.fetchone()[0]
            if count == 0:
                cursor.execute("SELECT MAX(IdCategorie) FROM Categorie")
                max_id = cursor.fetchone()[0]
                new_id = (max_id + 1) if max_id is not None else 1
                cursor.execute("INSERT INTO Categorie (IdCategorie, NomCategorie) VALUES (%s, %s)", (new_id, category))

        self.db_conn.commit()
        cursor.close()

    def save_to_db(self):
        file_id = self.file_id_input.text()
        file_name = self.file_name_input.text()
        titre = self.titre_input.text()  # Titre ajouté
        date = self.date_input.date().toString("yyyy-MM-dd")
        category = self.category_combo.currentText()

        if not (file_id and file_name and titre and category != "Sélectionner la catégorie"):
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs correctement.")
            return

        try:
            cursor = self.db_conn.cursor()
            cursor.execute(
                "INSERT INTO Fichier (IdFichier, NomFichier, Titre, Date, IdCategorie) VALUES (%s, %s, %s, %s, "
                "(SELECT IdCategorie FROM Categorie WHERE NomCategorie = %s))",
                (file_id, file_name, titre, date, category)
            )
            self.db_conn.commit()
            QMessageBox.information(self, "Succès", "Le fichier a été enregistré avec succès.")
            self.load_files()
            self.clear_inputs()
        except mysql.connector.Error as err:
            QMessageBox.warning(self, "Erreur", f"Erreur lors de l'enregistrement : {err}")

    def load_files(self):
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT IdFichier, NomFichier, Date, Titre, Categorie.NomCategorie FROM Fichier "
                       "JOIN Categorie ON Fichier.IdCategorie = Categorie.IdCategorie")
        rows = cursor.fetchall()
        self.table.setRowCount(0)
        for row in rows:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            for column, item in enumerate(row):
                self.table.setItem(row_position, column, QTableWidgetItem(str(item)))
        cursor.close()

    def load_selected_file(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            file_id = self.table.item(selected_row, 0).text()
            file_name = self.table.item(selected_row, 1).text()
            titre = self.table.item(selected_row, 3).text()
            date = self.table.item(selected_row, 2).text()
            category = self.table.item(selected_row, 4).text()

            self.file_id_input.setText(file_id)
            self.file_name_input.setText(file_name)
            self.titre_input.setText(titre)
            self.date_input.setDate(QDate.fromString(date, "yyyy-MM-dd"))
            self.category_combo.setCurrentText(category)

    def update_file(self):
        file_id = self.file_id_input.text()
        file_name = self.file_name_input.text()
        titre = self.titre_input.text()
        date = self.date_input.date().toString("yyyy-MM-dd")
        category = self.category_combo.currentText()

        if not (file_id and file_name and titre and category != "Sélectionner la catégorie"):
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs correctement.")
            return

        try:
            cursor = self.db_conn.cursor()
            cursor.execute(
                "UPDATE Fichier SET NomFichier = %s, Titre = %s, Date = %s, IdCategorie = "
                "(SELECT IdCategorie FROM Categorie WHERE NomCategorie = %s) WHERE IdFichier = %s",
                (file_name, titre, date, category, file_id)
            )
            self.db_conn.commit()
            QMessageBox.information(self, "Succès", "Le fichier a été modifié avec succès.")
            self.load_files()
            self.clear_inputs()
        except mysql.connector.Error as err:
            QMessageBox.warning(self, "Erreur", f"Erreur lors de la mise à jour : {err}")

    def delete_file(self):
        file_id = self.file_id_input.text()
        if not file_id:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un fichier à supprimer.")
            return

        reply = QMessageBox.question(self, "Confirmer la suppression", "Êtes-vous sûr de vouloir supprimer ce fichier ?",
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                cursor = self.db_conn.cursor()
                cursor.execute("DELETE FROM Fichier WHERE IdFichier = %s", (file_id,))
                self.db_conn.commit()
                QMessageBox.information(self, "Succès", "Le fichier a été supprimé avec succès.")
                self.load_files()
                self.clear_inputs()
            except mysql.connector.Error as err:
                QMessageBox.warning(self, "Erreur", f"Erreur lors de la suppression : {err}")

    def clear_inputs(self):
        self.file_id_input.clear()
        self.file_name_input.clear()
        self.titre_input.clear()
        self.date_input.clear()
        self.category_combo.setCurrentIndex(0)

    def aller_connexion(self):
        from connexion import LoginWindow  # Importer la classe LoginWindow depuis connexion.py
        self.login_window = LoginWindow() 
        self.login_window.show()            
        self.hide()  

    def Lister(self):
        from liste import ListeFichiersWindow  # Importer la classe LoginWindow depuis connexion.py
        self.liste_window = ListeFichiersWindow() 
        self.liste_window.show()            
        self.hide() 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EnregistrementWindow()
    window.show()
    sys.exit(app.exec())

