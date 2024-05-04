---
title: "WU Chall Base32 - THCon"
date: 2024-04-29T12:35:51+0200
tags: ["THCon","write-up","FR"]
author: clementS
draft: false
---

# Base64Custom
### Entrée : un fichier txt contenant une chaîne de charactère encodée : 
**KREEGTaOPNRDIcbFGYaFeMLTLcaHOMbTGBWWKXbJNZXGSdDd**

> Indice :[..] He said he just changed the sextets into quintuplets ? what does that even mean??

# Etape 1: comprendre comment fonctionne un encodage de string et plus particulièrement l’encodage base64
Pour représenter un string, on associe à chaque charactère, un indice. Exemple : A->0, B->1,C->3….a->27,b->28…
Les représentations les plus commune sont la bijection ASCII et UTF-8. La bijection ASCII comporte 128 charactères (A..Za..z1..9 ?/…).
 
Pour représenter un string on va écrire à la suite chaque identifiant de chaque charactère. Exemple 1 : « Aa »->0 26
Ici on veut représenter notre chaîne de charactère en utilisant ASCII (128 charactères) . On représentera donc chaque id sur 7 bits (2^7 = 128 bits).
0 26 -> 00000 11010
L’encodage en base64, permet de transférer plus facilement des données. En effet, son alphabet est [A..Za..z0..9 ?/], il ne possède donc aucun charactère spéciaux. Il prend en entrée une suite de bits, et les groupes par 6 (il complète avec des 0, à la fin si ca tombe pas juste). 
	000000 000111 000000 
	Pour avoir la représentation textuelle, on utilise l’alphabet bijection Base64. On a donc un tout autre string. Ici il devient : AHA

## Etape 2: On attaque le concret.
On sait que ici, on a pris le FLAG, on l’a mis en base 32 (groupement bits par 5, et à pris sa représentation). On doit donc faire l’étape inverse. On peut en théorie prendre n’importe quelle alphabet mais en analysant la chaîne donnée on remarque que elle est composée des caractères [A..Za..f]. 
## Etape 3 : Subtilité.
Comme on l’a préciser tout à l’heure, on peut mettre des 0 à la fin si on a pas assez de bits pour bien convertir. On regarde si il faut éventuellement retirer un bit ou en ajouter.
## Etape 4 : La dernière étape correspond a représenter les bits avec le format universelle pour représenter un texte : ASCII.

>Rq : Il faut différencier encodage base64 et ASCII

Base64 prend en entrée des bits et renvoie un chaine de charactère. C’est juste une bijection. ASCII prend en entrée une chaîne de charactère et renvoie des bits ou inversement. C’est une façon de représenter facilement un texte pour l’ordinateur.

## Résumé :
```
Flag     ------->      00101010001110     ------>   AGSHhhbsf  
       Encodage ASCII                 Bijection Base 32
On doit reverse le process :
AGSHhhbsf  ------>    00101010001110   ------->    Flag
         Bijection Base 32         Décodage ASCII
``` 
