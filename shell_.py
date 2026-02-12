import streamlit as st
import plotly.graph_objects as go

# --- 1. Page Configuration (Must be the first Streamlit command) ---
st.set_page_config(layout="wide", page_title="Digital Twin")

# --- 2. Enhanced CSS to hide all GitHub/Streamlit UI clutter ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            /* Hides the toolbar (GitHub, Manage App) */
            div[data-testid="stToolbar"] {display: none !important;}
            /* Hides the 'Deploy' button specifically */
            .stAppDeployButton {display:none !important;}
            /* Hides the decoration line at the top */
            div[data-testid="stDecoration"] {display:none !important;}
            /* Removes extra top whitespace for a flush look */
            .block-container {padding-top: 0rem;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

def add_3d_wall(fig, x_range, y_range, z_range, name="Wall", color='firebrick', opacity=0.9):
    fig.add_trace(go.Mesh3d(
        x=[x_range[0], x_range[1], x_range[1], x_range[0], x_range[0], x_range[1], x_range[1], x_range[0]],
        y=[y_range[0], y_range[0], y_range[1], y_range[1], y_range[0], y_range[0], y_range[1], y_range[1]],
        z=[z_range[0], z_range[0], z_range[0], z_range[0], z_range[1], z_range[1], z_range[1], z_range[1]],
        i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2], j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3], k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
        opacity=opacity, color=color, flatshading=True, name=name
    ))

st.title("Digital Twin: Building")

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
ENT_C = "rgba(0, 255, 100, 0.4)" # Transparent Green for entrances

# --- ROOM 5 VERTICAL DATUM ---
R5_Z = 0.45 
R5_CEIL = CEILING_H 

# --- 1. ROOM 1: MAIN HALL ---
add_3d_wall(fig, [0, WEST_LIMIT_X], [-T, 0], [0, CEILING_H], "R1 North Wall", R1_C)
add_3d_wall(fig, [-T, 0], [0, 1.15], [0, CEILING_H], "West Pillar 1", R1_C)
add_3d_wall(fig, [-T, 0], [1.15, 2.11], [2.06, CEILING_H], "West Door Header 1", R1_C) 
add_3d_wall(fig, [-T/2, -T/2], [1.15, 2.11], [0, 2.06], "Entrance 1 Glass", ENT_C)
add_3d_wall(fig, [-T, 0], [2.11, 5.20], [0, CEILING_H], "West Mid Wall", R1_C)
add_3d_wall(fig, [-T, 0], [5.20, 6.01], [2.09, CEILING_H], "West Door Header 2", R1_C)
add_3d_wall(fig, [-T/2, -T/2], [5.20, 6.01], [0, 2.09], "Entrance 2 Glass", ENT_C)
add_3d_wall(fig, [-T, 0], [6.01, R3_Y_DIVIDE], [0, CEILING_H], "West Pillar 2", R1_C)
add_3d_wall(fig, [0, 1.96], [R3_Y_DIVIDE, R3_Y_DIVIDE+T], [0, CEILING_H], "R1 South Divider E", R1_C) 
add_3d_wall(fig, [1.96, 2.77], [R3_Y_DIVIDE, R3_Y_DIVIDE+T], [2.09, CEILING_H], "R1 South Door Header", R1_C)
add_3d_wall(fig, [1.96, 2.77], [R3_Y_DIVIDE+T/2, R3_Y_DIVIDE+T/2], [0, 2.09], "Entrance South Glass", ENT_C)
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
add_3d_wall(fig, [-1.325, -0.62], [-T/2, -T/2], [1.46, 2.06], "Glass R2 N", G_C, G_O) 
add_3d_wall(fig, [R2_X_END, -1.325], [-T, 0], [0, CEILING_H], "R2 N End", R2_C)
add_3d_wall(fig, [R2_X_END-T, R2_X_END], [-T, 2.42], [0, CEILING_H], "R2 East Wall", R2_C)
add_3d_wall(fig, [R2_X_END, 0], [2.42, 2.42+T], [0, CEILING_H], "R2 South Shared Wall", R2_C)

