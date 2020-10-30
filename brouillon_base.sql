CREATE DATABASE festival;
\c festival;

CREATE TABLE affiche (
  ida serial,
  imgimp VARCHAR(42), --lien de img stocké
  imgweb VARCHAR(42), --lien de img stocké
  colori VARCHAR(42),
  profcoul VARCHAR(42),
  PRIMARY KEY (id_affiche)
);

CREATE TABLE disque (
  id_disque serial,
  nom VARCHAR(42),
  prix_disque VARCHAR(42),
  id_concert VARCHAR(42),
  PRIMARY KEY (id_disque)
);

CREATE TABLE theme (
  id_theme serial,
  nom VARCHAR(42),
  xxx VARCHAR(42),
  PRIMARY KEY (id_theme)
);

CREATE TABLE specialite (
  idspe serial,
  nom VARCHAR(20), --taille max 20
  PRIMARY KEY (id_specialite)
);

CREATE TABLE secondaire (
  id_interprete int,
  idspe int,
  PRIMARY KEY (id_interprete, idspe)
);

CREATE TABLE interprete (
  id_interprete serial,
  nom VARCHAR(42),
  prenom VARCHAR(42),
  tel CHAR(10), --car pas de cal sur num tel
  email VARCHAR(42),
  naiss VARCHAR(42),
  nat VARCHAR(42),
  resu_bio VARCHAR(42),
  spe_ppal VARCHAR(42),
  PRIMARY KEY (id_interprete)
);

CREATE TABLE concert (
  id_concert serial,
  date VARCHAR(42),
  heure VARCHAR(42),
  salle_spect VARCHAR(42),
  xxx VARCHAR(42),
  id_theme VARCHAR(42),
  id_affiche VARCHAR(42),
  id_bande_promo VARCHAR(42),
  PRIMARY KEY (id_concert)
);

CREATE TABLE programme (
  id_morceau VARCHAR(42),
  id_concert VARCHAR(42),
  ordre_(position) VARCHAR(42),
  PRIMARY KEY (id_morceau, id_concert)
);

CREATE TABLE morceau (
  id_morceau serial,
  auteur VARCHAR(42),
  titre VARCHAR(42),
  durée VARCHAR(42),
  PRIMARY KEY (id_morceau)
);

CREATE TABLE interpreteur_principal (
  id_morceau VARCHAR(42),
  id_interprete VARCHAR(42),
  PRIMARY KEY (id_morceau, id_interprete)
);

CREATE TABLE entracte (
  id_entracte serial,
  nom_(à_dez_???) VARCHAR(42),
  situe_(=position_en_temps_ou_après_x_morceaux) VARCHAR(42),
  xxx VARCHAR(42),
  id_concert VARCHAR(42),
  PRIMARY KEY (id_entracte)
);

CREATE TABLE se_derouler (
  id_concert VARCHAR(42),
  id_lieu VARCHAR(42),
  PRIMARY KEY (id_concert, id_lieu)
);

CREATE TABLE bande_promo (
  id_bande_promo serial,
  taille_(en_ko) VARCHAR(42),
  format_(ex:_mime) VARCHAR(42),
  mots_clés VARCHAR(42),
  durée VARCHAR(42),
  PRIMARY KEY (id_bande_promo)
);

personne( idp, nom, prénom, tél, email)
CREATE TABLE personne (
  idp serial,
  nom VARCHAR(42),
  prenom VARCHAR(40),
  tel CHAR(10), --car pas de cal sur num tel
  email VARCHAR(42),
  PRIMARY KEY (id_personne)
);

CREATE TABLE lieu (
  id_lieu serial,
  nom VARCHAR(42),
  adr VARCHAR(42),
  localite VARCHAR(42),
  dep VARCHAR(42),
  soustype_(null) VARCHAR(42),
   VARCHAR(42),
  id_lieu lieu VARCHAR(42),
  id_lieu_1 VARCHAR(42),
  PRIMARY KEY (id_lieu)
);

CREATE TABLE SALLE (
  nom(varchar(42)) VARCHAR(42),
  adr VARCHAR(42),
  directeur_(=id_personne) VARCHAR(42),
  charge_com_(=id_personne) VARCHAR(42),
  chef_regi(=id_personne) VARCHAR(42),
  id_lieu VARCHAR(42),
  PRIMARY KEY (nom(varchar(42)))
);

CREATE TABLE travailleur (
  id_personne serial,
  nom(varchar(42)) VARCHAR(42),
  PRIMARY KEY (id_personne, nom(varchar(42)))
);

CREATE TABLE categorie (
  id_categorie serial,
  nom VARCHAR(42),
  prix_ref VARCHAR(42),
  PRIMARY KEY (id_catégorie)
);

CREATE TABLE comporter(TICKET) (
  id_lieu VARCHAR(42),
  id_place VARCHAR(42),
  id_categorie VARCHAR(42),
  prix_final(selon_cas) VARCHAR(42),
  PRIMARY KEY (id_lieu, id_place, id_categorie)
);

CREATE TABLE place (
  id_place serial,
  xxxstatut(vendu/réservé_fnac) VARCHAR(42),
  PRIMARY KEY (id_place)
);

ALTER TABLE disque ADD FOREIGN KEY (id_concert) REFERENCES concert (id_concert);
ALTER TABLE secondaire ADD FOREIGN KEY (id_specialite) REFERENCES specialite (id_specialite);
ALTER TABLE secondaire ADD FOREIGN KEY (id_interprete) REFERENCES interprete (id_interprete);
ALTER TABLE concert ADD FOREIGN KEY (id_bande_promo) REFERENCES bande_promo (id_bande_promo);
ALTER TABLE concert ADD FOREIGN KEY (id_affiche) REFERENCES affiche (id_affiche);
ALTER TABLE concert ADD FOREIGN KEY (id_theme) REFERENCES theme (id_theme);
ALTER TABLE programme ADD FOREIGN KEY (id_concert) REFERENCES concert (id_concert);
ALTER TABLE programme ADD FOREIGN KEY (id_morceau) REFERENCES morceau (id_morceau);
ALTER TABLE interpreteur_principal ADD FOREIGN KEY (id_interprete) REFERENCES interprete (id_interprete);
ALTER TABLE interpreteur_principal ADD FOREIGN KEY (id_morceau) REFERENCES morceau (id_morceau);
ALTER TABLE entracte ADD FOREIGN KEY (id_concert) REFERENCES concert (id_concert);
ALTER TABLE se_derouler ADD FOREIGN KEY (id_lieu) REFERENCES lieu (id_lieu);
ALTER TABLE se_derouler ADD FOREIGN KEY (id_concert) REFERENCES concert (id_concert);
ALTER TABLE lieu ADD FOREIGN KEY (id_lieu lieu) REFERENCES lieu (id_lieu);
ALTER TABLE salle ADD FOREIGN KEY (id_lieu) REFERENCES lieu (id_lieu);
ALTER TABLE travailleur ADD FOREIGN KEY (nom(varchar(42))) REFERENCES salle (nom(varchar(42)));
ALTER TABLE travailleur ADD FOREIGN KEY (id_personne) REFERENCES personne (id_personne);
ALTER TABLE comporter(TICKET) ADD FOREIGN KEY (id_catégorie) REFERENCES categorie (id_catégorie);
ALTER TABLE comporter(TICKET) ADD FOREIGN KEY (id_place) REFERENCES place (id_place);
ALTER TABLE comporter(TICKET) ADD FOREIGN KEY (id_lieu) REFERENCES lieu (id_lieu);