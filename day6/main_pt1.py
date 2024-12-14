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

world, pstate = parse_map(input_str)

print(f"{world}", f"{pstate=}")

occupancy_map = np.zeros_like(world, dtype=np.bool)


leave = False
while not leave:
    occupancy_map[pstate.pos.y, pstate.pos.x] = True
    pstate, leave = move(pstate, world)
    if leave:
        print(f'left at {pstate}')

print(occupancy_map, sum(occupancy_map.flatten()))
    