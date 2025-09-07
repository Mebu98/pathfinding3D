"""
This example shows how Dijkstra algorithm differs from A* algorithm
Requires plotly for visualization. Install it using `pip install plotly`
"""

import plotly.graph_objects as go
import plotly.io as pio
from plotly.graph_objs import Volume

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
grid = Grid(matrix=matrix.matrix, grounded=True)

# Mark the start and end points
start = grid.node(matrix.start.x, matrix.start.y, matrix.start.z)
end = grid.node(matrix.end.x, matrix.end.y, matrix.end.z)

algo_list = ["Dijkstra", "BFS",
             "A* (octile)", "Bi A* (octile)", # Octile heuristic is default heuristic, but might be interesting too look at?
             "A* (euclidean)", "Bi A* (euclidean)"
             # "Theta*", # Theta* is pretty neat, but also pretty weird... idk if we should include it.
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

subtitle = f""""""
datapoints = []

point_offset = 0.0

def pathfinder(algorithm):
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

    path , operations = finder.find_path(start, end, grid)
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
    color = colours.pop(0)
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

for item in algo_list:
    path, operations = pathfinder(item)
    cost = calculate_path_cost(path)
    subtitle += add_to_subtitle(item, operations, cost, path)
    datapoints.append(create_data_points(item, path))
    grid.cleanup()

layout = go.Layout(
    scene = go.layout.Scene(
    aspectmode='manual',
    aspectratio=go.layout.scene.Aspectratio(
        x=1, y=max_y/max_x, z=max_z/max_x,
    ))
)

fig = go.Figure(
    layout=layout,
    data=[
        # Add start and endpoints
        go.Scatter3d(
            x=[start.x + point_offset],
            y=[start.y + point_offset],
            z=[start.z + point_offset],
            mode="markers",
            marker=dict(color="green", size=10),
            name="Start",
            hovertext=["Start point"],
        ),
        go.Scatter3d(
            x=[end.x + point_offset],
            y=[end.y + point_offset],
            z=[end.z + point_offset],
            mode="markers",
            marker=dict(color="orange", size=10),
            name="End",
            hovertext=["End point"],
        ),
    ]
)
for datapoint in datapoints:
    fig.add_trace(datapoint)

def obs_volume():
    # Extract obstacle and weight information directly from the grid
    X, Y, Z, obstacle_values, weight_values, obstacle_vol = [], [], [], [], [], Volume
    for x in range(max_x):
        for y in range(max_y):
            for z in range(max_z):
                node = grid.node(x, y, z)
                X.append(x)
                Y.append(y)
                Z.append(z)
                obstacle_values.append(0 if node.walkable else 1)
                weight_values.append(node.weight if node.walkable else 0)

            # Create obstacle volume visualization
            obstacle_vol = go.Volume(
                x=np.array(X),
                y=np.array(Y),
                z=np.array(Z),
                value=np.array(obstacle_values),
                isomin=0.5,
                isomax=1.0,
                opacity=0.1,
                surface_count=5,  # Increase for better visibility
                colorscale="Greys",
                showscale=False,
                name="Obstacles",
                hovertext=["Obstacles"],
            )
    return obstacle_vol


# 3d boxes for obstacles instead of volume... idk how to make it good :(
def obs_cubes():
    return_cubes = []
    obs_offset = .5
    obs_scale = [1, 1, 1]
    obstacle_nodes = []

    for x in range(max_x):
        for y in range(max_y):
            for z in range(max_z):
                node = grid.node(x, y, z)
                if node.weight == 0:
                    obstacle_nodes.append(Node(x, y, z))

    for n, pt in enumerate(obstacle_nodes):

        mesh_x = [0, 0, 1, 1, 0, 0, 1, 1]
        mesh_y = [0, 1, 1, 0, 0, 1, 1, 0]
        mesh_z = [0, 0, 0, 0, 1, 1, 1, 1]

        for i in range(len(mesh_x)):
            mesh_x[i] = (mesh_x[i] * obs_scale[0]) + pt.x - obs_offset
            mesh_y[i] = (mesh_y[i] * obs_scale[1]) + pt.y - obs_offset
            mesh_z[i] = (mesh_z[i] * obs_scale[2]) + pt.z - obs_offset

        return_cubes.append(
            go.Mesh3d(
                hovertext="obstacle",
                name="Obstacles",
                legendgroup="obstacles",
                showlegend=[False, True][n==1],
                color="blue",
                opacity=.05,
                alphahull=1,
                flatshading=True,
                x=mesh_x,
                y=mesh_y,
                z=mesh_z,
                # x=[pt.x- 1 + obs_offset, pt.x - 1 + obs_offset, pt.x + obs_offset, pt.x + obs_offset, pt.x-1 + obs_offset, pt.x-1 + obs_offset, pt.x + obs_offset, pt.x + obs_offset],
                # y=[pt.y- 1 + obs_offset, pt.y + obs_offset, pt.y + obs_offset, pt.y-1 + obs_offset, pt.y-1 + obs_offset, pt.y + obs_offset, pt.y + obs_offset, pt.y-1 + obs_offset],
                # z=[pt.z -1 + obs_offset, pt.z - 1 + obs_offset, pt.z - 1 + obs_offset, pt.z - 1 + obs_offset, pt.z + obs_offset, pt.z + obs_offset, pt.z + obs_offset, pt.z + obs_offset],
            )
        )
    return return_cubes

if obstacleMode.lower() == "cubes":
    cubes = obs_cubes()
    for cube in cubes:
        fig.add_trace(cube)
elif obstacleMode.lower() == "volume":
    fig.add_trace(obs_volume())

# Create a plotly figure to visualize the path

fig.update_layout(
    scene=dict(
        xaxis=dict(
            title="x - axis",
            backgroundcolor="white",
            gridcolor="lightgrey",
            showbackground=True,
            zerolinecolor="white",
            range=[0, max_x-.5],
            dtick=1,
        ),
        yaxis=dict(
            title="y - axis",
            backgroundcolor="white",
            gridcolor="lightgrey",
            showbackground=True,
            zerolinecolor="white",
            range=[0, max_y-.5],
            dtick=1,
        ),
        zaxis=dict(
            title="z - axis",
            backgroundcolor="white",
            gridcolor="lightgrey",
            showbackground=True,
            zerolinecolor="white",
            range=[0, max_z-.5],
            dtick=1,
        ),
    ),
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="right",
        x=0.99,
        bgcolor="rgba(255, 255, 255, 0.7)",
    ),
    ## Title takes html <br>
    title=dict(text=f"""
                    Dijkstra vs A* 
                    <br><sup>{subtitle}</sup>
    """,),
    font=dict(
                family="Courier New, monospace",
    ),
)

# Save the figure as a html file
# Show the figure in a new tab
fig.write_html("theta_star.html", full_html=False, include_plotlyjs="cdn")
fig.show()

# grid.visualize(
#   path=astar_path,  # optionally visualize the path
#   start=start,
#   end=end,
#   visualize_weight=True,  # weights above 1 (default) will be visualized
#   save_html=True,  # save visualization to html file
#   save_to="path_visualization.html",  # specify the path to save the html file
#   always_show=True,  # always show the visualization in the browser
# )
