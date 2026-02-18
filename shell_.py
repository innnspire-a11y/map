import streamlit as st
import plotly.graph_objects as go

# --- 1. Page Configuration ---
st.set_page_config(layout="wide", page_title="Digital Twin")

# --- 2. CSS UI cleanup ---
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div[data-testid="stToolbar"] {display: none !important;}
    .stAppDeployButton {display:none !important;}
    div[data-testid="stDecoration"] {display:none !important;}
    .block-container {padding-top: 0rem;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- 3. Data Store for Search ---
if 'wall_data' not in st.session_state:
    st.session_state.wall_data = {}

# --- 4. Enhanced Wall Function ---
def add_3d_wall(fig, x_range, y_range, z_range, name="Wall", color='firebrick', opacity=0.9):
    x_min, x_max = min(x_range), max(x_range)
    y_min, y_max = min(y_range), max(y_range)
    z_min, z_max = min(z_range), max(z_range)
    
    # Calculate dimensions for the search feature
    dx = abs(x_max - x_min)
    dy = abs(y_max - y_min)
    dz = abs(z_max - z_min)
    
    # Length is the longest horizontal dimension, height is vertical (Z)
    length = round(max(dx, dy), 2)
    thickness = round(min(dx, dy), 2)
    if thickness == 0: thickness = 0.02 # Handle glass/thin objects
    height = round(dz, 2)
    
    # Store data for the sidebar search
    st.session_state.wall_data[name] = {"Length": length, "Height": height, "Thickness": thickness}
    
    fig.add_trace(go.Mesh3d(
        x=[x_min, x_max, x_max, x_min, x_min, x_max, x_max, x_min],
        y=[y_min, y_min, y_max, y_max, y_min, y_min, y_max, y_max],
        z=[z_min, z_min, z_min, z_min, z_max, z_max, z_max, z_max],
        i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
        j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
        k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
        opacity=opacity,
        color=color,
        flatshading=True,
        name=name
    ))

# --- 5. Constants & Initialization ---
st.title("Digital Twin: Building")
fig = go.Figure()

T = 0.22
CEILING_H = 2.50
SLAB_TOP = 2.73
WEST_LIMIT_X = 4.84 + 0.5  
R3_Y_DIVIDE = 7.72
R3_Y_END = R3_Y_DIVIDE + 3.35 
R1_C, R2_C, R3_C, R4_C, R5_C = "royalblue", "firebrick", "darkgreen", "slategrey", "darkorange"
TAB_C, G_C, G_O = "plum", "skyblue", 0.4
ENT_C = "rgba(0, 255, 100, 0.4)"
KITCHEN_C, BATH_C = "lightsalmon", "lightseagreen"
DOOR_C = "peru"

# --- 6. BUILDING CONSTRUCTION ---

# --- ROOM 1: MAIN HALL ---
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

# --- HOLLOW PILLARS ---
P_DEPTH, P_WIDTH = 0.50, 0.63
SPAN_START, SPAN_END = -T, R3_Y_END + T
TOTAL_SPAN_LENGTH = SPAN_END - SPAN_START
P_X_OUT = WEST_LIMIT_X + P_DEPTH
gap = (TOTAL_SPAN_LENGTH - (4 * P_WIDTH)) / 3
pillar_starts = [SPAN_START, SPAN_START + P_WIDTH + gap, SPAN_START + 2 * (P_WIDTH + gap) + 0.43, SPAN_END - P_WIDTH]

for i, y_start in enumerate(pillar_starts):
    y_end = y_start + P_WIDTH
    add_3d_wall(fig, [WEST_LIMIT_X, P_X_OUT], [y_start, y_start+0.02], [0, CEILING_H], f"Hollow P{i+1} S", "gray")
    add_3d_wall(fig, [P_X_OUT-0.02, P_X_OUT], [y_start, y_end], [0, CEILING_H], f"Hollow P{i+1} W", "gray")
    add_3d_wall(fig, [WEST_LIMIT_X, P_X_OUT], [y_end-0.02, y_end], [0, CEILING_H], f"Hollow P{i+1} N", "gray")

# --- WESTERN COLONNADE ---
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [0, 0.90], [0, CEILING_H], "West Corner Pillar", R1_C)
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [0.90, 2.99], [0, 0.17], "West Curb", R1_C)
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [2.99, 4.53], [0, CEILING_H], "West Mid Pillar", R1_C)
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [7.03, R3_Y_DIVIDE], [0, CEILING_H], "West Corner South", R1_C)

