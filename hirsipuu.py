import csv
import json
import random

def sananvalinta(): #arpoo sanan
    with open("sanat.csv", "r") as f:
        sanalista = f.read().splitlines()
        arvottuSana = random.choice(sanalista)
        return arvottuSana

def piirraUkko(vaarVast): #Alunperin tarkoituksena ASCII-art tyylinen hirsipuu, mutta nyt käytetään teksiä 
    numero = str(vaarVast) #esim. "6 väärää arvausta jäljellä" (Mahdollisuus laajentaa ASCII arttiin!)
    with open("ukko.json", "r") as f:
        ukot = json.load(f)
        print(ukot[numero])
        
def save(tilanne):
    with open("save.json","w") as save:
        json.dump(tilanne, save)

def kokeilin(sana, arvaus): #kokeilee, onko kirjain sanassa
    sananListaus = list(sana)
    if arvaus in sananListaus:
        return True
    else:
        return False

def checkVoitto():
    for x in pelitilanne["arvaustilanne"]:
        if x == "_":
            return False
    else:
        return True

def lataaAlusta(): #Lataa lähtötilanteen alkutilanne.json tiedostosta pelitilanne hajatustauluun
    with open("alkutilanne.json","r") as f:
            reader = json.load(f)
            for x in reader:
                pelitilanne[x]=reader[x]
    pelitilanne["theSana"] = sananvalinta()
    for x in range(len(pelitilanne["theSana"])):
        pelitilanne["arvaustilanne"].append("_")

def lataaSavesta(): #Lataa tallennetun tilan save.json tiedostosta pelitilanne hajatustauluun
    with open("save.json","r") as f:
        reader = json.load(f)
        for x in reader:
            pelitilanne[x]=reader[x]

def peli():
    print()
    if len(pelitilanne["vaaratKirjaimet"])>0: #jos arvattuja vääriä kirjaimia on, tulostaa arvatut väärät kirjaimet 
        print("Arvatut väärät kirjaimet:")
    for x in pelitilanne["vaaratKirjaimet"]:
        print(x, end=" ")
    arvaus = "aa"
    print()
    print()
    piirraUkko(pelitilanne["vaarVast"])
    print()
    print(' '.join(pelitilanne["arvaustilanne"]))
    print()
    while len(arvaus) != 1 or not(arvaus.isalpha()): #pakottaa käyttäjää syöttämään YHDEN AAKKOSEN.
        arvaus = input("Arvaa yksi kirjain (a-ö): ").lower()
    if arvaus in pelitilanne["vaaratKirjaimet"] \
        or arvaus in pelitilanne["oikeatKirjaimet"]: 
        print()
        print("Olet jo arvannut tämän kirjaimen!")
        peli()
        return False
    if kokeilin(pelitilanne["theSana"], arvaus) == True:
        print()
        print("Hienoa!")
        pelitilanne["oikeatKirjaimet"].append(arvaus)
        for i,x in enumerate(pelitilanne["theSana"]):
            if x == arvaus:
                pelitilanne["arvaustilanne"][i]=x
    else:
        print()
        print("Eipä ollu!")
        print()
        pelitilanne["vaarVast"] += 1
        pelitilanne["vaaratKirjaimet"].append(arvaus)
    if pelitilanne["vaarVast"] > 6: #tarkistaa, onko pelaajalla vuoroja jäljellä
        piirraUkko(pelitilanne["vaarVast"])
        print()
        print("Hävisit pelin!")
        print("Sana oli", pelitilanne["theSana"])
        print()
        save(pelitilanne)
        return False
    if checkVoitto():
        print("Voitit pelin!")
        print("Sana oli", pelitilanne["theSana"])
        print()
        save(pelitilanne)
        return False
    else:
        save(pelitilanne)
        peli()
        return False
    save(pelitilanne) 

def peliKoko():
    peli()
    again = input("Pelataksesi uudelleen syötä k, poistuaksesi syötä mitä tahansa: ").lower()          
    if again == "k":
        lataaAlusta()
        peliKoko()
    else:
        print()
        print("Kiitos peleistä!")
        print()
        exit()

pelitilanne = {
    "vaarVast":0,
    "vaaratKirjaimet":[],
    "theSana":"",
    "oikeatKirjaimet":[],
    "arvaustilanne":[]
}

###PELI ALKAA!!###
try:
  print()
  print("Tervetuloa pelaamaan Ninon hirsipuuta.")
  print("Peli tallentuu aina automaattisesti kun poistut.")
  print()
  lataa = input("Lataa edellisestä kerrasta syöttämällä k, lataa uusi peli syöttämällä mitä tahansa: ").lower()
  if lataa == "k":
      juttu = False
      with open("save.json","r")as f:
          reader=json.load(f)
          for x in reader["arvaustilanne"]:
              if x == "_":
                  lataaSavesta()
                  juttu = True
                  break
          if not(juttu):
              print("Voitit viimekerralla, ladataan uusi peli...") #tarkastaa, miten edellinen plei päättyi, jos voitti,
              lataaAlusta() #ilmoittaa että voitti ja lataa uuden pelin.
              save(pelitilanne)
  else:
      lataaAlusta()
      save(pelitilanne)
  if pelitilanne["vaarVast"] > 6:
      print("Hävisit viimekerralla, ladataan uusi peli...") #jos hävinnyt viimekerralla, lataa uuden pelin.
      lataaAlusta()
      save(pelitilanne)    
  peliKoko()
except:
  print("Jokin meni pieleen... käynnistä peli uudelleen!")