"""
This example shows how Dijkstra algorithm differs from A* algorithm
Requires plotly for visualization. Install it using `pip install plotly`
"""
import time

import plotly.graph_objects as go

from examples.IN5060_visualizer import visualize
from examples.custom_maps import *
from pathfinding3d.core.diagonal_movement import DiagonalMovement
from pathfinding3d.core.grid import Grid
from pathfinding3d.core.heuristic import *
from pathfinding3d.finder.a_star import AStarFinder
from pathfinding3d.finder.breadth_first import BreadthFirstFinder
from pathfinding3d.finder.dijkstra import DijkstraFinder
from pathfinding3d.finder.bi_a_star import BiAStarFinder
from pathfinding3d.finder.theta_star import ThetaStarFinder

class Node:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def __repr__(self):
        return f"Node({self.x}, {self.y}, {self.z})"

class Run:
    def __init__(self, name, start, end, time, operations, cost, steps):
        self.name = name
        self.start = start
        self.end = end
        self.time = time
        self.operations = operations
        self.cost = cost
        self.steps = steps

    def __repr__(self):
        return f"Run(name: {self.name}, start: xyz=({start.x}, {start.y}, {start.z}), end: xyz=({end.x}, {end.y}, time(s): {self.time}, {end.z}), operations: {operations}, cost: {self.cost}, steps: {self.steps})"

class Result:
    name = None
    runs = []
    def __init__(self, name, runs):
        self.name = name
        self.runs = runs

    def __repr__(self):
        return f"Result({self.name}, {self.runs})"

results = []


#Multiple modes, Individual (one plot for each combo), Combined (all at once...) and Last
visualizeMode = "individual"

# 2 Obstacle mode, Cubes and Volume
obstacleMode = "Cubes"

matrix = getMap4()
max_x, max_y, max_z = len(matrix.matrix), len(matrix.matrix[0]), len(matrix.matrix[0][0])

# Create a 3D numpy array with 0s as obstacles and 1s as walkable paths
# Create a grid object from the numpy array
grid = Grid(matrix=matrix.matrix
            # , grounded=True, max_fly=10
            )
# Mark the start and end points
start_points = [grid.node(start.x, start.y, start.z) for start in matrix.start_points]
end_points = [grid.node(end.x, end.y, end.z) for end in matrix.end_points]

algo_list = ["Dijkstra", "BFS",
             "A*", "Bi A*",
             # "A* (octile)", "Bi A* (octile)", # Octile heuristic is default heuristic, but might be interesting too look at?
             # "A* (euclidean)", "Bi A* (euclidean)",
             "Theta*" # Theta* is pretty neat, but also pretty weird... idk if we should include it.
             ]

# Colours are added to the algo based on index, so algo[0] has colours[0], etc.
colours = [
    '#636EFA',
    '#EF553B',
    '#00CC96',
    '#AB63FA',
    '#FFA15A',
    '#19D3F3',
    '#FF6692',
    '#B6E880',
    '#FF97FF',
    '#FECB52',
]


point_offset = 0.0

def pathfinder(algorithm, l_start, l_end):
    finder = None
    match algorithm:
        case "Dijkstra": finder = DijkstraFinder(diagonal_movement=DiagonalMovement.always)
        case "A*": finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        case "Bi A*": finder = BiAStarFinder(diagonal_movement=DiagonalMovement.always)
        case "BFS": finder = BreadthFirstFinder(diagonal_movement=DiagonalMovement.always)

        case "A* (octile)": finder = AStarFinder(diagonal_movement=DiagonalMovement.always, heuristic=octile)
        case "Bi A* (octile)": finder = BiAStarFinder(diagonal_movement=DiagonalMovement.always, heuristic=octile)

        case "A* (euclidean)": finder = AStarFinder(diagonal_movement=DiagonalMovement.always, heuristic=euclidean)
        case "Bi A* (euclidean)": finder = BiAStarFinder(diagonal_movement=DiagonalMovement.always, heuristic=euclidean)

        case "Theta*": finder = ThetaStarFinder(diagonal_movement=DiagonalMovement.always)

    path , operations = finder.find_path(l_start, l_end, grid)
    path = [p.identifier for p in path]

    print(algorithm, " operations:", operations, algorithm, " path steps: ", len(path))
    print(algorithm, " path:", path)

    return path, operations


def calculate_path_cost(path):
    total_cost = 0
    for pt, pt_next in zip(path[:-1], path[1:]):
        dx, dy, dz = pt_next[0] - pt[0], pt_next[1] - pt[1], pt_next[2] - pt[2]
        total_cost += (dx**2 + dy**2 + dz**2) ** 0.5
    return total_cost

def add_to_subtitle(algorithm, operations, cost, path):
    return f"""
    {algorithm}:<br>
        Operations: {operations}<br>
        Cost: {cost:.2f}<br>
        "Steps": {len(path)}
    <br>"""

def create_data_points(algorithm, path):
    color = colours[i]
    return go.Scatter3d(
            x=[pt[0] + point_offset for pt in path],
            y=[pt[1] + point_offset for pt in path],
            z=[pt[2] + point_offset for pt in path],
            mode="lines + markers",
            line=dict(width=4, color=color),
            marker=dict(size=4, color=color),
            name= algorithm + " path",
            hovertext=[algorithm + " path point"] * len(path),
        )

datapoints = [] # Keep last datapoints for displaymode "Last"
subtitle = f"""""" # Same for subtitle
all_data_points = []

for start in start_points:
    for end in end_points:
        datapoints = []
        subtitle = f""""""
        for i, algo in enumerate(algo_list):
            start_time = time.time()

            path, operations = pathfinder(algo, start, end)

            end_time = time.time()
            time_taken = end_time - start_time

            ## Calculations for visualisations and data gathering, not sure if it should be a part of the time taken or not?
            cost = calculate_path_cost(path)
            all_data_points.append(create_data_points(algo, path))
            subtitle += add_to_subtitle(algo, operations, cost, path)
            datapoints.append(create_data_points(algo, path))
            grid.cleanup()

            run = Run(algo, start, end, time_taken, operations, cost, len(datapoints))

            added = False
            for ri, result in enumerate(results):
                if result.name.lower() == algo.lower():
                    results[ri].runs.append(run)
                    added = True
                    break

            if not added:
                results.append(Result(algo.lower(), [run]))


        if visualizeMode.lower() == "individual": visualize(grid=grid, start=start, end=end,
                  max_x=max_x, max_y=max_y, max_z=max_z,
                  datapoints=datapoints, subtitle=subtitle)

if visualizeMode.lower() == "combined": visualize(grid=grid, start=start_points, end=end_points,
          max_x=max_x, max_y=max_y, max_z=max_z,
          datapoints=all_data_points)

if visualizeMode.lower() == "last": visualize(grid=grid, start=start_points[-1], end=end_points[-1],
                                              max_x=max_x, max_y=max_y, max_z=max_z, datapoints=datapoints, subtitle=subtitle)

print(results)