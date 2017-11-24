# -*- coding: utf-8 -*
import Tree
import Rules as R
from abc import ABCMeta, abstractmethod


class ConstantCRule:
    __metaclass__ = ABCMeta
    def __init__(self, obj):
        self._object = obj

class Epsilon(ConstantCRule):

    def __init__(self, obj):
        super(Epsilon, self).__init__(obj)

    # Chaque règle crée a comme identifiant une chaine de caractère
    # qui contient un entier (égal à la taille du dictionnaire lors de 
    # la création de la règle)
    def to_simple_rule(self, g):
        ''' Convertit la règle en EpsilonRule ''' 
        rule_name = str(len(g))
        g[rule_name] = R.EpsilonRule(self._object)
        return (g, rule_name)

class Singleton(ConstantCRule):
    
    def __init__(self, obj):
        super(Singleton, self).__init__(obj)

    def to_simple_rule(self, g):
        ''' Convertit la règle en SingletonRule '''
        rule_name = str(len(g))
        g[str(len(g))] =  R.SingletonRule(self._object)
        return (g, rule_name)

    
class ConstructorCRule:

    __metaclass__ = ABCMeta
    def __init__(self, r1, r2):
        # sous règle de gauche
        self._r1 = r1
        # sous règle de droite
        self._r2 = r2

class Union(ConstructorCRule):

    def __init__(self, r1, r2, f = None):
        super(Union, self).__init__(r1, r2)
        self._f = f
        

    def to_simple_rule(self, g, name =""):
        ''' Convertit la règle en UnionRule '''

        # On convertit d'abord les règles contenues dans 
        # l'union
        g, name1 = self._r1.to_simple_rule(g)
        g, name2 = self._r2.to_simple_rule(g)
        # Si un nom a été donnée dans la grammaire on le conserve
        if name == "":
            rule_name = str(len(g))
        else:
            rule_name = name
        # On crée la règle union
        g[rule_name] = R.UnionRule(name1, name2, self._f)
        return (g, rule_name)

class Prod(ConstructorCRule):

    def __init__(self, r1, r2, join, f = None):
        super(Prod, self).__init__(r1, r2)
        self._join = join
        self._f = f


    def to_simple_rule(self, g, name = ""):
        ''' Convertit la règle en ProductRule '''
        g, name1 = self._r1.to_simple_rule(g)
        g, name2 = self._r2.to_simple_rule(g)
        if name == "":
            rule_name = str(len(g))
        else:
            rule_name = name
        g[rule_name] = R.ProductRule(name1, name2, self._join, self._f)
        return (g, rule_name)


class NonTerm:
    def __init__(self, rule):
        self._rule = rule

    def to_simple_rule(self, g):
        ''' Ne modifie pas la grammaire, car par définition, il existe
        une règle dans la grammaire dont la clé est égale à self.rule '''
        return (g, self._rule)

class Sequence():

    def __init__(self, nt, casvide, cons, frank_union = None, frank_product = None):
        self._nt = nt
        self._vide = casvide
        self._cons = cons
        self._frank_u = frank_union
        self._frank_p = frank_product
    
    def to_simple_rule(self, g, name =""):
        ''' Convertit la règle en Union qui est converties en UnionRule '''
        if name == "":
            rule_name = str(len(g))
        else:
            rule_name = name
        rule = Union(Epsilon(self._vide), Prod(NonTerm(rule_name), NonTerm(self._nt), self._cons,
                                               self._frank_p), self._frank_u)
        (g, rn) = rule.to_simple_rule(g, rule_name)
        return (g, rn)


def dvp_gram (g):
    ''' Convertit une grammaire condensée en une grammaire développée'''

    new_gram = g.copy()
    for rule_name in g:
        (a, r) = g[rule_name].to_simple_rule(new_gram, rule_name)
        # Ajoute les paires du dictionnaire a au dictionnaire new_gram
        new_gram.update(a)
    return new_gram
            
