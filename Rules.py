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

    @abstractmethod
    def list(self, i):
        '''Return list of all objects of weight i'''

class EpsilonRule(ConstantRule) :
    
    def __init__(self, obj):
        super(EpsilonRule, self).__init__(obj)
        self.__valuation = 0
        
    def valuation(self):
        return self.__valuation

    def count(self, i):
        if i < 0 : 
            raise ValueError("Weight must be positive or null")
        if i == 0:
            return 1
        return 0

    def list(self, i):
        if i < 0:
            raise ValueError("Weight must be positive or null")
        if i == 0:
            return [self._object]
        return []

class SingletonRule(ConstantRule) :
    
    def __init__(self, obj):
        super(SingletonRule, self).__init__(obj)
        self.__valuation = 1

    def valuation(self):
        return self.__valuation

    def count(self, i):
        if i < 0 : 
            raise ValueError("Weight must be positive or null")
        if i == 1:
            return 1
        return 0
    
    def list(self, i):
        if i < 0:
            raise ValueError("Weight must be positive or null")
        if i == 1:
            return [self._object]
        return []
            

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

    @abstractmethod
    def list(self, i):
        '''Return list of all objects of weight i'''

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

    def list(self, i):
        fst, snd = self._parameters
        fst, snd = self._grammar[fst], self._grammar[snd]
        return fst.list(i) + snd.list(i)

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
                

    def list(self, i):
        fun = self._constructor
        fst, snd = self._parameters
        fst, snd = self._grammar[fst], self._grammar[snd]
        l = []
        v1 = fst.valuation()
        v2 = snd.valuation()
        for i1 in range (v1, i + 1):
            if (i - i1 >= v2):
                l1 = fst.list(i1)
                l2 = snd.list(i - i1)
                for x in l1:
                    for y in l2:
                        # print (x, y)
                        # print ("ici", self._constructor([x, y]))
                        l.append( self._constructor([x, y]))
        return l

