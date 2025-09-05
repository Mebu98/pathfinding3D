"""
This example shows how Dijkstra algorithm differs from A* algorithm
Requires plotly for visualization. Install it using `pip install plotly`
"""

import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px

from examples.custom_maps import *
from pathfinding3d.core.diagonal_movement import DiagonalMovement
from pathfinding3d.core.grid import Grid
from pathfinding3d.finder.a_star import AStarFinder
from pathfinding3d.finder.breadth_first import BreadthFirstFinder
from pathfinding3d.finder.dijkstra import DijkstraFinder
from pathfinding3d.finder.bi_a_star import BiAStarFinder
from pathfinding3d.finder.theta_star import ThetaStarFinder

#pio.renderers.default = "browser"
matrix = getMap3()
max_x, max_y, max_z = len(matrix.matrix), len(matrix.matrix[0]), len(matrix.matrix[0][0])

print(matrix.matrix)

class Node:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

# Create a 3D numpy array with 0s as obstacles and 1s as walkable paths
# matrix = np.ones((max_x, max_y, max_z), dtype=np.int8)
# obstacles are marked with 0

# obstacles = [Node(x,y,2) for x in range(10) for y in range(9)]
# obstacles.extend(Node(x, y, 4) for x in range(10) for y in range(1, 10))
#
# for obs in obstacles:
#     matrix[obs.x, obs.y, obs.z] = 0


# Create a grid object from the numpy array
grid = Grid(matrix=matrix.matrix)

# Mark the start and end points

# start = grid.node(0, 0, 0)
# end = grid.node(max_x-1, 0, max_z-1)
start = grid.node(matrix.start.x, matrix.start.y, matrix.start.z)
end = grid.node(matrix.end.x, matrix.end.y, matrix.end.z)

list = ["Dijkstra", "BFS", "A*","Bi A*", "Theta*"]
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

def pathfinder(algorithm):
    finder = None
    match algorithm:
        case "Dijkstra": finder = DijkstraFinder(diagonal_movement=DiagonalMovement.always)
        case "A*": finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        case "Bi A*": finder = BiAStarFinder(diagonal_movement=DiagonalMovement.always)
        case "BFS": finder = BreadthFirstFinder(diagonal_movement=DiagonalMovement.always)
        case "Theta*": finder = ThetaStarFinder(diagonal_movement=DiagonalMovement.only_when_no_obstacle)

    path , operations = finder.find_path(start, end, grid)
    path = [p.identifier for p in path]

    print(algorithm, " operations:", operations, algorithm, " path length: ", len(path))
    print(algorithm, " path:", path)

    return path, operations


def calculate_path_cost(path):
    cost = 0
    for pt, pt_next in zip(path[:-1], path[1:]):
        dx, dy, dz = pt_next[0] - pt[0], pt_next[1] - pt[1], pt_next[2] - pt[2]
        cost += (dx**2 + dy**2 + dz**2) ** 0.5
    return cost

def addtosubtitle(algorithm, operations, cost, path):
    return f"""
    {algorithm}:<br>
        Operations: {operations}<br>
        Cost: {cost:.2f}<br>
        Length: {len(path)}
    <br>"""

def createdatapoints(algorithm, path):
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

subtitle = f""""""
datapoints = []

for item in list:
    path, operations = pathfinder(item)
    cost = calculate_path_cost(path)
    subtitle += addtosubtitle(item, operations, cost, path)
    datapoints.append(createdatapoints(item, path))
    grid.cleanup()


# Extract obstacle and weight information directly from the grid
X, Y, Z, obstacle_values, weight_values = [], [], [], [], []
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
            isomin=0.9,
            isomax=1.0,
            opacity=0.1,
            surface_count=5,  # Increase for better visibility
            colorscale="Greys",
            showscale=False,
            name="Obstacles",
        )


layout = go.Layout(
    scene = go.layout.Scene(
    aspectmode='manual',
    aspectratio=go.layout.scene.Aspectratio(
        x=1, y=max_y/max_x, z=max_z/max_x,
    ))
)

