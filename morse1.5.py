#On importe pygame et ses dépendances
import pygame     
from pygame.locals import *

#MODE DE DEMARAGE : TRUE = MORSE, FALSE = FRANCAIS
#
#
morse=True
dark=True
#
#
#MODE DE DEMARAGE : TRUE = MORSE, FALSE = FRANCAIS

#Alphabet morse et sa traduction en lettre
alphamorse=[".-","-...","-.-.","-..",".","..-.","--.","....","..",".---","-.-",".-..","--","-.","---",".--.","--.-",".-.","...","-","..-","...-",".--","-..-","-.--","--..","-----",".----","..---","...--","....-",".....","-....","--...","---..","----.",".-.-.-","--..--","..--..","-.-.--",".----.",".-..-.","-.--.","-.--.-",".-...","---...","-.-.-.","-..-.","..--.-","-...-",".-.-.","-....-","...-..-",".--.-.","/",".--.-","..-..",".","-.-.",".-",".","..","---","..-",".."]

alphabet=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","0","1","2","3","4","5","6","7","8","9",".",",","?","!",'\'',"\"","(",")","&",":",";","/","_","=","+","-","$","@"," ","À","É","È","Ç","Â","Ê","Î","Ô","Û","Ä","Ë","Ï"]

#motlist est la liste qui va stocker notre mot en morse
motlist=[]

#On initialise pygame
pygame.init()
#On donne un nom à la fenetre
pygame.display.set_caption("Projet Morse Benjamin-Leo TS")
#On défini la police et sa taille
font = pygame.font.SysFont("arial", 25, True)
#On défini la taille de la fenetre
fenetre = pygame.display.set_mode((1552, 279))

#On défini l'image de fond en fonction du theme
if dark:
    imagemorse = pygame.image.load("mfd.png").convert()
    imagefra = pygame.image.load("fmd.png").convert()
    palette=(54,54,54),(200,200,200)
else:
    imagemorse = pygame.image.load("mf.png").convert()
    imagefra = pygame.image.load("fm.png").convert()
    palette=(255,255,255),(100,100,100)

#fond remplis toute la fenètre d'un blanc
fond = pygame.Surface(fenetre.get_size()).convert()
fond.fill(palette[0])
#On place le fond
fenetre.blit(fond,(0,0))
fleche = pygame.Rect((754,21), (38,33))
#cache est un rectangle nous permettant d'actualiser la traduction
cache = pygame.Surface((730,170)).convert()
cache.fill(palette[0])
#Lors de la pression sur une touche, elle va se répeter. Permet de savoir le temps entre deux pressions
pygame.key.set_repeat(1,10)

son = pygame.mixer.Sound("bip.wav")
sonlong = pygame.mixer.Sound("biplong.wav")

clock = pygame.time.Clock()
clock.tick(60)

if morse:
    fenetre.blit(imagemorse,(0,0))
else:
    fenetre.blit(imagefra,(0,0))
#On actualise le tout
pygame.display.flip()


#tradu permet d'effectuer et d'afficher la traduction morse->mot
def tradu():
    global trait,clair,motlist,alphamorse,alphabet
    trait=[]
    clair=[]
    #boucle jusqu'à la fin du message morse
    for i in range(len(motlist)):
        #On ajoute a la liste trait tout ce qui n'est pas un espace ou un /
        if motlist[i]!=" " and motlist[i]!="/":
            trait.append(motlist[i])
        else:
            #Si on tombe sur un espace ou un / : fin de la lettre donc traitement
            #s = lettre en morse sans perturbation
            s="".join(trait)
            #Boucle de la longueur de notre alphamorse
            for j in range(len(alphamorse)):
                #Si on trouve notre lettre
                if alphamorse[j]==s:
                    #On l'ajoute à une liste clair
                    clair.append(alphabet[j])
            #Si c'est un / et non un espace, on ajoute un espace dans la liste au clair (nouveau mot)
            if motlist[i]=="/":
                clair.append(" ")
            #On nettoie la liste de traitement
            trait.clear()
    #On affiche sur la fenetre notre texte (sans perturbation)
    update_screen(1)

def update_screen(endroit):
    global cache,text,motlist,clair,textclair,texte,traduction,motliste
    if morse:
        if endroit==0:
            text = font.render(str(motlist).replace("[","").replace("]","").replace("'","").replace(",",""),1,palette[1])
            fenetre.blit(cache,(20,75))
            fenetre.blit(text, (20, 75))
        if endroit==1:
            textclair = font.render(str(clair).replace("[","").replace("]","").replace("'","").replace(",",""),1,palette[1])
            fenetre.blit(cache,(800,75))
            fenetre.blit(textclair, (800, 75))
    else:
        if endroit==0:
            text=font.render(texte,0,palette[1])
            fenetre.blit(cache,(20,75))
            fenetre.blit(text, (20, 75))
        if endroit==1:
            traduction=font.render("".join(motliste),1,palette[1])
            fenetre.blit(cache,(800,75))
            fenetre.blit(traduction, (800, 75))
    pygame.display.flip()