# --- 4. ROOM 3: SOUTH WING ---
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [R3_Y_DIVIDE+0.72, R3_Y_DIVIDE+2.71], [0, 0.86], "R3 W Sill", R3_C)
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [R3_Y_DIVIDE+0.72, R3_Y_DIVIDE+2.71], [2.46, CEILING_H], "R3 W Header", R3_C)
add_3d_wall(fig, [WEST_LIMIT_X+T/2, WEST_LIMIT_X+T/2], [R3_Y_DIVIDE+0.72, R3_Y_DIVIDE+2.71], [0.86, 2.46], "Glass R3 W", G_C, G_O)

W_END_X_R3 = WEST_LIMIT_X - 0.35
W_START_X_R3 = W_END_X_R3 - 1.53
add_3d_wall(fig, [W_START_X_R3, W_END_X_R3], [R3_Y_END, R3_Y_END+T], [0, 0.43], "R3 S Sill", R3_C)
add_3d_wall(fig, [W_START_X_R3, W_END_X_R3], [R3_Y_END, R3_Y_END+T], [2.45, CEILING_H], "R3 S Header", R3_C)
add_3d_wall(fig, [W_START_X_R3, W_END_X_R3], [R3_Y_END+T/2, R3_Y_END+T/2], [0.43, 2.45], "Glass R3 S", G_C, G_O)
add_3d_wall(fig, [-T, 0], [R3_Y_DIVIDE, R3_Y_END], [0, CEILING_H], "R3 East Shared Wall", R3_C)
add_3d_wall(fig, [0, W_START_X_R3], [R3_Y_END, R3_Y_END+T], [0, CEILING_H], "R3 S Wall East", R3_C)
add_3d_wall(fig, [W_END_X_R3, WEST_LIMIT_X], [R3_Y_END, R3_Y_END+T], [0, CEILING_H], "R3 S Wall West", R3_C)
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [R3_Y_DIVIDE, R3_Y_DIVIDE+0.72], [0, CEILING_H], "R3 W Wall N", R3_C)
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [R3_Y_DIVIDE+2.71, R3_Y_END], [0, CEILING_H], "R3 W Wall S", R3_C)

# --- 5. ROOM 4: THE ENCLOSED MEZZANINE ---
R4_X_RIGHT = 0.0
R4_X_LEFT = R2_X_END         
R4_Y_TOP = 2.42               
R4_FLOOR = 0.77
R4_Y_BOTTOM_EDGE = 5.0
R4_Y_BOTTOM_START = R4_Y_BOTTOM_EDGE - T 

add_3d_wall(fig, [R4_X_LEFT, R4_X_RIGHT], [R4_Y_TOP, R4_Y_BOTTOM_EDGE], [R4_FLOOR, R4_FLOOR+0.05], "R4 Floor", R4_C)
add_3d_wall(fig, [R4_X_LEFT, R4_X_RIGHT], [R4_Y_TOP, R4_Y_TOP+T], [R4_FLOOR, 2.5], "R4 North Shared Wall", R4_C)
add_3d_wall(fig, [-T, 0], [R4_Y_TOP, R4_Y_BOTTOM_EDGE], [R4_FLOOR, 2.5], "R4 West Shared Wall (from R1)", R4_C)
add_3d_wall(fig, [R4_X_LEFT-T, R4_X_LEFT], [R4_Y_TOP, R4_Y_BOTTOM_EDGE], [R4_FLOOR, 2.5], "R4 East Wall (aligned R2)", R4_C)
add_3d_wall(fig, [R4_X_LEFT + 0.82, R4_X_RIGHT], [R4_Y_BOTTOM_START, R4_Y_BOTTOM_EDGE], [R4_FLOOR, 2.5], "R4 South Wall", R4_C)
add_3d_wall(fig, [R4_X_LEFT, R4_X_LEFT + 0.82], [R4_Y_BOTTOM_START + T/2, R4_Y_BOTTOM_START + T/2], [R4_FLOOR, 2.5], "R4 Entrance Glass", ENT_C)

