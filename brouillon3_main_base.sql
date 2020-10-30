








affiche ( ida, imgimp, imgweb, colori, profcoul )
CREATE TABLE affiche(
  ida,  --
  imgimp,  --
  imgweb,  --
  colori,  --
  profcoul,  --
  PRIMARY KEY ()
);

disque ( idd, nom, prixdisque, idc )
CREATE TABLE disque(
  idd,  -- 
  nom,  -- 
  prixdisque,  -- 
  idc,  -- 
  PRIMARY KEY ()
);

spécialité ( idspe, nom, )
CREATE TABLE specialite(
  idspe,  --
  nom,  --
  PRIMARY KEY ()
);

secondaire ( idi, idspe, )
CREATE TABLE secondaire(
  idi, --
  idspe, --
  PRIMARY KEY ()
);

interprète ( idi, nom, prénom, tel, email, naiss, nat, bioresu, speppal, )
CREATE TABLE interprete (
  idi,  -- 
  nom,  -- 
  prénom,  -- 
  tel,  -- 
  email,  -- 
  naiss,  -- 
  nat,  -- 
  bioresu,  -- 
  speppal,  -- 
  PRIMARY KEY ()
);


concert ( idc, datec, heure, sallespect, theme, ida, )
CREATE TABLE concert (
  idc,  -- 
  datec,  -- 
  heure,  -- 
  sallespect,  -- 
  theme,  -- 
  ida,  -- 
  PRIMARY KEY ()
);

programme ( idm, idc, ordre, )
CREATE TABLE programme (
  idm,  -- 
  idc,  -- 
  ordre,  -- 
  PRIMARY KEY ()
);


morceau ( idm, auteur, titre, durée, )
CREATE TABLE morceau (
  idm,  -- 
  auteur,  -- 
  titre,  -- 
  durée,  -- 
  PRIMARY KEY ()
);

interpréteur principal ( idm, idi, )
CREATE TABLE interpreteur_principal (
  idm,  -- 
  idi,  -- 
  PRIMARY KEY ()
);

entracte ( ide, situe, idc, )
CREATE TABLE entracte (
  ide,  --
  situe,  --
  idc,  --
  PRIMARY KEY ()
);

se dérouler ( idc, idl, )
CREATE TABLE se_derouler (
  idc, -- 
  idl, --
  PRIMARY KEY ()
);


bande_promo ( id_bande_promo, taille (en ko), format, motsclés, durée, idc, )
CREATE TABLE bande_promo (
  id_bande_promo, 
  taille (en ko), -- 
  format, -- 
  motsclés, -- 
  durée, -- 
  idc, -- 
  PRIMARY KEY ()
);

personne ( idp, nom, prénom, tél, email, )
CREATE TABLE personne (
  idp, -- 
  nom, -- 
  prénom, -- 
  tél, -- 
  email, -- 
  PRIMARY KEY ()
);


lieu ( idl, nom, adr, localité, dep, soustype, idsouslieu, )
CREATE TABLE lieu (
  idl,  -- 
  nom,  -- 
  adr,  -- 
  localité,  -- 
  dep,  -- 
  soustype,  -- 
  id_souslieu,  -- 
  PRIMARY KEY ()
);

salle ( nom, adr, directeur, chargecom, chefregi, idl, )
CREATE TABLE salle (
  nom varchar(42),  -- 
  adr,  --  
  directeur,  --  
  chargecom,  -- 
  chefregi,  -- 
  idl, -- 
  PRIMARY KEY ()
);

travailleur ( idp, nom )
CREATE TABLE travailleur (
  idp, -- 
  nom varchar(42), --
  PRIMARY KEY ()
);


comporter(ticket) ( idl, idcat, prixfinal, )
CREATE TABLE comporter (
  idl, --
  idcat, --
  prixfinal, -- (selon cas)
  PRIMARY KEY ()
);


catégorie ( idcat, nom, prixref )
CREATE TABLE categorie (
  idcat, -- 
  nom, -- 
  prixref, --
  PRIMARY KEY ()
);

place ( idpla, XXXstatut(vendu/réservé FNAC), idl, idcat )
CREATE TABLE place (
  idpla, --
  XXXstatut, --(vendu/réservé FNAC)
  idl, --
  idcat, --
  PRIMARY KEY ()
);










