import streamlit as st
import plotly.graph_objects as go

def add_3d_wall(fig, x_range, y_range, z_range, name="Wall", color='firebrick', opacity=0.9):
    fig.add_trace(go.Mesh3d(
        x=[x_range[0], x_range[1], x_range[1], x_range[0], x_range[0], x_range[1], x_range[1], x_range[0]],
        y=[y_range[0], y_range[0], y_range[1], y_range[1], y_range[0], y_range[0], y_range[1], y_range[1]],
        z=[z_range[0], z_range[0], z_range[0], z_range[0], z_range[1], z_range[1], z_range[1], z_range[1]],
        i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2], j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3], k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
        opacity=opacity, color=color, flatshading=True, name=name
    ))

st.set_page_config(layout="wide")
st.title("Digital Twin: Master Model (Stairs Relocated)")
st.write("**Frame of Reference:** West = (+X) | East = (-X)")

fig = go.Figure()

# --- CONSTANTS ---
T = 0.22             
CEILING_H = 2.50     
SLAB_TOP = 2.73      
WEST_LIMIT_X = 4.84   
EAST_LIMIT_X = -4.98  
R3_Y_DIVIDE = 7.72   
R3_Y_END = R3_Y_DIVIDE + 3.35 
BUILDING_SOUTH_EDGE = R3_Y_END + T

# --- 1. ROOM 1: MAIN HALL PERIMETER ---
add_3d_wall(fig, [0, WEST_LIMIT_X], [-T, 0], [0, CEILING_H], "R1 North Wall")
add_3d_wall(fig, [-T, 0], [0, 1.15], [0, CEILING_H], "West Pillar 1")
add_3d_wall(fig, [-T, 0], [1.15, 2.11], [2.06, CEILING_H], "West Door Header 1") 
add_3d_wall(fig, [-T, 0], [2.11, 5.20], [0, CEILING_H], "West Mid Wall")
add_3d_wall(fig, [-T, 0], [5.20, 6.01], [2.09, CEILING_H], "West Door Header 2")
add_3d_wall(fig, [-T, 0], [6.01, R3_Y_DIVIDE], [0, CEILING_H], "West Pillar 2")
add_3d_wall(fig, [0, 1.96], [R3_Y_DIVIDE, R3_Y_DIVIDE+T], [0, CEILING_H], "R1 South Divider E") 
add_3d_wall(fig, [1.96, 2.77], [R3_Y_DIVIDE, R3_Y_DIVIDE+T], [2.09, CEILING_H], "R1 South Door Header")
add_3d_wall(fig, [2.77, WEST_LIMIT_X], [R3_Y_DIVIDE, R3_Y_DIVIDE+T], [0, CEILING_H], "R1 South Divider W")

# --- 2. WESTERN COLONNADE ---
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [0, 0.90], [0, CEILING_H], "West Corner Pillar")
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [0.90, 2.99], [0, 0.17], "West Curb")
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [2.99, 4.53], [0, CEILING_H], "West Mid Pillar")
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [7.03, R3_Y_DIVIDE], [0, CEILING_H], "West Corner South")

# --- 3. ROOM 2: EAST WING NORTH ---
R2_X_END = -1.79
add_3d_wall(fig, [-0.62, 0], [-T, 0], [0, CEILING_H], "R2 N Pillar", "darkred")
add_3d_wall(fig, [-1.325, -0.62], [-T, 0], [0, 1.46], "R2 N Sill", "darkred")
add_3d_wall(fig, [-1.325, -0.62], [-T, 0], [2.06, CEILING_H], "R2 N Header", "darkred")
add_3d_wall(fig, [R2_X_END, -1.325], [-T, 0], [0, CEILING_H], "R2 N End", "darkred")
add_3d_wall(fig, [R2_X_END-T, R2_X_END], [-T, 2.42], [0, CEILING_H], "R2 East Wall", "darkred")
add_3d_wall(fig, [R2_X_END, 0], [2.42, 2.42+T], [0, CEILING_H], "R2 South Wall", "darkred")
add_3d_wall(fig, [-1.325, -0.62], [-T/2, -T/2], [1.46, 2.06], "Glass R2", "skyblue", 0.4)