# --- ROOM 2: EAST WING ---
R2_X_END = -1.79
add_3d_wall(fig, [-0.62, 0], [-T, 0], [0, CEILING_H], "R2 N Pillar", R2_C)
add_3d_wall(fig, [-1.325, -0.62], [-T, 0], [0, 1.46], "R2 N Sill", R2_C)
add_3d_wall(fig, [-1.325, -0.62], [-T, 0], [2.06, CEILING_H], "R2 N Header", R2_C)
add_3d_wall(fig, [-1.325, -0.62], [-T/2, -T/2], [1.46, 2.06], "Glass R2 N", G_C, G_O)
add_3d_wall(fig, [R2_X_END, -1.325], [-T, 0], [0, CEILING_H], "R2 N End", R2_C)
add_3d_wall(fig, [R2_X_END-T, R2_X_END], [-T, 2.42], [0, CEILING_H], "R2 East Wall", R2_C)
add_3d_wall(fig, [R2_X_END, 0], [2.42, 2.42+T], [0, CEILING_H], "R2 South Shared Wall", R2_C)

# --- ROOM 3: SOUTH WING ---
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

# --- ROOM 4: MEZZANINE ---
R4_X_RIGHT, R4_X_LEFT, R4_Y_TOP, R4_FLOOR, R4_Y_BOT = 0.0, R2_X_END, 2.42, 0.77, 5.0
add_3d_wall(fig, [R4_X_LEFT, R4_X_RIGHT], [R4_Y_TOP, R4_Y_BOT], [R4_FLOOR, R4_FLOOR+0.05], "R4 Floor", R4_C)
add_3d_wall(fig, [R4_X_LEFT, R4_X_RIGHT], [R4_Y_TOP, R4_Y_TOP+T], [R4_FLOOR, 2.5], "R4 North Shared Wall", R4_C)
add_3d_wall(fig, [-T, 0], [R4_Y_TOP, R4_Y_BOT], [R4_FLOOR, 2.5], "R4 West Shared Wall", R4_C)
add_3d_wall(fig, [R4_X_LEFT-T, R4_X_LEFT], [R4_Y_TOP, R4_Y_BOT], [R4_FLOOR, 2.5], "R4 East Wall", R4_C)
add_3d_wall(fig, [R4_X_LEFT + 0.82, R4_X_RIGHT], [R4_Y_BOT - T, R4_Y_BOT], [R4_FLOOR, 2.5], "R4 South Wall", R4_C)
add_3d_wall(fig, [R4_X_LEFT, R4_X_LEFT + 0.82], [R4_Y_BOT - T + T/2, R4_Y_BOT - T + T/2], [R4_FLOOR, 2.5], "R4 Entrance Glass", ENT_C)

# --- ROOM 5: THE HUB ---
R5_XW, R5_XE, R5_YN, R5_YS, R5_Z, R5_CEIL = -T, -T-3.75, 6.46, R3_Y_END, 0.45, CEILING_H
add_3d_wall(fig, [R5_XW, R5_XE], [R5_YN, R5_YS], [R5_Z-0.05, R5_Z], "R5 Floor", "tan")
S_D_X_START, S_D_X_END = R5_XW - 0.49, R5_XW - 0.49 - 0.89
NW_WIN_Z_SILL, NW_WIN_Z_HEAD = R5_Z + 1.72, R5_Z + 1.72 + 0.29
NW_X1, NW_X2 = S_D_X_END - 0.335, S_D_X_END - 0.335 - 1.0