# --- 6. ROOM 5: THE HUB ---
R5_XW, R5_XE = -T, -T - 3.75
R5_YN = 6.46
R5_YS = R3_Y_END 
add_3d_wall(fig, [R5_XW, R5_XE], [R5_YN, R5_YS], [R5_Z-0.05, R5_Z], "R5 Floor", "tan")

S_D_X_START = R5_XW - 0.49
S_D_X_END = S_D_X_START - 0.89 
NW_WIN_Z_SILL, NW_WIN_Z_HEAD = R5_Z + 1.72, R5_Z + 1.72 + 0.29
NW_WIN_X_START = S_D_X_END - 0.335
NW_WIN_X_END = NW_WIN_X_START - 1.0

add_3d_wall(fig, [R5_XW, S_D_X_START], [R5_YN, R5_YN+T], [R5_Z, R5_CEIL], "R5 N Wall W", R5_C)
add_3d_wall(fig, [S_D_X_START, S_D_X_END], [R5_YN, R5_YN+T], [R5_Z+2.03, R5_CEIL], "R5 N Door Header", R5_C)
add_3d_wall(fig, [S_D_X_START, S_D_X_END], [R5_YN+T/2, R5_YN+T/2], [R5_Z, R5_Z+2.03], "Entrance R5 N Glass", ENT_C) 
add_3d_wall(fig, [S_D_X_END, NW_WIN_X_START], [R5_YN, R5_YN+T], [R5_Z, R5_CEIL], "R5 N Wall Mid", R5_C)
add_3d_wall(fig, [NW_WIN_X_START, NW_WIN_X_END], [R5_YN, R5_YN+T], [R5_Z, NW_WIN_Z_SILL], "R5 N Win Sill", R5_C)
add_3d_wall(fig, [NW_WIN_X_START, NW_WIN_X_END], [R5_YN, R5_YN+T], [NW_WIN_Z_HEAD, R5_CEIL], "R5 N Win Header", R5_C)
add_3d_wall(fig, [NW_WIN_X_END, R5_XE], [R5_YN, R5_YN+T], [R5_Z, R5_CEIL], "R5 N Wall E", R5_C)
add_3d_wall(fig, [NW_WIN_X_START, NW_WIN_X_END], [R5_YN+T/2, R5_YN+T/2], [NW_WIN_Z_SILL, NW_WIN_Z_HEAD], "Glass R5 N", G_C, G_O)

# East Wall 
E_W_Y1, E_W_Y2 = R5_YN + 0.70, R5_YN + 1.68
E_WIN_Z_SILL, E_WIN_Z_HEAD = R5_Z + 1.22, R5_Z + 1.22 + 0.79
add_3d_wall(fig, [R5_XE, R5_XE+T], [R5_YN, E_W_Y1], [R5_Z, R5_CEIL], "R5 E Wall N", R5_C)
add_3d_wall(fig, [R5_XE, R5_XE+T], [E_W_Y1, E_W_Y2], [R5_Z, E_WIN_Z_SILL], "R5 E Sill", R5_C)
add_3d_wall(fig, [R5_XE, R5_XE+T], [E_W_Y1, E_W_Y2], [E_WIN_Z_HEAD, R5_CEIL], "R5 E Header", R5_C)
add_3d_wall(fig, [R5_XE, R5_XE+T], [E_W_Y2, R5_YS], [R5_Z, R5_CEIL], "R5 E Wall S", R5_C)
add_3d_wall(fig, [R5_XE+T/2, R5_XE+T/2], [E_W_Y1, E_W_Y2], [E_WIN_Z_SILL, E_WIN_Z_HEAD], "Glass R5 E", G_C, G_O)

