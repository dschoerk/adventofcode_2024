


import math


def parse_input(filepath):
    input = open(filepath).readlines()

    results = []
    nums = []
    for line in input:
        res, numbers = line.split(":")
        res = int(res)
        numbers = numbers.strip().split(" ")
        numbers = [int(x.strip()) for x in numbers]
        results.append(res)
        nums.append(numbers)
    return results, nums
    
results, numbers = parse_input('day7/input.txt')



def build_operator_sequences(num_operators, operators, selected_operators=[]):
    seqs = []
    def dfs(num_operators, operators, selected_operators=[]):
        if len(selected_operators) < num_operators:
            for op in operators:
                dfs(num_operators, operators, selected_operators + [op])
        else:
            seqs.append(selected_operators)
    dfs(num_operators, operators, selected_operators)
    return seqs

def compute_base(number):
    i = 10
    while(number >= 10):
        number /= 10
        i*=10
    return i



def compute_result_with_opsel(opsec, numbers):
    total = numbers[0]
    for op, number in zip(opsec, numbers[1:]):
        if op == '+':
            total += number
        elif op == '*':
            total *= number
        elif op == '||':
            #print(total, number, math.log10(number), 10**int(math.log10(number)), total * 10**int(math.log10(number)+0.5) + number)
            total = int(str(total) + str(number))
            #total = total * 10**(1+int(math.log10(number))) + number
            #base = compute_base(number)
            #total = total * base + number

            #print(number, base)
            #assert total_check == total, f"check failed {total_check} != {total}"
        else:
            raise NotImplementedError(f'{op=} not implemented')
    return total

def check_for_match(operator_sequences, expected_result, numbers):
    for sel in operator_sequences:
        computed_res = compute_result_with_opsel(sel, numbers)

        if expected_result == computed_res:
            return True
    return False


def compute_task(operators):
    total = 0
    for (res, nums) in zip(results, numbers):
        operator_sequences = build_operator_sequences(len(nums) - 1, operators)
        matched = check_for_match(operator_sequences, res, nums)
        if matched:
            total += res
    return total

print("task1: ", compute_task(['+', '*']))
print("task2: ", compute_task(['+', '*', '||']))

    