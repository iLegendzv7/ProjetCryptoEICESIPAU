from sys import argv
from collections import Counter
from tkinter import *
import tkinter as tk
from tkinter import filedialog as fd
import binascii

#Fonction pour récupérer le fichier à déchiffrer
def nomFichier():
    filename = fd.askopenfilename()
    print(filename)
    crypto(filename)
    
# Affichage du menu
def window():
    fenetre = Tk()

    fenetre.geometry('1000x600') 

    label = Label(fenetre, text="Hello World")
    label.pack()
    
    bouton1=Button(fenetre, text="Fermer", width = 15, height = 10, command=fenetre.quit)
    bouton1.pack(side = "left")

    bouton2 =Button(fenetre, text="Ouvrir",  width = 15, height = 10, command=nomFichier)
    bouton2.pack(side = "right")    
    fenetre.mainloop()
    
# Affichage des résultats
def window2(totalFind, key, texteClair):
    fenetre = tk.Tk()

    fenetre.geometry('1450x900') 
        
    label = Label(fenetre, text="Il y a " + str(totalFind) + " mots français")
    label.pack()
    
    label = Label(fenetre, text="Voici un extrait du texte déchiffré\n" + texteClair)
    label.pack()
    
    label = Label(fenetre, text="La clé est " + str(key))
    label.pack()
    
    bouton=Button(fenetre, text="Fermer", command=fenetre.quit)
    bouton.pack()
    
    fenetre.mainloop()

#Fonction pour trouver la bonne clé
def findXorKey(text, key_len, most_common_byte=32):
    key = bytearray([0] * key_len)
    for st_idx in range(key_len):
        keyspace_text = []
        for idx in range(st_idx, len(text), key_len):
            keyspace_text.append(text[idx])
        most_common_found = Counter(keyspace_text).most_common(1)[0][0]
        key[st_idx] = most_common_byte ^ most_common_found
    return key

#Fonction pour déchiffrer le document
def decrypt(bytearr, key):
    output = bytearray()
    for i in range(len(bytearr)):
        output.append(bytearr[i] ^ key[i % len(key)])
    return output

keylen        = None
key           = None
do_decrypt    = False
    
def  crypto(filename):   
    
    source_text = open(filename, 'rb').read()
    keylen = 6
    
    #Trouve la clé
    if keylen:
        key = findXorKey(source_text, keylen)
        print("Found a key:", key.decode("utf-8"))
        textLower = decrypt(source_text[:20000], key).lower().decode("latin-1")
        
    #Déchiffre le document à l'aide de la clé
    if do_decrypt:
        with open(output_file, 'wb') as fout: fout.write(decrypt(source_text, key))
        fout.close()
        
    francais(textLower, source_text, key)

#Vérification de l'existance de mot en rfrançais
def francais(textLower, source_text, key):
    fichier = open("liste_francais2.txt", "r", encoding='latin-1')

    var = fichier.read().split(", ")

    word = ["de", "le", "faeqsdv", "putezez", 'pute']
    str = "Welcome to WayToLearn."
    find = 0
    temp = 0
    # Vérifier si des mots se trouve dans le dictionnaire
    for x in var:
        if x in textLower:
            find = find +1
            if find == 10:
                print("Decrypted text sample:", decrypt(source_text[:200], key).decode("latin-1"))

            else:
                temp = temp + 1
    totalFind = find
    print ("Nombre de mot Français trouvé ")
    print (totalFind)
    
    texteClair = decrypt(source_text[:2000], key).decode("latin-1")
    key = key.decode("latin-1")
    
    window2(totalFind, key, texteClair)
            
window()
