import random
import copy

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

Tester의 False condition initialize: new_instance.reset(argnum, max_range, error_rate), argnum은 테스트할 파라미터 개수를 입력, max_range는 파라미터의 범위 최대값, error_rate는 전체 가능한 value 조합중 error 의 비율

False condition 갱신: 위와 같음. new_instance.reset(argnum)

실제 테스트 진행: new_instance.run(arglist), arglist 는 테스트 input(2-dimension 리스트) 입력 ex) [[1,2,3], [-1,-2,-3]]. False condition에 해당하는 경우 -1 반환, 아니면 0

False condition 값 확인: new_instance.get_range(), False condition 범위의 시작값들을 리스트로 반환. range()의 list 형태를 가지고 있음.



1. instance 생성 -> new_instance = Tester.instance()
2. False condition initialize(처음 한번 필수) -> new_instance.reset(argnum, max_range, error_rate)
3. Test 실행 -> new_instance.run(input)

이후 필요에 따라 reset() 이나 get_range() 적절히 활용



현재 버전은 파라미터의 condition이 [0, max_range) 범위 중에서 10만큼의 range가 False인 경우로 지정. 원하는 error_rate를 만족하지 못하면 condition을 추가.
ex) 파라미터 3개: [ [range(11,21), range(30,40), range(44, 54)], [range(2,12), range(51,61), range(99, 109)], ... ]

'''

class Tester(SingletonInstane):
    def __init__(self):
        self.argnum = 0 # 테스트할 parameter 개수
        self.max_range = 0 # parameter의 최대값
        self.error_rate = 0 # 모든 경우 중 error case 비율
        self.condition = [] # parameter 별 False condition을 담고있는 list
        self._initCondition()

    def _initCondition(self): # 클래스 구현용 내부함수. self.condition을 initialize 하는 함수.
        self.condition = []

        current_error_rate = 0

        while current_error_rate < self.error_rate:
            temp_condition = []
            temp_error_rate = 1

            for _ in range(self.argnum):
                rand_range_start = random.randrange(0, self.max_range-10)
                temp_condition.append(range(rand_range_start, rand_range_start+10))
                temp_error_rate *= 10/self.max_range

            self.condition.append(temp_condition)
            current_error_rate += temp_error_rate

            # self.condition.append(lambda x: x[i] in temp_condition[i] for i in range(self.argnum))
    
    def reset(self, argnum=0, max_range=0, error_rate = 0, correction_range = None): # condition을 initialize 하기위한 함수.
        self.argnum = argnum
        self.max_range = max_range
        self.error_rate = error_rate
        self._initCondition()
    
    def run(self, arglist): # 실제로 테스트 할 때 사용하는 함수.
        result = []

        for args in arglist:
            assert (len(args) == self.argnum)
            result_temp = 0
            for condition in self.condition:
                for i in range(len(args)):
                    if not args[i] in condition[i]:
                        break
                else:
                    result_temp = -1
            result.append(result_temp)

        return result
    
    def get_range(self): # 디버깅용 함수. self.condition 안의 조건을 반환하는 함수.
        return self.condition

            

if __name__ == "__main__":
    test = Tester.instance()
    test.reset(argnum=2, max_range = 199, error_rate = 0.1)
    print(test.run([[10, 10], [20, 30]]))
    print(test.get_range())