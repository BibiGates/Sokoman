'''
Implemente les scores.
'''

import options

def init(nb_niv, fich_score):
    '''Initialise les scores.
    Argument :
        nb_niv : --
        fich_score : str -- nom du fichier.
    Retour :
        dict -- '''

    att = {}
    att['c_niv'] = []
    att['t_niv'] = []
    att['s_niv'] = []
    
    for i in range(nb_niv):
        att['c_niv'] += [options.recup_options(fich_score)['c_niv_' + str(i)].rstrip()]
        att['t_niv'] += [options.recup_options(fich_score)['t_niv_' + str(i)].rstrip()]
        att['s_niv'] += [options.recup_options(fich_score)['s_niv_' + str(i)].rstrip()]

    return att

def init_fich_score(nb_niv, fich_score):
    '''(Re)initialise le fichier des scores.
    Arguments :
        scen : dict -- scenario.
        fich_score : str -- nom du fichier.
    Retour :
        None.'''

    for i in range(nb_niv):
        options.modif_option(fich_score, 'c_niv_' + str(i), 0)
        options.modif_option(fich_score, 't_niv_' + str(i), 0)
        options.modif_option(fich_score, 's_niv_' + str(i), 0)

    
