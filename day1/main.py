
# read the file
def read_input(fpath):
  f = open(fpath, 'r')
  lines = f.readlines()
  lines = [line.strip().split() for line in lines]
  items = [[int(i) for i in line_items] for line_items in lines]
  return items

items = read_input('day1/input.txt')
items_t = list(map(list, zip(*items)))
items_t[0].sort()
items_t[1].sort()
items = list(map(list, zip(*items_t)))
diff = [abs(i[0]-i[1]) for i in items]

#print(diff)
print("q1: ", sum(diff))

# part 2
items = read_input('day1/input.txt')
items_t = list(map(list, zip(*items)))

total = 0
for n in items_t[0]:
  num = sum([n == x for x in items_t[1]])
  total += num * n

print("q2: ", total)







