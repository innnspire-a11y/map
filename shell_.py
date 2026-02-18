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

def add_3d_wall(fig, x_range, y_range, z_range, name="Wall", color='firebrick', opacity=0.9):
    x_min, x_max = min(x_range), max(x_range)
    y_min, y_max = min(y_range), max(y_range)
    z_min, z_max = min(z_range), max(z_range)
    
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

st.title("Digital Twin: Building (4-Room Upper Floor with Doors & Windows)")

fig = go.Figure()

# --- CONSTANTS ---
T = 0.22
CEILING_H = 2.50
SLAB_TOP = 2.73
WEST_LIMIT_X = 4.84 + 0.5  # Extended by 0.5m
R3_Y_DIVIDE = 7.72
R3_Y_END = R3_Y_DIVIDE + 3.35 
R1_C, R2_C, R3_C, R4_C, R5_C = "royalblue", "firebrick", "darkgreen", "slategrey", "darkorange"
TAB_C, G_C, G_O = "plum", "skyblue", 0.4
ENT_C = "rgba(0, 255, 100, 0.4)"
KITCHEN_C, BATH_C = "lightsalmon", "lightseagreen"
DOOR_C = "peru"

R5_XW, R5_XE = -T, -T - 3.75 
R5_Z, R5_CEIL = 0.45, CEILING_H
R5_YN, R5_YS = 6.46, R3_Y_END

# --- GROUND FLOOR: ROOM 1 (MAIN HALL) ---
add_3d_wall(fig, [0, 4.84], [-T, 0], [0, CEILING_H], "R1 North Wall", R1_C)
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
add_3d_wall(fig, [2.77, 4.84], [R3_Y_DIVIDE, R3_Y_DIVIDE+T], [0, CEILING_H], "R1 South Divider W", R1_C)

# --- GROUND FLOOR: ROOM 2 & 4 ---
R2_X_END = -1.79
add_3d_wall(fig, [-0.62, 0], [-T, 0], [0, CEILING_H], "R2 N Pillar", R2_C)
add_3d_wall(fig, [-1.325, -0.62], [-T, 0], [0, 1.46], "R2 N Sill", R2_C)
add_3d_wall(fig, [-1.325, -0.62], [-T, 0], [2.06, CEILING_H], "R2 N Header", R2_C)
add_3d_wall(fig, [-1.325, -0.62], [-T/2, -T/2], [1.46, 2.06], "Glass R2 N", G_C, G_O)
add_3d_wall(fig, [R2_X_END, -1.325], [-T, 0], [0, CEILING_H], "R2 N End", R2_C)
add_3d_wall(fig, [R2_X_END-T, R2_X_END], [-T, 2.42], [0, CEILING_H], "R2 East Wall", R2_C)
add_3d_wall(fig, [R2_X_END, 0], [2.42, 2.42+T], [0, CEILING_H], "R2 South Shared Wall", R2_C)
R4_X_LEFT, R4_Y_TOP, R4_FLOOR, R4_Y_BOTTOM_EDGE = R2_X_END, 2.42, 0.77, 5.0
add_3d_wall(fig, [R4_X_LEFT, 0], [R4_Y_TOP, R4_Y_BOTTOM_EDGE], [R4_FLOOR, R4_FLOOR+0.05], "R4 Floor", R4_C)
add_3d_wall(fig, [R4_X_LEFT, 0], [R4_Y_TOP, R4_Y_TOP+T], [R4_FLOOR, 2.5], "R4 North Shared Wall", R4_C)
add_3d_wall(fig, [-T, 0], [R4_Y_TOP, R4_Y_BOTTOM_EDGE], [R4_FLOOR, 2.5], "R4 West Shared Wall", R4_C)
add_3d_wall(fig, [R4_X_LEFT-T, R4_X_LEFT], [R4_Y_TOP, R4_Y_BOTTOM_EDGE], [R4_FLOOR, 2.5], "R4 East Wall", R4_C)
add_3d_wall(fig, [R4_X_LEFT + 0.82, 0], [R4_Y_BOTTOM_EDGE - T, R4_Y_BOTTOM_EDGE], [R4_FLOOR, 2.5], "R4 South Wall", R4_C)

