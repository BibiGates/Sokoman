'''
Implemente les differents niveaux.
'''

import pygame
import couleur
import options
import avatar
import caisse
import ouverture
import scores

T_GRILLE = 30
FICH_OPTIONS = 'options.txt'

def init(num, path):
    '''Initialise les attributs du scenario.
    Arguments :
        num : int -- index du niveau.
        path : str -- chemin du fichier contenant les niveaux.
        l : int -- index de ligne.
        c : int -- index de colonne.
        d : int -- direction.
    Retour :
        dict -- attributs.'''

    # Ici, les attributs s'initialisent apres etre entre dans le jeu. Probleme pour les options
    # (en particulier le nombre de niveaux)
    # Donc, quand on souhaite ajouter un niveau, il faut :
        # - Reinitialiser les scores dans les options
        # - Modifier manuellement le nombre de niveau dans le fichier options.txt
    # (Pas le temps de regler ce probleme de taille).

    grille = grilles(path)

    liste_caisses = []
    for pos in pos_item(grille[num], '$'):
        liste_caisses += [caisse.init(pos[0], pos[1])]

    att = {}
    att['caisses'] = liste_caisses
    att['grille'] = grille[num]
    att['nb_niv'] = len(grille)
    att['joueur'] = avatar.init(pos_item(grille[num], '@')[0][0], pos_item(grille[num], '@')[0][1], 1, att)
    att['start_time'] = pygame.time.get_ticks()
    att['scores'] = scores.init(att['nb_niv'], 'scores.txt')
    
    options.modif_option('options.txt', 'nb_niv', att['nb_niv'])
    return att

def grilles(path):
    '''Initialise la grille.
    Argument :
    path : '''

    grille = []
    niveau = []
    for elem in recup_niveaux(path):
        if elem != '':
            niveau.append(elem)
        else:
            grille.append(niveau)
            niveau = []
    grille.append(niveau)

    return grille

def pos_item(grille, item):
    '''Renvoie la liste des positions d'un objet d'un niveau.
    Argument :
        grille : list -- lignes d'un niveau.
        item : str -- objet.
    Retour :
        list -- liste des positions.'''

    liste_pos = []
    for l in range(len(grille)):
        for c in range(len(grille[l])):
            if grille[l][c] == item:
                liste_pos += [(l*T_GRILLE, c*T_GRILLE)]

    return liste_pos

def init_dessin(f):
    '''Recupere le niveau a partir d'un fichier texte.
    Argument :
        f : str -- chemin vers fichier contenant les images.
    Retour :
        dict -- dictionnaire des images.'''

    image = {}

    titre_images = ['mur', 'plat', 'cible', 'fond_jeu', 'menu', 'option', 'avatar_b',
                    'avatar_h', 'avatar_g', 'avatar_d', 'caisse']
    
    for i in titre_images:
        image[i] = pygame.image.load_basic(f + '/' + i + '.bmp').convert()
    return image

def recup_niveaux(path):
    '''Recupere le niveau a partir d'un fichier texte.
    Argument :
        path : str -- chemin du fichier texte.
    Retour :
        list -- liste des lignes du niveau.'''

    liste = []
    fich = open(path, 'r')
    ligne = fich.readline()

    while ligne != '':

        while ligne[0] == '/':
            ligne = fich.readline()
        
        liste.append(ligne.rstrip())
        ligne = fich.readline()
    
    fich.close()
    return liste

def dessine_mur(surf, image, l, c):
    '''Dessine un mur.
    Arguments :
        surf : -- surface de l'ecran.
        l : int -- numero de ligne.
        c : int -- numero de colonne.
    Retour :
        None.'''

    surf.blit(image['mur'], [c,l])

def dessine_cible(surf, image, l, c):
    '''Dessine une cible.
    Arguments :
        surf : -- surface de l'ecran.
        l : int -- numero de ligne.
        c : int -- numero de colonne.
    Retour :
        None.'''

    surf.blit(image['cible'], [c,l])

