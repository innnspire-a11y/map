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
st.title("Digital Twin: Room 5 Flush Alignment")

fig = go.Figure()

# --- CONSTANTS ---
T = 0.22             
CEILING_H = 2.50     
SLAB_TOP = 2.73      
WEST_LIMIT_X = 4.84   
EAST_LIMIT_X = -4.98  
R3_Y_DIVIDE = 7.72   
R3_Y_END = R3_Y_DIVIDE + 3.35 
R1_C, R2_C, R3_C, R4_C, R5_C = "royalblue", "firebrick", "darkgreen", "slategrey", "darkorange"
G_C, G_O = "skyblue", 0.4 

# --- ROOM 5 VERTICAL DATUM ---
# Flush with top of stairs (19cm + 26cm = 45cm)
R5_Z = 0.45 

# --- 1. ROOM 1: MAIN HALL ---
add_3d_wall(fig, [0, WEST_LIMIT_X], [-T, 0], [0, CEILING_H], "R1 North Wall", R1_C)
add_3d_wall(fig, [-T, 0], [0, 1.15], [0, CEILING_H], "West Pillar 1", R1_C)
add_3d_wall(fig, [-T, 0], [1.15, 2.11], [2.06, CEILING_H], "West Door Header 1", R1_C) 
add_3d_wall(fig, [-T, 0], [2.11, 5.20], [0, CEILING_H], "West Mid Wall", R1_C)
add_3d_wall(fig, [-T, 0], [5.20, 6.01], [2.09, CEILING_H], "West Door Header 2", R1_C)
add_3d_wall(fig, [-T, 0], [6.01, R3_Y_DIVIDE], [0, CEILING_H], "West Pillar 2", R1_C)
add_3d_wall(fig, [0, 1.96], [R3_Y_DIVIDE, R3_Y_DIVIDE+T], [0, CEILING_H], "R1 South Divider E", R1_C) 
add_3d_wall(fig, [1.96, 2.77], [R3_Y_DIVIDE, R3_Y_DIVIDE+T], [2.09, CEILING_H], "R1 South Door Header", R1_C)
add_3d_wall(fig, [2.77, WEST_LIMIT_X], [R3_Y_DIVIDE, R3_Y_DIVIDE+T], [0, CEILING_H], "R1 South Divider W", R1_C)

# --- 2. WESTERN COLONNADE ---
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [0, 0.90], [0, CEILING_H], "West Corner Pillar", R1_C)
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [0.90, 2.99], [0, 0.17], "West Curb", R1_C)
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [2.99, 4.53], [0, CEILING_H], "West Mid Pillar", R1_C)
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [7.03, R3_Y_DIVIDE], [0, CEILING_H], "West Corner South", R1_C)

# --- 3. ROOM 2: EAST WING ---
R2_X_END = -1.79
add_3d_wall(fig, [-0.62, 0], [-T, 0], [0, CEILING_H], "R2 N Pillar", R2_C)
add_3d_wall(fig, [-1.325, -0.62], [-T, 0], [0, 1.46], "R2 N Sill", R2_C)
add_3d_wall(fig, [-1.325, -0.62], [-T, 0], [2.06, CEILING_H], "R2 N Header", R2_C)
add_3d_wall(fig, [R2_X_END, -1.325], [-T, 0], [0, CEILING_H], "R2 N End", R2_C)
add_3d_wall(fig, [R2_X_END-T, R2_X_END], [-T, 2.42], [0, CEILING_H], "R2 East Wall", R2_C)
add_3d_wall(fig, [R2_X_END, 0], [2.42, 2.42+T], [0, CEILING_H], "R2 South Wall", R2_C)

# --- 4. ROOM 3: SOUTH WING ---
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [R3_Y_DIVIDE+0.72, R3_Y_DIVIDE+2.71], [0, 0.86], "R3 W Sill", R3_C)
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [R3_Y_DIVIDE+0.72, R3_Y_DIVIDE+2.71], [2.46, CEILING_H], "R3 W Header", R3_C)
add_3d_wall(fig, [WEST_LIMIT_X+T/2, WEST_LIMIT_X+T/2], [R3_Y_DIVIDE+0.72, R3_Y_DIVIDE+2.71], [0.86, 2.46], "Glass R3 W", G_C, G_O)

W_END_X_R3 = WEST_LIMIT_X - 0.35
W_START_X_R3 = W_END_X_R3 - 1.53
add_3d_wall(fig, [W_START_X_R3, W_END_X_R3], [R3_Y_END, R3_Y_END+T], [0, 0.43], "R3 S Sill", R3_C)
add_3d_wall(fig, [W_START_X_R3, W_END_X_R3], [R3_Y_END, R3_Y_END+T], [2.45, CEILING_H], "R3 S Header", R3_C)
add_3d_wall(fig, [W_START_X_R3, W_END_X_R3], [R3_Y_END+T/2, R3_Y_END+T/2], [0.43, 2.45], "Glass R3 S", G_C, G_O)
add_3d_wall(fig, [-T, 0], [R3_Y_DIVIDE, R3_Y_END], [0, CEILING_H], "R3 East Wall", R3_C)
add_3d_wall(fig, [0, W_START_X_R3], [R3_Y_END, R3_Y_END+T], [0, CEILING_H], "R3 S Wall East", R3_C)
add_3d_wall(fig, [W_END_X_R3, WEST_LIMIT_X], [R3_Y_END, R3_Y_END+T], [0, CEILING_H], "R3 S Wall West", R3_C)
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [R3_Y_DIVIDE, R3_Y_DIVIDE+0.72], [0, CEILING_H], "R3 W Wall N", R3_C)
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [R3_Y_DIVIDE+2.71, R3_Y_END], [0, CEILING_H], "R3 W Wall S", R3_C)

