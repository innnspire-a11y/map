import streamlit as st
import plotly.graph_objects as go
import pandas as pd

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

# --- 3. Navigation Sidebar ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Digital Twin Model", "Materials & Dimensions"])

# --- 4. Data Store Initialization ---
if 'wall_data' not in st.session_state:
    st.session_state.wall_data = {}

# --- 5. Enhanced Wall Function ---
def add_3d_wall(fig, x_range, y_range, z_range, name="Wall", color='firebrick', opacity=0.9):
    x_min, x_max = min(x_range), max(x_range)
    y_min, y_max = min(y_range), max(y_range)
    z_min, z_max = min(z_range), max(z_range)
    
    dx = abs(x_max - x_min)
    dy = abs(y_max - y_min)
    dz = abs(z_max - z_min)
    
    length = round(max(dx, dy), 2)
    thickness = round(min(dx, dy), 2)
    if thickness == 0: thickness = 0.02 
    height = round(dz, 2)
    
    st.session_state.wall_data[name] = {
        "Length (m)": length, 
        "Height (m)": height, 
        "Thickness (m)": thickness,
        "Area (m²)": round(length * height, 2)
    }
    
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

# --- 6. Constants & Construction Logic ---
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

fig = go.Figure()

# --- BUILDING CONSTRUCTION BLOCKS ---
# GROUND FLOOR: ROOM 1
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

# PILLARS
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

# WESTERN COLONNADE
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [0, 0.90], [0, CEILING_H], "West Corner Pillar", R1_C)
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [0.90, 2.99], [0, 0.17], "West Curb", R1_C)
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [2.99, 4.53], [0, CEILING_H], "West Mid Pillar", R1_C)
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [7.03, R3_Y_DIVIDE], [0, CEILING_H], "West Corner South", R1_C)

# ROOM 2: EAST WING
R2_X_END = -1.79
add_3d_wall(fig, [-0.62, 0], [-T, 0], [0, CEILING_H], "R2 N Pillar", R2_C)
add_3d_wall(fig, [-1.325, -0.62], [-T, 0], [0, 1.46], "R2 N Sill", R2_C)
add_3d_wall(fig, [-1.325, -0.62], [-T, 0], [2.06, CEILING_H], "R2 N Header", R2_C)
add_3d_wall(fig, [-1.325, -0.62], [-T/2, -T/2], [1.46, 2.06], "Glass R2 N", G_C, G_O)
add_3d_wall(fig, [R2_X_END, -1.325], [-T, 0], [0, CEILING_H], "R2 N End", R2_C)
add_3d_wall(fig, [R2_X_END-T, R2_X_END], [-T, 2.42], [0, CEILING_H], "R2 East Wall", R2_C)
add_3d_wall(fig, [R2_X_END, 0], [2.42, 2.42+T], [0, CEILING_H], "R2 South Shared Wall", R2_C)

# ROOM 3: SOUTH WING
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

# ROOM 4: MEZZANINE
R4_X_RIGHT, R4_X_LEFT, R4_Y_TOP, R4_FLOOR, R4_Y_BOT = 0.0, R2_X_END, 2.42, 0.77, 5.0
add_3d_wall(fig, [R4_X_LEFT, R4_X_RIGHT], [R4_Y_TOP, R4_Y_BOT], [R4_FLOOR, R4_FLOOR+0.05], "R4 Floor", R4_C)
add_3d_wall(fig, [R4_X_LEFT, R4_X_RIGHT], [R4_Y_TOP, R4_Y_TOP+T], [R4_FLOOR, 2.5], "R4 North Shared Wall", R4_C)
add_3d_wall(fig, [-T, 0], [R4_Y_TOP, R4_Y_BOT], [R4_FLOOR, 2.5], "R4 West Shared Wall", R4_C)
add_3d_wall(fig, [R4_X_LEFT-T, R4_X_LEFT], [R4_Y_TOP, R4_Y_BOT], [R4_FLOOR, 2.5], "R4 East Wall", R4_C)
add_3d_wall(fig, [R4_X_LEFT + 0.82, R4_X_RIGHT], [R4_Y_BOT - T, R4_Y_BOT], [R4_FLOOR, 2.5], "R4 South Wall", R4_C)
add_3d_wall(fig, [R4_X_LEFT, R4_X_LEFT + 0.82], [R4_Y_BOT - T + T/2, R4_Y_BOT - T + T/2], [R4_FLOOR, 2.5], "R4 Entrance Glass", ENT_C)

