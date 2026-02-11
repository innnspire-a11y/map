import streamlit as st
import plotly.graph_objects as go

# Function to create 3D rectangular prisms (Walls)
def add_3d_wall(fig, x_range, y_range, z_range, name="Wall", color='firebrick'):
    fig.add_trace(go.Mesh3d(
        x=[x_range[0], x_range[1], x_range[1], x_range[0], x_range[0], x_range[1], x_range[1], x_range[0]],
        y=[y_range[0], y_range[0], y_range[1], y_range[1], y_range[0], y_range[0], y_range[1], y_range[1]],
        z=[z_range[0], z_range[0], z_range[0], z_range[0], z_range[1], z_range[1], z_range[1], z_range[1]],
        # Explicit triangle definitions for a clean cube/box
        i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
        j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
        k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
        opacity=0.9,
        color=color,
        flatshading=True,
        name=name,
        showlegend=True
    ))

st.set_page_config(layout="wide")
st.title("Building Survey: Final Accurate Digital Twin")

fig = go.Figure()

# --- WALL THICKNESS PARAMETER (22cm) ---
T = 0.22 

# --- 1. NORTH WALL (Main 4.84m) ---
add_3d_wall(fig, [0, 4.84], [-T, 0], [0, 2.5], "North Wall")

# --- 2. EAST WALL (The Colonnade at X = 4.84) ---
# Thickness pushed East (Positive X)
add_3d_wall(fig, [4.84, 4.84+T], [0, 0.90], [0, 2.5], "East Corner Pillar")
add_3d_wall(fig, [4.84, 4.84+T], [0.90, 2.99], [0, 0.17], "East Curb")
add_3d_wall(fig, [4.84, 4.84+T], [2.99, 4.53], [0, 2.5], "East Mid Pillar")
add_3d_wall(fig, [4.84, 4.84+T], [4.53, 7.03], [0, 0.0], "East Curb 2")
add_3d_wall(fig, [4.84, 4.84+T], [7.03, 7.72], [0, 2.5], "East Corner South")

# --- 3. WEST WALL (Door Frames at X = 0) ---
# Thickness pushed West (Negative X)
add_3d_wall(fig, [-T, 0], [0, 1.15], [0, 2.5], "West Pillar 1")
add_3d_wall(fig, [-T, 0], [1.15, 2.11], [2.06, 2.5], "West Door Header 1") 
add_3d_wall(fig, [-T, 0], [2.11, 5.20], [0, 2.5], "West Mid Wall")
add_3d_wall(fig, [-T, 0], [5.20, 6.01], [2.09, 2.5], "West Door Header 2")
add_3d_wall(fig, [-T, 0], [6.01, 7.72], [0, 2.5], "West Pillar 2")

# --- 4. SOUTH WALL (Closing the Box at Y = 7.72) ---
# Thickness pushed South (Positive Y)
# SW Segment
add_3d_wall(fig, [0, 1.96], [7.72, 7.72+T], [0, 2.5], "South SW Corner") 
# South Door (81cm wide) starts at 1.96m, ends at 2.77m
add_3d_wall(fig, [1.96, 2.77], [7.72, 7.72+T], [2.09, 2.5], "South Door Header")
# Final Main Section (2.77m to 4.84m)
add_3d_wall(fig, [2.77, 4.84], [7.72, 7.72+T], [0, 2.5], "South Wall Main")

# Camera and Scene Settings
fig.update_layout(
    scene=dict(
        aspectmode='data',
        xaxis=dict(title='Width (X) in meters'),
        yaxis=dict(title='Depth (Y) in meters'),
        zaxis=dict(title='Height (Z) in meters'),
        camera=dict(eye=dict(x=1.2, y=1.2, z=1.2))
    ),
    margin=dict(l=0, r=0, b=0, t=50)
)


st.plotly_chart(fig, use_container_width=True)