# --- 5. ROOM 4 & THE WINDER ---
add_3d_wall(fig, [-1.0, 0], [4.96, 5.3], [0, 0.19], "Step 1", "silver")
fig.add_trace(go.Mesh3d(
    x=[0, -1.0, -1.0, 0], y=[4.96, 4.96, 6.11, 6.11], z=[0.32, 0.32, 0.32, 0.32],
    color='darkgray', name="Triangular Winder"
))
add_3d_wall(fig, [-3.0, 0], [2.86, 4.96], [0.77, 0.82], "R4 Floor", R4_C)

# --- 6. ROOM 5: THE HUB ---
R5_XW, R5_XE = -0.22, -0.22 - 3.75
R5_YN, R5_YS = 6.46, 6.46 + 4.61
# Floor is now at 0.45, thickness 0.05
add_3d_wall(fig, [R5_XW, R5_XE], [R5_YN, R5_YS], [R5_Z-0.05, R5_Z], "R5 Floor", "tan")

S_D_X_START = R5_XW - 0.49
S_D_X_END = S_D_X_START - 0.89 

# North Wall Window (High clearance: starts at 172cm from ground)
NW_WIN_Z_SILL, NW_WIN_Z_HEAD = R5_Z + 1.72, R5_Z + 1.72 + 0.29
NW_WIN_X_START = S_D_X_END - 0.335
NW_WIN_X_END = NW_WIN_X_START - 1.0

add_3d_wall(fig, [R5_XW, S_D_X_START], [R5_YN, R5_YN+T], [R5_Z, SLAB_TOP], "R5 N Wall W", R5_C)
add_3d_wall(fig, [S_D_X_START, S_D_X_END], [R5_YN, R5_YN+T], [R5_Z+2.03, SLAB_TOP], "R5 N Door Header", R5_C)
add_3d_wall(fig, [S_D_X_END, NW_WIN_X_START], [R5_YN, R5_YN+T], [R5_Z, SLAB_TOP], "R5 N Wall Mid", R5_C)
add_3d_wall(fig, [NW_WIN_X_START, NW_WIN_X_END], [R5_YN, R5_YN+T], [R5_Z, NW_WIN_Z_SILL], "R5 N Win Sill", R5_C)
add_3d_wall(fig, [NW_WIN_X_START, NW_WIN_X_END], [R5_YN, R5_YN+T], [NW_WIN_Z_HEAD, SLAB_TOP], "R5 N Win Header", R5_C)
add_3d_wall(fig, [NW_WIN_X_END, R5_XE], [R5_YN, R5_YN+T], [R5_Z, SLAB_TOP], "R5 N Wall E", R5_C)
add_3d_wall(fig, [NW_WIN_X_START, NW_WIN_X_END], [R5_YN+T/2, R5_YN+T/2], [NW_WIN_Z_SILL, NW_WIN_Z_HEAD], "Glass R5 N", G_C, G_O)

# East Wall Window (starts 122cm from ground)
E_W_Y1, E_W_Y2 = R5_YN + 0.70, R5_YN + 1.68
E_WIN_Z_SILL, E_WIN_Z_HEAD = R5_Z + 1.22, R5_Z + 1.22 + 0.79
add_3d_wall(fig, [R5_XE, R5_XE+T], [R5_YN, E_W_Y1], [R5_Z, SLAB_TOP], "R5 E Wall N", R5_C)
add_3d_wall(fig, [R5_XE, R5_XE+T], [E_W_Y1, E_W_Y2], [R5_Z, E_WIN_Z_SILL], "R5 E Sill", R5_C)
add_3d_wall(fig, [R5_XE, R5_XE+T], [E_W_Y1, E_W_Y2], [E_WIN_Z_HEAD, SLAB_TOP], "R5 E Header", R5_C)
add_3d_wall(fig, [R5_XE, R5_XE+T], [E_W_Y2, R5_YS], [R5_Z, SLAB_TOP], "R5 E Wall S", R5_C)
add_3d_wall(fig, [R5_XE+T/2, R5_XE+T/2], [E_W_Y1, E_W_Y2], [E_WIN_Z_SILL, E_WIN_Z_HEAD], "Glass R5 E", G_C, G_O)

