---
permalink: /fr/tutorials/make_tartan_font_easier/
title: "Uniformiser les tartans d'une fonte et limiter les changements de fils"
language: fr
last_modified_at: 2024-04-29
excerpt: "Diminuer le nombre de changements de fil avec un remplissage global pour toutes les lettres"
image: "/assets/images/tutorials/tutorial-preview-images/make_tartan_font_easier.jpg"
tutorial-type:
  - Sample File
stitch-type:
  - "Tartan Fill"
  - "Linear Gradient Fill"
techniques:
tool:
  - "Fill"
field-of-use:
user-level:
---
![Brodée](/assets/images/tutorials/tutorial-preview-images/make_tartan_font_easier.jpg)

Les fontes en tartan donnent des résultats très colorés, mais aussi nécessitant beaucoup de changements de fil.
Il est possible de combiner les surfaces correspondant aux tartans des lettres en un unique tartan, et de limiter ainsi très fortement le nombre de changements de fils.

Ainsi, si l'on souhaite utiliser Emilio 20 Tartan, on se trouve dans cette situation

![Trop de sauts de fils ](/assets/images/tutorials/make_tartan_font_easier/too_many_colors-changes.jpg)
Si l'on accepte de passer à un même remplissage tartan pour toutes les lettres

![Brodée](/assets/images/tutorials/make_tartan_font_easier/primavera.jpg)
alors la situation est très différente

![Brodée](/assets/images/tutorials/make_tartan_font_easier/only_a_few_color_changes.jpg)

Beaucoup moins de sauts de fils, mais en revanche des grands sauts entre les lettres. Cette méthode est donc à utiliser de préférence avec une machine capable de couper des fils.

Vous pourrez alors ajouter  au remplissage tartan une commande "couper après" avec Ink/Stitch > Paramètres pour convertir les sauts internes du tartan en découpe de fil.

![Brodée](/assets/images/tutorials/make_tartan_font_easier/add_trims.jpg)


La technique est très simple: 
* Utiliser la fonte Emilio 2O Tartan 
* Sélectionner tous les tartans (si vous n'avez pas d'autres remplissage rouge visible , sélectionner un des remplissages  et faire Inkscape > Édition> Sélectionner même couleur de fond)
* Les combiner (Inkscape > Chemin > Combiner)
* Placer  la forme résultante sous le reste du lettrage
* Ink/Stitch > Outils : Remplissage  > [Tartan](/fr/docs/fill-tools/#tartan) et choisissez les paramètres à votre convenance.
  
Vous pouvez aussi choisir d'utiliser un autre type de remplissage, en particulier  un 
[remplissage en dégradé linaire](/fr/docs/stitches/linear-gradient-fill)

![Brodée](/assets/images/tutorials/make_tartan_font_easier/herbst.jpg)