# ROOM 5: THE HUB
R5_XW, R5_XE, R5_YN, R5_YS, R5_Z, R5_CEIL = -T, -3.97, 6.46, R3_Y_END, 0.45, CEILING_H
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
E_W_Y1, E_W_Y2, E_SILL, E_HEAD = R5_YN + 0.70, R5_YN + 1.68, R5_Z + 1.22, R5_Z + 2.01
add_3d_wall(fig, [R5_XE, R5_XE+T], [R5_YN, E_W_Y1], [R5_Z, R5_CEIL], "R5 E Wall N", R5_C)
add_3d_wall(fig, [R5_XE, R5_XE+T], [E_W_Y1, E_W_Y2], [R5_Z, E_SILL], "R5 E Sill", R5_C)
add_3d_wall(fig, [R5_XE, R5_XE+T], [E_W_Y1, E_W_Y2], [E_SILL, E_HEAD], "R5 E Header", R5_C)
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

# STAIRS
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

# SLABS
SL_N, SL_S = -T, R3_Y_END + T
add_3d_wall(fig, [0, WEST_LIMIT_X], [SL_N, SL_S], [CEILING_H, SLAB_TOP], "Slab West", "rgba(100,100,100,0.5)")
add_3d_wall(fig, [R2_X_END, 0], [SL_N, 2.42 + T], [CEILING_H, SLAB_TOP], "Slab NE", "rgba(100,100,100,0.5)")
add_3d_wall(fig, [R5_XE, 0], [R5_YN - 0.2, SL_S], [CEILING_H, SLAB_TOP], "Slab SE", "rgba(100,100,100,0.5)")

# FIRST FLOOR
TAB_ZS, TAB_ZE = SLAB_TOP, SLAB_TOP + 2.50
ROOM_W = (SL_S - SL_N) / 4
TAB_C_STRONG = "#9932CC"
for i in range(4):
    ymin = SL_N + i * ROOM_W
    ymax = SL_N + (i + 1) * ROOM_W
    add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X + T], [ymin, ymin + 0.5], [TAB_ZS, TAB_ZE], f"FF W-Wall {i+1}a", TAB_C_STRONG)
    add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X + T], [ymin + 0.5, ymin + 1.4], [TAB_ZS, TAB_ZS + 2.1], f"Balc Door {i+1}", DOOR_C)
    add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X + T], [ymin + 0.5, ymin + 1.4], [TAB_ZS + 2.1, TAB_ZE], f"Balc Door {i+1} Header", TAB_C_STRONG)
    add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X + T], [ymin + 1.4, ymin + 1.6], [TAB_ZS, TAB_ZE], f"FF W-Wall {i+1}b", TAB_C_STRONG)
    add_3d_wall(fig, [WEST_LIMIT_X + T/2, WEST_LIMIT_X + T/2], [ymin + 1.6, ymin + 2.5], [TAB_ZS + 1.0, TAB_ZS + 2.0], f"FF Window {i+1}", G_C, G_O)
    add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X + T], [ymin + 1.6, ymin + 2.5], [TAB_ZS, TAB_ZS + 1.0], f"FF W-Sill {i+1}", TAB_C_STRONG)
    add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X + T], [ymin + 1.6, ymin + 2.5], [TAB_ZS + 2.0, TAB_ZE], f"FF W-Header {i+1}", TAB_C_STRONG)
    add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X + T], [ymin + 2.5, ymax], [TAB_ZS, TAB_ZE], f"FF W-Wall {i+1}c", TAB_C_STRONG)
    y_pos = SL_N + i * ROOM_W
    add_3d_wall(fig, [WEST_LIMIT_X - 3.5, WEST_LIMIT_X], [y_pos, y_pos + T], [TAB_ZS, TAB_ZE], f"FF Divider {i+1}", TAB_C_STRONG)

