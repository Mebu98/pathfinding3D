import json
import os

import numpy as np

class Node (object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Map:
    def __init__(self, matrix, start, end):
        self.matrix = matrix
        self.start = start
        self.end = end


def getMap1():

    start = Node(0, 0, 0)
    end = Node(7, 7, 5)

    grid = [
        [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ],
        [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ],
        [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ],
        [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ],
        [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ],
        [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
    ]
    grid = np.swapaxes(grid, 2, 0)

    m = Map(grid, start, end)
    return m

def getMap2():

    start = Node(1, 0, 0)
    end = Node(9, 2, 4)

    grid = [
        [
            [0, 1, 0, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 0, 1, 0, 1, 0, 0, 0, 1],
            [0, 1, 0, 1, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 0, 0, 1, 0, 0],
            [1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
        ],
        [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
        [
            [1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
            [1, 0, 1, 1, 1, 0, 0, 0, 1, 1],
            [1, 0, 1, 0, 0, 0, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 1, 1, 0, 1, 1, 0, 1, 1],
        ],
        [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
        [
            [0, 0, 1, 1, 1, 1, 0, 0, 1, 1],
            [0, 1, 1, 1, 1, 1, 0, 0, 1, 0],
            [1, 1, 1, 0, 0, 1, 0, 0, 1, 1],
            [1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
        ]
    ]



    grid = np.swapaxes(grid, 2, 0)

    m = Map(grid, start, end)
    return m

def getMap3():
    start = Node(4, 4, 2)
    end = Node(28, 4, 0)
    grid = [
        [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,],
        ],
        [
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, ],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
        ],
        [
            [1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
            [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, ],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, ],
            [1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
            [1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
        ],
    ]
    grid = np.swapaxes(grid, 2, 0)

    m = Map(grid, start, end)
    return m

class States:
    def __init__(self, air, start, end):
        self.air = air
        self.start = start
        self.end = end

def getMap4():
    # """
    # Found a very jank way of turning a minecraft area into our desired input.
    # Programs needed: NBTUtil.exe (part of NBTExplorer) and Minecraft (duh)
    #
    # Steps to reproduce:
    #     1. In minecraft (creative):
    #         Give yourself a structure block using "/give @p structure_block 1".
    #         Place it down and right click on it.
    #         Swap to save mode by clicking the load/corner button in the bottom left.
    #         Give the structure a name.
    #         Play around with structure size and relative position until it fills your needs.
    #         Save the area using the save button to the right.
    #
    #     2. In terminal (admin mode recommended):
    #         cd to where NBTUtil is located. ("C:\Program Files (x86)\NBTExplorer\",
    #         at least on default windows)
    #
    #         run this command to transform to the .nbt to .json:
    #         ./NBTUtil.exe --path="location of .nbt" --json="name of json.json"
    #
    #         (.nbt location is usually in: (replace "save" with world name, at least on windows)
    #         "\AppData\Roaming\.minecraft\saves\"save"\generated\minecraft\structures\"
    #
    #     put the new json in here and do as below (for now at least)
    # """

    file_name = 'ifi_house_test.json'
    try:
        cwd = os.getcwd()
        json_file = open(cwd + '\\examples\\' + file_name, 'r').read()
    except FileNotFoundError:
        json_file = open(file_name, 'r').read()

    data = json.loads(json_file)
    states = States(0,0,0)

    # Start and end are found later by green and red wool.
    start = Node(0,0,0)
    end = Node(0, 0, 0)

    palette = data['palette']
    for i, p in enumerate(palette):
        match p['Name']:
            case 'minecraft:air':
                states.air = i
            case 'minecraft:green_wool':
                states.start = i
            case 'minecraft:red_wool':
                states.end = i
        # if p['Name'] == 'minecraft:air':
        #     air = i

    dimensions = data['size']
    nodes = np.ones([dimensions[0], dimensions[1], dimensions[2]])
    nodes = nodes.tolist()

    blocks = data.get('blocks')
    for block in blocks:
        pos = block.get('pos')
        state = block.get('state')
        x, y, z = 0, 1, 2

        match state:
            case states.air:
                nodes[pos[x]][pos[y]][pos[z]] = 1

            case states.start:
                start = Node(pos[x], pos[z], pos[y])

            case states.end:
                end = Node(pos[x], pos[z], pos[y])

            case _:
                nodes[pos[x]][pos[y]][pos[z]] = 0

    nodes = np.swapaxes(nodes, 2, 1) # Our code uses XYZ, while input uses XZY, I think.

    # Attempting to "unmirror" the map
    # nodes = np.flip(nodes, 2) # "Unmirror" the map?, messes up start and end :(
    # Unmirroring using swapaxes might mess up the map if it has different max x and y (might also mess up start and end)
    #nodes = np.swapaxes(nodes, 0, 1)

    matrix = Map(nodes, start, end)

    return matrix

getMap4()