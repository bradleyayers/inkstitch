---
title: "Point droit"
permalink: /fr/docs/stitches/running-stitch/
excerpt: ""
last_modified_at: 2023-01-20
toc: true
---
## Qu'est-ce que c'est

[![Papillon au point droit](/assets/images/docs/running-stitch.jpg){: width="200x"}](/assets/images/docs/running-stitch.svg){: title="Download SVG File" .align-left download="running-stitch.svg" }

Le point droit produit une série de petits points suivant une ligne ou une courbe.

![Point droit Détail](/assets/images/docs/running-stitch-detail.jpg)

## Comment le créer
Le point droit est créé en définissant un trait en pointillé sur un chemin. Tout type de tiret fera l'affaire et la largeur du trait n'est pas pertinente.

![Pointillé pour point droit](/assets/images/docs/running-stitch-dashes.jpg){: .align-left style="padding: 5px"}
Sélectionnez le trait et allez à `Objet > Fond et contour...` et choisissez l’une des lignes pointillées de l’onglet `Style du contour`.


Ouvrir [`Extensions > Ink/Stitch  > Paramètres`](/fr/docs/params/#stroke-params) pour modifier les paramètres selon vos besoins.

Le sens de la broderie est influencé par la direction du chemin. Si vous souhaitez échanger le départ et l'arrivée de votre point droit, exécutez `Chemin > Inverser`.

**Info:** Afin d'éviter les angles arrondis, un point supplémentaire sera ajouté à la pointe des coins pointus.
{: .notice--info style="clear: both;" }

## Paramétres

Ouvrir `Extensions > Ink/Stitch  > Paramètres` pour paramétrer selon vos besoins.

Paramètres|Description
---|---
Points droits le long des chemins |Doit être activé pour que ces paramètres prennent effet
Méthode                           |Choisir Point Droit
Placement de points manuels       |Doit être desactivé pour ne pas activer [le mode point manuel](/fr/docs/stitches/manual-stitch/)
Répéter                           |Définir combien de fois aller et revenir le long du chemin<br />◦ par défaut: 1 (aller une fois du début à la fin du chemin)<br />◦ Nombre impair: les points se termineront à la fin du chemin<br />◦ Nombre pair: la broderie va revenir au début du chemin
Nombre de répétitions du point triple |Active le [Mode point triple](/fr/docs/stitches/bean-stitch/)<br />◦ Repasse sur chaque point le nombre de fois indiqué.<br />◦ Une valeur de 1 triplera chaque point (avant, arrière, avant).<br />◦ Une valeur de 2 permettra de quintupler chaque point, etc..<br />
Longueur du point droit           |Longueur des points 
Tolerance du point droit          |Les points ne peuvent pas être éloignés de plus que cette distance au chemin. Une tolerance basse peut impliquer des points plus courts. Une tolerance haute entraine un arrondissement des angles aigus.
Espacement Zig-Zag (crête à crête)|Ce paramètre est sans effet sur le point droit
Autoriser les points d'arrêts     |Ajoute un point d'arrêt à la ou les positions choisies
Forcer les points d'arrêts        |Force un point d'arrêt après l'objet indépendament de la valeur de "Saut de fil" dans les Préférences d'Ink/Stitch.
Couper après                      |Couper le fil après avoir brodé cet objet
Arrêter après                     |Arrêter (pause machine) après avoir brodé cet objet. Avant l'arrêt, il y aura un saut vers la position d'arrêt si elle a été définie

## Fichiers exemple avec point droit
{% include tutorials/tutorial_list key="stitch-type" value="Running Stitch" %}