# --- UPDATED SERVICE CORE ALIGNMENT (Stacked over Ground Floor x=0) ---

# 1. FF EXTRA WALL (Stacked over Ground Floor x=0)
add_3d_wall(fig, [-0.22, -0.22 + T], [5.0, 6.45], [TAB_ZS, TAB_ZE], "FF Extra Wall Aligned", TAB_C)

# 2. KITCHEN (East side aligned to x=0)
K_XW, K_XE, K_YN, K_YS = 0.0, -2.0, 5.0, -0.22 
OP_S, OP_E = 3.38, 4.78
add_3d_wall(fig, [K_XE, K_XW], [K_YN - T, K_YN], [TAB_ZS, TAB_ZE], "FF Kitchen South Wall", KITCHEN_C)
add_3d_wall(fig, [K_XW - T, K_XW], [K_YS, OP_S], [TAB_ZS, TAB_ZE], "FF Kitchen East-South", KITCHEN_C)
add_3d_wall(fig, [K_XW - T, K_XW], [OP_E, K_YN], [TAB_ZS, TAB_ZE], "FF Kitchen East-North", KITCHEN_C)
add_3d_wall(fig, [K_XE, K_XE + T], [K_YS, OP_S], [TAB_ZS, TAB_ZE], "FF Kitchen West-South", KITCHEN_C)
add_3d_wall(fig, [K_XE, K_XE + T], [OP_E, K_YN], [TAB_ZS, TAB_ZE], "FF Kitchen West-North", KITCHEN_C)

# 3. BATHROOM COMPLEX (East wall aligned to x=0)
BX_0, BX_W, BY_N, BY_S = 0.0, -3.97, 11.29, 6.46 

# External Shell
add_3d_wall(fig, [BX_W, BX_0], [BY_N - T, BY_N], [TAB_ZS, TAB_ZE], "BATH North Outer Wall", BATH_C)
add_3d_wall(fig, [BX_W, BX_0], [BY_S, BY_S + T], [TAB_ZS, TAB_ZE], "BATH South Outer Wall", BATH_C)
add_3d_wall(fig, [BX_W, BX_W + T], [BY_S, BY_N], [TAB_ZS, TAB_ZE], "BATH West Outer Wall", BATH_C)
add_3d_wall(fig, [BX_0 - T, BX_0], [BY_S, BY_N], [TAB_ZS, TAB_ZE], "BATH East Outer Wall Aligned", BATH_C)

# Central Vanity
add_3d_wall(fig, [BX_W + 1.0, BX_0 - 1.0], [BY_S + 2.0, BY_S + 2.6], [TAB_ZS, TAB_ZS + 0.9], "BATH Central Vanity", "sandybrown")

# Toilet Area (3 Stalls)
stall_depth = 1.5
for i in range(3):
    y_stall = BY_S + T + (i * 1.1)
    add_3d_wall(fig, [BX_W + T, BX_W + T + stall_depth], [y_stall, y_stall + 0.05], [TAB_ZS, TAB_ZE], f"WC Stall {i+1} Partition", BATH_C, 0.7)
    if (i + 1) != 3:
        add_3d_wall(fig, [BX_W + T + stall_depth, BX_W + T + stall_depth], [y_stall + 0.1, y_stall + 1.0], [TAB_ZS, TAB_ZS + 2.1], f"WC Door {i+1}", DOOR_C)

# Shower Area
for i in range(3):
    x_sh = BX_0 - T - (i * 1.2)
    add_3d_wall(fig, [x_sh, x_sh - 0.05], [BY_N - T - 1.5, BY_N - T], [TAB_ZS, TAB_ZE], f"SH Stall {i+1} Partition", "lightblue", 0.5)
    add_3d_wall(fig, [x_sh, x_sh - 1.2], [BY_N - T - 1.5, BY_N - T - 1.5], [TAB_ZS, TAB_ZS + 2.0], f"SH Glass {i+1}", G_C, 0.3)

