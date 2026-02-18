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

st.title("Digital Twin: Complete Building Architecture")

fig = go.Figure()

# --- CONSTANTS ---
T = 0.22
CEILING_H = 2.50
SLAB_TOP = 2.73
WEST_LIMIT_X = 4.84
R3_Y_DIVIDE = 7.72
R3_Y_END = R3_Y_DIVIDE + 3.35  # 11.07
R1_C, R2_C, R3_C, R4_C, R5_C = "royalblue", "firebrick", "darkgreen", "slategrey", "darkorange"
TAB_C = "plum"
G_C, G_O = "skyblue", 0.4
ENT_C = "rgba(0, 255, 100, 0.4)"
KITCHEN_C, BATH_C = "lightsalmon", "lightseagreen"

# Room 5 Footprint
R5_XW, R5_XE = -T, -3.97
R5_YN, R5_YS = 6.46, R3_Y_END
R5_Z = 0.45

# --- GROUND FLOOR: ALL ORIGINAL FEATURES RESTORED ---

# 1. ROOM 1: MAIN HALL
add_3d_wall(fig, [0, WEST_LIMIT_X], [-T, 0], [0, CEILING_H], "R1 North Wall", R1_C)
add_3d_wall(fig, [-T, 0], [0, 1.15], [0, CEILING_H], "West Pillar 1", R1_C)
add_3d_wall(fig, [-T, 0], [1.15, 2.11], [2.06, CEILING_H], "West Door Header 1", R1_C)
add_3d_wall(fig, [-T/2, -T/2], [1.15, 2.11], [0, 2.06], "Entrance 1 Glass", ENT_C)
add_3d_wall(fig, [-T, 0], [2.11, 5.20], [0, CEILING_H], "West Mid Wall", R1_C)
add_3d_wall(fig, [-T, 0], [5.20, 6.01], [2.09, CEILING_H], "West Door Header 2", R1_C)
add_3d_wall(fig, [-T/2, -T/2], [5.20, 6.01], [0, 2.09], "Entrance 2 Glass", ENT_C)
add_3d_wall(fig, [-T, 0], [6.01, R3_Y_DIVIDE], [0, CEILING_H], "West Pillar 2", R1_C)

# 2. HOLLOW PILLARS
P_DEPTH, P_WIDTH = 0.50, 0.63
SPAN_START, SPAN_END = -T, R3_Y_END + T
P_X_OUT = WEST_LIMIT_X + P_DEPTH
gap = ((SPAN_END - SPAN_START) - (4 * P_WIDTH)) / 3
pillar_starts = [SPAN_START, SPAN_START + P_WIDTH + gap, SPAN_START + 2 * (P_WIDTH + gap) + 0.43, SPAN_END - P_WIDTH]
for i, y_start in enumerate(pillar_starts):
    y_end = y_start + P_WIDTH
    add_3d_wall(fig, [WEST_LIMIT_X, P_X_OUT], [y_start, y_start+0.02], [0, CEILING_H], f"Hollow P{i+1} S", "gray")
    add_3d_wall(fig, [P_X_OUT-0.02, P_X_OUT], [y_start, y_end], [0, CEILING_H], f"Hollow P{i+1} W", "gray")
    add_3d_wall(fig, [WEST_LIMIT_X, P_X_OUT], [y_end-0.02, y_end], [0, CEILING_H], f"Hollow P{i+1} N", "gray")

# 3. ROOM 2: EAST WING
R2_X_END = -1.79
add_3d_wall(fig, [-0.62, 0], [-T, 0], [0, CEILING_H], "R2 N Pillar", R2_C)
add_3d_wall(fig, [R2_X_END-T, R2_X_END], [-T, 2.42], [0, CEILING_H], "R2 East Wall", R2_C)

# 4. ROOM 4: ENCLOSED MEZZANINE
add_3d_wall(fig, [R2_X_END, 0], [2.42, 5.0], [0.77, 0.82], "R4 Floor", R4_C)

# 5. ROOM 5: THE HUB
add_3d_wall(fig, [R5_XW, R5_XE], [R5_YN, R5_YS], [R5_Z, CEILING_H], "R5 Hub", R5_C)
add_3d_wall(fig, [-2.1, -1.1], [5.0, 6.4], [0, 0.45], "Step 2 (R5 Base)", "silver")

