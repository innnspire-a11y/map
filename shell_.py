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

st.title("Digital Twin: Multi-Level Building")

fig = go.Figure()

# --- CONSTANTS ---
T = 0.22
CEILING_H = 2.50
SLAB_TOP = 2.73
WEST_LIMIT_X = 4.84
R3_Y_END = 11.07
R1_C, R2_C, R3_C, R4_C, R5_C = "royalblue", "firebrick", "darkgreen", "slategrey", "darkorange"
TAB_C = "plum"
G_C, G_O = "skyblue", 0.4
ENT_C = "rgba(0, 255, 100, 0.4)"
KITCHEN_C = "lightsalmon"
BATH_C = "lightseagreen"

# Room 5 Footprint
R5_XW, R5_XE = -T, -3.97
R5_YN, R5_YS = 6.46, R3_Y_END
R5_Z = 0.45

# --- GROUND FLOOR (Summary of previous rooms for context) ---
# Main Hall (R1)
add_3d_wall(fig, [0, WEST_LIMIT_X], [-T, 0], [0, CEILING_H], "R1 North", R1_C)
# Room 5 (The Hub)
add_3d_wall(fig, [R5_XW, R5_XE], [R5_YN, R5_YS], [R5_Z, CEILING_H], "Room 5 Hub", R5_C)

# --- CONCRETE SLAB (The Floor of Level 1) ---
# Covers everything from West Limit to R5 East Edge
add_3d_wall(fig, [R5_XE, WEST_LIMIT_X + T], [-T, R3_Y_END + T], [CEILING_H, SLAB_TOP], "Level 1 Slab", "rgba(100,100,100,0.5)")

# --- 10. FIRST FLOOR DESIGN ---
Z_S, Z_E = SLAB_TOP, SLAB_TOP + 2.50

# Outer Perimeter
add_3d_wall(fig, [R5_XE, WEST_LIMIT_X], [-T, -T+T], [Z_S, Z_E], "FF North Perimeter", TAB_C)
add_3d_wall(fig, [R5_XE, WEST_LIMIT_X], [R3_Y_END, R3_Y_END+T], [Z_S, Z_E], "FF South Perimeter", TAB_C)
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [-T, R3_Y_END], [Z_S, Z_E], "FF West Perimeter", TAB_C)
add_3d_wall(fig, [R5_XE-T, R5_XE], [-T, R3_Y_END], [Z_S, Z_E], "FF East Perimeter", TAB_C)

# INTERNAL LAYOUT: Three Rooms (West), Kitchen & Bath (East over R5)
HALL_X_START, HALL_X_END = -1.0, 0.5  # Central hallway 1.5m wide

# 1. THE THREE ROOMS (Western Side)
y_splits = [-T, 3.5, 7.2, R3_Y_END]
for i in range(3):
    ys, ye = y_splits[i], y_splits[i+1]
    # Room Outer West Wall
    add_3d_wall(fig, [HALL_X_END, WEST_LIMIT_X], [ys, ye], [Z_S, Z_S+0.05], f"Room {i+1} Floor", "white")
    # Dividers between the 3 rooms
    if i < 2:
        add_3d_wall(fig, [HALL_X_END, WEST_LIMIT_X], [ye-T/2, ye+T/2], [Z_S, Z_E], f"Divider {i+1}/{i+2}", TAB_C)
    # Hallway partition for rooms
    add_3d_wall(fig, [HALL_X_END-T, HALL_X_END], [ys, ye], [Z_S, Z_E], f"Room {i+1} Hall Wall", TAB_C)
    # Room Doors
    mid_y = (ys + ye) / 2
    add_3d_wall(fig, [HALL_X_END-T, HALL_X_END], [mid_y-0.45, mid_y+0.45], [Z_S, Z_S+2.1], f"Room {i+1} Door", ENT_C)

# 2. THE KITCHEN (North-East over Room 5)
KITCH_Y_END = 6.0
add_3d_wall(fig, [R5_XE, HALL_X_START], [-T, KITCH_Y_END], [Z_S, Z_S+0.05], "Kitchen Floor", KITCHEN_C)
add_3d_wall(fig, [R5_XE, HALL_X_START], [KITCH_Y_END-T, KITCH_Y_END], [Z_S, Z_E], "Kitchen South Wall", "silver")
add_3d_wall(fig, [HALL_X_START, HALL_X_START+T], [-T, KITCH_Y_END], [Z_S, Z_E], "Kitchen Hall Wall", "silver")
# Kitchen Entrance
add_3d_wall(fig, [HALL_X_START, HALL_X_START+T], [1.0, 2.0], [Z_S, Z_S+2.1], "Kitchen Door", ENT_C)

# 3. THE BATHROOM (South-East over Room 5)
BATH_Y_START = KITCH_Y_END
add_3d_wall(fig, [R5_XE, HALL_X_START], [BATH_Y_START, R3_Y_END], [Z_S, Z_S+0.05], "Bath Floor", BATH_C)
add_3d_wall(fig, [HALL_X_START, HALL_X_START+T], [BATH_Y_START, R3_Y_END], [Z_S, Z_E], "Bath Hall Wall", "silver")

# Two Showers inside the bathroom
SHOWER_W = 1.2
add_3d_wall(fig, [R5_XE+0.2, R5_XE+0.2+SHOWER_W], [R3_Y_END-1.5, R3_Y_END-0.3], [Z_S, Z_S+2.1], "Shower 1", "teal", 0.6)
add_3d_wall(fig, [R5_XE+0.2+SHOWER_W+0.2, R5_XE+0.2+2*SHOWER_W+0.2], [R3_Y_END-1.5, R3_Y_END-0.3], [Z_S, Z_S+2.1], "Shower 2", "teal", 0.6)

# Bath Entrance
add_3d_wall(fig, [HALL_X_START, HALL_X_START+T], [BATH_Y_START+1, BATH_Y_START+2], [Z_S, Z_S+2.1], "Bath Door", ENT_C)

# 4. THE HALLWAY
add_3d_wall(fig, [HALL_X_START, HALL_X_END], [-T, R3_Y_END], [Z_S, Z_S+0.02], "FF Hallway Floor", "lightgrey")

# --- Final View ---
fig.update_layout(
    scene=dict(
        aspectmode='data',
        camera=dict(eye=dict(x=1.8, y=-1.8, z=1.5)),
        xaxis=dict(title="West <-> East"),
        yaxis=dict(title="North <-> South"),
        zaxis=dict(title="Height")
    ),
    margin=dict(l=0, r=0, b=0, t=50),
    height=800
)

st.plotly_chart(fig, use_container_width=True)