add_3d_wall(fig, [R5_XW, S_D_X_START], [R5_YN, R5_YN+T], [R5_Z, R5_CEIL], "R5 N Wall W", R5_C)
add_3d_wall(fig, [S_D_X_START, S_D_X_END], [R5_YN, R5_YN+T], [R5_Z+2.03, R5_CEIL], "R5 N Door Header", R5_C)
add_3d_wall(fig, [S_D_X_START, S_D_X_END], [R5_YN+T/2, R5_YN+T/2], [R5_Z, R5_Z+2.03], "Entrance R5 N Glass", ENT_C)
add_3d_wall(fig, [S_D_X_END, NW_X1], [R5_YN, R5_YN+T], [R5_Z, R5_CEIL], "R5 N Wall Mid", R5_C)
add_3d_wall(fig, [NW_X1, NW_X2], [R5_YN, R5_YN+T], [R5_Z, NW_WIN_Z_SILL], "R5 N Win Sill", R5_C)
add_3d_wall(fig, [NW_X1, NW_X2], [R5_YN, R5_YN+T], [NW_WIN_Z_HEAD, R5_CEIL], "R5 N Win Header", R5_C)
add_3d_wall(fig, [NW_X2, R5_XE], [R5_YN, R5_YN+T], [R5_Z, R5_CEIL], "R5 N Wall E", R5_C)
add_3d_wall(fig, [NW_X1, NW_X2], [R5_YN+T/2, R5_YN+T/2], [NW_WIN_Z_SILL, NW_WIN_Z_HEAD], "Glass R5 N", G_C, G_O)

# R5 East/South/Internal
E_W_Y1, E_W_Y2, E_SILL, E_HEAD = R5_YN + 0.70, R5_YN + 1.68, R5_Z + 1.22, R5_Z + 2.01
add_3d_wall(fig, [R5_XE, R5_XE+T], [R5_YN, E_W_Y1], [R5_Z, R5_CEIL], "R5 E Wall N", R5_C)
add_3d_wall(fig, [R5_XE, R5_XE+T], [E_W_Y1, E_W_Y2], [R5_Z, E_SILL], "R5 E Sill", R5_C)
add_3d_wall(fig, [R5_XE, R5_XE+T], [E_W_Y1, E_W_Y2], [E_HEAD, R5_CEIL], "R5 E Header", R5_C)
add_3d_wall(fig, [R5_XE+T/2, R5_XE+T/2], [E_W_Y1, E_W_Y2], [E_SILL, E_HEAD], "Glass R5 E", G_C, G_O)
add_3d_wall(fig, [R5_XE, R5_XE+T], [E_W_Y2, R5_YS], [R5_Z, R5_CEIL], "R5 E Wall S", R5_C)

S_X1, S_X2, S_SILL, S_HEAD = R5_XE + 0.36, R5_XE + 1.26, R5_Z + 1.31, R5_Z + 2.03
add_3d_wall(fig, [R5_XW, S_D_X_START], [R5_YS, R5_YS+T], [R5_Z, R5_CEIL], "R5 S Wall W", R5_C)
add_3d_wall(fig, [S_D_X_START, S_D_X_END], [R5_YS, R5_YS+T], [R5_Z+2.03, R5_CEIL], "R5 S Door Header", R5_C)
add_3d_wall(fig, [S_D_X_START, S_D_X_END], [R5_YS+T/2, R5_YS+T/2], [R5_Z, R5_Z+2.03], "Entrance R5 S Glass", ENT_C)
add_3d_wall(fig, [S_D_X_END, S_X2], [R5_YS, R5_YS+T], [R5_Z, R5_CEIL], "R5 S Wall Mid", R5_C)
add_3d_wall(fig, [S_X2, S_X1], [R5_YS, R5_YS+T], [R5_Z, S_SILL], "R5 S Win Sill", R5_C)
add_3d_wall(fig, [S_X2, S_X1], [R5_YS, R5_YS+T], [S_HEAD, R5_CEIL], "R5 S Win Header", R5_C)
add_3d_wall(fig, [S_X1, R5_XE], [R5_YS, R5_YS+T], [R5_Z, R5_CEIL], "R5 S Wall E", R5_C)
add_3d_wall(fig, [S_X2, S_X1], [R5_YS+T/2, R5_YS+T/2], [S_SILL, S_HEAD], "Glass R5 S", G_C, G_O)

