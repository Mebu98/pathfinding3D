import random
from random import Random
from typing import Optional

import plotly.graph_objects as go
import numpy as np
from _plotly_utils.colors.qualitative import Plotly
from narwhals import Array
from plotly.graph_objs import Figure, Volume

from examples.custom_maps import Node


def visualize(grid, start, end,
                  max_x, max_y, max_z,
                  datapoints, subtitle: Optional[str] = None,
              point_offset: Optional[float] = 0.0,
              obs_offset: Optional[float] = .5,
              obstacle_mode: Optional[str] = "cubes",):

    fig = create_fig(grid, datapoints, start, end, max_x, max_y, max_z, obstacle_mode, point_offset, obs_offset, subtitle)

    # Save the figure as a html file
    # Show the figure in a new tab
    fig.write_html(f"theta_star.html", full_html=False, include_plotlyjs="cdn")
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

    # return fig


def create_fig(grid, datapoints, start, end, max_x, max_y, max_z, obstacle_mode: str | None, point_offset: float | None, obs_offset: float | None,
               subtitle: str | None) -> Figure:
    layout = go.Layout(
        scene=go.layout.Scene(
            aspectmode='manual',
            aspectratio=go.layout.scene.Aspectratio(
                x=1, y=max_y / max_x, z=max_z / max_x,
            ))
    )

    start_arr = np.array(start) if type(start) is list else [start]
    end_arr = np.array(end) if type(end) is list else [end]

    fig = go.Figure(
        layout=layout,
        data=[
            # Add start and endpoints
            go.Scatter3d(
                x=[s.x + point_offset for s in start_arr],
                y=[s.y + point_offset for s in start_arr],
                z=[s.z + point_offset for s in start_arr],
                mode="markers",
                marker=dict(color="green", size=10),
                name="Start",
                hovertext=["Start point"],
            ),
            go.Scatter3d(
                x=[end.x + point_offset for end in end_arr],
                y=[end.y + point_offset for end in end_arr],
                z=[end.z + point_offset for end in end_arr],
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
                    showlegend=[False, True][n == 1],
                    color="black",
                    opacity=.25,
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

    if obstacle_mode.lower() == "cubes":
        cubes = obs_cubes()
        for cube in cubes:
            fig.add_trace(cube)
    elif obstacle_mode.lower() == "volume":
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
                range=[0, max_x - .5],
                dtick=1,
            ),
            yaxis=dict(
                title="y - axis",
                backgroundcolor="white",
                gridcolor="lightgrey",
                showbackground=True,
                zerolinecolor="white",
                range=[0, max_y - .5],
                dtick=1,
            ),
            zaxis=dict(
                title="z - axis",
                backgroundcolor="white",
                gridcolor="lightgrey",
                showbackground=True,
                zerolinecolor="white",
                range=[0, max_z - .5],
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
        """, ),
        font=dict(
            family="Courier New, monospace",
        ),
    )
    return fig
