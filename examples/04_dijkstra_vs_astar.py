"""
This example shows how Dijkstra algorithm differs from A* algorithm
Requires plotly for visualization. Install it using `pip install plotly`
"""

import numpy as np
import plotly.graph_objects as go

from pathfinding3d.core.diagonal_movement import DiagonalMovement
from pathfinding3d.core.grid import Grid
from pathfinding3d.finder.a_star import AStarFinder
from pathfinding3d.finder.dijkstra import DijkstraFinder

width, height, depth = 10, 10, 10

# Create a 3D numpy array with 0s as obstacles and 1s as walkable paths
matrix = np.ones((width, height, depth), dtype=np.int8)
# obstacles are marked with 0

obstacles = [[x, y, 5] for x in range(10) for y in range(9)]

print(obstacles)
for obs in obstacles:
    matrix[obs[0], obs[1], obs[2]] = 0
# Create a grid object from the numpy array
grid = Grid(matrix=matrix)

# Mark the start and end points
start = grid.node(0, 0, 0)
end = grid.node(9, 0, 9)

# Create an instance of the Dijkstra finder with diagonal movement allowed
finder = DijkstraFinder(diagonal_movement=DiagonalMovement.always)
dijkstra_path, dijkstra_operations = finder.find_path(start, end, grid)

# Path will be a list with all the waypoints as nodes
# Convert it to a list of coordinate tuples
dijkstra_path = [p.identifier for p in dijkstra_path]

print("Dijkstra operations:", dijkstra_operations, "Dijkstra path length:", len(dijkstra_path))
print("Dijkstra path:", dijkstra_path)

# clean up the grid
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
    A:<br>
        Operations: {astar_operations}<br>
        Cost: {astar_cost:.2f} <br>
        Length: {len(astar_path)}
""")
point_offset = .5

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
            y=[pt[1] + point_offset for pt in astar_path],
            x=[pt[0] + point_offset for pt in astar_path],
            z=[pt[2] + point_offset for pt in astar_path],
            mode="lines + markers",
            line=dict(color="red", width=4),
            marker=dict(size=4, color="red"),
            name="A* path",
            hovertext=["A* path point"] * len(astar_path),
        ),
        # go.Scatter3d(
        #     x=[5.5],
        #     y=[5.5],
        #     z=[5.5],
        #     mode="markers",
        #     marker=dict(color="black", size=7.5),
        #     name="Obstacle",
        #     hovertext=["Obstacle point"],
        # ),
        go.Volume(
            x=[pt[0] + point_offset for pt in obstacles],
            y=[pt[1] + point_offset for pt in obstacles],
            z=[pt[2] + point_offset for pt in obstacles],
            value=np.array([1 for obs in obstacles]),
            isomin=0.1,
            isomax=1.0,
            opacity=0.1,
            surface_count=100,  # Increase for better visibility
            colorscale="Greys",
            showscale=False,
            name="Obstacles",
        ),
        # go.Scatter3d(
        #     x=[pt[0] + point_offset for pt in obstacles],
        #     y=[pt[1] + point_offset for pt in obstacles],
        #     z=[pt[2] + point_offset for pt in obstacles],
        #     mode="lines + markers",
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
            range=[0, 10],
            dtick=1,
        ),
        yaxis=dict(
            title="y - axis",
            backgroundcolor="white",
            gridcolor="lightgrey",
            showbackground=True,
            zerolinecolor="white",
            range=[0, 10],
            dtick=1,
        ),
        zaxis=dict(
            title="z - axis",
            backgroundcolor="white",
            gridcolor="lightgrey",
            showbackground=True,
            zerolinecolor="white",
            range=[0, 10],
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
# fig.write_html("theta_star.html", full_html=False, include_plotlyjs="cdn")
# Show the figure in a new tab
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
