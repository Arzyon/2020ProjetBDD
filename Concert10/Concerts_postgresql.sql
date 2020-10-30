CREATE DATABASE CONCERTS;
\c CONCERTS;

CREATE TABLE AFFICHE (
  id_affiche VARCHAR(42),
  img_imp VARCHAR(42),
  img_web VARCHAR(42),
  colori VARCHAR(42),
  prof_coul VARCHAR(42),
  PRIMARY KEY (id_affiche)
);

CREATE TABLE DISQUE (
  id_disque VARCHAR(42),
  nom VARCHAR(42),
  prix_disque VARCHAR(42),
  id_concert VARCHAR(42),
  PRIMARY KEY (id_disque)
);

CREATE TABLE SPÉCIALITÉ (
  id_spécialité VARCHAR(42),
  nom_(ex:_violon VARCHAR(42),
  harpe) VARCHAR(42),
  PRIMARY KEY (id_spécialité)
);

CREATE TABLE SECONDAIRE (
  id_interprète VARCHAR(42),
  id_spécialité VARCHAR(42),
  PRIMARY KEY (id_interprète, id_spécialité)
);

CREATE TABLE INTERPRÈTE (
  id_interprète VARCHAR(42),
  nom VARCHAR(42),
  prénom VARCHAR(42),
  tel VARCHAR(42),
  email VARCHAR(42),
  naiss VARCHAR(42),
  nat VARCHAR(42),
  resu_bio VARCHAR(42),
  spe_ppal VARCHAR(42),
  PRIMARY KEY (id_interprète)
);

CREATE TABLE CONCERT (
  id_concert VARCHAR(42),
  date VARCHAR(42),
  heure VARCHAR(42),
  salle_spect VARCHAR(42),
  theme VARCHAR(42),
  id_affiche VARCHAR(42),
  PRIMARY KEY (id_concert)
);

CREATE TABLE PROGRAMME (
  id_morceau VARCHAR(42),
  id_concert VARCHAR(42),
  ordre_(position) VARCHAR(42),
  PRIMARY KEY (id_morceau, id_concert)
);

CREATE TABLE MORCEAU (
  id_morceau VARCHAR(42),
  auteur VARCHAR(42),
  titre VARCHAR(42),
  durée VARCHAR(42),
  PRIMARY KEY (id_morceau)
);

CREATE TABLE INTERPRÉTEUR_PRINCIPAL (
  id_morceau VARCHAR(42),
  id_interprète VARCHAR(42),
  PRIMARY KEY (id_morceau, id_interprète)
);

CREATE TABLE ENTRACTE (
  id_entracte VARCHAR(42),
  situe VARCHAR(42),
  id_concert VARCHAR(42),
  PRIMARY KEY (id_entracte)
);

CREATE TABLE SE_DÉROULER (
  id_concert VARCHAR(42),
  id_lieu VARCHAR(42),
  PRIMARY KEY (id_concert, id_lieu)
);

CREATE TABLE BANDE_PROMO (
  id_bande_promo VARCHAR(42),
  taille_(en_ko) VARCHAR(42),
  format VARCHAR(42),
  mots_clés VARCHAR(42),
  durée VARCHAR(42),
  id_concert VARCHAR(42),
  PRIMARY KEY (id_bande_promo)
);

CREATE TABLE PERSONNE (
  id_personne VARCHAR(42),
  nom VARCHAR(42),
  prénom VARCHAR(42),
  tél VARCHAR(42),
  email VARCHAR(42),
  PRIMARY KEY (id_personne)
);

CREATE TABLE LIEU (
  id_lieu VARCHAR(42),
  nom VARCHAR(42),
  adr VARCHAR(42),
  localité VARCHAR(42),
  dep VARCHAR(42),
  soustype VARCHAR(42),
   VARCHAR(42),
  id_lieu lieu VARCHAR(42),
  id_lieu_1 VARCHAR(42),
  PRIMARY KEY (id_lieu)
);

