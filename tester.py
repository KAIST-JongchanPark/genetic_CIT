import random

class SingletonInstane: # Singleton 포맷의 클래스. 한번 Tester 클래스를 호출하여 작업하면 이후 Tester 클래스의 새로운 instance를 만들어도 이전의 상태를 유지.
    __instance = None

    @classmethod
    def __getInstance(cls):
        return cls.__instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls.__instance = cls(*args, **kargs)
        cls.instance = cls.__getInstance
        return cls.__instance

'''
기본 클래스 사용법

instance 만들기: new_instance = Tester.instance()

Tester의 True condition initialize: new_instance.reset(argnum), argnum은 테스트할 파라미터 개수를 입력

True condition 갱신: 위와 같음. new_instance.reset(argnum)

실제 테스트 진행: new_instance.run(arglist), arglist 는 테스트 input(2-dimension 리스트) 입력 ex) [[1,2,3], [-1,-2,-3]]. 모든 파라미터가 통과시 0을 반환. 하나라도 통과 실패시 -1 반환.

True condition 값 확인: new_instance.get_range(), True condition 범위의 시작값들을 리스트로 반환. ex) 2개의 파라미터에 대한 True condition이 [0, 100), [100, 200) 이라면 [0, 100] 을 반환.



1. instance 생성 -> new_instance = Tester.instance()
2. True condition initialize(처음 한번 필수) -> new_instance.reset(argnum)
3. Test 실행 -> new_instance.run(input)

이후 필요에 따라 reset() 이나 get_range() 적절히 활용



초기버전은 파라미터의 condition이 [-100000, 100000) 범위 중에서 100만큼의 range가 True 범위로 지정됨. ex) [0, 100), [100, 200)

'''

class Tester(SingletonInstane):
    def __init__(self):
        self.argnum = 0 # 테스트할 parameter 개수
        self.condition = [] # parameter 별 True condition을 담고있는 list
        self._initCondition()

    def _initCondition(self): # 클래스 구현용 내부함수. self.condition을 initialize 하는 함수.
        self.condition = []
        for _ in range(self.argnum):
            rand_range_start = random.randrange(-1000, 1000) 
            self.condition.append((rand_range_start, lambda x: x in range(rand_range_start*100, (rand_range_start+1)*100)))
    
    def reset(self, argnum): # condition을 initialize 하기위한 함수.
        self.argnum = argnum
        self._initCondition()
    
    def run(self, arglist): # 실제로 테스트 할 때 사용하는 함수.
        for args in arglist:
            assert (len(args) == self.argnum)
            for i in range(len(args)):
                if not self.condition[i][1](args[i]):
                    return -1
        return 0
    
    def get_range(self): # 디버깅용 함수. self.condition 안의 조건을 반환하는 함수.
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