def dessine_sol(surf, image, l, c):
    '''Dessine un sol.
    Arguments :
        surf : -- surface de l'ecran.
        l : int -- index de la ligne.
        c : int -- index de la colonne.
    Retour :
        None.'''

    surf.blit(image['plat'], [c,l])

def mesure_niveau(niv, echelle):
    '''Renvoie la valeur de la largeur et de la hauteur en pixel ou en caractere.
    Argument :
        niv : list -- liste des lignes du niveau.
        echelle : bool -- True pour une valeur a l'echelle du jeu. False pour une valeur en pixels.
    Retour :
        tuple(int,int) -- taille x et y.'''

    l_max = 0
    for l in niv:
        if len(l) > l_max:
            l_max = len(l)
    
    if echelle == True:
        return (l_max, len(niv))

    return (l_max*T_GRILLE, len(niv)*T_GRILLE)

def pos_corrige(grille, axe):
    '''Renvoie deux entiers corrigeant la position d'une grille pour la dessiner au milieu.
    Arguments :
        scen : dict -- attributs
        axe : int -- index de l'axe
    Retour :
        int -- position en x si axe = 0, en y si axe = 1.'''
    
    larg_ecr = int(options.recup_options(FICH_OPTIONS)['res_x'])
    haut_ecr = int(options.recup_options(FICH_OPTIONS)['res_y'])

    t_x = mesure_niveau(grille, False)[0]
    t_y = mesure_niveau(grille, False)[1]

    pos = ((larg_ecr - t_x) // 2, (haut_ecr - t_y) // 2)

    return pos[axe]

def dessine_hud(scen, surf, nb_coups, num, image):
    '''Dessine l'hud.
    Arguments :
        surf : -- surface de l'ecran.
        nb_coups : int --
        scen : dict -- scenario.
        num : index du niveau.
    Retour :
        None.'''

    larg_ecr = int(options.recup_options(FICH_OPTIONS)['res_x'])
    haut_ecr = int(options.recup_options(FICH_OPTIONS)['res_y'])

    # Fond
    pygame.draw.rect(surf, (254, 156, 90), (0, 0, 15, haut_ecr))
    pygame.draw.rect(surf, (254, 156, 90), (larg_ecr - 15, 0, 15, haut_ecr))
    
    pygame.draw.rect(surf, (255, 215, 226), (0, 0, larg_ecr, 75))
    pygame.draw.rect(surf, (255, 215, 226), (0, haut_ecr - 65, larg_ecr, 65))

    pygame.draw.polygon(surf, (255, 188, 174), [(larg_ecr//2 - 150, 75), (larg_ecr//2 - 90, 130), (larg_ecr//2 + 90, 130), (larg_ecr//2 + 150, 75)])
    pygame.draw.polygon(surf, (255, 215, 226), [(larg_ecr//2 - 50, 75), (larg_ecr//2 - 30, 85), (larg_ecr//2 + 30, 85), (larg_ecr//2 + 50, 75)])

    # 'Retour au menu'
    police = pygame.font.Font('polices/Fipps.otf', 10)
    
    texte = police.render('[ESC] Retour au menu principale', True, couleur.JOUER)
    surf.blit(texte, [5, 5])

    # 'Recommencer'
    texte = police.render('[R] Recommencer', True, couleur.OPTIONS)
    surf.blit(texte, [5, 25])

    # 'Passer le niveau'
    texte = police.render('[ENTER] Passer le niveau', True, couleur.QUITTER)
    surf.blit(texte, [5, 45])

    # 'Niveau x'
    police = pygame.font.Font('polices/Fipps.otf', 16)
    
    texte = police.render('Niveau ' + str(num) + ' / ' + str(scen['nb_niv'] - 1), True, couleur.JOUER)
    surf.blit(texte, [ouverture.centrer(texte), 85])

    if num != 0:
        police = pygame.font.Font('polices/Fipps.otf', 14)
        
        # 'Coups x : '
        texte = police.render('Coups : ' + str(nb_coups), True, couleur.NOIR)
        surf.blit(texte, [larg_ecr - texte.get_width() - 20, 20])

        # High score / meilleur coups / meilleurs temps
        police = pygame.font.Font('polices/Fipps.otf', 14)
        
        texte = police.render('Meilleur score : ' + str(scen['scores']['s_niv'][num]), True, couleur.NOIR)
        surf.blit(texte, [30, haut_ecr - 45])

        texte = police.render('Meilleurs coups : ' + str(scen['scores']['c_niv'][num]), True, couleur.NOIR)
        surf.blit(texte, [ouverture.centrer(texte), haut_ecr - 45])

        texte = police.render('Meilleur temps : ' + str(scen['scores']['t_niv'][num]) + 's', True, couleur.NOIR)
        surf.blit(texte, [larg_ecr - texte.get_width() - 20, haut_ecr - 45])

        # Timer
        police = pygame.font.Font('polices/Fipps.otf', 20)

        texte = police.render(str(timer(scen) // 1000) + 's', True, couleur.NOIR)
        surf.blit(texte, [ouverture.centrer(texte), 20])

def dessine_victoire(surf, nms, score, coups, tps):
    '''Dessine les textes de victoires.
    Arguments :
        surf : -- surface de l'ecran.
        nms : bool -- nouveau meilleur score.
        score : int --
        coups : int -- nombre de coups.
        tps : int -- temps.
    Retour :
        None.'''

    #'Niveau termine'
    police = pygame.font.Font('polices/Fipps.otf', 45)
    texte = police.render('Niveau termine !', True, couleur.NOIR)
    surf.blit(texte, [ouverture.centrer(texte), 200])

    if nms:
        #'Nouveau meilleur score'
        police = pygame.font.Font('polices/Fipps.otf', 28)
        texte = police.render('Nouveau Meilleur Score !', True, couleur.OR)
        surf.blit(texte, [ouverture.centrer(texte), 300])

    #scores
    police = pygame.font.Font('polices/Fipps.otf', 20)
    texte = police.render('Score : ' + str(score), True, couleur.NOIR)
    surf.blit(texte, [ouverture.centrer(texte), 370])

    texte = police.render('Nombre de coups : ' + str(coups), True, couleur.NOIR)
    surf.blit(texte, [ouverture.centrer(texte), 415])

    texte = police.render('Temps : ' + str(tps), True, couleur.NOIR)
    surf.blit(texte, [ouverture.centrer(texte), 465])
    
def dessine(scen, image, surf):
    '''Dessine le niveau au centre.
    Arguments :
        scen : dict -- attributs.
        surf : -- surface de l'ecran.
    Retour :
        None.'''

    surf.fill((0, 0, 0))

    larg_ecr = int(options.recup_options(FICH_OPTIONS)['res_x'])
    haut_ecr = int(options.recup_options(FICH_OPTIONS)['res_y'])
    
    surf.blit(pygame.transform.scale(image['fond_jeu'], (larg_ecr + 300, haut_ecr + 300)), [0,0])
    
    for l in range(len(scen['grille'])):
        for c in range(len(scen['grille'][l])):
            
            if scen['grille'][l][c] == '#':
                dessine_mur(surf, image, l*T_GRILLE + pos_corrige(scen['grille'], 1), c*T_GRILLE + pos_corrige(scen['grille'], 0))
            elif scen['grille'][l][c] == '.' or scen['grille'][l][c] == '$' or scen['grille'][l][c] == '@':
                dessine_sol(surf, image, l*T_GRILLE + pos_corrige(scen['grille'], 1), c*T_GRILLE + pos_corrige(scen['grille'], 0))
            elif scen['grille'][l][c] == 'x':
                dessine_cible(surf, image, l*T_GRILLE + pos_corrige(scen['grille'], 1), c*T_GRILLE + pos_corrige(scen['grille'], 0))

    for ca in scen['caisses']:
        caisse.dessine(ca, scen['grille'], image, surf)
    
    avatar.dessine(scen, surf)
    
def execute(scen, num, surf):
    '''Execute le scenario.
    Arguments :
        scen : dict -- attributs.
    Retour :
        int -- '''

    horloge = pygame.time.Clock()
    
    image = init_dessin('images')

    nb_coups = 0

    terminer = False
    while not terminer:

        for event in pygame.event.get():
            if event.type == pygame.constants.USEREVENT:
                pygame.mixer.music.play()

            if event.type == pygame.QUIT:
                return 0
            
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP or event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT:
                    if event.key == pygame.K_UP:
                        scen['joueur']['vit_l'] = -1*T_GRILLE
                        scen['joueur']['vit_c'] = 0
                        scen['joueur']['direc'] = 0
                    elif event.key == pygame.K_RIGHT:
                        scen['joueur']['vit_l'] = 0
                        scen['joueur']['vit_c'] = 1*T_GRILLE
                        scen['joueur']['direc'] = 1
                    elif event.key == pygame.K_DOWN:
                        scen['joueur']['vit_l'] = 1*T_GRILLE
                        scen['joueur']['vit_c'] = 0
                        scen['joueur']['direc'] = 2
                    elif event.key == pygame.K_LEFT:
                        scen['joueur']['vit_l'] = 0
                        scen['joueur']['vit_c'] = -1*T_GRILLE
                        scen['joueur']['direc'] = 3

                    avatar.update(scen['joueur'])
                    caisse.update(scen)

                    nb_coups += 1
                
                if event.key == pygame.K_r:
                    return 1
                if event.key == pygame.K_RETURN:
                    if num < scen['nb_niv'] - 1:
                        return 2
                    else:
                        return 3
                if event.key == pygame.K_ESCAPE:
                    return 3

        surf.fill((0, 0, 0))

        dessine(scen, image, surf)
        dessine_hud(scen, surf, nb_coups, num, image)

        pygame.display.update()

        if a_gagne(scen):
            if num != 0:
                sc = score(timer(scen), nb_coups, len(scen['caisses']))
                if sc > int(scen['scores']['s_niv'][num]):
                    options.modif_option('scores.txt', 's_niv_' + str(num), score(timer(scen), nb_coups, len(scen['caisses'])))
                if nb_coups < int(scen['scores']['c_niv'][num]) or int(scen['scores']['c_niv'][num]) == 0:
                    options.modif_option('scores.txt', 'c_niv_' + str(num), nb_coups)
                if timer(scen) // 1000 < int(scen['scores']['t_niv'][num]) or int(scen['scores']['t_niv'][num]) == 0:
                    options.modif_option('scores.txt', 't_niv_' + str(num), timer(scen) // 1000)
                
                dessine_victoire(surf, sc > int(scen['scores']['s_niv'][num]), sc, nb_coups, timer(scen) // 1000)
                pygame.display.update()

                pygame.time.wait(5000)

            if num < scen['nb_niv']:
                return 2
            else:
                return 3

        horloge.tick(30)

def a_gagne(scen):
    '''Indique si le joueur a place toutes les caisses sur une cible.
    Argument :
        scen : dict -- attribut d'un scenario.
    Retour :
        bool --'''

    pos_cibles = pos_item(scen['grille'], 'x')
    
    pos_caisses = []
    for c in scen['caisses']:
        pos_caisses += [(c['pos_l'], c['pos_c'])]
    
    for c in pos_caisses:
        if c not in pos_cibles:
            return False

    return True

def timer(scen):
    '''Renvoie le timer.
    Argument :
        scen : dict -- scenario.
    Retour :
        float -- temps en millisecondes.'''
    
    return pygame.time.get_ticks() - scen['start_time']

def score(tps, nb_coups, nb_caisses):
    '''Calcule et renvoie le score du joueur.
    Arguments :
        tps : int -- temps en millisecondes.
        nb_coups : int --
    Retour :
        int -- score.'''

    # Arbitraire
    score = 10000
    score -= 0.25*(nb_coups)
    score -= 0.15*((tps/1000)**2)

    if int(score) < 0:
        return 0
    return int(score)
    











