from dataclasses import dataclass
import numpy as np

# dir: up, left, down, right

@dataclass
class Point2D:
    y: int
    x: int

    def __repr__(self):
        return f'({self.x},{self.y})'

def dir_to_vec(dir):
    assert dir in [0,1,2,3], f"{dir=} not found"
    match(dir):
        case 0:
            return Point2D(y=-1, x=0)
        case 1: 
            return Point2D(y=0, x=1)
        case 2:
            return Point2D(y=1, x=0)
        case 3: 
            return Point2D(y=0, x=-1)

def vec_add(a, b):
    return Point2D(y=a.y+b.y, x=a.x+b.x)

def point_in_world(point, world):
    inbounds_y = point.y >= 0 and point.y < world.shape[0]
    inbounds_x = point.x >= 0 and point.x < world.shape[1]
    return inbounds_x and inbounds_y

@dataclass
class PlayerState:
    pos: Point2D
    dir: int

def move(pstate, world):
    forward_pos = vec_add(pstate.pos, dir_to_vec(pstate.dir))
    forward_pos_in_world = point_in_world(forward_pos, world)

    if not forward_pos_in_world:
        return pstate, True
    
    obstructed = world[forward_pos.y, forward_pos.x] == '#'
    if obstructed:
        # turn left
        dir = (pstate.dir + 1) % 4
        new_pstate = PlayerState(pos = pstate.pos, dir=dir)
    else:
        # move in forward dir
        new_pstate = PlayerState(pos = forward_pos, dir=pstate.dir)

    return new_pstate, False 


input_str = open('day6/input.txt').readlines()

def parse_map(input_str):
    lines = [list(line.strip()) for line in input_str]
    world = np.array(lines)

    start_pos = np.where(world == '^')
    start_pos = (start_pos[0][0], start_pos[1][0])
    pstate = PlayerState(pos = Point2D(start_pos[0], x = start_pos[1]), dir = 0)

    return world, pstate

origin_world, pstate_start = parse_map(input_str)

print(f"{origin_world}", f"{pstate_start=}")



def find_loop(new_pstate, pstate_history):

    remove_ids = []
    for i, h in enumerate(pstate_history):
        if i <= 0 or i == len(pstate_history)-1:
            continue

        if pstate_history[i].dir == pstate_history[i-1].dir:
            remove_ids.append(i)

    pstate_history = [h for i,h in enumerate(pstate_history) if i not in remove_ids]
    #del pstate_history[remove_ids]
    #print(len(pstate_history))

    for h in pstate_history:
        if new_pstate == h:
            return True, pstate_history
    return False, pstate_history


# find possible candidates
obstr_map = origin_world == '#'
print(obstr_map)
#exit()

world = origin_world.copy()
pstate = PlayerState(pos=Point2D(y=pstate_start.pos.y, x=pstate_start.pos.x), dir=pstate_start.dir)
leave = False
found_loop = False
occupancy_map = np.zeros_like(origin_world, dtype=np.bool)
while not leave and not found_loop:
    occupancy_map[pstate.pos.y, pstate.pos.x] = True
    pstate, leave = move(pstate, world)



possible_new_obstructions = []

for y in range(origin_world.shape[0]):
    for x in range(origin_world.shape[1]):

        if not occupancy_map[y,x]:
            continue

        print(y,x)
        world = origin_world.copy()
        #occupancy_map = np.zeros_like(origin_world, dtype=np.bool)
        pstate = PlayerState(pos=Point2D(y=pstate_start.pos.y, x=pstate_start.pos.x), dir=pstate_start.dir)
        # modify world

        # check if we can modify at x,y
        if world[y,x] != '.':
            continue

        # try to insert an obstruction
        world[y,x] = '#'

        print("new_world:")
        print(world)

        history = []
        leave = False
        found_loop = False
        while not leave and not found_loop:
            found_loop, history = find_loop(pstate, history)
            history.append(pstate)
            #occupancy_map[pstate.pos.y, pstate.pos.x] = True
            pstate, leave = move(pstate, world)
            if leave:
                pass
                #print(f'left at {pstate}')
            if found_loop:
                possible_new_obstructions.append(Point2D(y=y, x=x))

        #print(occupancy_map)
        print(f'{possible_new_obstructions=}')
        #print(history)

print(len(possible_new_obstructions))
        #print(occupancy_map, sum(occupancy_map.flatten()))
        #print(possible_new_obstructions)
    