
import re

input_string = open('day3/input.txt').read()
matches = re.findall(r'mul\((\d{1,3})\,(\d{1,3})\)', input_string)

# sum of product for all matching groups
sum = sum([int(x[0])*int(x[1]) for x in matches])

print("q1: ", sum)

matches = re.findall(r'(mul\((\d{1,3})\,(\d{1,3})\))|(do\(\))|(don\'t\(\))', input_string)

sum = 0
active = True
for m in matches:
    if len(m[0]) > 0 and active: # is mul op
       sum += int(m[1]) * int(m[2])
    elif len(m[3]) > 0: # is do op
        active = True
    elif len(m[4]) > 0: # is dont op
        active = False
print(sum)

