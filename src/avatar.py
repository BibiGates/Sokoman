'''
Implemente l'avatar du joueur.
'''

import pygame
import scenario
import options

FICH_OPTIONS = 'options.txt'

def init(l, c, d, scen):
    '''Initialise les attributs du personnage.
    Arguments :
        l : int -- index de ligne
        c : int -- index de colonne
        d : int -- direction du personnage.
        scen : dict -- attributs d'un scenario.
    Retour :
        dict -- attributs.'''

    images = scenario.init_dessin('images')

    img_perso = [images['avatar_h'], images['avatar_d'], images['avatar_b'], images['avatar_g']]
    
    att = {'pos_l': l, 'pos_c': c, 'direc': d, 'vit_l': 0, 'vit_c': 0, 'img': img_perso, 'scen': scen}

    return att

def dessine(att, surf):
    '''Dessine l'avatar.
    Argument :
        att : dict -- attributs de l'avatar
        surf : -- surface de l'ecran
    Retour :
        None.'''

    larg_ecr = int(options.recup_options(FICH_OPTIONS)['res_x'])
    haut_ecr = int(options.recup_options(FICH_OPTIONS)['res_y'])

    pos_x = att['joueur']['pos_l'] + scenario.pos_corrige(att['grille'], 1)
    pos_y = att['joueur']['pos_c'] + scenario.pos_corrige(att['grille'], 0)

    surf.blit(att['joueur']['img'][att['joueur']['direc']], [pos_y, pos_x])

def update(att):
    '''Met a jour l'etat de l'avatar et d'une caisse.
    Argument :
        att : dict -- attributs
    Retour :
        None.'''

    n_pos_l = att["pos_l"] + att["vit_l"]
    n_pos_c = att["pos_c"] + att["vit_c"]
    n_pos_caisse_l = att["pos_l"] + att["vit_l"] * 2
    n_pos_caisse_c = att["pos_c"] + att["vit_c"] * 2
    
    if (est_sur_caisse(n_pos_l, n_pos_c, att['scen'])):
        if (not est_sur_caisse(n_pos_caisse_l, n_pos_caisse_c, att['scen'])) and \
            (not est_sur_mur(n_pos_caisse_l, n_pos_caisse_c, att['scen'])):
            att['pos_l'] += att['vit_l']
            att['pos_c'] += att['vit_c']

            for c in att['scen']['caisses']:
                
                if att['pos_l'] == c['pos_l'] and att['pos_c'] == c['pos_c']:
                    c['vit_l'] = att['vit_l']
                    c['vit_c'] = att['vit_c']
                else:
                    c['vit_l'] = 0
                    c['vit_c'] = 0
        else:
            for c in att['scen']['caisses']:
                c['vit_l'] = 0
                c['vit_c'] = 0
    
    elif not est_sur_mur(n_pos_l, n_pos_c, att['scen']):
        att['pos_l'] += att['vit_l']
        att['pos_c'] += att['vit_c']

        for c in att['scen']['caisses']:
            c['vit_l'] = 0
            c['vit_c'] = 0
    else:
        for c in att['scen']['caisses']:
            c['vit_l'] = 0
            c['vit_c'] = 0

def est_sur_mur(lig, col, scen):
    '''Indique si la position correspond a celle d'un mur.
    Arguments :
        lig : int -- index de ligne.
        col : int -- index de colonne.
        scen : dict -- attributs de scenario.
    Retour :
        bool -- '''

    return scen['grille'][int(lig/scenario.T_GRILLE)][int(col/scenario.T_GRILLE)] == '#'

def est_sur_caisse(lig, col, scen):
    '''Indique si la position correspond a celle d'une caisse.
    Arguments :
        lig : int -- index de ligne.
        col : int -- index de colonne.
        scen : dict -- attributs de scenario.
    Retour :
        bool --'''

    pos_caisses = []
    for c in scen['caisses']:
        pos_caisses += [(c['pos_l'], c['pos_c'])]
    
    return (lig, col) in pos_caisses













