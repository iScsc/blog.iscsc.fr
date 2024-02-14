---
title: "Write-up de "A l'envers" - FSCS 2022"
date: 2024-14-02
draft: false
tags: ["write-up","FCSC","programming","pwntools"]
---

> on peut retrouver ce challenge sur [Hacropole](https://hackropole.fr/fr/challenges/misc/fcsc2022-misc-a-l-envers/)

## Première idée
Le programme contenu dans le docker nous envoie des mots un par un. Le challenge consiste à lui renvoyer les mots en les inversants. Ma première idée consiste à faire simplement un script pyhton qui renvoie le mot retourné. Mais problème : comment intérargir avec le challenge, ie récupérer les mots qu'il envoie et lui retourner les mots inversés ? En effet, une simple pipe ne suffit pas puisqu'il faut lire plusieurs fois ce qu'envoie le challenge et à chaque fois lui envoyer une réponse.

## Pwntools
Pour résoudre ce problème, on utilise la librairie python Pwntools. Pour commencer, on set la target (le docker) avec la fonction `remote` : `target = remote("localhost", 4000)`
Ensuite, on veut récupérer ce qu'envoie la target, l'inverser puis le renvoyer. Tout ceci est possible avec les méthodes suivantes:
`target.recvuntil(bstr)` `target.recvline()`  `target.sendline()`
On commence donc par demander au script d'attendre tant que on n'a pas une ligne du style `>>> txt` avec `target.recvuntil(b">>>")` : on se contente de lire ce qu'il y a après les chevrons, et on ajoute un _b_ pour préciser qu'il s'agit d'un bytestring et non d'un string qu'on souhaite lire.

## Premier problème
Les deux dernières méthodes ne renvoient / prennent pas un string, mais un bytestring. Voici ce qui est renvoyé par la première méthode :
`b' ANSSI\n'`
_On remarque qu'on a bien récupéré seulement ce qui suivait les chevrons_. Dans l'état, on ne peut pas en faire grand chose. On note aussi qu'il faut se débarasser des caractères superflus. Pour convertir un bytestring en string, il faut le décoder avec la méthode : `.decode("utf-8")` (ou un autre type d'encodage bien évidemment). De même, on passe d'un string à un bytestring avec la fonction `bytes(str,str encoding)`. On sait donc maintenant passer de l'un à l'autre, et donc notre scipt ressemble désormais à ça :

```py
from pwn import *

target = remote("localhost",4000)

target.recvuntil(b">>>")
bytestring = target.recvline()
string = bytestring.decode("utf-8")
string = string[:-1:-1]
bstr = bytes(string,'utf-8')
target.sendline(bstr)
```

Plus qu'à rajouter une petite boucle `While True:` et on est bon ! Ou presque ...

## Deuxième problème
En effet, le programme renvoie désormais une erreur lorsqu'on l'execute. Elle est dûe au `recvuntil(b">>>")`. Lorsque le docker envoie le flag (à la fin de l'execution du docker), la ligne ne commence pas par des chevrons. On va donc feinter en utilisant la méthode `target.interactive()` qui permet de redonner la main au terminal lors de l'execution du script, et ce en catchant l'erreur, afin d'arrêter le script. On rajoute donc au début de la boucle 

```py
try:      
    target.recvuntil(b">>> ")
except:
    target.interactive()
```


Et voilà ! 

## Programme final
```py
from pwn import *

target = remote("localhost",4000)

while True:
    try:      
        target.recvuntil(b">>> ")
    except:
        target.interactive()
    bytestring = target.recvline()
    string = bytestring.decode("utf-8")
    string = string[:len(string)-1]
    string = string[::-1]
    bstr = bytes(string,'utf-8')

    target.sendline(bstr)
```