# South Wall
S_W_X1, S_W_X2 = R5_XE + 0.36, R5_XE + 1.26
S_WIN_Z_SILL, S_WIN_Z_HEAD = R5_Z + 1.31, R5_Z + 1.31 + 0.72
add_3d_wall(fig, [R5_XW, S_D_X_START], [R5_YS, R5_YS+T], [R5_Z, R5_CEIL], "R5 S Wall W", R5_C)
add_3d_wall(fig, [S_D_X_START, S_D_X_END], [R5_YS, R5_YS+T], [R5_Z+2.03, R5_CEIL], "R5 S Door Header", R5_C)
add_3d_wall(fig, [S_D_X_START, S_D_X_END], [R5_YS+T/2, R5_YS+T/2], [R5_Z, R5_Z+2.03], "Entrance R5 S Glass", ENT_C)
add_3d_wall(fig, [S_D_X_END, S_W_X2], [R5_YS, R5_YS+T], [R5_Z, R5_CEIL], "R5 S Wall Mid", R5_C)
add_3d_wall(fig, [S_W_X2, S_W_X1], [R5_YS, R5_YS+T], [R5_Z, S_WIN_Z_SILL], "R5 S Win Sill", R5_C)
add_3d_wall(fig, [S_W_X2, S_W_X1], [R5_YS, R5_YS+T], [S_WIN_Z_HEAD, R5_CEIL], "R5 S Win Header", R5_C)
add_3d_wall(fig, [S_W_X1, R5_XE], [R5_YS, R5_YS+T], [R5_Z, R5_CEIL], "R5 S Wall E", R5_C)
add_3d_wall(fig, [S_W_X2, S_W_X1], [R5_YS+T/2, R5_YS+T/2], [S_WIN_Z_SILL, S_WIN_Z_HEAD], "Glass R5 S", G_C, G_O)

# --- 7. INTERNAL PARTITION ---
INT_X = S_D_X_END - 0.36
INT_Y1, INT_Y2, INT_Y3 = R5_YS - 0.35, R5_YS - 1.15, R5_YS - 2.15
W_INT_X1, W_INT_X2 = INT_X - 0.11, INT_X - 1.10
add_3d_wall(fig, [INT_X, INT_X+0.05], [R5_YS, INT_Y1], [R5_Z, R5_CEIL], "Int Vert 1", "silver")
add_3d_wall(fig, [INT_X, INT_X+0.05], [INT_Y1, INT_Y2], [R5_Z+2.01, R5_CEIL], "Int Door Header", "silver")
add_3d_wall(fig, [INT_X+0.025, INT_X+0.025], [INT_Y1, INT_Y2], [R5_Z, R5_Z+2.01], "Int Entrance Glass", ENT_C)
add_3d_wall(fig, [INT_X, INT_X+0.05], [INT_Y2, INT_Y3], [R5_Z, R5_CEIL], "Int Vert 2", "silver")
I_WIN_Z_SILL, I_WIN_Z_HEAD = R5_Z + 1.29, R5_Z + 1.29 + 0.71
add_3d_wall(fig, [INT_X, W_INT_X1], [INT_Y3, INT_Y3+0.05], [R5_Z, R5_CEIL], "Int Horiz 1", "silver")
add_3d_wall(fig, [W_INT_X1, W_INT_X2], [INT_Y3, INT_Y3+0.05], [R5_Z, I_WIN_Z_SILL], "Int Win Sill", "silver")
add_3d_wall(fig, [W_INT_X1, W_INT_X2], [INT_Y3, INT_Y3+0.05], [I_WIN_Z_HEAD, R5_CEIL], "Int Win Header", "silver")
add_3d_wall(fig, [W_INT_X2, R5_XE], [INT_Y3, INT_Y3+0.05], [R5_Z, R5_CEIL], "Int Horiz 2", "silver")
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

