from collections import namedtuple
from copy import deepcopy as copy
from sys import argv
from time import perf_counter

start = perf_counter()

nt = namedtuple('nt', ['value', 'string'])
nt1 = namedtuple('nt', ['value', 'string', 'remaining'])


def add(x, y):
    return nt(x.value + y.value, f'({x.string} + {y.string})')


def sub(x, y):
    return nt(x.value - y.value, f'({x.string} - {y.string})')


def mul(x, y):
    return nt(x.value * y.value, f'({x.string} * {y.string})')


def div(x, y):
    return nt(x.value / y.value, f'({x.string} / {y.string})')


operations = [add, sub, mul, div]

if len(argv) >= 2:
    number_list = argv[1:-1]
    target = int(argv[-1])
# Enter numbers here
else:
    number_list = '1 2 3 4 25 100'.split(' ')
    target = 420

numbers = []
for number in number_list:
    number_list1 = copy(number_list)
    number_list1.remove(number)
    numbers.append(nt(int(number), str(number)))

new_numbers = []

for item in numbers:
    numbers1 = copy(numbers)
    numbers1.remove(item)
    new_numbers.append(nt1(item.value, item.string, numbers1))

numbers = new_numbers
results = []
results.extend(numbers)

correct = []

for item in results:
    for remainder in item.remaining:
        remain1 = copy(item.remaining)
        remain1.remove(remainder)
        for oper in operations:
            returned = oper(item, remainder)
            if returned.value % 1 == 0 and returned.value >= 0:
                results.append(nt1(int(returned.value), returned.string, remain1))
                if returned.value == target:
                    correct.append(nt1(int(returned.value), returned.string, remain1))
            try:
                returned = oper(remainder, item)
            except ZeroDivisionError:
                continue
            if returned.value % 1 == 0 and returned.value >= 0:
                results.append(nt1(int(returned.value), returned.string, remain1))
                if returned.value == target:
                    correct.append(nt1(int(returned.value), returned.string, remain1))

if len(correct) != 0:
    for result in correct:
        print(f'{result.string[1:-1]} = {result.value}')
else:
    min_gap = target
    closest = []
    for result in results:
        gap = abs(target - result.value)
        if gap < min_gap:
            min_gap = gap
            closest.clear()
            closest.append(result)
        elif gap == min_gap:
            closest.append(result)
    for result in closest:
        print(f'{result.string[1:-1]} = {result.value}')
    print(f'Closest we could find was {min_gap} away')


end = perf_counter()

print(f'finished in {end - start}s')