def createCube(x,y,z):
    return go.Mesh3d(
        hovertext="cube",
        x=[0, 0, x, x, 0, 0, x, x],
        y=[0, y, y, 0, 0, y, y, 0],
        z=[0, 0, 0, 0, z, z, z, z],

        i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
        j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
        k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
    ),

obstacles = []

for x in range(max_x):
    for y in range(max_y):
        for z in range(max_z):
            node = grid.node(x, y, z)
            if not node.walkable:
                obstacles.append(Node(x, y, z))

fig = go.Figure(
    layout=layout,
    data=[
        # obstacle_vol,
        # go.Mesh3d(
        #     hovertext="obstacle",
        #     x=[[pt.x-1, pt.x-1, pt.x, pt.x, pt.x-1, pt.x-1, pt.x, pt.x] for pt in obstacles],
        #     y=[[pt.y-1, pt.y, pt.y, pt.y-1, pt.y-1, pt.y, pt.y, pt.y-1] for pt in obstacles],
        #     z=[[pt.z-1, pt.z-1, pt.z-1, pt.z-1, pt.z, pt.z, pt.z, pt.z] for pt in obstacles],
        #
        #     i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
        #     j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
        #     k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
        # ),
        # go.Scatter3d(
        #     x=[pt.x + point_offset for pt in obstacles],
        #     y=[pt.y + point_offset for pt in obstacles],
        #     z=[pt.z + point_offset for pt in obstacles],
        #     mode="markers",
        #
        #     marker=dict(color="black", size=7.5),
        #     name="Obstacle",
        #     hovertext=["Obstacle point"],
        # ),
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

obs_offset = .5
obs_scale = [1, 1, 1]

# 3d boxes for obstacles instead of volume... idk how to make it good :(
for pt in obstacles:
    mesh_x = [0, 0, 1, 1, 0, 0, 1, 1]
    mesh_y = [0, 1, 1, 0, 0, 1, 1, 0]
    mesh_z = [0, 0, 0, 0, 1, 1, 1, 1]

    for i in range(len(mesh_x)):
        mesh_x[i] = (mesh_x[i] * obs_scale[0]) + pt.x - obs_offset
        mesh_y[i] = (mesh_y[i] * obs_scale[1]) + pt.y - obs_offset
        mesh_z[i] = (mesh_z[i] * obs_scale[2]) + pt.z - obs_offset

    fig.add_trace(
        go.Mesh3d(
                hovertext="obstacle",
                color = "blue",
                opacity=.05,
                alphahull=1,
                x = mesh_x,
                y = mesh_y,
                z = mesh_z,
                # x=[pt.x- 1 + obs_offset, pt.x - 1 + obs_offset, pt.x + obs_offset, pt.x + obs_offset, pt.x-1 + obs_offset, pt.x-1 + obs_offset, pt.x + obs_offset, pt.x + obs_offset],
                # y=[pt.y- 1 + obs_offset, pt.y + obs_offset, pt.y + obs_offset, pt.y-1 + obs_offset, pt.y-1 + obs_offset, pt.y + obs_offset, pt.y + obs_offset, pt.y-1 + obs_offset],
                # z=[pt.z -1 + obs_offset, pt.z - 1 + obs_offset, pt.z - 1 + obs_offset, pt.z - 1 + obs_offset, pt.z + obs_offset, pt.z + obs_offset, pt.z + obs_offset, pt.z + obs_offset],
        )
    )

# Create a plotly figure to visualize the path

fig.update_layout(
    scene=dict(
        xaxis=dict(
            title="x - axis",
            backgroundcolor="white",
            gridcolor="lightgrey",
            showbackground=True,
            zerolinecolor="white",
            range=[0, max_x-1],
            dtick=1,
        ),
        yaxis=dict(
            title="y - axis",
            backgroundcolor="white",
            gridcolor="lightgrey",
            showbackground=True,
            zerolinecolor="white",
            range=[0, max_y-1],
            dtick=1,
        ),
        zaxis=dict(
            title="z - axis",
            backgroundcolor="white",
            gridcolor="lightgrey",
            showbackground=True,
            zerolinecolor="white",
            range=[0, max_z-1],
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