INT_X, INT_Y1, INT_Y2, INT_Y3 = S_D_X_END - 0.36, R5_YS - 0.35, R5_YS - 1.15, R5_YS - 2.15
W_INT1, W_INT2, I_SILL, I_HEAD = INT_X - 0.11, INT_X - 1.10, R5_Z + 1.29, R5_Z + 2.00
add_3d_wall(fig, [INT_X, INT_X+0.05], [R5_YS, INT_Y1], [R5_Z, R5_CEIL], "Int Vert 1", "silver")
add_3d_wall(fig, [INT_X, INT_X+0.05], [INT_Y1, INT_Y2], [R5_Z+2.01, R5_CEIL], "Int Door Header", "silver")
add_3d_wall(fig, [INT_X+0.025, INT_X+0.025], [INT_Y1, INT_Y2], [R5_Z, R5_Z+2.01], "Int Entrance Glass", ENT_C)
add_3d_wall(fig, [INT_X, INT_X+0.05], [INT_Y2, INT_Y3], [R5_Z, R5_CEIL], "Int Vert 2", "silver")
add_3d_wall(fig, [INT_X, W_INT1], [INT_Y3, INT_Y3+0.05], [R5_Z, R5_CEIL], "Int Horiz 1", "silver")
add_3d_wall(fig, [W_INT1, W_INT2], [INT_Y3, INT_Y3+0.05], [R5_Z, I_SILL], "Int Win Sill", "silver")
add_3d_wall(fig, [W_INT1, W_INT2], [INT_Y3, INT_Y3+0.05], [I_HEAD, R5_CEIL], "Int Win Header", "silver")
add_3d_wall(fig, [W_INT2, R5_XE], [INT_Y3, INT_Y3+0.05], [R5_Z, R5_CEIL], "Int Horiz 2", "silver")
add_3d_wall(fig, [W_INT1, W_INT2], [INT_Y3+0.025, INT_Y3+0.025], [I_SILL, I_HEAD], "Glass Int", G_C, G_O)

# --- STAIRCASE ---
curr_z, curr_x = 0.32, -1.1
y_f1_start, y_f1_end = 5.0, 6.4
f1_steps = [(0.19, 0.24), (0.21, 0.4), (0.19, 0.4), (0.18, 0.39), (0.18, 0.39), (0.18, 0.4), (0.18, 0.4), (0.18, 0.415)]
for i, (r, d) in enumerate(f1_steps):
    add_3d_wall(fig, [curr_x - d, curr_x], [y_f1_start, y_f1_end], [0, curr_z + r], f"Stair F1_{i+1}", "silver")
    curr_z += r; curr_x -= d
add_3d_wall(fig, [curr_x - 1.3, curr_x], [y_f1_start - 1.5, y_f1_end], [0, 1.81], "Mid Landing", "darkgray")
y_f2_s, y_f2_e, cz2, cx2 = y_f1_start - 1.62, y_f1_start - 0.22, 1.81, curr_x - 1.3
for i in range(6):
    add_3d_wall(fig, [cx2, cx2 + 0.5], [y_f2_s, y_f2_e], [0, cz2 + 0.153], f"Stair F2_{i+1}", "silver")
    cz2 += 0.153; cx2 += 0.5
add_3d_wall(fig, [cx2, 0], [y_f2_s, y_f2_e], [SLAB_TOP - 0.05, SLAB_TOP], "FF Arrival", "silver")

# --- SLAB & FIRST FLOOR ---
SL_N, SL_S = -T, R3_Y_END + T
add_3d_wall(fig, [0, WEST_LIMIT_X], [SL_N, SL_S], [CEILING_H, SLAB_TOP], "Slab West", "rgba(100,100,100,0.5)")
add_3d_wall(fig, [R2_X_END, 0], [SL_N, 2.42 + T], [CEILING_H, SLAB_TOP], "Slab NE", "rgba(100,100,100,0.5)")
add_3d_wall(fig, [R5_XE, 0], [R5_YN - 0.2, SL_S], [CEILING_H, SLAB_TOP], "Slab SE", "rgba(100,100,100,0.5)")

