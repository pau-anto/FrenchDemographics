DROP DATABASE IF EXISTS Statistiques;
CREATE DATABASE Statistiques;
USE Statistiques;

CREATE TABLE Regions (
   codeRegion TINYINT UNSIGNED,
   nomRegion VARCHAR(26) NOT NULL,
   PRIMARY KEY (codeRegion)
);

CREATE TABLE Departements (
   codeDepartement CHAR(3),
   nomDepartement VARCHAR(23) NOT NULL,
   codeRegion TINYINT UNSIGNED NOT NULL,
   PRIMARY KEY (codeDepartement),
   CONSTRAINT fk_region FOREIGN KEY (codeRegion) REFERENCES Regions (codeRegion)
);

CREATE TABLE Communes (
   codeCommune CHAR(5),
   nomCommune VARCHAR(45) NOT NULL,
   superficie FLOAT,
   codeDepartement CHAR(3) NOT NULL,
   PRIMARY KEY (codeCommune),
   CONSTRAINT fk_departement FOREIGN KEY (codeDepartement) REFERENCES Departements (codeDepartement)
);

CREATE TABLE Statistiques (
   codeCommune CHAR(5),
   anneeSup SMALLINT UNSIGNED,
   anneeInf SMALLINT UNSIGNED,
   populationDebut INT,
   populationFin INT,
   naissances INT,
   deces INT,
   logementsDebut INT,
   logementsFin INT,
   PRIMARY KEY (codeCommune, anneeSup, anneeInf),
   CONSTRAINT fk_commune FOREIGN KEY (codeCommune) REFERENCES Communes (codeCommune)
);