# --- 4. ROOM 3: SOUTH WING ---
add_3d_wall(fig, [-T, 0], [R3_Y_DIVIDE, R3_Y_END], [0, CEILING_H], "R3 East Wall", "darkgreen")
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [R3_Y_DIVIDE, R3_Y_DIVIDE+0.72], [0, CEILING_H], "R3 W Wall N", "darkgreen")
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [R3_Y_DIVIDE+0.72, R3_Y_DIVIDE+2.71], [0, 0.86], "R3 W Sill")
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [R3_Y_DIVIDE+0.72, R3_Y_DIVIDE+2.71], [2.46, CEILING_H], "R3 W Header")
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [R3_Y_DIVIDE+2.71, R3_Y_END], [0, CEILING_H], "R3 W Wall S", "darkgreen")
add_3d_wall(fig, [WEST_LIMIT_X+T/2, WEST_LIMIT_X+T/2], [R3_Y_DIVIDE+0.72, R3_Y_DIVIDE+2.71], [0.86, 2.46], "Glass R3 W", "skyblue", 0.4)

# South Window R3
W_END_X = WEST_LIMIT_X - 0.35
W_START_X = W_END_X - 1.53
add_3d_wall(fig, [0, W_START_X], [R3_Y_END, R3_Y_END+T], [0, CEILING_H], "R3 S Wall East", "darkgreen")
add_3d_wall(fig, [W_START_X, W_END_X], [R3_Y_END, R3_Y_END+T], [0, 0.43], "R3 S Sill")
add_3d_wall(fig, [W_START_X, W_END_X], [R3_Y_END, R3_Y_END+T], [2.45, CEILING_H], "R3 S Header")
add_3d_wall(fig, [W_END_X, WEST_LIMIT_X], [R3_Y_END, R3_Y_END+T], [0, CEILING_H], "R3 S Wall West (35cm)", "darkgreen")
add_3d_wall(fig, [W_START_X, W_END_X], [R3_Y_END+T/2, R3_Y_END+T/2], [0.43, 2.45], "Glass R3 S", "skyblue", 0.4)

# --- 5. ROOM 4 & THE WINDER ---
add_3d_wall(fig, [-1.0, 0], [4.96, 5.3], [0, 0.19], "Step 1", "silver")
fig.add_trace(go.Mesh3d(
    x=[0, -1.0, -1.0, 0],
    y=[4.96, 4.96, 4.96+1.15, 4.96+1.15],
    z=[0.32, 0.32, 0.32, 0.32],
    color='darkgray', name="Triangular Winder"
))
add_3d_wall(fig, [-3.0, 0], [2.86, 4.96], [0.77, 0.82], "R4 Floor", "gray")

# --- 6. ROOM 5: THE HUB (R5 North Wall at Y=6.46) ---
R5_XW, R5_XE = -0.22, -3.97
R5_YN, R5_YS = 6.46, 11.07
R5_Z = 0.45

# Floor
add_3d_wall(fig, [R5_XW, R5_XE], [R5_YN, R5_YS], [R5_Z, R5_Z+0.05], "R5 Floor", "tan")

# North Wall + Glass
add_3d_wall(fig, [R5_XW, -1.445], [R5_YN, R5_YN+T], [R5_Z, SLAB_TOP])
add_3d_wall(fig, [-1.445, -2.445], [R5_YN, R5_YN+T], [R5_Z, 2.17], "N-Win Sill")
add_3d_wall(fig, [-1.445, -2.445], [R5_YN, R5_YN+T], [2.46, SLAB_TOP], "N-Win Header")
add_3d_wall(fig, [-1.445, -2.445], [R5_YN+T/2, R5_YN+T/2], [2.17, 2.46], "Glass R5 N", "skyblue", 0.4)
add_3d_wall(fig, [-2.445, R5_XE], [R5_YN, R5_YN+T], [R5_Z, SLAB_TOP])