def makeButton(cur, rect):
    if rect.collidepoint(cur):
        chg_gamemode()

def chg_gamemode():
    global morse
    if not morse:
        fenetre.blit(imagemorse,(0,0))
        morse=True
    else:
        fenetre.blit(imagefra,(0,0))
        morse=False
    pygame.display.flip()

#Boucle infinie
end=False
while not end:
    if morse:
        #temps et temps2 nous servent à savoir la durée de pression
        temps=0
        temps2=0
        #Securite permet de quitter la boucle après avoir relaché la barre espace
        securite=False
        securite2=False
        while not securite:
            #boucle permettant l'imagemorse
            for event in pygame.event.get():
                if event.type==QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        pygame.key.set_repeat(0)
                        chg_gamemode()
                        break
                    if event.key == pygame.K_BACKSPACE:
                        pygame.key.set_repeat(0)
                        motlist.reverse()
                        s="".join(motlist)
                        #print(s)
                        for i in range(1,len(s)):
                            if s[i]=="/" or s[i]==" ":
                                motlist=list(s[:i-1:-1])
                                #print(motlist)
                                pygame.key.set_repeat(1,10)
                                update_screen(0)
                                tradu()
                                break
                        pygame.key.set_repeat(1,10)
                    if event.key == pygame.K_SPACE:
                        #Si pression sur espace, on incrémente le temps
                        temps+=1
                elif event.type == pygame.KEYUP :
                    if event.key == pygame.K_SPACE :
                        #Quand on relache, on quitte la boucle
                         securite=True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # left mouse button?
                        makeButton(event.pos, fleche)
                        if not morse:
                            securite=True
            if not morse:
                break
        if morse:
            #On regarde la durée de la pression et on ajoute un point ou un trait en fonction de celle ci
            if temps>15:
                #print("-")
                sonlong.play()
                motlist.append("-")
            else:
                #print(".")
                son.play()
                motlist.append(".")
            #On affiche sur la fenetre le message en morse
            pygame.time.delay(100)
            update_screen(0)
            #On vient de relacher la barre espace, on rentre dans une autre boucle
            while not securite2:
                for event in pygame.event.get():
                    if event.type==QUIT:
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_TAB:
                            pygame.key.set_repeat(0)
                            chg_gamemode()
                            break
                        if event.key == pygame.K_SPACE:
                            securite2=True
                #On incrémente un autre temps (durée de non pression)
                temps2+=1
                #Si le temps est vraiment haut, on passe (permet d'afficher le texte traduit plus vite)
                if temps2>100001:
                    break
                if not morse:
                    break
            if not morse:
                break
            #Action en fonction du temps de non pression (nouvelle lettre ou nouveau mot)
            if temps2>40000 and temps2<100000:
                #print("newletter")
                motlist.append(" ")
            elif temps2>=93000:
                #print("newword")
                motlist.append("/")
            #On reset la traduction
            #On retraduit (réaffichage compris)
            tradu()
    elif not morse:
        pygame.key.set_repeat(1,10)
        continuer=True
        texte=""
        textz=""
        while continuer:
            for event in pygame.event.get():
                if event.type==QUIT:
                    exit()
                elif event.type==KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        pygame.key.set_repeat(0)
                        texte=texte[0:len(texte)-1]
                        motliste=motliste[0:len(motliste)-1]
                        update_screen(0)
                        update_screen(1)
                        pygame.key.set_repeat(1,10)
                    elif event.key == pygame.K_TAB:
                        pygame.key.set_repeat(0)
                        chg_gamemode()
                        motlist=[]
                        pygame.key.set_repeat(1,10)
                        break
                    elif event.key == pygame.K_LALT and texte!="":
                        pygame.key.set_repeat(0)
                        for i in range(len("".join(motliste))):
                            if "".join(motliste)[i]==".":
                                son.play()
                                pygame.time.delay(200)
                            elif "".join(motliste)[i]=="-":
                                sonlong.play()
                                pygame.time.delay(400)
                            elif "".join(motliste)[i]==" ":
                                pygame.time.delay(450)
                            elif "".join(motliste)[i]=="/":
                                pygame.time.delay(500)
                            textz+="".join(motliste)[i]
                            traduction=font.render(textz,1,(250,20,0))
                            fenetre.blit(traduction,(800,75))
                            pygame.display.flip()
                        textz=""
                        update_screen(1)
                    else:
                        pygame.key.set_repeat(0)
                        texte+=event.unicode.upper()
                        text=font.render(texte,0,palette[1])
                        fenetre.blit(text,(20,75))
                        motliste=[]
                        for j in range(len(list(texte))):
                            for i in range(len(alphabet)):
                                if alphabet[i]==list(texte)[j]:
                                    motliste.append(alphamorse[i]+" ")
                        traduction=font.render("".join(motliste),1,palette[1])
                        fenetre.blit(traduction,(800,75))
                        pygame.display.flip()
                        update_screen(1)
                        pygame.key.set_repeat(1,10)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # left mouse button?
                        makeButton(event.pos, fleche)
                        if morse:
                            motlist=[]
                            break
            if morse:
                break
