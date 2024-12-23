from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QLabel, QTableWidget, QTableWidgetItem, QWidget, 
                               QApplication, QFrame, QPushButton, 
                               QLineEdit, QMessageBox, QFileDialog, QComboBox)
import sys
import mysql.connector
import os
import shutil


class ListeFichiersWindow(QWidget): 
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tableau des fichiers")
        self.setGeometry(100, 100, 940, 500)  # Fenêtre plus grande
        self.setStyleSheet("background-color: lightblue;")

        # Connexion à la base de données
        self.db_conn = self.connect_to_db()

        # Créer une frame blanche pour contenir la table et les boutons
        self.frame = QFrame(self)
        self.frame.setStyleSheet("background-color: white; border-radius: 10px;")
        self.frame.setGeometry(50, 30, 840, 400)  # Taille et position de la frame

        # Table
        self.table = QTableWidget(self.frame)
        self.table.setColumnCount(5)  # Ajout de la colonne "Titre"
        self.table.setHorizontalHeaderLabels(["  ID   ", "   Nom   ", "   Date   ", "   Catégorie   ", "   Titre   "])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setGeometry(20, 20, 560, 200)  # Taille et position de la table

        # Label pour la catégorie
        self.label_ = QLabel(self.frame)
        self.label_.setText("Faite vos recherches Ici ")
        self.label_.setGeometry(600, 50, 220, 40)   # Taille et position du label
        self.label_.setStyleSheet(""" 
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333333;
                background-color: #f0f0f0;
                padding: 8px;
                border: 2px solid #cccccc;
                border-radius: 10px;
            }
        """)

        # Sélectionner la catégorie
        self.category_combo = QComboBox(self.frame)
        self.category_combo.setGeometry(610, 100, 190, 35)
        self.category_combo.addItem("Sélectionner la catégorie")

        predefined_categories = ["Sport", "Musique", "Informations"]
        self.category_combo.addItems(predefined_categories)
        self.category_combo.setStyleSheet("border: 1px solid #000000; background-color: #f0f0f0; padding: 5px;")

        # Champ de Titre
        self.titre = QLineEdit(self.frame)
        self.titre.setPlaceholderText("Titre du fichier")
        self.titre.setGeometry(610, 140, 190, 35)  # Taille et position du champ de Titre
        self.titre.setStyleSheet("""
            QLineEdit {
                border: 2px solid #cccccc;
                border-radius: 10px;
                padding: 8px;
                background-color: #f9f9f9;
            }
        """)

        # Bouton Rechercher
        self.search_button = QPushButton("Rechercher", self.frame)
        self.search_button.setGeometry(640, 190, 130, 35)  # Taille et position du bouton rechercher
        self.search_button.setStyleSheet("background-color: #333333; color: #FFFFFF;")
        self.search_button.clicked.connect(self.filter_files)

        # Bouton Actualiser
        self.refresh_button = QPushButton("Actualiser", self.frame)
        self.refresh_button.setGeometry(640, 240, 130, 35)  # Taille et position du bouton actualiser
        self.refresh_button.setStyleSheet("background-color: #333333; color: #FFFFFF;")
        self.refresh_button.clicked.connect(self.load_files)  # Recharger la liste complète

        # Bouton Télécharger
        self.download_button = QPushButton("Télécharger", self.frame)
        self.download_button.setGeometry(640, 350, 130, 30)  # Taille et position du bouton télécharger
        self.download_button.setStyleSheet("background-color: #333333; color: #FFFFFF;")
        self.download_button.clicked.connect(self.download_file)

        # Bouton Quitter
        self.exit_button = QPushButton("Quitter", self.frame)
        self.exit_button.setGeometry(760, 10, 60, 30)  # Position du bouton quitter
        self.exit_button.setStyleSheet("background-color: #FF0000; color: #FFFFFF;")  # Style du bouton
        self.exit_button.clicked.connect(self.close_application)  # Connecter le bouton à la méthode

        self.load_files()

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

    def load_files(self):
        cursor = self.db_conn.cursor()
        cursor.execute(""" 
            SELECT f.IdFichier, f.NomFichier, f.Date, c.NomCategorie, f.Titre 
            FROM Fichier f 
            JOIN Categorie c ON f.IdCategorie = c.IdCategorie
        """)
        records = cursor.fetchall()

        self.table.setRowCount(len(records))
        for row_idx, row_data in enumerate(records):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.table.setItem(row_idx, col_idx, item)

        cursor.close()

    def filter_files(self):
        search_category = self.category_combo.currentText().lower()  # Rechercher par catégorie
        titre_text = self.titre.text().lower()  # Recherche aussi dans le titre
        cursor = self.db_conn.cursor()

        # Vérifier si une catégorie a été sélectionnée
        category_filter = "" if search_category == "sélectionner la catégorie" else search_category

        # Recherche des fichiers en fonction de la catégorie et du titre
        cursor.execute("""
            SELECT f.IdFichier, f.NomFichier, f.Date, c.NomCategorie, f.Titre 
            FROM Fichier f 
            JOIN Categorie c ON f.IdCategorie = c.IdCategorie
        """)
        records = cursor.fetchall()

        # Filtrer les fichiers par catégorie et titre
        filtered_records = [
            record for record in records 
            if (category_filter in record[3].lower() or category_filter == "") 
            and titre_text in (record[4].lower() if record[4] else "")  # Gestion du None
        ]
        
        self.table.setRowCount(len(filtered_records))
        for row_idx, row_data in enumerate(filtered_records):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.table.setItem(row_idx, col_idx, item)

        cursor.close()

    def download_file(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Avertissement", "Veuillez sélectionner un fichier à télécharger.")
            return
        
        file_name = self.table.item(current_row, 1).text()  # Obtenir le nom du fichier

        # Définir le chemin source
        source_directory = "C:/Users/Daouda/Desktop/projet"  # Chemin d'origine (généré automatiquement)
        source_file = os.path.join(source_directory, file_name)

        # Vérifier si le fichier source existe
        if not os.path.exists(source_file):
            QMessageBox.warning(self, "Erreur", f"Le fichier {file_name} n'existe pas dans le répertoire source : {source_file}.")
            return

        # Ouvrir une boîte de dialogue pour sélectionner le répertoire de destination
        destination_directory = QFileDialog.getExistingDirectory(self, "Choisissez un répertoire de téléchargement", os.path.expanduser("~"))

        if not destination_directory:  # Si l'utilisateur annule la sélection
            return

        # Construire le chemin complet de destination
        destination_file = os.path.join(destination_directory, file_name)

        # Vérifier si le fichier existe déjà dans le répertoire de destination
        if os.path.exists(destination_file):
            QMessageBox.warning(self, "Erreur", f"Le fichier {file_name} existe déjà dans le répertoire de destination.")
            return

        # Copier le fichier dans le répertoire sélectionné
        shutil.copy(source_file, destination_file)
        QMessageBox.information(self, "Succès", f"Le fichier {file_name} a été téléchargé avec succès dans {destination_directory}.")

    def close_application(self):
        from connexion import LoginWindow  # Importer la classe LoginWindow depuis connexion.py
        self.login_window = LoginWindow() 
        self.login_window.show()            
        self.hide()  


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ListeFichiersWindow()
    window.show()
    sys.exit(app.exec())










