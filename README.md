# EIT-PPS-2019
Evaluation de deux plateformes open source d’analyse linguistique: CEA LIST LIMA et Stanford Core NLP.

## Lancer
Le programme est prévu pour être lancé en ligne de commande.
### Lima
Pour lancer une analyse Lima, la commande suivante doit être saisie à partir du dossier de script Lima:
`Lima_NLP_Core.py -p <File Path> -f <File Name> -l <Lima Path> -o <Script Output>`
* File Path correspondant au chemin relatif du fichier à analyser
* File Name correspondant au nom du fichier
* Lima Path correspondant au chemin relatif vers les fichiers Lima générés précédemment
* Script Output correspondant à la localisation des fichiers générés.
#### Exemple:
`python Lima_NLP_Core.py -p "../../Files/" -f "wsj_0010_sample.txt" -l '../../Files/Lima/' -o 'Generated/'`

Aura pour effet de lancer l'analyse du fichier ../../Files/wsj_0010_sample.txt à partir des fichier Lima contenus dans ../../Files/Lima/, et génèrera les fichiers .pos.lima, .pos.univ.lima ainsi que .ner.lima dans le dossier Generated/

### Dossiers
Le projet se compose de 3 dossiers, à savoir:
* Files/, qui comprend des fichiers déjà générés par Lima/Stanford Core, ainsi que des corpus de test
* src/, qui comprend les scripts pythons relatifs au projet.
* docs/, qui comprend le rapport de projet.

### Pré-requis
* Python 2.7 - Python 3.5+ peut être utilisé mais l'évaluation peut crash.
* lxml library (`pip install lxml`)
* Stanford Core NLP (NER and POS Tagger)
* CEA LIST LIMA

-- Note that this code was tested on a Ubuntu 16.04 LTS distribution. -- 

## Auteurs
* **Anthony WOZNICA**
* **Benjamin BRINDAMOUR**
* **Thomas AZEMARD**
