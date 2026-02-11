import streamlit as st
import plotly.graph_objects as go

# Function to create 3D rectangular prisms
def add_3d_wall(fig, x_range, y_range, z_range, name="Wall", color='firebrick', opacity=0.9):
    fig.add_trace(go.Mesh3d(
        x=[x_range[0], x_range[1], x_range[1], x_range[0], x_range[0], x_range[1], x_range[1], x_range[0]],
        y=[y_range[0], y_range[0], y_range[1], y_range[1], y_range[0], y_range[0], y_range[1], y_range[1]],
        z=[z_range[0], z_range[0], z_range[0], z_range[0], z_range[1], z_range[1], z_range[1], z_range[1]],
        i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
        j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
        k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
        opacity=opacity,
        color=color,
        flatshading=True,
        name=name
    ))

st.set_page_config(layout="wide")
st.title("Building Survey: Integrated Master Digital Twin")

fig = go.Figure()

# --- CONSTANTS ---
T = 0.22             # Wall Thickness
CEILING_SLAB = 2.73  # Calibrated slab height

# --- 1. MAIN HALL (ROOM 1) PERIMETER ---
# North Wall
add_3d_wall(fig, [0, 4.84], [-T, 0], [0, CEILING_SLAB], "R1 North Wall")
# West Wall (Headers & Pillars)
add_3d_wall(fig, [-T, 0], [0, 1.15], [0, CEILING_SLAB], "West Pillar 1")
add_3d_wall(fig, [-T, 0], [1.15, 2.11], [2.06, CEILING_SLAB], "West Door Header 1") 
add_3d_wall(fig, [-T, 0], [2.11, 5.20], [0, CEILING_SLAB], "West Mid Wall")
add_3d_wall(fig, [-T, 0], [5.20, 6.01], [2.09, CEILING_SLAB], "West Door Header 2")
add_3d_wall(fig, [-T, 0], [6.01, 7.72], [0, CEILING_SLAB], "West Pillar 2")
# South Wall (Main Hall portion)
add_3d_wall(fig, [0, 1.96], [7.72, 7.72+T], [0, CEILING_SLAB], "South SW Corner") 
add_3d_wall(fig, [1.96, 2.77], [7.72, 7.72+T], [2.09, CEILING_SLAB], "South Door Header")
add_3d_wall(fig, [2.77, 4.84], [7.72, 7.72+T], [0, CEILING_SLAB], "South Wall Main")

# --- 2. EAST COLONNADE (The Interface) ---
add_3d_wall(fig, [4.84, 4.84+T], [0, 0.90], [0, CEILING_SLAB], "East Corner Pillar")
add_3d_wall(fig, [4.84, 4.84+T], [0.90, 2.99], [0, 0.17], "East Curb")
add_3d_wall(fig, [4.84, 4.84+T], [2.99, 4.53], [0, CEILING_SLAB], "East Mid Pillar")
add_3d_wall(fig, [4.84, 4.84+T], [7.03, 7.72], [0, CEILING_SLAB], "East Corner South")

# --- 3. ROOM 5: LANDING HUB (+45cm Elevation) ---
R5_Z = 0.45
add_3d_wall(fig, [5.18, 8.93], [5.1, 9.71], [R5_Z, R5_Z+0.05], "R5 Floor", "tan")
# R5 North Door Header (Entrance from stairs)
add_3d_wall(fig, [5.18, 6.07], [5.1, 5.1+T], [2.48, CEILING_SLAB], "R5 North Header")
# R5 Internal Partition
add_3d_wall(fig, [6.92, 6.97], [8.56, 9.71], [R5_Z, CEILING_SLAB], "Int Wall West")
add_3d_wall(fig, [6.92, 6.97], [8.56, 9.36], [2.46, CEILING_SLAB], "Int Door Header")
add_3d_wall(fig, [6.92, 8.93], [7.56, 7.61], [R5_Z, CEILING_SLAB], "Int Wall North")

# --- 4. ROOM 4: MEZZANINE (+77cm Elevation) ---
add_3d_wall(fig, [5.56, 7.44], [2.86, 4.96], [0.77, 0.82], "R4 Floor", "purple")

# --- 5. THE STAIRCASE & VOID ---
# First Step (19cm)
add_3d_wall(fig, [4.84, 5.18], [4.96, 5.3], [0, 0.19], "Step 1", "silver")
# Second Step to R5 (45cm)
add_3d_wall(fig, [5.18, 6.07], [4.96, 5.1], [0.19, 0.45], "Step 2", "silver")

# High Flight
rises = [0.19, 0.21, 0.19, 0.18, 0.18, 0.18, 0.18, 0.18]
runs = [0.24, 0.40, 0.40, 0.39, 0.39, 0.40, 0.40, 0.415, 0.62]
curr_z, curr_y = 0.32, 6.11
for i, (r, d) in enumerate(zip(rises, runs)):
    add_3d_wall(fig, [4.84, 6.25], [curr_y, curr_y+d], [0, curr_z+r], f"Stair {i+1}", "silver")
    curr_z += r
    curr_y += d

# Camera and Scene Settings
fig.update_layout(
    scene=dict(
        aspectmode='data',
        xaxis=dict(title='Width (X)'),
        yaxis=dict(title='Depth (Y)'),
        zaxis=dict(title='Height (Z)'),
        camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
    ),
    margin=dict(l=0, r=0, b=0, t=50)
)

st.plotly_chart(fig, use_container_width=True)
