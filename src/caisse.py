'''
Implemente les caisses.
'''

import pygame
import scenario

def init(l, c):
    '''Initialise les attributs de la caisse.
    Arguments :
        l : int -- index de ligne
        c : int -- index de colonne
    Retour :
        dict -- attributs.'''

    att = {'pos_l': l, 'pos_c': c, 'vit_l': 0, 'vit_c': 0}

    return att

def dessine(att, grille, image, surf):
    '''Dessine une caisse.
    Arguments :
        att : dict -- attributs
        surf : -- surface de l'ecran
    Retour :
        None.'''

    surf.blit(image['caisse'], [att['pos_c'] + scenario.pos_corrige(grille, 0), att['pos_l'] + scenario.pos_corrige(grille, 1)])

def update(att_caisses):
    '''Met a jour la position des caisses.
    Argument :
        att_caisses : list - liste des attributs de caisses.
    Retour :
        None.'''

    for c in att_caisses['caisses']:
        c['pos_l'] += c['vit_l']
        c['pos_c'] += c['vit_c']












