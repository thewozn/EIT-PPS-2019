# EIT-PPS-2019
Evaluation de deux plateformes open source d’analyse linguistique: CEA LIST LIMA et Stanford Core NLP.

## Utilisation
Le programme est prévu pour être lancé en ligne de commande.

### Lima
Pour lancer une analyse Lima, la commande suivante doit être saisie à partir du dossier de script Lima:
`Lima_NLP_Core.py -p <File Path> -f <File Name> -l <Lima Path> -o <Script Output>`
* File Path correspondant au chemin relatif du fichier à analyser
* File Name correspondant au nom du fichier
* Lima Path correspondant au chemin relatif vers les fichiers Lima générés précédemment
* Script Output correspondant à la localisation des fichiers générés.


##### Exemple:
`python Lima_NLP_Core.py -p "../../Files/" -f "wsj_0010_sample.txt" -l '../../Files/Lima/' -o 'Generated/'`
Aura pour effet de lancer l'analyse du fichier ../../Files/wsj_0010_sample.txt à partir des fichier Lima contenus dans ../../Files/Lima/, et génèrera les fichiers .pos.lima, .pos.univ.lima ainsi que .ner.lima dans le dossier Generated/

Attention, il est nécessaire d'avoir au préalable généré les fichier Lima à l'aide de la commande analyzeText !

### Stanford Core
Pour lancer une analyse Stanford Core, la commande suivante doit être saisie à partir du dossier de script Lima:
`Lima_NLP_Core.py -p <File Path> -f <File Name>`
* File Path correspondant au chemin relatif du fichier à analyser
* File Name correspondant au nom du fichier


##### Exemple:
`python Stanford_NLP_Core.py -p '../../Files/Stanford/' -f 'wsj_0010_sample.txt'`
Aura pour effet de lancer l'analyse du fichier ../../Files/Stanford/wsj_0010_sample.txt.ner.stanford et d'afficher les entités nommées et de créer le fichier wsj0010_sample.txt.pos.univ.stanford (conversion des étiquettes en étiqquettes universelles) dans ../../Files/Stanford/

Attention, il est nécessaire d'avoir au préalable généré les fichiers Stanford pos et ner à partir des commandes prévues à cet effet !


## Conversion Lima vers Stanford
Il peut être intéressant de comparer les taux de reconnaissances d'entités nommées de Lima et de Stanford Core NLP. Pour cela, il suffit de lancer le script convert.py dans la console.
En raison du grand nombre d'arguments nécessaires, (fichiers lima, fichiers stanford, fichiers de référence), il est nécessaire d'éditer le script si l'on souhaite effectuer la conversion à partir d'autres fichiers.

Le résultat de la conversion crée les fichiers NE.txt.lima.out, NE.txt.ref.out et NE.txt.lima.out, pouvant être diectement évalués (texte en forme standardisée).


## Evaluation
Afin d'évaluer un fichier, il est nécessaire de convertir le texte de référence en majuscules et d'en supprimer les sauts de ligne, les fichiers de sortie des scripts dans src/Stanford_NLP et src/Lima_NLP étant convertis en majuscules sans sauts de ligne.

## Dossiers
Le projet se compose de 3 dossiers, à savoir:
* Files/, qui comprend des fichiers déjà générés par Lima/Stanford Core, ainsi que des corpus de test
* src/, qui comprend les scripts pythons relatifs au projet.
* docs/, qui comprend le rapport de projet.

## Pré-requis
* Python 2.7 - Python 3.5+ peut être utilisé mais l'évaluation peut crash.
* lxml library (`pip install lxml`)
* Stanford Core NLP (NER and POS Tagger)
* CEA LIST LIMA

-- Note that this code was tested on a Ubuntu 16.04 LTS distribution. -- 

## Auteurs
* **Anthony WOZNICA**
* **Benjamin BRINDAMOUR**
* **Thomas AZEMARD**
