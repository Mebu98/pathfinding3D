"""
This example shows how Dijkstra algorithm differs from A* algorithm
Requires plotly for visualization. Install it using `pip install plotly`
"""

import plotly.graph_objects as go
import plotly.io as pio
from plotly.graph_objs import Volume

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

# Change this to change Plotly renderer
# Available renderers:
#         ['plotly_mimetype', 'jupyterlab', 'nteract', 'vscode',
#          'notebook', 'notebook_connected', 'kaggle', 'azure', 'colab',
#          'cocalc', 'databricks', 'json', 'png', 'jpeg', 'jpg', 'svg',
#          'pdf', 'browser', 'firefox', 'chrome', 'chromium', 'iframe',
#          'iframe_connected', 'sphinx_gallery', 'sphinx_gallery_png']
# pio.renderers.default = "browser"

# 2 Obstacle modes so far, Cubes and Volume
obstacleMode = "Cubes"
matrix = getMap4()
max_x, max_y, max_z = len(matrix.matrix), len(matrix.matrix[0]), len(matrix.matrix[0][0])


# Create a 3D numpy array with 0s as obstacles and 1s as walkable paths
# Create a grid object from the numpy array
grid = Grid(matrix=matrix.matrix)
# Mark the start and end points
start_points = [grid.node(matrix.start.x, matrix.start.y, matrix.start.z)]
end_points = [grid.node(matrix.end.x, matrix.end.y, matrix.end.z)]

algo_list = ["Dijkstra", "BFS",
             "A* (octile)", "Bi A* (octile)", # Octile heuristic is default heuristic, but might be interesting too look at?
             "A* (euclidean)", "Bi A* (euclidean)",
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

for start in start_points:
    for end in end_points:
        datapoints = []
        subtitle = f""""""
        for i, item in enumerate(algo_list):
            path, operations = pathfinder(item, start, end)
            cost = calculate_path_cost(path)
            subtitle += add_to_subtitle(item, operations, cost, path)
            datapoints.append(create_data_points(item, path))
            grid.cleanup()

        visualize(grid=grid, start=start, end=end,
                  max_x=max_x, max_y=max_y, max_z=max_z,
                  datapoints=datapoints, subtitle=subtitle)
