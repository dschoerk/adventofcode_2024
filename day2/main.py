import numpy as np


def check_safety(input):
  diff = input[:, 1:] - input[:, :-1]
  safe = (np.all(diff < 0, axis = 1) | np.all(diff > 0, axis = 1)) & np.all(np.abs(diff) <= 3, axis = 1)
  return safe

def create_with_removal(input):
  new_input = np.zeros((input.shape[0], input.shape[0]-1), int)
  for i in range(input.shape[0]):
    new_input[i, :] = input[list(set(range(input.shape[0])) - set([i]))]
  return new_input

# part 1
safety_cnt = 0
for line in open('day2/input.txt').readlines():
  input = np.array(line.split(), int)
  input = np.expand_dims(input, 0)
  safe = check_safety(input)[0]
  safety_cnt += safe

print(safety_cnt)

# part 2
safety_cnt = 0
for line in open('day2/input.txt').readlines():
  input = np.array(line.split(), int)
  input = create_with_removal(input)
  safe = check_safety(input).any()
  safety_cnt += safe

print(safety_cnt)