# --- GROUND FLOOR: ROOM 5 ---
add_3d_wall(fig, [-T, R5_XE], [R5_YN, R5_YS], [R5_Z-0.05, R5_Z], "R5 Floor", "tan")
add_3d_wall(fig, [R5_XW, R5_XE], [R5_YN, R5_YN+T], [R5_Z, R5_CEIL], "R5 N Wall", R5_C)
add_3d_wall(fig, [R5_XE, R5_XE+T], [R5_YN, R5_YS], [R5_Z, R5_CEIL], "R5 E Wall", R5_C)
add_3d_wall(fig, [R5_XW, R5_XE], [R5_YS, R5_YS+T], [R5_Z, R5_CEIL], "R5 S Wall", R5_C)

# --- STAIRCASE SYSTEM (U-TURN) ---
curr_z, curr_x = 0.32, -1.1
y_f1_start, y_f1_end = 5.0, 6.4
f1_steps = [(0.19, 0.24), (0.21, 0.4), (0.19, 0.4), (0.18, 0.39), (0.18, 0.39), (0.18, 0.4), (0.18, 0.4), (0.18, 0.415)]
for i, (r, d) in enumerate(f1_steps):
    add_3d_wall(fig, [curr_x - d, curr_x], [y_f1_start, y_f1_end], [0, curr_z + r], f"Stair F1_{i+1}", "silver")
    curr_z += r
    curr_x -= d
landing_depth = 1.3
add_3d_wall(fig, [curr_x - landing_depth, curr_x], [y_f1_start - 1.5, y_f1_end], [0, 1.81], "Mid Landing", "darkgray")
y_f2_start, y_f2_end = y_f1_start - 1.62, y_f1_start - 0.22 
curr_z_f2, curr_x_f2 = 1.81, curr_x - landing_depth 
for i in range(6):
    add_3d_wall(fig, [curr_x_f2, curr_x_f2 + 0.5], [y_f2_start, y_f2_end], [0, curr_z_f2 + 0.153], f"Stair F2_{i+1}", "silver")
    curr_z_f2 += 0.153
    curr_x_f2 += 0.5
add_3d_wall(fig, [curr_x_f2, 0], [y_f2_start, y_f2_end], [SLAB_TOP - 0.05, SLAB_TOP], "FF Arrival", "silver")

# --- CONCRETE SLAB ---
SLAB_Y_N, SLAB_Y_S = -T, R3_Y_END + T
add_3d_wall(fig, [0, WEST_LIMIT_X], [SLAB_Y_N, SLAB_Y_S], [CEILING_H, SLAB_TOP], "Slab West Extended", "rgba(100,100,100,0.5)")
add_3d_wall(fig, [R2_X_END, 0], [SLAB_Y_N, 2.42 + T], [CEILING_H, SLAB_TOP], "Slab NE", "rgba(100,100,100,0.5)")
add_3d_wall(fig, [R5_XE, 0], [R5_YN - 0.2, SLAB_Y_S], [CEILING_H, SLAB_TOP], "Slab SE", "rgba(100,100,100,0.5)")

# --- FIRST FLOOR INTERIOR (4 ROOMS) & BALCONIES ---
TAB_Z_S, TAB_Z_E = SLAB_TOP, SLAB_TOP + 2.50
ROOM_COUNT = 4
ROOM_WIDTH_Y = (SLAB_Y_S - SLAB_Y_N) / ROOM_COUNT