# South Wall Window (starts 131cm from ground)
S_W_X1, S_W_X2 = R5_XE + 0.36, R5_XE + 0.36 + 0.90 # 36cm from east wall, 90cm wide
S_WIN_Z_SILL, S_WIN_Z_HEAD = R5_Z + 1.31, R5_Z + 1.31 + 0.72
add_3d_wall(fig, [R5_XW, S_D_X_START], [R5_YS-T, R5_YS], [R5_Z, SLAB_TOP], "R5 S Wall W", R5_C)
add_3d_wall(fig, [S_D_X_START, S_D_X_END], [R5_YS-T, R5_YS], [R5_Z+2.03, SLAB_TOP], "R5 S Door Header", R5_C)
add_3d_wall(fig, [S_D_X_END, S_W_X2], [R5_YS-T, R5_YS], [R5_Z, SLAB_TOP], "R5 S Wall Mid", R5_C)
add_3d_wall(fig, [S_W_X2, S_W_X1], [R5_YS-T, R5_YS], [R5_Z, S_WIN_Z_SILL], "R5 S Win Sill", R5_C)
add_3d_wall(fig, [S_W_X2, S_W_X1], [R5_YS-T, R5_YS], [S_WIN_Z_HEAD, SLAB_TOP], "R5 S Win Header", R5_C)
add_3d_wall(fig, [S_W_X1, R5_XE], [R5_YS-T, R5_YS], [R5_Z, SLAB_TOP], "R5 S Wall E", R5_C)
add_3d_wall(fig, [S_W_X2, S_W_X1], [R5_YS-T/2, R5_YS-T/2], [S_WIN_Z_SILL, S_WIN_Z_HEAD], "Glass R5 S", G_C, G_O)

# West Wall
add_3d_wall(fig, [R5_XW-T, R5_XW], [R5_YN, R5_YS], [R5_Z, SLAB_TOP], "R5 West Shared Wall", R5_C)

# --- 7. INTERNAL L-SHAPED PARTITION ---
INT_X = S_D_X_END - 0.36
INT_Y1, INT_Y2, INT_Y3 = R5_YS - 0.35, R5_YS - 1.15, R5_YS - 2.15
W_INT_X1, W_INT_X2 = INT_X - 0.11, INT_X - 1.10
# Door is 201cm high
add_3d_wall(fig, [INT_X, INT_X+0.05], [R5_YS, INT_Y1], [R5_Z, SLAB_TOP], "Int Vert 1", "silver")
add_3d_wall(fig, [INT_X, INT_X+0.05], [INT_Y1, INT_Y2], [R5_Z+2.01, SLAB_TOP], "Int Door Header", "silver")
add_3d_wall(fig, [INT_X, INT_X+0.05], [INT_Y2, INT_Y3], [R5_Z, SLAB_TOP], "Int Vert 2", "silver")
# Horizontal section with window (starts 129cm from ground, height 71cm)
I_WIN_Z_SILL, I_WIN_Z_HEAD = R5_Z + 1.29, R5_Z + 1.29 + 0.71
add_3d_wall(fig, [INT_X, W_INT_X1], [INT_Y3, INT_Y3+0.05], [R5_Z, SLAB_TOP], "Int Horiz 1", "silver")
add_3d_wall(fig, [W_INT_X1, W_INT_X2], [INT_Y3, INT_Y3+0.05], [R5_Z, I_WIN_Z_SILL], "Int Win Sill", "silver")
add_3d_wall(fig, [W_INT_X1, W_INT_X2], [INT_Y3, INT_Y3+0.05], [I_WIN_Z_HEAD, SLAB_TOP], "Int Win Header", "silver")
add_3d_wall(fig, [W_INT_X2, R5_XE], [INT_Y3, INT_Y3+0.05], [R5_Z, SLAB_TOP], "Int Horiz 2", "silver")
add_3d_wall(fig, [W_INT_X1, W_INT_X2], [INT_Y3+0.025, INT_Y3+0.025], [I_WIN_Z_SILL, I_WIN_Z_HEAD], "Glass Int", G_C, G_O)

# --- 8. STEPS & STAIRCASE ---
add_3d_wall(fig, [-2.1, -1.1], [5.0, 6.4], [0, 0.45], "Step 2 (R5 Base)", "silver")
curr_z, curr_x = 0.32, -1.1
for i, (r, d) in enumerate([(0.19, 0.24), (0.21, 0.4), (0.19, 0.4), (0.18, 0.39), (0.18, 0.39), (0.18, 0.4), (0.18, 0.4), (0.18, 0.415)]):
    add_3d_wall(fig, [curr_x - d, curr_x], [5.0, 6.4], [0, curr_z + r], f"Stair {i+1}", "silver")
    curr_z += r; curr_x -= d

add_3d_wall(fig, [EAST_LIMIT_X-2, WEST_LIMIT_X+2], [-T, R5_YS+T], [CEILING_H, SLAB_TOP], "Concrete Slab", "rgba(100,100,100,0.2)")

fig.update_layout(scene=dict(aspectmode='data'), margin=dict(l=0, r=0, b=0, t=50))
st.plotly_chart(fig, use_container_width=True)
