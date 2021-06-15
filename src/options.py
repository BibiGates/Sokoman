'''
Implemente le menu des options.
'''

import pygame
import couleur
import ouverture
import scenario
import scores

RES_POSS = [(900, 675),
            (1000, 750),
            (1050, 788),
            (1100, 825)]

OPTIONS = 4
FICH_OPTIONS = 'options.txt'

def execute(surf):
    '''Execute le menu des options.
    Argument :
        surf : -- surface de l'ecran
    Retour :
        0 -- si le joueur quitte
        1 -- si le joueur applique les changements
        2 -- si le joueur souhaite retourner a l'ecran titre'''

    pygame.mixer.music.load('musiques/switch2.wav')
    pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)

    choix = 0
    choix_res = int(recup_options(FICH_OPTIONS)['index_act_res'])
    choix_niv = int(recup_options(FICH_OPTIONS)['act_niv_base'])
    terminer = False
    while not terminer:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return 0
            
            if event.type == pygame.KEYDOWN:
            
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.load('musiques/click.wav')
                    pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
                    pygame.mixer.music.play()
                    return 2

                if event.key == pygame.K_UP and choix > 0:
                    choix -= 1
                    pygame.mixer.music.play()
                if event.key == pygame.K_DOWN and choix < OPTIONS - 1:
                    choix += 1
                    pygame.mixer.music.play()

                if choix == 0:
                    
                    if event.key == pygame.K_RIGHT and choix_res < len(RES_POSS) - 1:
                        choix_res += 1
                        pygame.mixer.music.play()
                    if event.key == pygame.K_LEFT and choix_res > 0:
                        choix_res -= 1
                        pygame.mixer.music.play()

                elif choix == 1:
                    
                    if event.key == pygame.K_RIGHT and choix_niv < int(recup_options(FICH_OPTIONS)['nb_niv']) - 1:
                        choix_niv += 1
                        pygame.mixer.music.play()
                    if event.key == pygame.K_LEFT and choix_niv > 0:
                        choix_niv -= 1
                        pygame.mixer.music.play()
 

                elif event.key == pygame.K_RETURN:

                    if choix == 2 or choix == 3:
                        
                        if choix == 2:
                            pygame.mixer.music.play()
                            scores.init_fich_score(int(recup_options(FICH_OPTIONS)['nb_niv']), 'scores.txt')

                        elif choix == 3:
                            pygame.mixer.music.play()
                            modif_option(FICH_OPTIONS, 'res_x', RES_POSS[choix_res][0])
                            modif_option(FICH_OPTIONS, 'res_y', RES_POSS[choix_res][1])
                            modif_option(FICH_OPTIONS, 'index_act_res', choix_res)
                            modif_option(FICH_OPTIONS, 'act_niv_base', choix_niv)
                            return 1

        surf.fill(couleur.FOND)

        dessine(surf, choix, choix_res, choix_niv)

        pygame.display.update()