CREATE TABLE SALLE (
  nom(varchar(42)) VARCHAR(42),
  adr VARCHAR(42),
  directeur VARCHAR(42),
  charge_com VARCHAR(42),
  chef_regi VARCHAR(42),
  id_lieu VARCHAR(42),
  PRIMARY KEY (nom(varchar(42)))
);

CREATE TABLE TRAVAILLEUR (
  id_personne VARCHAR(42),
  nom(varchar(42)) VARCHAR(42),
  PRIMARY KEY (id_personne, nom(varchar(42)))
);

CREATE TABLE COMPORTER(TICKET) (
  id_lieu VARCHAR(42),
  id_catégorie VARCHAR(42),
  prix_final(selon_cas) VARCHAR(42),
  PRIMARY KEY (id_lieu, id_catégorie)
);

CREATE TABLE CATÉGORIE (
  id_catégorie VARCHAR(42),
  nom VARCHAR(42),
  prix_ref VARCHAR(42),
  PRIMARY KEY (id_catégorie)
);

CREATE TABLE PLACE (
  id_place VARCHAR(42),
  xxxstatut(vendu/réservé_fnac) VARCHAR(42),
  id_lieu VARCHAR(42),
  id_catégorie VARCHAR(42),
  PRIMARY KEY (id_place)
);

ALTER TABLE DISQUE ADD FOREIGN KEY (id_concert) REFERENCES CONCERT (id_concert);
ALTER TABLE SECONDAIRE ADD FOREIGN KEY (id_spécialité) REFERENCES SPÉCIALITÉ (id_spécialité);
ALTER TABLE SECONDAIRE ADD FOREIGN KEY (id_interprète) REFERENCES INTERPRÈTE (id_interprète);
ALTER TABLE CONCERT ADD FOREIGN KEY (id_affiche) REFERENCES AFFICHE (id_affiche);
ALTER TABLE PROGRAMME ADD FOREIGN KEY (id_concert) REFERENCES CONCERT (id_concert);
ALTER TABLE PROGRAMME ADD FOREIGN KEY (id_morceau) REFERENCES MORCEAU (id_morceau);
ALTER TABLE INTERPRÉTEUR_PRINCIPAL ADD FOREIGN KEY (id_interprète) REFERENCES INTERPRÈTE (id_interprète);
ALTER TABLE INTERPRÉTEUR_PRINCIPAL ADD FOREIGN KEY (id_morceau) REFERENCES MORCEAU (id_morceau);
ALTER TABLE ENTRACTE ADD FOREIGN KEY (id_concert) REFERENCES CONCERT (id_concert);
ALTER TABLE SE_DÉROULER ADD FOREIGN KEY (id_lieu) REFERENCES LIEU (id_lieu);
ALTER TABLE SE_DÉROULER ADD FOREIGN KEY (id_concert) REFERENCES CONCERT (id_concert);
ALTER TABLE BANDE_PROMO ADD FOREIGN KEY (id_concert) REFERENCES CONCERT (id_concert);
ALTER TABLE LIEU ADD FOREIGN KEY (id_lieu lieu) REFERENCES LIEU (id_lieu);
ALTER TABLE SALLE ADD FOREIGN KEY (id_lieu) REFERENCES LIEU (id_lieu);
ALTER TABLE TRAVAILLEUR ADD FOREIGN KEY (nom(varchar(42))) REFERENCES SALLE (nom(varchar(42)));
ALTER TABLE TRAVAILLEUR ADD FOREIGN KEY (id_personne) REFERENCES PERSONNE (id_personne);
ALTER TABLE COMPORTER(TICKET) ADD FOREIGN KEY (id_catégorie) REFERENCES CATÉGORIE (id_catégorie);
ALTER TABLE COMPORTER(TICKET) ADD FOREIGN KEY (id_lieu) REFERENCES LIEU (id_lieu);
ALTER TABLE PLACE ADD FOREIGN KEY (id_catégorie) REFERENCES CATÉGORIE (id_catégorie);
ALTER TABLE PLACE ADD FOREIGN KEY (id_lieu) REFERENCES LIEU (id_lieu);