import Tree
import Rules as R
from abc import ABCMeta, abstractmethod

class ConstantCRule:
    __metaclass__ = ABCMeta
    def __init__(self, obj):
        self._object = obj

    @abstractmethod
    def to_simple_rule(self, g):
        ''' Returns equivalent rule in developped form'''

class Epsilon(ConstantCRule):
    def __init__(self, obj):
        super(Epsilon, self).__init__(obj)

    def to_simple_rule(self, g):
        rule_name = str(len(g))
        g[rule_name] = R.EpsilonRule(self._object)
        return (g, rule_name)

class Singleton(ConstantCRule):
    def __init__(self, obj):
        super(Singleton, self).__init__(obj)

    def to_simple_rule(self, g):
        rule_name = str(len(g))
        g[str(len(g))] =  R.SingletonRule(self._object)
        return (g, rule_name)

class ConstructorCRule:
    __metaclass__ = ABCMeta
    def __init__(self, r1, r2):
        self._r1 = r1
        self._r2 = r2

    # @abstractmethod
    # def to_simple_rule:
    #     ''' Returns equivalent rule in developped form'''

class Union(ConstructorCRule):

    def __init__(self, r1, r2, f):
        super(Union, self).__init__(r1, r2)
        self._f = f
        
    def to_simple_rule(self, g, name =""):
        g, name1 = self._r1.to_simple_rule(g)
        g, name2 = self._r2.to_simple_rule(g)
        if name == "":
            rule_name = str(len(g))
        else:
            rule_name = name
        g[rule_name] = R.UnionRule(name1, name2, self._f)
        print ("union", rule_name, g[rule_name])
        return (g, rule_name)

class Prod(ConstructorCRule):
    def __init__(self, r1, r2, join, f):
        super(Prod, self).__init__(r1, r2)
        self._join = join
        self._f = f

    def to_simple_rule(self, g, name = ""):
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
        return (g, self._rule)

ng = {"Tree" : Union (Singleton (Tree.Leaf), Prod(NonTerm ("Tree"), NonTerm ("Tree"), 
                                                  lambda (l) : Tree.Node(l), lambda (t) : (t.left(), t.right())), lambda(t) : t.is_leaf())}

def init_grammar (grammar):

    for rule_id in grammar:
        grammar[rule_id]._set_grammar(grammar)

    # check_defined_rules(grammar)

    constr_before, constr_after = {}, {}
    for rule in grammar.values():
        if isinstance(rule, R.ConstructorRule):
            constr_before [rule] = rule.valuation() 
            constr_after [rule] = 0

    while (constr_before != constr_after):
        constr_before = constr_after.copy()
        for rule in constr_after:
            rule._update_valuation()
            constr_after[rule] = rule.valuation()
   
    for rule_id in grammar:
        if grammar[rule_id].valuation() == float('inf'):
            raise IncorrectGrammar("Rule "+rule_id+" is incorrect (inf valuation)")

   

def dvp_gram (g):
    new_gram = g.copy()
    for rule_name in g:
        print("rule name", rule_name)
        print(type(g[rule_name]))
        (a, r) = g[rule_name].to_simple_rule(new_gram, rule_name)
        print ("dvp", a)
        new_gram.update(a)
        init_grammar(new_gram)
    for k in new_gram:
        print(k, str(new_gram[k]))

print (R.SingletonRule(""))
dvp_gram (ng)
            