def dessine(surf, choix, choix_res, choix_niv):
    '''Dessine le menu des options.
    Arguments :
        surf : -- surface de l'ecran
        choix_res : int -- index du choix
    Retour :
        None'''

    larg_ecr = int(recup_options(FICH_OPTIONS)['res_x'])
    haut_ecr = int(recup_options(FICH_OPTIONS)['res_y'])
    
    surf.blit(pygame.transform.scale(scenario.init_dessin('images')['option'], (larg_ecr, haut_ecr)), [0,0])

    #'Options'
    police = pygame.font.Font('polices/Fipps.otf', 32)
    texte = police.render('Options :', True, couleur.JOUER)
    surf.blit(texte, [20, 20])

    #Liste des resolutions
    police = pygame.font.Font('polices/Fipps.otf', 20)
    
    res_texte = ''
    if choix_res == 0:
        res_texte = '  Resolution : ' + str(RES_POSS[choix_res][0]) + 'x' + str(RES_POSS[choix_res][1]) + ' >'
    elif choix_res == len(RES_POSS) - 1:
        res_texte = '< Resolution : ' + str(RES_POSS[choix_res][0]) + 'x' + str(RES_POSS[choix_res][1]) + '  '
    else:
        res_texte = '< Resolution : ' + str(RES_POSS[choix_res][0]) + 'x' + str(RES_POSS[choix_res][1]) + ' >'
    
    texte = police.render(res_texte, True, couleur.NOIR)
    surf.blit(texte, [ouverture.centrer(texte), 200])

    #Liste des niveaux
    niv_texte = ''
    if int(recup_options(FICH_OPTIONS)['nb_niv']) != 1:
        if choix_niv == 0:
            niv_texte = '  Niveau : ' + str(choix_niv) + ' >'
        elif choix_niv == int(recup_options(FICH_OPTIONS)['nb_niv']) - 1:
            niv_texte = '< Niveau : ' + str(choix_niv) + '  '
        else:
            niv_texte = '< Niveau : ' + str(choix_niv) + ' >'
    else:
        niv_texte = '  Niveau : ' + str(choix_niv) + '  '

    texte = police.render(niv_texte, True, couleur.NOIR)
    surf.blit(texte, [ouverture.centrer(texte), 250])

    #'Reinitialiser les scores'
    texte = police.render('Reinitialiser les scores', True, couleur.NOIR)
    surf.blit(texte, [ouverture.centrer(texte), 300])

    #'Appliquer le changement'
    texte = police.render('Appliquer les changements', True, couleur.NOIR)
    surf.blit(texte, [ouverture.centrer(texte), 350])

    #Selection
    pygame.draw.line(surf, couleur.NOIR, (larg_ecr//2 - 100, 240 + choix*50),(larg_ecr//2 + 100, 240 + choix*50), 2)

    #'< Retour [ESC]'
    police = pygame.font.Font('polices/Fipps.otf', 16)
    texte = police.render('< Retour [ESC]', True, couleur.JOUER)
    surf.blit(texte, [10, haut_ecr - 35])

    # Indicateur de changement
    c_indic = couleur.VERT
    
    if choix_res != int(recup_options(FICH_OPTIONS)['index_act_res']) or choix_niv != int(recup_options(FICH_OPTIONS)['act_niv_base']):
        c_indic = couleur.ROUGE

    pygame.draw.circle(surf, c_indic, [larg_ecr - 45, haut_ecr - 45], 15)

def recup_options(path):
    '''Renvoie un dictionnaire de parametres initialement presents dans un fichier texte.
    Argument :
        path : str -- chemin du fichier des options
    Retour :
        dict -- parametres'''

    dict_options = {}
    fich = open(path, 'r')
    ligne = fich.readline()
    
    while ligne != '': #Tant que ce n'est pas la fin du fichier:
        
        # Attribut au dictionnaire un attribut nomme dans le fichier
        # et lui attribut la valeur correspondante:
        dict_options[ligne.split(':')[0]] = ligne.split(':')[1]
        ligne = fich.readline()

    fich.close()
    return dict_options

def modif_option(path, nom_par, par):
    '''S'il existe, modifie un parametre dans le fichier des options. Sinon, il est cree.
    Arguments :
        path : str -- chemin du fichier des options
        nom_par : str -- nom du parametre
        par : obj -- valeur du parametre
    Retour :
        None.'''

    fich = open(path, 'r') #Lecture

    liste_noms = []
    liste_pars = []

    ligne = fich.readline()
    while ligne != '':

        liste_noms += [ligne.split(':')[0].strip()] #Ajoute tous les noms de parametres dans cette liste
        liste_pars += [ligne.split(':')[1].strip()] #Ajoute toutes les valeurs correspondantes

        ligne = fich.readline()
    fich.close()

    fich = open(path, 'w') #Reecriture
    if nom_par in liste_noms: # Si le parametre existe deja :
        for i in range(len(liste_noms)):
            
            # Ecrit la ligne de ce parametre avec la nouvelle valeur
            if nom_par == liste_noms[i]:
                fich.write(nom_par + ':' + str(par))
            else:
                fich.write(liste_noms[i] + ':' + liste_pars[i])
            fich.write('\n')
            
    else:

        # Reecrit tous les parametres
        for i in range(len(liste_noms)):
            fich.write(liste_noms[i] + ':' + liste_pars[i] + '\n')

        # et ajoute la derniere
        fich.write(nom_par + ':' + str(par))
    fich.close()
            



        








