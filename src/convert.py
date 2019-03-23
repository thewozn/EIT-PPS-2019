# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 14:06:49 2018

Partie relative à l'évaluation d'entités nommées du projet d'EIT d'ET5 INFO | 
POLYTECH PARIS-SUD 2019.

-- First published on git/anthwozn

Toute réutilisation du programme ci dessous requiert la mention de l'auteur
dans l'en-tête du fichier.

@author: WOZNICA A.
"""


import copy, string
import Lima_NLP.Lima_NLP_Core as Lima
import Stanford_NLP.Stanford_NLP_Core as Stanford
import re
    

# Localisation des fichiers de test
test_folder     = '../Files/format-tst/'
lima_file       = 'formal-tst.NE.key.04oct95_small.txt'
lima_sources    = '../Files/format-tst/'
lima_output     = '../Files/format-tst/'
stanford_file   = 'formal-tst.NE.key.04oct95_small'

    

def LIMA_transform_NER():
    """
    Conversion d'un set d'étiquettes Lima en Stanford.
    /!\ NON UTILISE DANS LE PROGRAMME
    """
    new_dict = {}
    
    for item in lima_ner.dataset.items():
        new_keys = item[0].split(' ')
        for key in new_keys:
            new_dict[key] = lima_ner.dataset[item[0]]['type']
    
    print(new_dict)
    return new_dict
    
    
    
def LIMA_transform_NER_from_string(text, ner_dict):
    """
    Transforme les entités nommées de Lima de la forme:
    Boca Raton_LOCATION
    
    En:
    Boca_LOCATION Raton_LOCATION
    
    Cela au sein d'un texte fourni en argument.    
    
    La méthode mise en oeuvre consiste à créer une copie du dictionnaire
    contenant non plus les entités nommées mais les entités nommées étiquetées.
    
    Ainsi, si on a [Boca Raton] dans ner_dict, on aura [Boca_LOCATION Raton_LOCATION] dans nn
    
    Cette méthode permet très simplement de modifier de grands segments de texte, puisqu'il
    suffira de remplacer les valeurs de ner_dict par celles de nn dans le texte, les méthodes
    d'accès étant les mêmes pour les deux dictionnaires.
    """
    
    
    nn = copy.deepcopy(ner_dict) # Copie modifiable
    
    # Remplacement des mots du dictionnaire copié par des couples mots_étiquettes
    for key in nn:
        # Rappel: le tableau string est trié par ordre de longueur décroissant !
        nn[key]["string"] = list(nn[key]["string"])
        for i in range(0, len(nn[key]["string"])):
            if(nn[key]['type'] in ['ORGANIZATION', 'PERSON', 'LOCATION']):
                nn[key]["string"][i] = nn[key]["string"][i].replace(' ', '_' + nn[key]['type'] + ' ') + '_' + nn[key]['type']
                
    # Remplacement des éléments du dictionnaire détéctés dans le texte
    # Par ceux du dictionnaire copié !
    for key in ner_dict:
        for i in range(0, len(ner_dict[key]['string'])):
            text = text.replace(' ' + ner_dict[key]['string'][i] + ' ', ' ' + nn[key]['string'][i] + ' ')
            for i_ in string.punctuation:   # Gestion des ponctuations
                if(i_ != '_'):
                    text = text.replace(' ' + ner_dict[key]['string'][i] + i_, ' ' + nn[key]['string'][i] + i_)

    for i_ in string.punctuation:
                if(i_ != '_'):
                    text = text.replace(i_, i_ + ' ')
    return text



def STANFORD_transform_NER():
    """
    Conversion d'un set d'étiquettes Stanford en Lima.
    /!\ NON UTILISE DANS LE PROGRAMME
    """
    new_dict = {}
    for item in stanford_ner.dataset.items():
        new_keys = item[0].split(' ')
        for key in new_keys:
            new_dict[key] = stanford_ner.dataset[item[0]]['type']
    
    return new_dict
    
    
def STANFORD_transform_NER_from_string(text, ner_dict):
    """
    Méthode analogue à son équivalent Lima.
    -- Etiquettage d'un texte
    """

    for key in ner_dict.keys():
        if(ner_dict[key]['type'] in ['ORGANIZATION', 'PERSON', 'LOCATION']):
            replacement = ('_' + ner_dict[key]['type'] + ' ').join(key.split(' ')) + '_' + ner_dict[key]['type']
            text = text.replace(' ' + key + ' ',
                                ' ' + replacement + ' ')
            for i_ in string.punctuation:
                if(i_ != '_'):
                    text = text.replace(' ' + key + i_,
                                ' ' + replacement + i_)
                      
    return text
    
    
    
### ==================================================================
###
###             MAIN
### ==================================================================
if __name__ == '__main__':
    
    # Traitement du texte avec CEA List
    f = open(test_folder + lima_file)
    s = f.read()
    f.close()
        
    lima_ner = Lima.NLP_core_Lima(test_folder, lima_file, lima_sources, lima_output)
    lima_result = LIMA_transform_NER_from_string(s, lima_ner.dataset)
    
    f = open("NE.txt.lima.out", "w")
    while('\n' in lima_result):
        lima_result = lima_result.replace('\n', '')
        lima_result = lima_result.replace('  ', ' ')
    for i_ in string.punctuation:
        if(i_ not in ['_', '(']):
            lima_result = lima_result.replace(' '+ i_, i_)
    f.write(lima_result.upper())
    f.close()
    
    
    # Traitement du texte Stanford NER
    stanford_ner = Stanford.NLP_core_Stanford(test_folder, stanford_file)
    stanford_result = STANFORD_transform_NER_from_string(s, stanford_ner.dataset)
    
    f = open("NE.txt.stanford.out", "w")
    f.write(stanford_result.replace('\n', '').upper())
    f.close()
    
    f = open(test_folder + "formal-tst.NE.key.04oct95_small.ne")
    reference = f.read()
    f.close()
    

    # Traitement des entités nommées du texte de référence à l'aide d'un Regex
    balises = re.findall(r'(<E(.*?)</ENAMEX>)', reference)
    for balise in balises:
        
        sequence = re.findall(r'(>(.*?)</ENAMEX>)', balise[0])[0][1]
        type_seq = re.findall(r'(\"(.*?)\")', balise[0])[0][1]
        
        tokens = sequence.lstrip().split(' ')
        tokens = ('_' + type_seq + ' ').join(tokens) + '_' + type_seq + ' '
        
        reference = reference.replace(balise[0], tokens)

    balises = re.findall(r'(<T(.*?)</TIMEX>)', reference)
    for balise in balises:
        sequence = re.findall(r'(>(.*?)</TIMEX>)', balise[0])[0][1]
        reference = reference.replace(balise[0], sequence)
        
        balises = re.findall(r'(<N(.*?)</NUMEX>)', reference)
    for balise in balises:
        sequence = re.findall(r'(>(.*?)</NUMEX>)', balise[0])[0][1]
        reference = reference.replace(balise[0], sequence)
        
    reference = reference.replace('  ', ' ')
    for i_ in string.punctuation:
        if(i_ not in ['_', '(']):
            reference = reference.replace(' '+ i_, i_)
    f = open("NE.txt.ref.out", "w")
    f.write(reference.replace('\n', '').upper())
    f.close()

    print("Test done.")
    

    



