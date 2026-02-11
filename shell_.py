import streamlit as st
import plotly.graph_objects as go

def add_3d_wall(fig, x_range, y_range, z_range, name="Wall", color='firebrick', opacity=0.9):
    # Generates a 3D box for walls, floors, or headers
    fig.add_trace(go.Mesh3d(
        x=[x_range[0], x_range[1], x_range[1], x_range[0], x_range[0], x_range[1], x_range[1], x_range[0]],
        y=[y_range[0], y_range[0], y_range[1], y_range[1], y_range[0], y_range[0], y_range[1], y_range[1]],
        z=[z_range[0], z_range[0], z_range[0], z_range[0], z_range[1], z_range[1], z_range[1], z_range[1]],
        i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2], j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3], k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
        opacity=opacity, color=color, flatshading=True, name=name
    ))

st.set_page_config(layout="wide")
st.title("Master Survey: Full Building Integrated Model")

fig = go.Figure()

# --- ARCHITECTURAL CONSTANTS ---
T = 0.22             # Wall Thickness
CEILING_SLAB = 2.73  # Master Slab Height

# --- ROOM 1: MAIN HALL (Ground Level) ---
add_3d_wall(fig, [0, 4.84], [-T, 0], [0, CEILING_SLAB], "R1 North Wall")
add_3d_wall(fig, [-T, 0], [0, 4.96], [0, CEILING_SLAB], "R1 West Wall")
add_3d_wall(fig, [0, 4.84], [0, 4.96], [-0.05, 0], "R1 Floor", "gray")

# --- ROOM 2: EAST SIDE ROOM (Ground Level) ---
add_3d_wall(fig, [4.84, 7.44], [0, 2.86], [-0.05, 0], "R2 Floor", "blue")
add_3d_wall(fig, [7.44, 7.44+T], [0, 2.86], [0, CEILING_SLAB], "R2 East Wall")

# --- ROOM 3: SOUTH ROOM (Large Windows) ---
add_3d_wall(fig, [0, 4.84], [4.96, 9.71], [-0.05, 0], "R3 Floor", "green")
# South Window Wall (R3)
add_3d_wall(fig, [0, 4.84], [9.71, 9.71+T], [0.8, 2.2], "R3 South Window", "lightblue", 0.5)

# --- ROOM 4: MEZZANINE (77cm Elevation) ---
R4_Z = 0.77
add_3d_wall(fig, [5.56, 7.44], [2.86, 4.96], [R4_Z, R4_Z+0.05], "R4 Floor", "purple")
add_3d_wall(fig, [5.56, 7.44], [4.96, 4.96+T], [2.1, CEILING_SLAB], "R4 Entrance Header")

# --- THE STAIRCASE SYSTEM ---
# Ground to Step 1 (19cm)
add_3d_wall(fig, [4.84, 5.18], [4.96, 5.3], [0, 0.19], "Step 1", "silver")
# Step 1 to Room 5 Threshold (45cm cumulative)
add_3d_wall(fig, [5.18, 6.07], [4.96, 5.1], [0.19, 0.45], "R5 Threshold Step", "silver")

# The High Flight (to 181cm)
rises = [0.19, 0.21, 0.19, 0.18, 0.18, 0.18, 0.18, 0.18]
runs = [0.24, 0.40, 0.40, 0.39, 0.39, 0.40, 0.40, 0.415, 0.62]
curr_z = 0.32
curr_y = 6.11
for i, (r, d) in enumerate(zip(rises, runs)):
    add_3d_wall(fig, [4.84, 4.84+1.41], [curr_y, curr_y+d], [0, curr_z+r], f"Stair {i+1}", "silver")
    curr_z += r
    curr_y += d

# --- ROOM 5: THE HUB (+45cm Elevation) ---
R5_XW, R5_XE = 5.18, 8.93
R5_YN, R5_YS = 5.1, 9.71
R5_Z = 0.45

add_3d_wall(fig, [R5_XW, R5_XE], [R5_YN, R5_YS], [R5_Z, R5_Z+0.05], "R5 Floor", "tan")

# North Wall with Clerestory Window
add_3d_wall(fig, [R5_XW, 6.405], [R5_YN, R5_YN+T], [R5_Z, CEILING_SLAB])
add_3d_wall(fig, [6.405, 7.405], [R5_YN, R5_YN+T], [R5_Z, 2.17], "N-Win Sill")
add_3d_wall(fig, [6.405, 7.405], [R5_YN, R5_YN+T], [2.46, CEILING_SLAB], "N-Win Header")
add_3d_wall(fig, [7.405, R5_XE], [R5_YN, R5_YN+T], [R5_Z, CEILING_SLAB])

# East Wall with Main Window
add_3d_wall(fig, [R5_XE, R5_XE+T], [5.8, 6.78], [R5_Z, 1.67], "E-Win Sill")
add_3d_wall(fig, [R5_XE, R5_XE+T], [5.8, 6.78], [2.46, CEILING_SLAB], "E-Win Header")

# South Wall with Door and Window
add_3d_wall(fig, [5.67, 6.56], [R5_YS, R5_YS+T], [2.48, CEILING_SLAB], "S-Door Header")
add_3d_wall(fig, [7.67, 8.57], [R5_YS, R5_YS+T], [R5_Z, 1.76], "S-Win Sill")
add_3d_wall(fig, [7.67, 8.57], [R5_YS, R5_YS+T], [2.48, CEILING_SLAB], "S-Win Header")

# --- ROOM 5 INTERNAL PARTITION ---
INT_X = 6.92
INT_Y_C = 7.56
# Internal North Wall (with window)
add_3d_wall(fig, [7.03, 8.02], [INT_Y_C, INT_Y_C+0.05], [R5_Z, 1.74], "Int-Win Sill")
add_3d_wall(fig, [7.03, 8.02], [INT_Y_C, INT_Y_C+0.05], [2.45, CEILING_SLAB], "Int-Win Header")
# Internal West Wall (with door)
add_3d_wall(fig, [INT_X, INT_X+0.05], [8.56, 9.36], [2.46, CEILING_SLAB], "Int-Door Header")

# Final Polish
fig.update_layout(scene=dict(aspectmode='data'), margin=dict(l=0, r=0, b=0, t=0))
st.plotly_chart(fig, use_container_width=True)
