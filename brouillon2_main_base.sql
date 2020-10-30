



affiche( ida, imgimp, imgweb, colori, profcoul )
specialite( idspe, nom (ex: violon, harpe))
personne( idp, nom, prénom, tél, email)
morceau( idm, auteur, titre, durée)
categorie( idcat, nom, prixref)


CREATE TABLE affiche (
  ida serial, 
  imgimp VARCHAR(60), --lien web pour image
  imgweb VARCHAR(60), --lien web pour image
  colori CHAR(8), --base hexa pour couleur
  profcoul VARCHAR(10), --???
  PRIMARY KEY (ida)
);
CREATE TABLE specialite (
  idspe serial, 
  nom VARCHAR(19) unique, --19 taille max
  PRIMARY KEY (idspe)
);
CREATE TABLE personne (
  idp serial, 
  nom VARCHAR(50), --lien web pour image
  prénom VARCHAR(40), --lien web pour image
  tel CHAR(10), --pas de cal sur num tel
  email VARCHAR(60), --
  PRIMARY KEY (idp)
);
CREATE TABLE morceau (
  idm serial, 
  auteur VARCHAR(50), --lien web pour image
  titre VARCHAR(60), --lien web pour image
  durée time, --heure minute
  PRIMARY KEY (idm)
);
CREATE TABLE categorie (
  idcat serial, 
  nom VARCHAR(60), --lien web pour image
  prixref int, --en € >= 0
  PRIMARY KEY (idcat)
);


concert( idc, date, heure, sallespect, theme, #ida, )
CREATE TABLE concert (
  idc serial, 
  datec date, --
  heure time, --
  sallespect VARCHAR(42), --PK salle
  theme VARCHAR(30), -- NULL par défaut 
  ida int,
  PRIMARY KEY (idcat)
);
CREATE TABLE lieu (
	idl serial, 
	nom VARCHAR(60), --
	adr VARCHAR(132), -- 
	localité VARCHAR(90), --trouver non ville la plus longue de france 
	dep VARCHAR(30), -- trouver non dep le plus long de france 
	soustype, --can be NULL
	souslieu,
	PRIMARY KEY (idl)
);
CREATE TABLE lieu (
  idcat serial, 
  nom VARCHAR(60), --lien web pour image
  prixref int, --en € >= 0
  PRIMARY KEY (idcat)
);
CREATE TABLE categorie (
  idcat serial, 
  nom VARCHAR(60), --lien web pour image
  prixref int, --en € >= 0
  PRIMARY KEY (idcat)
);
CREATE TABLE categorie (
  idcat serial, 
  nom VARCHAR(60), --lien web pour image
  prixref int, --en € >= 0
  PRIMARY KEY (idcat)
);

