TAB_ZS, TAB_ZE = SLAB_TOP, SLAB_TOP + 2.50
ROOM_W = (SL_S - SL_N) / 4
for i in range(4):
    ymin, ymax = SL_N + (i * ROOM_W), SL_N + ((i+1) * ROOM_W)
    add_3d_wall(fig, [WEST_LIMIT_X - 3.5, WEST_LIMIT_X], [ymin, ymax], [TAB_ZS, TAB_ZE], f"FF Room {i+1}", TAB_C, 0.4)
    add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+0.05], [ymin, ymin + 0.5], [TAB_ZS, TAB_ZE], f"W-Wall L {i+1}", TAB_C)
    add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+0.05], [ymin + 0.5, ymin + 1.4], [TAB_ZS, TAB_ZS + 2.1], f"Balc Door {i+1}", DOOR_C, 0.8)
    add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+0.02], [ymin + 1.6, ymax - 0.4], [TAB_ZS + 1.0, TAB_ZS + 2.0], f"Window {i+1}", G_C, G_O)
    add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+0.05], [ymin + 1.4, ymax], [TAB_ZS, TAB_ZS + 1.0], f"Wall-Below-Window {i+1}", TAB_C)
    add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+0.05], [ymin + 1.4, ymax], [TAB_ZS + 2.0, TAB_ZE], f"Wall-Above-Window {i+1}", TAB_C)
    add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X + 1.0], [ymin, ymax], [TAB_ZS, TAB_ZS + 0.1], f"Balcony {i+1}", "grey")
    add_3d_wall(fig, [WEST_LIMIT_X + 1.0, WEST_LIMIT_X + 1.05], [ymin, ymax], [TAB_ZS, TAB_ZS + 1.1], f"Rail {i+1}", "black", 0.5)

add_3d_wall(fig, [R2_X_END, 0], [SL_N, 1.5], [TAB_ZS, TAB_ZE], "FF Kitchen", KITCHEN_C)
add_3d_wall(fig, [2.0, 2.0+T], [0, 3.5], [TAB_ZS, TAB_ZE], "Kitchen-Hall Split", "white")
add_3d_wall(fig, [R5_XE, 0], [R3_Y_END - 2.0, R3_Y_END], [TAB_ZS, TAB_ZE], "FF Bathroom", BATH_C)
add_3d_wall(fig, [R5_XE + 1.0, R5_XE + 2.5], [R3_Y_END - 4.5, R3_Y_END - 2.0], [TAB_ZS, TAB_ZE], "Wet Area Split", "lightgrey")
add_3d_wall(fig, [R5_XE + 1.1, R5_XE + 1.7], [R3_Y_END - 4.4, R3_Y_END - 3.3], [TAB_ZS, TAB_ZS+2.0], "Shower 1", "lightblue", 0.6)
add_3d_wall(fig, [R5_XE + 1.1, R5_XE + 1.7], [R3_Y_END - 3.2, R3_Y_END - 2.1], [TAB_ZS, TAB_ZS+2.0], "Shower 2", "lightblue", 0.6)
add_3d_wall(fig, [R2_X_END, WEST_LIMIT_X], [SL_N, SL_N+T], [TAB_ZS, TAB_ZE], "FF North Perimeter", TAB_C)
add_3d_wall(fig, [R5_XE, WEST_LIMIT_X], [SL_S-T, SL_S], [TAB_ZS, TAB_ZE], "FF South Perimeter", TAB_C)
add_3d_wall(fig, [R5_XE-T, R5_XE], [R5_YN, SL_S], [TAB_ZS, TAB_ZE], "FF East Perimeter", TAB_C)

# --- 7. Sidebar Search UI ---
st.sidebar.header("🔍 Wall Inspector")
search_query = st.sidebar.selectbox(
    "Select or Search a Wall:", 
    [""] + sorted(list(st.session_state.wall_data.keys()))
)

if search_query:
    data = st.session_state.wall_data[search_query]
    st.sidebar.info(f"**Component:** {search_query}")
    st.sidebar.write(f"📏 **Length:** {data['Length']} m")
    st.sidebar.write(f"⬆️ **Height:** {data['Height']} m")
    st.sidebar.write(f"厚 **Thickness:** {data['Thickness']} m")

# --- 8. Final Layout & Render ---
fig.update_layout(
    scene=dict(
        aspectmode='data', 
        camera=dict(eye=dict(x=-2.2, y=-2.2, z=2.5)),
        xaxis=dict(title="East-West"),
        yaxis=dict(title="North-South")
    ),
    margin=dict(l=0, r=0, b=0, t=50)
)
st.plotly_chart(fig, use_container_width=True)