# --- CONCRETE SLAB (LEVEL 1 FLOOR) ---
add_3d_wall(fig, [R5_XE, WEST_LIMIT_X + T], [-T, R3_Y_END + T], [CEILING_H, SLAB_TOP], "Concrete Slab", "rgba(100,100,100,0.4)")

# --- FIRST FLOOR DESIGN ---
Z_S, Z_E = SLAB_TOP, SLAB_TOP + 2.50
HALL_X_START, HALL_X_END = -1.0, 0.5 

# Perimeter Walls
add_3d_wall(fig, [R5_XE, WEST_LIMIT_X], [-T, -T+T], [Z_S, Z_E], "FF North Perimeter", TAB_C)
add_3d_wall(fig, [R5_XE, WEST_LIMIT_X], [R3_Y_END, R3_Y_END+T], [Z_S, Z_E], "FF South Perimeter", TAB_C)
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [-T, R3_Y_END], [Z_S, Z_E], "FF West Perimeter", TAB_C)
add_3d_wall(fig, [R5_XE-T, R5_XE], [-T, R3_Y_END], [Z_S, Z_E], "FF East Perimeter", TAB_C)

# 1. THREE ROOMS (WEST WING)
y_splits = [-T, 3.5, 7.2, R3_Y_END]
for i in range(3):
    ys, ye = y_splits[i], y_splits[i+1]
    add_3d_wall(fig, [HALL_X_END-T, HALL_X_END], [ys, ye], [Z_S, Z_E], f"Room {i+1} Hall Wall", TAB_C)
    if i < 2:
        add_3d_wall(fig, [HALL_X_END, WEST_LIMIT_X], [ye-T/2, ye+T/2], [Z_S, Z_E], f"Divider {i+1}", TAB_C)
    # Doors for the 3 rooms
    mid_y = (ys + ye) / 2
    add_3d_wall(fig, [HALL_X_END-T, HALL_X_END], [mid_y-0.45, mid_y+0.45], [Z_S, Z_S+2.1], f"Room {i+1} Door", ENT_C)

# 2. KITCHEN (NORTH-EAST OVER R5)
K_Y_E = 6.0
add_3d_wall(fig, [R5_XE, HALL_X_START], [-T, K_Y_E], [Z_S, Z_S+0.05], "Kitchen Floor", KITCHEN_C)
add_3d_wall(fig, [R5_XE, HALL_X_START], [K_Y_E-T, K_Y_E], [Z_S, Z_E], "Kitchen South Partition", "gray")
add_3d_wall(fig, [HALL_X_START, HALL_X_START+T], [-T, K_Y_E], [Z_S, Z_E], "Kitchen Hall Wall", TAB_C)
add_3d_wall(fig, [HALL_X_START, HALL_X_START+T], [1.0, 2.0], [Z_S, Z_S+2.1], "Kitchen Door", ENT_C)

# 3. BATHROOM (SOUTH-EAST OVER R5)
add_3d_wall(fig, [R5_XE, HALL_X_START], [K_Y_E, R3_Y_END], [Z_S, Z_S+0.05], "Bath Floor", BATH_C)
add_3d_wall(fig, [HALL_X_START, HALL_X_START+T], [K_Y_E, R3_Y_END], [Z_S, Z_E], "Bath Hall Wall", TAB_C)
# Two Showers
add_3d_wall(fig, [R5_XE+0.5, R5_XE+1.5], [R3_Y_END-1.5, R3_Y_END-0.5], [Z_S, Z_S+2.0], "Shower 1", "teal", 0.7)
add_3d_wall(fig, [R5_XE+2.0, R5_XE+3.0], [R3_Y_END-1.5, R3_Y_END-0.5], [Z_S, Z_S+2.0], "Shower 2", "teal", 0.7)
add_3d_wall(fig, [HALL_X_START, HALL_X_START+T], [K_Y_E+1.0, K_Y_E+2.0], [Z_S, Z_S+2.1], "Bath Door", ENT_C)

# 4. HALLWAY
add_3d_wall(fig, [HALL_X_START, HALL_X_END], [-T, R3_Y_END], [Z_S, Z_S+0.02], "FF Hallway", "lightgrey")

# --- Final View Settings ---
fig.update_layout(
    scene=dict(
        aspectmode='data',
        camera=dict(eye=dict(x=2.2, y=-2.2, z=1.8))
    ),
    margin=dict(l=0, r=0, b=0, t=50),
    height=900
)

st.plotly_chart(fig, use_container_width=True)
