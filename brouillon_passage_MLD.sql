




affiche( ida, imgimp, imgweb, colori, profcoul )
specialite( idspe, nom (ex: violon, harpe))
personne( idp, nom, prénom, tél, email)
interprete( idi, nom, prénom, tel, email, naiss, nat, resubio, #speppal)
morceau( idm, auteur, titre, duée)
categorie( idcat, nom, prixref)

PK: affiche(ida)
PK: specialite(idspe)
PK: personne(idp)
PK: interprete(idi)
FK: interprete(speppal) cf specialite(idspe)
PK: morceau(idm)
PK: categorie(idcat)



disque( idd, nom, prixdisq, #idc)
entracte( ide, situe, #idc)
bandepromo( idb, taille (en ko), format, mots clés, durée, #idc)
salle( nom, adr, directeur, chargecom, chefregi, #idl)

PK: disque(idd)
FK: disque(idc) cf concert(idc)
PK: entracte(ide)
FK: entracte(idc) cf concert(idc)
PK: bandepromo(idb)
FK: bandepromo(idc) cf concert(idc)
PK: salle(nom)
FK: salle(idl) cf lieu(idl)



place( idpl, XXXstatut(vendu/réservé FNAC), #idl, #idcat)
lieu( idl, nom, adr, localité, dep, soustype, souslieu(#idl))
concert( idc, date, heure, sallespect, theme, #ida, )

PK: place(idpl)
FK: place(idl) cf lieu(idl)
FK: place(idcat) cf categorie(idcat)
PK: lieu(idl)
FK: lieu(souslieu) cf lieu(idl)
PK: concert(idc)
FK: concert(ida) cf affiche(ida)



travailleur(#idp, #salle.nom)
secondaire(#idspe, #idi)
interppal(#idi, #idm) 
programme(#idc, #idm, ordre (position))
sederouler(#idc, #idl) 
comporter(ticket)(#idl, #idcat ,prix_final(selon cas))

FK: travailleur(idp) cf personne(idp)
FK: travailleur(salle.nom) cf salle(nom)
PK: (idp, salle.nom)
PK: secondaire(idspe, idi)
FK: secondaire(idspe) cf specialite(idspe)
FK: secondaire(idi) cf interprete(idi)
PK: interppal(idi, idm)
FK: interppal(idi) cf interprete(idi)
FK: interppal(idm) cf morceau(idm)
PK: programme(idc, idm)
FK: programme(idc) cf concert(idc)
FK: programme(idm) cf morceau(idm)
PK: sederouler(idc, idl)
FK: sederouler(idc) cf concert(idc)
FK: sederouler(idl) cf lieu(idl)
PK: comporter(ticket)(idl, idcat)
FK: comporter(ticket)(idl) cf lieu(idl)
FK: comporter(ticket)(idcat) cf categorie(idcat)







PK: ()
PK: ()
PK: ()
FK: () cf ()
FK: () cf ()
FK: () cf ()
FK: () cf ()
FK: () cf ()