for i in range(ROOM_COUNT):
    y_min, y_max = SLAB_Y_N + (i * ROOM_WIDTH_Y), SLAB_Y_N + ((i+1) * ROOM_WIDTH_Y)
    
    # 1. Room Shell
    add_3d_wall(fig, [WEST_LIMIT_X - 3.5, WEST_LIMIT_X], [y_min, y_max], [TAB_Z_S, TAB_Z_E], f"FF Room {i+1}", TAB_C, 0.4)
    
    # 2. West Wall with Window and Balcony Door
    # Wall Part Left of Door
    add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+0.05], [y_min, y_min + 0.5], [TAB_Z_S, TAB_Z_E], f"W-Wall L {i+1}", TAB_C)
    # Balcony Door
    add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+0.05], [y_min + 0.5, y_min + 1.4], [TAB_Z_S, TAB_Z_S + 2.1], f"Balc Door {i+1}", DOOR_C, 0.8)
    # Window
    add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+0.02], [y_min + 1.6, y_max - 0.4], [TAB_Z_S + 1.0, TAB_Z_S + 2.0], f"Window {i+1}", G_C, G_O)
    # Wall Part Right/Bottom/Top of Windows
    add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+0.05], [y_min + 1.4, y_max], [TAB_Z_S, TAB_Z_S + 1.0], f"Wall-Below-Window {i+1}", TAB_C)
    add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+0.05], [y_min + 1.4, y_max], [TAB_Z_S + 2.0, TAB_Z_E], f"Wall-Above-Window {i+1}", TAB_C)
    
    # 3. Balconies (West facing)
    add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X + 1.0], [y_min, y_max], [TAB_Z_S, TAB_Z_S + 0.1], f"Balcony {i+1}", "grey")
    # Railing
    add_3d_wall(fig, [WEST_LIMIT_X + 1.0, WEST_LIMIT_X + 1.05], [y_min, y_max], [TAB_Z_S, TAB_Z_S + 1.1], f"Rail {i+1}", "black", 0.5)

# --- FIRST FLOOR SERVICE AREAS ---
# FF Kitchen
add_3d_wall(fig, [R2_X_END, 0], [SLAB_Y_N, 1.5], [TAB_Z_S, TAB_Z_E], "FF Kitchen", KITCHEN_C)
add_3d_wall(fig, [2.0, 2.0+T], [0, 3.5], [TAB_Z_S, TAB_Z_E], "Kitchen-Hall Split", "white")

# FF Bathroom & Showers
add_3d_wall(fig, [R5_XE, 0], [R3_Y_END - 2.0, R3_Y_END], [TAB_Z_S, TAB_Z_E], "FF Bathroom", BATH_C)
WET_Y_START, WET_Y_END = 3.5, 6.5
add_3d_wall(fig, [R5_XE + 1.0, R5_XE + 2.5], [R3_Y_END - 4.5, R3_Y_END - 2.0], [TAB_Z_S, TAB_Z_E], "Wet Area Split", "lightgrey")
add_3d_wall(fig, [R5_XE + 1.1, R5_XE + 1.7], [R3_Y_END - 4.4, R3_Y_END - 3.3], [TAB_Z_S, TAB_Z_S+2.0], "Shower 1", "lightblue", 0.6)
add_3d_wall(fig, [R5_XE + 1.1, R5_XE + 1.7], [R3_Y_END - 3.2, R3_Y_END - 2.1], [TAB_Z_S, TAB_Z_S+2.0], "Shower 2", "lightblue", 0.6)

# FF Outer Perimeter Walls
add_3d_wall(fig, [R2_X_END, WEST_LIMIT_X], [SLAB_Y_N, SLAB_Y_N+T], [TAB_Z_S, TAB_Z_E], "FF North Perimeter", TAB_C)
add_3d_wall(fig, [R5_XE, WEST_LIMIT_X], [SLAB_Y_S-T, SLAB_Y_S], [TAB_Z_S, TAB_Z_E], "FF South Perimeter", TAB_C)
add_3d_wall(fig, [R5_XE-T, R5_XE], [R5_YN, SLAB_Y_S], [TAB_Z_S, TAB_Z_E], "FF East Perimeter", TAB_C)

# --- Final view ---
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
