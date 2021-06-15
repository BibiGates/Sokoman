'''
Implemente l'ouverture du jeu.
'''

import __init__
import pygame
import couleur
import scenario
import options

FICH_OPTIONS = 'options.txt'

def execute(surf):
    '''Execute l'ouverture.
    Argument :
        surf : -- surface de l'ecran.
    Retour :
        bool -- True si le joueur a choisi de commencer. False sinon.'''

    pygame.mouse.set_visible(False)

    image = scenario.init_dessin('images')
    pygame.mixer.music.load('musiques/switch.wav')
    pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)

    choix = 0
    terminer = False
    while not terminer:

        #Traite les evenements.
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return 2
            if event.type == pygame.KEYDOWN:
                    
                if event.key == pygame.K_DOWN and choix < 2:
                    choix += 1
                    pygame.mixer.music.play()
                if event.key == pygame.K_UP and choix > 0:
                    choix -= 1
                    pygame.mixer.music.play()

                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.load('musiques/click.wav')
                    pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
                    pygame.mixer.music.play()
                    
                    return choix

        surf.fill(couleur.FOND)

        dessine(surf, image, choix)

        pygame.display.update()

def dessine(surf, image, choix):
    '''Dessine l'ouverture.
    Argument :
        surf : -- surface de l'ecran.
    Retour :
        None.'''
    
    espace = 80
    larg_ecr = int(options.recup_options(FICH_OPTIONS)['res_x'])
    haut_ecr = int(options.recup_options(FICH_OPTIONS)['res_y'])

    #Background
    surf.blit(pygame.transform.scale(image['menu'],(larg_ecr, haut_ecr)), [0, 0])

    #Menu avec selection
    dessine_texte(surf)
    pygame.draw.rect(surf, couleur.BLANC, ((larg_ecr - 205)//2, 370 + choix*espace, 205, 50), 3)

def dessine_texte(surf):

    '''Implemente les formalites liees au projet.
    Argument :
        surf : -- surface de l'ecran.
    Retour :
        None.'''

    haut_ecr = int(options.recup_options(FICH_OPTIONS)['res_y'])

    # Titre du jeu.
    police = pygame.font.Font('polices/Titre.ttf', 100)
    texte = police.render(__init__._titre_, True, couleur.MARRON)
    surf.blit(texte, [centrer(texte), 180])

    #Jouer / Options / Quitter.
    police = pygame.font.Font('polices/Fipps.otf', 30)
    
    texte = police.render('JOUER', True, couleur.JOUER)
    surf.blit(texte, [centrer(texte), 360])

    texte = police.render('OPTIONS', True, couleur.OPTIONS)
    surf.blit(texte, [centrer(texte), 440])
    
    texte = police.render('QUITTER', True, couleur.QUITTER)
    surf.blit(texte, [centrer(texte), 520])

    # Noms des auteurs.
    police = pygame.font.SysFont('Calibri', 18)
    texte = police.render('Auteurs : Jordan HERENG et Mathilde PELLOIS.', True, couleur.BLANC)
    surf.blit(texte, [centrer(texte), 280])

    # Institution / discipline / date de creation.
    police = pygame.font.SysFont('Calibri', 12)
    
    texte = police.render('Universite d\'Artois.', True, couleur.BLANC)
    surf.blit(texte, [5, haut_ecr - 30])
    
    texte = police.render('Algorithme et programmation 1', True, couleur.BLANC)
    surf.blit(texte, [5,haut_ecr - 15])

    texte = police.render('Date : ' + __init__._date_, True, couleur.BLANC)
    surf.blit(texte, [5, 5])

def centrer(rect):
    '''Renvoie la position centree sur l'ecran pour un objet possedant les parametre d'un rectange.
    Argument :
        rect : Rect --
    Retour :
        int -- position.'''

    larg_ecr = int(options.recup_options(FICH_OPTIONS)['res_x'])
    
    return (larg_ecr - rect.get_width()) // 2























