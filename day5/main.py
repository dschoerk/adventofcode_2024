



filecontent = open('day5/input.txt').read()

def parse_rule(input_str):
    left, right = input_str.split("|")
    return dict(left = int(left), right = int(right))

def parse_sequence(input_str):
    parts = input_str.split(",")
    seq = [int(x) for x in parts]
    return seq

def parse_input(input_str):
    p1,p2 = input_str.split('\n\n')
    p1 = p1.split()
    p2 = p2.split()

    rules = [parse_rule(x) for x in p1]
    sequences = [parse_sequence(x) for x in p2]

    return rules, sequences

def validate_rule(seq, rule):
    if rule['left'] in seq and rule['right'] in seq:
        return seq.index(rule['left']) < seq.index(rule['right'])
    else:
        return True

def validate_rules(seq, rules):
    for rule in rules:
        if not validate_rule(seq, rule):
            print(f'failed rule {rule["left"]}|{rule["right"]}')
            return False
    return True

def validate_rules_and_fix(seq, rules):
    needed_fix = False
    for rule in rules:
        if not validate_rule(seq, rule):
            print(f'need fix for rule {rule["left"]}|{rule["right"]}')
            ind_left = seq.index(rule['left'])
            ind_right = seq.index(rule['right'])
            print(seq, end="")
            seq[ind_right], seq[ind_left] = seq[ind_left], seq[ind_right]
            print(f' -> {seq}')
            needed_fix = True
    return needed_fix, seq

rules, sequences = parse_input(filecontent)

correct_middle = []
for seq in sequences:
    is_valid = validate_rules(seq, rules)
    if is_valid:
        middle = seq[len(seq) // 2]
        correct_middle.append(middle)
print (sum(correct_middle))
    
correct_middle = []
for seq in sequences:
    needed_fix, seq = validate_rules_and_fix(seq, rules)
    loop_needed_fix = needed_fix

    while loop_needed_fix:
        loop_needed_fix, seq = validate_rules_and_fix(seq, rules)

    assert validate_rules(seq, rules), "is not fixed"

    if needed_fix:
        print(seq, )
        middle = seq[len(seq)//2]
        correct_middle.append(middle)

print(sum(correct_middle))
            


