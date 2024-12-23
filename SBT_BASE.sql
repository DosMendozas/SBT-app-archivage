-- Table Personne (pour les utilisateurs et les administrateurs)
CREATE TABLE Personne (
    IdPersonne INT AUTO_INCREMENT PRIMARY KEY,
    NomPersonne VARCHAR(50) NOT NULL UNIQUE,
    MotDePasse VARCHAR(255) NOT NULL,  -- Augmenter la taille pour hash de mot de passe
    Role ENUM('Utilisateur', 'Administrateur') NOT NULL  -- Rôle défini
);

-- Table Administrateur (spécialisation de Personne)
CREATE TABLE Administrateur (
    IdPersonne INT PRIMARY KEY,
    NomAdministrateur VARCHAR(50),  -- Correction du type pour plus de flexibilité
    FOREIGN KEY (IdPersonne) REFERENCES Personne(IdPersonne) ON DELETE CASCADE -- Cascade suppression
);

-- Table Utilisateur (spécialisation de Personne)
CREATE TABLE Utilisateur (
    IdPersonne INT PRIMARY KEY,
    NomUtilisateur VARCHAR(50),  -- Correction du type
    FOREIGN KEY (IdPersonne) REFERENCES Personne(IdPersonne) ON DELETE CASCADE -- Cascade suppression
);

-- Table Categorie
CREATE TABLE Categorie (
    IdCategorie INT AUTO_INCREMENT PRIMARY KEY,  -- Ajout de AUTO_INCREMENT pour les catégories
    NomCategorie VARCHAR(50) UNIQUE NOT NULL  -- UNIQUE pour éviter les doublons de catégories
);

-- Table Fichier (lié à une personne et une catégorie)
CREATE TABLE Fichier (
    IdFichier INT AUTO_INCREMENT PRIMARY KEY,
    NomFichier VARCHAR(255) NOT NULL,  -- Plus de caractères pour les noms de fichiers
    Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Changement pour un type date-heure approprié
    IdPersonne INT,  -- Lien vers Personne (peut être administrateur ou utilisateur)
    IdCategorie INT,  -- Lien vers Categorie
    Telecharge TINYINT(1) DEFAULT 0,
    FOREIGN KEY (IdPersonne) REFERENCES Personne(IdPersonne) ON DELETE SET NULL, -- Si personne supprimée, laisser NULL
    FOREIGN KEY (IdCategorie) REFERENCES Categorie(IdCategorie) ON DELETE SET NULL -- Si catégorie supprimée, laisser NULL
);