# Entrance & Privacy
add_3d_wall(fig, [BX_0 - T, BX_0], [BY_S + 0.5, BY_S + 1.5], [TAB_ZS, TAB_ZS + 2.1], "BATH Entrance Door", DOOR_C)
add_3d_wall(fig, [BX_0 - 1.5, BX_0 - T], [BY_S + 1.8, BY_S + 1.85], [TAB_ZS, TAB_ZE], "BATH Privacy Screen", BATH_C)

# ── Aligned East Doors (Residential Units) ──────────────
EAST_WALL_X = 1.84
for i in range(4):
    ymin = SL_N + i * ROOM_W
    door_y_start, door_y_end = ymin + 0.5, ymin + 1.4
    ymax = SL_N + (i + 1) * ROOM_W
    add_3d_wall(fig, [EAST_WALL_X, EAST_WALL_X + T], [ymin, door_y_start], [TAB_ZS, TAB_ZE], f"FF E-Wall {i+1}a", TAB_C_STRONG)
    add_3d_wall(fig, [EAST_WALL_X, EAST_WALL_X + T], [door_y_start, door_y_end], [TAB_ZS, TAB_ZS + 2.1], f"FF Door {i+1}", DOOR_C)
    add_3d_wall(fig, [EAST_WALL_X, EAST_WALL_X + T], [door_y_start, door_y_end], [TAB_ZS + 2.1, TAB_ZE], f"FF Door {i+1} Header", TAB_C_STRONG)
    add_3d_wall(fig, [EAST_WALL_X, EAST_WALL_X + T], [door_y_end, ymax], [TAB_ZS, TAB_ZE], f"FF E-Wall {i+1}b", TAB_C_STRONG)

# ── Perimeters & Balconies ──────────────────────────
for i in range(4):
    ymin, ymax = SL_N + (i * ROOM_W), SL_N + ((i + 1) * ROOM_W)
    add_3d_wall(fig, [WEST_LIMIT_X + T, WEST_LIMIT_X + T + 1.0], [ymin, ymax], [TAB_ZS, TAB_ZS + 0.1], f"Balcony {i+1}", "grey")
    add_3d_wall(fig, [WEST_LIMIT_X + T + 1.0, WEST_LIMIT_X + T + 1.05], [ymin, ymax], [TAB_ZS, TAB_ZS + 1.1], f"Rail {i+1}", "black", 0.5)

add_3d_wall(fig, [R2_X_END, WEST_LIMIT_X], [SL_N, SL_N+T], [TAB_ZS, TAB_ZE], "FF North Perimeter", TAB_C_STRONG)
add_3d_wall(fig, [BX_W, WEST_LIMIT_X], [SL_S-T, SL_S], [TAB_ZS, TAB_ZE], "FF South Perimeter", TAB_C_STRONG)
add_3d_wall(fig, [BX_W-T, BX_W], [BY_S, SL_S], [TAB_ZS, TAB_ZE], "FF East Perimeter Hub Side", TAB_C_STRONG)

# --- 7. Page Rendering Logic ---
if page == "Digital Twin Model":
    st.title("Digital Twin: Vertical Alignment Applied")
    fig.update_layout(
        scene=dict(aspectmode='data', camera=dict(eye=dict(x=-2.2, y=-2.2, z=2.5))),
        margin=dict(l=0, r=0, b=0, t=50)
    )
    st.plotly_chart(fig, use_container_width=True)

elif page == "Materials & Dimensions":
    st.title("🧱 Materials & Wall Dimensions")
    df = pd.DataFrame.from_dict(st.session_state.wall_data, orient='index')
    df.index.name = 'Component Name'
    df.reset_index(inplace=True)
    
    search_query = st.text_input("🔍 Search for a component")
    if search_query:
        df = df[df['Component Name'].str.contains(search_query, case=False)]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Components", len(df))
    col2.metric("Surface Area", f"{df['Area (m²)'].sum():.2f} m²")
    col3.metric("Avg Height", f"{df['Height (m)'].mean():.2f} m")
    
    st.dataframe(df, use_container_width=True, height=600)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV", csv, "materials.csv", "text/csv")
