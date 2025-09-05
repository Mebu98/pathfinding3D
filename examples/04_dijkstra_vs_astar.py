"""
This example shows how Dijkstra algorithm differs from A* algorithm
Requires plotly for visualization. Install it using `pip install plotly`
"""

import numpy as np
import plotly.graph_objects as go

from examples.custom_maps import *
from pathfinding3d.core.diagonal_movement import DiagonalMovement
from pathfinding3d.core.grid import Grid
from pathfinding3d.finder.a_star import AStarFinder
from pathfinding3d.finder.dijkstra import DijkstraFinder

matrix = getMap2()
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


# Create an instance of the Dijkstra finder with diagonal movement allowed
finder = DijkstraFinder(diagonal_movement=DiagonalMovement.always)
dijkstra_path, dijkstra_operations = finder.find_path(start, end, grid)

# Path will be a list with all the waypoints as nodes
# Convert it to a list of coordinate tuples
dijkstra_path = [p.identifier for p in dijkstra_path]

print("Dijkstra operations:", dijkstra_operations, "Dijkstra path length:", len(dijkstra_path))
print("Dijkstra path:", dijkstra_path)

# # clean up the grid
grid.cleanup()

# Create an instance of the A* finder with diagonal movement allowed
finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
astar_path, astar_operations = finder.find_path(start, end, grid)

astar_path = [p.identifier for p in astar_path]

print("AStarFinder operations:", astar_operations, "AStarFinder path length:", len(astar_path))
print("AStarFinder path:", astar_path)


def calculate_path_cost(path):
    cost = 0
    for pt, pt_next in zip(path[:-1], path[1:]):
        dx, dy, dz = pt_next[0] - pt[0], pt_next[1] - pt[1], pt_next[2] - pt[2]
        cost += (dx**2 + dy**2 + dz**2) ** 0.5
    return cost


dijkstra_cost = calculate_path_cost(dijkstra_path)
astar_cost = calculate_path_cost(astar_path)

print("Dijkstra path cost:", dijkstra_cost, "\nAStar path cost:", astar_cost)

subtitle = (f"""
    Dijkstra:<br>
        Operations: {dijkstra_operations}<br>
        Cost: {dijkstra_cost:.2f}<br>
        Length: {len(dijkstra_path)}
    <br>
    A*:<br>
        Operations: {astar_operations}<br>
        Cost: {astar_cost:.2f} <br>
        Length: {len(astar_path)}
""")
point_offset = .0


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
            isomin=0.7,
            isomax=1.0,
            opacity=0.1,
            surface_count=5,  # Increase for better visibility
            colorscale="Greys",
            showscale=False,
            name="Obstacles",
        )

fig = go.Figure(
    data=[
        go.Scatter3d(
            x=[pt[0] + point_offset for pt in dijkstra_path],
            y=[pt[1] + point_offset for pt in dijkstra_path],
            z=[pt[2] + point_offset for pt in dijkstra_path],
            mode="lines + markers",
            line=dict(color="blue", width=4),
            marker=dict(size=4, color="blue"),
            name="Dijkstra path",
            hovertext=["Dijkstra path point"] * len(dijkstra_path),
        ),
        go.Scatter3d(
            x=[pt[0] + point_offset for pt in astar_path],
            y=[pt[1] + point_offset for pt in astar_path],
            z=[pt[2] + point_offset for pt in astar_path],
            mode="lines + markers",
            line=dict(color="red", width=4),
            marker=dict(size=4, color="red"),
            name="A* path",
            hovertext=["A* path point"] * len(astar_path),
        ),
        obstacle_vol,
        # go.Volume(
            # x=[pt.x + point_offset for pt in obstacles],
            # y=[pt.y + point_offset for pt in obstacles],
            # z=[pt.z + point_offset for pt in obstacles],
            # value=np.array([1 for obs in obstacles]),
            # isomin=0.1,
            # isomax=1.0,
            # opacity=0.1,
            # surface_count=20,  # Increase for better visibility
            # colorscale="Greys",
            # showscale=False,
            # name="Obstacles",
        # ),
        # go.Mesh3d(
        #     x=[pt.x + point_offset for pt in obstacles],
        #     y=[pt.y + point_offset for pt in obstacles],
        #     z=[pt.z + point_offset for pt in obstacles],
        #
        #     i = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
        #     j = [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
        #     k = [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
        #
        #     opacity=0.1,
        #     colorscale="Greys",
        #     name="Obstacles",
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
            marker=dict(color="green", size=7.5),
            name="Start",
            hovertext=["Start point"],
        ),
        go.Scatter3d(
            x=[end.x + point_offset],
            y=[end.y + point_offset],
            z=[end.z + point_offset],
            mode="markers",
            marker=dict(color="orange", size=7.5),
            name="End",
            hovertext=["End point"],
        ),
    ]
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
