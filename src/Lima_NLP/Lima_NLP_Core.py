# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 14:06:49 2018

Partie relative à Lima du projet d'EIT d'ET5 INFO | POLYTECH PARIS-SUD 2019.

-- First published on git/anthwozn

Toute réutilisation du programme ci dessous requiert la mention de ses auteurs
dans l'en-tête du fichier.

@authors: BRINDAMOUR B., AZEMARD T. WOZNICA A.
"""


from lxml import etree
import string
import sys, getopt

class NLP_core_Lima:
    """
    Classe qui rassemble les fonctions de tokénisation, d'analyse et de labellisation des
    textes sous Lima.
    
    Chaque méthode est commentée.
    """
    
    
    def __init__(self, path, file, limaPath, generatedFolder = "Generated"):
        """
        Initialise la classe et génère un dictionnaire contenant les entrées nommées.
        
        Pour l'initialisation, on demande à connaître le chemin du fichier à charger,
        son nom, les fichiers générés par Lima ainsi que l'emplacement de sauvegarde
        des fichiers générés par ce script.
        """
        
        # Initialisation des variables relatives au texte
        self.file = file
        self.limaPath = limaPath
        self.generatedFolder = generatedFolder
        self.path = path
        
        # Création du dictionnaire d'entités nommées
        self.dataset = dict()

        # Parsage du document contenant les entités nommées
        tree_ = etree.parse(limaPath + file+'.se.xml')
        t_path_ = tree_.xpath("/specific_entities/specific_entity")
        self.size_ = len(t_path_) 
        # Parcours des noeuds du XML
        for node_ in t_path_:
            id_ = str(node_[0].text)
            
            #Si l'entité nommée n'est pas déjà dans le dictionnaire
            if(id_ not in self.dataset.keys()):
                self.dataset[str(node_[0].text)] = {
                   node_[0].tag : set([str(node_[0].text)]),
                   node_[3].tag : node_[3].text.split('.')[1],
                   node_[2].tag: int(node_[2].text),
                   node_[1].tag: int(node_[1].text),
                   "occurrences" : 1,
                   "proportion" : 1/self.size_,  # /!\ On recalcule à chaque fois la proportion !
                   "drop": False
                }
                
            else:
                self.dataset[id_]["occurrences"] += 1
                self.dataset[id_]["proportion"] = self.dataset[id_]["occurrences"]/self.size_


        # On merge à présent les éléments redondants.
        # Par exemple, on considère que Boca et Boca Raton font tous deux référence
        # à Boca Raton.
        for word_ in self.dataset.keys():
            for sub_ in self.dataset.keys():
                if(sub_ in word_ and self.dataset[sub_]["drop"] == False and len(sub_) < len(word_)):
                    index = word_.find(sub_)
                    if(self.dataset[sub_][node_[1].tag] - index >= self.dataset[sub_][node_[2].tag] \
                        or self.dataset[sub_]['type'] == self.dataset[sub_]['type']):
                            self.dataset[word_][node_[0].tag].update(self.dataset[sub_][node_[0].tag])
                            self.dataset[word_]["occurrences"] += self.dataset[sub_]["occurrences"]
                            self.dataset[word_]["proportion"]  += self.dataset[sub_]["proportion"]
                            self.dataset[sub_]["drop"] = True
                        
        # Retrait des éléments redondants
        switchset_ = {k:v for k, v in self.dataset.items() if not v["drop"]}
        self.dataset = switchset_
        
        # Mise en forme des données 
        for word_ in self.dataset.keys():
            self.dataset[word_]['string'] = list(self.dataset[word_]['string'])
            self.dataset[word_]['string'].sort(key = len, reverse = True)
            
        
        
        

    def morpho_syntaxic_analysis(self):
        """
        Effectue l'analyse morpho-syntaxique du texte chargé précédemment
        à partir du fichier disambiguated.xml généré par Lima.
        
        On crée une liste d'entités du type:
        [[MOT, ETIQUETTE, ETIQUETTE2], [MOT, ETIQUETTE, ETIQUETTE2]...]
        """
        tree_ = etree.parse(self.limaPath + self.file + '.disambiguated.xml')
        self.analyzer = []
        
        for lemma_ in tree_.xpath("/vertices/vertex"):
             entity = []
             for node in lemma_.getchildren():
                 if(node.text != None):
                     entity.append(node.text.upper())
             self.analyzer.append(entity)
        
        
        
    def morpho_syntaxic_analysis2(self):
        """
        Effectue l'analyse morpho-syntaxique du texte chargé précédemment
        à partir du fichier furnished.disambiguated.xml généré par Lima.
        Ce dernier dispose immédiatement d'étiquettes Penn TreeBank.
        
        On crée une liste d'entités du type:
        [[MOT, ETIQUETTE, ETIQUETTE2], [MOT, ETIQUETTE, ETIQUETTE2]...]
        """
        tree_ = etree.parse(self.limaPath + self.file + '.furnished.disambiguated.xml')
        self.analyzer = []
        
        for lemma_ in tree_.xpath("/vertices/vertex"):
             entity = []
             for node in lemma_.getchildren():
                 if(node.text != None):
                     entity.append(node.text.upper())
             self.analyzer.append(entity)


        
    def morpho_syntaxic_labels(self):
        """
        Chargement des labels du texte à partir du fichier .conll
        """
        
        loader_ = open(self.limaPath + self.file + '.conll', 'r')
        self.labels = {};
        for line in loader_.readlines():
            if(line.strip() != ''):
                entry_ = line.split('\t')
                self.labels[entry_[1].upper()] = {
                    'normal_form': entry_[2].upper(),
                    'label1': entry_[3],
                    'label2': entry_[4],
                    'type': entry_[5],
                    'subtype': entry_[6],
                    'num': entry_[7],
                    'form': entry_[8]
                }
                
                
        
    def labelize(self, string_):
        """
        Etiquettage du texte à partir des étiquettes précédemment chargée.
        
        La fonction présente effectue l'étiquettage à partie du fichier .conll généré
        par Lima.
        """
        
        # On normalise la chaîne de caractères
        self.output = string_.upper()
        
        # On espace la ponctuation afin de ne pas empêcher la reconnaissance de certains termes
        for i_ in string.punctuation:
            self.output = self.output.replace(i_, ' '+i_)
        
        self.output = ' ' + ' '.join(self.output.split()) + ' '
        
        # On trie les étiquettes suivant la longueur !
        # On cherche en premier temps à mettre les étiquettes les plus longues,
        # Car cela permet entre autres de se débarasser d'éventuelles ambiguïtés
        # sur des mots composés.
        # Exemple, si on a JET OFF dans le texte, mais également le mot JET,
        # il sera préférable d'étiquetter JET OFF en premier et ainsi ne pas
        # étiquetter JET !
        l = list(self.labels.keys())
        l.sort(key = len, reverse = True)
        
        # Remplacement des labels
        for key in l:
            self.output = self.output.replace(' ' + key + ' ', ' ' + key + '_' + self.labels[key]['label2'] + ' ')
            
        self.output = self.output.lstrip()
        print("LIMA STRING ->\n\n", self.output)
      
      
      
    def convert_Penn_TreeBank(self, banksource, isRef = False):
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
        
        # Chargement de .pos.lima
        if(not isRef):
            file = open(self.generatedFolder + self.file + '.pos.lima', "r")
            s = file.read()
            file.close()
        else:
            file = open(self.path + self.file + '.pos.ref', "r")
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
        d_ = self.dataset    
        
        out = ("{}\t{}\t{}\t{}\n".format("Entite Nommee", "Type", "Nombre d'occurrences", "Proportion"))
         
        for value_ in d_.values():
            out += ("{}\t{}\t{}\t{:.2%}({}/{})\n".format(
                                    value_["string"], value_["type"],
                                    value_["occurrences"], value_["occurrences"]/self.size_,
                                    value_["occurrences"], self.size_))            
        
        return out
        
        
        
    ### ===================================================================
    ###
    ###             FONCTION D'EXPORT DE DONNEES
    ### ===================================================================
    def export(self):
        file = open(self.generatedFolder + self.file + '.ner.lima', "w")        
        file.write(str(self))    
        file.close()


    def export_lima_pos(self):
        file = open(self.generatedFolder + self.file + '.pos.lima', "w")        
        file.write(self.output)  
        file.close()
        
    def export_lima_univ_pos(self, isRef = False):
        if(not isRef):
            file = open(self.generatedFolder + self.file + '.pos.univ.lima', "w")        
            file.write(self.ptbString)  
            file.close()
        else:
            file = open(self.path + self.file + '.pos.univ.ref', "w")        
            file.write(self.ptbString)  
            file.close()
    


def main(argv):

    path = file = limaPath = generatedFolder = ''
    try:
        opts, args = getopt.getopt(argv, "hp:f:l:o:",["path", "file", "lima", "output"])
    except getopt.GetoptError:
        print('Lima_NLP_Core.py -p <File Path> -f <File Name> -l <Lima Path> -o <Script Output>')
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
        elif opt in ("-l", "--lima"):
            limaPath = arg
        elif opt in ("-o", "--output"):
            generatedFolder = arg
        
    print("PARAMETERS")
    print("File Path:", path)
    print("File Name:", file)
    print("Lima Path:", limaPath)
    print("Script Output:", generatedFolder)
    
    #lima_ner = NLP_core_Lima("../Files/", "wsj_0010_sample.txt", '../Files/Lima/', 'Generated/')
    lima_ner = NLP_core_Lima(path, file, limaPath, generatedFolder)    
    print(lima_ner)
    
    # Exporte au format .ner.lima
    lima_ner.export()
    
    # Charge le fichier .disambiguated.xml
    lima_ner.morpho_syntaxic_analysis()
    
    #Charge le fichier .conll
    lima_ner.morpho_syntaxic_labels()
    
    # Phrase pour laquelle on a une référence.
    #s = "When it's time for their biannual powwow, the nation's manufacturing titans typically \
    #    jet off to the sunny confines of resort towns like Boca Raton and Hot Springs."
    
    s = open(path + file, 'r').read()
    lima_ner.labelize(s)
    
    lima_ner.export_lima_pos()

    lima_ner.convert_Penn_TreeBank("../../POSTags_PTB_Universal.txt")
    lima_ner.export_lima_univ_pos()
    
    lima_ner.convert_Penn_TreeBank("../../POSTags_PTB_Universal.txt", True)
    lima_ner.export_lima_univ_pos(True)
    

### ==================================================================
###
###             MAIN
### ==================================================================
if __name__ == '__main__':
    
    main(sys.argv[1:])
    
    