# East Wall + Glass
add_3d_wall(fig, [R5_XE, R5_XE-T], [R5_YN, 7.16], [R5_Z, SLAB_TOP], "E-Wall South")
add_3d_wall(fig, [R5_XE, R5_XE-T], [7.16, 8.14], [R5_Z, 1.67], "E-Win Sill")
add_3d_wall(fig, [R5_XE, R5_XE-T], [7.16, 8.14], [2.46, SLAB_TOP], "E-Win Header")
add_3d_wall(fig, [R5_XE-T/2, R5_XE-T/2], [7.16, 8.14], [1.67, 2.46], "Glass R5 E", "skyblue", 0.4)
add_3d_wall(fig, [R5_XE, R5_XE-T], [8.14, R5_YS], [R5_Z, SLAB_TOP], "E-Wall North")

# South Wall + Glass
add_3d_wall(fig, [-0.71, -1.60], [R5_YS, R5_YS+T], [2.48, SLAB_TOP], "S-Door Header")
add_3d_wall(fig, [-1.60, -2.71], [R5_YS, R5_YS+T], [R5_Z, SLAB_TOP], "S-Wall Mid") 
add_3d_wall(fig, [-2.71, -3.61], [R5_YS, R5_YS+T], [R5_Z, 1.76], "S-Win Sill")
add_3d_wall(fig, [-2.71, -3.61], [R5_YS, R5_YS+T], [2.48, SLAB_TOP], "S-Win Header")
add_3d_wall(fig, [-2.71, -3.61], [R5_YS+T/2, R5_YS+T/2], [1.76, 2.48], "Glass R5 S", "skyblue", 0.4)
add_3d_wall(fig, [-3.61, R5_XE], [R5_YS, R5_YS+T], [R5_Z, SLAB_TOP], "S-Wall Corner")

# Internal Partition + Glass
INT_X, INT_Y_C = -1.96, 8.92
add_3d_wall(fig, [-2.07, -3.06], [INT_Y_C, INT_Y_C+0.05], [R5_Z, 1.74], "Int-Win Sill")
add_3d_wall(fig, [-2.07, -3.06], [INT_Y_C, INT_Y_C+0.05], [2.45, SLAB_TOP], "Int-Win Header")
add_3d_wall(fig, [-2.07, -3.06], [INT_Y_C+0.025, INT_Y_C+0.025], [1.74, 2.45], "Glass R5 Int", "skyblue", 0.4)
add_3d_wall(fig, [INT_X, INT_X-0.05], [9.92, 10.72], [2.46, SLAB_TOP], "Int-Door Header")

# --- 7. STRUCTURAL SLAB ---
add_3d_wall(fig, [EAST_LIMIT_X - 5.0, WEST_LIMIT_X+T], [-T, R5_YS+T], [CEILING_H, SLAB_TOP], "Concrete Slab", "rgba(100,100,100,0.3)")

# --- 8. MAIN STAIRCASE (East of Winder & North of R5) ---
# Start X at -1.1 (East of winder which is at -1.0)
# Start Y range at [5.0, 6.4] (North of R5_YN which is 6.46)
curr_z, curr_x = 0.32, -1.1
step_y_range = [5.0, 6.4] 
for i, (r, d) in enumerate([(0.19, 0.24), (0.21, 0.4), (0.19, 0.4), (0.18, 0.39), (0.18, 0.39), (0.18, 0.4), (0.18, 0.4), (0.18, 0.415)]):
    add_3d_wall(fig, [curr_x - d, curr_x], step_y_range, [0, curr_z + r], f"Stair {i+1}", "silver")
    curr_z += r
    curr_x -= d

fig.update_layout(scene=dict(aspectmode='data'), margin=dict(l=0, r=0, b=0, t=50))
st.plotly_chart(fig, use_container_width=True)
