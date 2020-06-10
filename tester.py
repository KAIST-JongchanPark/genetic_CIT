import random

class SingletonInstane:
    __instance = None

    @classmethod
    def __getInstance(cls):
        return cls.__instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls.__instance = cls(*args, **kargs)
        cls.instance = cls.__getInstance
        return cls.__instance

class Tester(SingletonInstane):
    def __init__(self):
        self.argnum = 0
        self.condition = []
        self._initCondition()

    def _initCondition(self):
        self.condition = []
        for _ in range(self.argnum):
            rand_range_start = random.randrange(-1000, 1000) 
            self.condition.append((rand_range_start, lambda x: x in range(rand_range_start*100, (rand_range_start+1)*100)))
    
    def reset(self, argnum):
        self.argnum = argnum
        self._initCondition()
    
    def run(self, arglist):
        for args in arglist:
            assert (len(args) == self.argnum)
            for i in range(len(args)):
                if not self.condition[i][1](args[i]):
                    return -1
        return 0
    
    def get_range(self):
        return [v[0] for v in self.condition]

            

# if __name__ == "__main__":
#     test = Tester.instance()
#     test.reset(1)
#     print(test.run([[1]]))
#     print(test.get_range())
#     test2 = Tester.instance()
#     print(test2.run([[1]]))
#     test2.reset(1)
#     print(test.get_range())