from abc import ABCMeta, abstractmethod


class AbstractRule:
    __metaclass__ = ABCMeta

    def __init__(self):
        self._grammar = {}

    def _set_grammar(self, gram):
        self._grammar = gram

class ConstantRule(AbstractRule):

    def __init__(self, obj):
        __metaclass__ = ABCMeta
        super(ConstantRule, self).__init__()
        self._object = obj

        
    @abstractmethod
    def valuation(self):
        ''' Return valuation '''
        
    @abstractmethod
    def count(self, i):
        ''' Return number of object of weight i '''

class EpsilonRule(ConstantRule) :
    
    def __init__(self, obj):
        super(EpsilonRule, self).__init__(obj)
        self.__valuation = 0
        
    def valuation(self):
        return self.__valuation

    def count(self, i):
        if i < 0 : 
            raise ValueError("Weight must be positive or null")
        elif i == 0:
            return 1
        else:
            return 0

class SingletonRule(ConstantRule) :
    
    def __init__(self, obj):
        super(SingletonRule, self).__init__(obj)
        self.__valuation = 1

    def valuation(self):
        return self.__valuation

    def count(self, i):
        if i < 0 : 
            raise ValueError("Weight must be positive or null")
        elif i == 1:
            return 1
        else:
            return 0

class ConstructorRule(AbstractRule):

    def __init__(self, fst, snd):
        __metaclass__ = ABCMeta
        super(ConstructorRule, self).__init__()
        self._valuation = float('inf')
        self._parameters = (fst, snd)

    def valuation(self):
        return self._valuation

    @abstractmethod
    def _calc_valuation(self):
        """update valuation"""
   
    @abstractmethod
    def count(self, i):
        ''' Return number of object of weight i '''


    def _update_valuation(self):
        v1 = self._grammar[self._parameters[0]].valuation()
        v2 = self._grammar[self._parameters[1]].valuation()
        self._calc_valuation(v1, v2)
      
class UnionRule(ConstructorRule):

    def __init__(self, fst, snd):

        super(UnionRule, self).__init__(fst, snd)

    def _calc_valuation(self, v1, v2):
        self._valuation =  min(v1, v2)
       
    def count(self, i):
        if i < 0 : 
            raise ValueError("Weight must be positive or null")
        r0 = self._grammar[self._parameters[0]]
        r1 = self._grammar[self._parameters[1]]
        return r0.count(i) + r1.count(i)

class ProductRule(ConstructorRule):

    def __init__(self, fst, snd, cons):

        super(ProductRule, self).__init__(fst, snd)
        self._constructor = cons

    def _calc_valuation(self, v1, v2):
        self._valuation =  v1 + v2

    def count(self, i):
        if i < 0 : 
            raise ValueError("Weight must be positive or null")
        r1 = self._grammar[self._parameters[0]]
        r2 = self._grammar[self._parameters[1]]
        v1 = r1.valuation()
        v2 = r2.valuation()
        res = 0
        for i1 in range (v1, i + 1):
            if (i - i1 >= v2):
                res += r1.count(i1) * r2.count(i - i1)
        return res
                
