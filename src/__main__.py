'''
Module principale du jeu.
'''

import pygame
import ouverture
import scenario
import options

FICH_NIVEAUX = 'niveaux.txt'
FICH_OPTIONS = 'options.txt'

def main():
    '''Fonction principale du programme.
    Argument : None.
    Retour : None.'''

    pygame.init()

    surface = pygame.display.set_mode((int(options.recup_options(FICH_OPTIONS)['res_x']), int(options.recup_options(FICH_OPTIONS)['res_y'])))
    pygame.display.set_caption('@ SOKOBAN @')

    sortir = False
    while not sortir:
        terminer = sortir = menus(surface)

        pygame.mixer.music.load('musiques/princ.wav')
        pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
        pygame.mixer.music.play()

        num = int(options.recup_options(FICH_OPTIONS)['act_niv_base'])
        while not terminer:

            scen = scenario.init(num, FICH_NIVEAUX)            

            action = scenario.execute(scen, num, surface)
            if action == 0:   # Quitter le jeu'
                terminer = True
                sortir = True
            elif action == 1: # Recommencer
                scen = scenario.init(num, FICH_NIVEAUX)
            elif action == 2: # Prochain niveau
                num += 1
            elif action == 3: # Retour au menu
                terminer = True
    
    pygame.quit()

def menus(surf):
    '''Gere le menu.
    Argument :
        surf : -- surface de l'ecran.
    Retour :
        bool -- True si le joueur entre dans le jeu. False s'il veut quitter.'''

    sortir_menu = False
    while not sortir_menu:
        sortir_options = False
        sortir_niveaux = False
        
        act_menu = ouverture.execute(surf)
        if act_menu == 0: # Jouer
            
            sortir_menu = True
            sortir_options = True
            
        elif act_menu == 1: # Options
            sortir_options = False
            
            while not sortir_options:
                act_opt = options.execute(surf)
                if act_opt == 0: # Ferme la fenetre
                    return True
                elif act_opt == 1: # Enregistre
                    surface = pygame.display.set_mode((int(options.recup_options(FICH_OPTIONS)['res_x']), int(options.recup_options(FICH_OPTIONS)['res_y'])))
                elif act_opt == 2: # Retour ecran titre
                    sortir_options = True
        
        elif act_menu == 2: # Quitter
            return True

    return False

main()
