# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 14:06:49 2018

Partie relative à l'extraction d'entitées nommées à l'aide de l'outil
NER Stanford dans le cadre du projet d'EIT d'ET5 INFO | POLYTECH PARIS-SUD 2019.

-- First published on git/anthwozn

Toute réutilisation du programme ci dessous requiert la mention de l'auteur
dans l'en-tête du fichier.

@author: WOZNICA A.
"""

import sys, getopt

class NLP_core_Stanford:
    """
    Classe qui concerne la reconnaissance d'entités nommées sous Stanford NER
    
    Chaque méthode est commentée.
    """
    
    
    def __init__(self, path, fileName):
        """
        Initialise la classe et génère un dictionnaire contenant les entrées nommées.
        
        Afin d'éviter que entités comme 'the White House' soient coupées en trois entités
        nommées [the, White, House] - ce qui poserait problème lors de la reconnaissance
        (certaines entités communes auraient été reconnues comme entités nommées)-, on 
        privilégie une lecture séquentielle.
        
        Le principe est le suivant:
        Chaque mot est lu, et lorsque le dernier mot lu change d'étiquette, on considère
        l'ensemble précédent comme une entité nommée à part entière. 
        
        Exemple:
        Prenons la phrase:
        L'/LOCATION Université/LOCATION Paris-Sud/LOCATION concentre/O de/O grandes/O écoles/O ./O
        
        Elle sera lue comme suit:
        L'/LOCATION
        Université/LOCATION (Précédent: LOCATION)
        Paris-Sud/LOCATION (Précédent: LOCATION)
        concentre/O (Précédent: LOCATION)
        ==> /O n'est pas /LOCATION, on considère l'ensemble "L'Université Paris-Sud" comme 
            une novelle entité nommée.
        """
        
        # Création du dictionnaire d'entités nommées
        self.dataset = {}
        self.path = path
        self.fileName = fileName
        file = open(path + fileName + '.ner.stanford', 'r')
    
        splitted = file.read().replace('\n', ' ').split(' ')

        # Création d'une pile qui stock l'étique actuelle ainsi que celle qui la précède
        self.tag_pile = ["", splitted[0].split('/')[1]]
        
        self.named_entity = []  # Entitée nommée partielle
        self.number = 0         # Nombre d'entités nommées
        
        # Parcours de chaque couple Mot_Etiquette
        for item in splitted:
            if(item.lstrip() != ""):
                
                
                p_entity = item.split('/')  # Séparation du mot de l'étiquette
                self.push(p_entity[1])      # Ajout de l'étiquette à la pile
                
                # Cas du changement d'étiquette
                if(self.tag_pile[0] != self.tag_pile[1]):
                    
                    if(self.tag_pile[0] != 'O'):    # On ne s'intéresse qu'aux entités nommées...
                      
                        entity = ' '.join(self.named_entity)
                        if(entity not in self.dataset.keys()): # Si l'entité n'est pas connue, on crée une entrée
                            self.dataset[entity] = {
                                'type':     self.tag_pile[0],
                                'occurrences':   1
                            }
                        else:
                            self.dataset[entity]['occurrences'] += 1
                            
                        self.number += 1
                        
                    self.named_entity = [] # Remise à vide de l'entité nommée
                
                # Ajout d'une partie d'étiquette
                self.named_entity.append(p_entity[0])



    def push(self, etiquette):
        """
        Etiquette actuelle -> Ancienne étiquette
        Nouvelle étiquette (argument de fonction) -> Etiquette actuelle
        """
        self.tag_pile[0] = self.tag_pile[1]
        self.tag_pile[1] = etiquette
    
    
    def convert_Penn_TreeBank(self, banksource):
        """
        Convertit un texte Lima en étiquettes Penn TreeBank.
        
        On s'appuie sur la table de correspondances chargée.
        """
        
        # Dictionnaire contenant la table de correspondance
        self.match_bank = {}
        
        bank_ = open(banksource, 'rb')
        content_ = bank_.read()
        content_ = content_.decode("utf-16").split("\r\n") # Si le fichier est écrit sous Windows, on le décode !
        bank_.close()
        
        # Remplissage du dictionnaire
        for match_ in content_:
            match_ = match_.split(' ')
            self.match_bank[match_[0]] = match_[1]
        
        # Chargement de .pos.stanford
        file = open(self.path + self.fileName + '.pos.stanford', "r")
        s = file.read()
        file.close()
        
        tokens = s.split(' ')
        
        # Remplacement des tokens
        for i in range(0, len(tokens)):
            if('_' in tokens[i]):
                entity = tokens[i].split('_')[1]
                if(entity in self.match_bank.keys()):
                    tokens[i] = tokens[i].replace('_' + entity, '_' + self.match_bank[entity])
                
        s = ' '.join(tokens)
        
        
        #s = s.replace("_PROPN", "_NNP")
        s = s.replace("_SENT", "_.")
        s = s.replace("_SCONJ", "_CC")
        s = s.replace("_COMMA", "_,")
        s = s.replace("_COLON", "_:")
        
        
        self.ptbString = s
        
    def __str__(self):
        """
        Redéfinition de print()
        Affiche les entités nommées sous forme d'un tableau
        
        """
        
        s = ("{}\t{}\t{}\t{}\n".format('Entité nommée', 'Type', 'Occurrences', 'Proportion'))
        
        for key in self.dataset.keys():
            s += ("{}\t{}\t{}\t{:.2%}({}/{})\n".format(key, self.dataset[key]['type'], 
                  self.dataset[key]['occurrences'], self.dataset[key]['occurrences']/self.number,
                self.dataset[key]['occurrences'], self.number))
        return s


    def export_stanford_univ_pos(self):
        file = open(self.path + self.fileName + '.pos.univ.stanford', "w")        
        file.write(self.ptbString)  
        file.close()


def main(argv):

    path = file = ''
    try:
        opts, args = getopt.getopt(argv, "hp:f:",["path", "file"])
    except getopt.GetoptError:
        print('Stanford_NLP_Core.py -p <File Path> -f <File Name>')
        sys.exit(2)
    print(opts)
    for opt, arg in opts:
        
        if opt == '-h':
            print('Lima_NLP_Core.py -p <File Path> -f <File Name> -l <Lima Path> -o <Script Output>')
            sys.exit()
        elif opt in ("-p", "--path"):
            path = arg
        elif opt in ("-f", "--file"):
            file = arg
        
    print("PARAMETERS")
    print("File Path:", path)
    print("File Name:", file)
      
    nlp_stanford = NLP_core_Stanford(path, file)
    print(nlp_stanford)
    nlp_stanford.convert_Penn_TreeBank("../../POSTags_PTB_Universal.txt")
    nlp_stanford.export_stanford_univ_pos()
    
### ==================================================================
###
###             MAIN
### ==================================================================
if __name__ == '__main__':
    main(sys.argv[1:])