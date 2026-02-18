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
    fig.add_trace(go.Mesh3d(
        x=[x_range[0], x_range[1], x_range[1], x_range[0], x_range[0], x_range[1], x_range[1], x_range[0]],
        y=[y_range[0], y_range[0], y_range[1], y_range[1], y_range[0], y_range[0], y_range[1], y_range[1]],
        z=[z_range[0], z_range[0], z_range[0], z_range[0], z_range[1], z_range[1], z_range[1], z_range[1]],
        i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2], j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3], k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
        opacity=opacity, color=color, flatshading=True, name=name
    ))

st.title("Digital Twin: Building ")

fig = go.Figure()

# --- CONSTANTS ---
T = 0.22
CEILING_H = 2.50
SLAB_TOP = 2.73
WEST_LIMIT_X = 4.84
EAST_LIMIT_X = -4.98
R3_Y_DIVIDE = 7.72
R3_Y_END = R3_Y_DIVIDE + 3.35  # ≈ 11.07
R1_C, R2_C, R3_C, R4_C, R5_C = "royalblue", "firebrick", "darkgreen", "slategrey", "darkorange"
TAB_C = "plum"
G_C, G_O = "skyblue", 0.4
ENT_C = "rgba(0, 255, 100, 0.4)"
KITCHEN_C = "lightsalmon"
BATH_C = "lightseagreen"

# --- ROOM 5 VERTICAL DATUM ---
R5_Z = 0.45
R5_CEIL = CEILING_H

# --- 1. ROOM 1: MAIN HALL --- (unchanged)
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

# --- 2. HOLLOW PILLARS --- (unchanged)
P_DEPTH = 0.50
P_WIDTH = 0.63
SPAN_START = -T
SPAN_END = R3_Y_END + T
TOTAL_SPAN_LENGTH = SPAN_END - SPAN_START
P_X_OUT = WEST_LIMIT_X + P_DEPTH
gap = (TOTAL_SPAN_LENGTH - (4 * P_WIDTH)) / 3
pillar_starts = [SPAN_START, SPAN_START + P_WIDTH + gap, SPAN_START + 2 * (P_WIDTH + gap) + 0.43, SPAN_END - P_WIDTH]
for i, y_start in enumerate(pillar_starts):
    y_end = y_start + P_WIDTH
    add_3d_wall(fig, [WEST_LIMIT_X, P_X_OUT], [y_start, y_start+0.02], [0, CEILING_H], f"Hollow P{i+1} S", "gray")
    add_3d_wall(fig, [P_X_OUT-0.02, P_X_OUT], [y_start, y_end], [0, CEILING_H], f"Hollow P{i+1} W", "gray")
    add_3d_wall(fig, [WEST_LIMIT_X, P_X_OUT], [y_end-0.02, y_end], [0, CEILING_H], f"Hollow P{i+1} N", "gray")

# --- 3. WESTERN COLONNADE --- (unchanged)
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [0, 0.90], [0, CEILING_H], "West Corner Pillar", R1_C)
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [0.90, 2.99], [0, 0.17], "West Curb", R1_C)
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [2.99, 4.53], [0, CEILING_H], "West Mid Pillar", R1_C)
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [7.03, R3_Y_DIVIDE], [0, CEILING_H], "West Corner South", R1_C)

# --- 4. ROOM 2: EAST WING --- (unchanged)
R2_X_END = -1.79
add_3d_wall(fig, [-0.62, 0], [-T, 0], [0, CEILING_H], "R2 N Pillar", R2_C)
add_3d_wall(fig, [-1.325, -0.62], [-T, 0], [0, 1.46], "R2 N Sill", R2_C)
add_3d_wall(fig, [-1.325, -0.62], [-T, 0], [2.06, CEILING_H], "R2 N Header", R2_C)
add_3d_wall(fig, [-1.325, -0.62], [-T/2, -T/2], [1.46, 2.06], "Glass R2 N", G_C, G_O)
add_3d_wall(fig, [R2_X_END, -1.325], [-T, 0], [0, CEILING_H], "R2 N End", R2_C)
add_3d_wall(fig, [R2_X_END-T, R2_X_END], [-T, 2.42], [0, CEILING_H], "R2 East Wall", R2_C)
add_3d_wall(fig, [R2_X_END, 0], [2.42, 2.42+T], [0, CEILING_H], "R2 South Shared Wall", R2_C)

# --- 5-9. ROOMS 3,4,5 + INTERNAL + STAIRS + SLAB --- (unchanged, omitted for brevity in this message)
# ... (keep all the original code for ROOM 3, ROOM 4, ROOM 5, INTERNAL PARTITION, STEPS & STAIRCASE, CONCRETE SLAB)

# Paste the original sections for ROOM 3, ROOM 4, ROOM 5, INTERNAL PARTITION, STEPS & STAIRCASE, and CONCRETE SLAB here.
# They remain identical to your previous version.

# --- 10. FIRST FLOOR (updated with 4 rooms + kitchen + bathroom) ---

TAB_Z_START = SLAB_TOP          # ≈ 2.73
TAB_Z_END   = TAB_Z_START + 2.50

HALL_START_X   = 0.00
HALL_WIDTH     = 2.00
HALL_END_X     = HALL_START_X + HALL_WIDTH

# East outer wall aligned above Room 2 / Room 4
EAST_WALL_X    = -1.79

# Outer walls
add_3d_wall(fig, [EAST_WALL_X, WEST_LIMIT_X], [SLAB_Y_NORTH_EDGE, SLAB_Y_NORTH_EDGE+T], [TAB_Z_START, TAB_Z_END], "FF North Outer", TAB_C)
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [SLAB_Y_NORTH_EDGE, SLAB_Y_SOUTH_EDGE], [TAB_Z_START, TAB_Z_END], "FF West Outer", TAB_C)
add_3d_wall(fig, [EAST_WALL_X, WEST_LIMIT_X], [SLAB_Y_SOUTH_EDGE-T, SLAB_Y_SOUTH_EDGE], [TAB_Z_START, TAB_Z_END], "FF South Outer", TAB_C)
add_3d_wall(fig, [EAST_WALL_X-T, EAST_WALL_X], [SLAB_Y_NORTH_EDGE, SLAB_Y_SOUTH_EDGE], [TAB_Z_START, TAB_Z_END], "FF East Outer", TAB_C)

# Hallway floor
add_3d_wall(fig, [HALL_START_X, HALL_END_X], [SLAB_Y_NORTH_EDGE, SLAB_Y_SOUTH_EDGE], [TAB_Z_START, TAB_Z_START+0.05], "FF Hallway Floor", "lightgray")

# ── Four tenant rooms (west of hallway) ──
y_dividers = [
    SLAB_Y_NORTH_EDGE,
    SLAB_Y_NORTH_EDGE + (SLAB_Y_SOUTH_EDGE - SLAB_Y_NORTH_EDGE)/4,
    SLAB_Y_NORTH_EDGE + 2*(SLAB_Y_SOUTH_EDGE - SLAB_Y_NORTH_EDGE)/4,
    SLAB_Y_NORTH_EDGE + 3*(SLAB_Y_SOUTH_EDGE - SLAB_Y_NORTH_EDGE)/4,
    SLAB_Y_SOUTH_EDGE
]

for i in range(4):
    ys, ye = y_dividers[i], y_dividers[i+1]
    room_name = f"FF Tenant Room {i+1}"
    # East wall (to hallway)
    add_3d_wall(fig, [HALL_START_X - T, HALL_START_X], [ys, ye], [TAB_Z_START, TAB_Z_END], f"{room_name} E Wall", TAB_C)
    # Partitions between rooms
    if i > 0:
        add_3d_wall(fig, [HALL_START_X, WEST_LIMIT_X], [ys - T/2, ys + T/2], [TAB_Z_START, TAB_Z_END], f"Partition {i}", TAB_C)
    # Door to hallway
    door_mid = (ys + ye) / 2
    add_3d_wall(fig, [HALL_START_X - T, HALL_START_X], [door_mid-0.45, door_mid+0.45], [TAB_Z_START+0.1, TAB_Z_START+2.1], f"{room_name} Door", ENT_C)

# ── Kitchen & Bathroom (east side, above Room 5 area) ──

# Kitchen: roughly x = -1.79 to -3.5 , y = middle-south
KITCHEN_XW = -1.79
KITCHEN_XE = -3.5
KITCHEN_YS = SLAB_Y_NORTH_EDGE + (SLAB_Y_SOUTH_EDGE - SLAB_Y_NORTH_EDGE) * 0.55
KITCHEN_YE = SLAB_Y_SOUTH_EDGE

add_3d_wall(fig, [KITCHEN_XW, KITCHEN_XE], [KITCHEN_YS, KITCHEN_YE], [TAB_Z_START, TAB_Z_END], "Kitchen North Wall", KITCHEN_C)
add_3d_wall(fig, [KITCHEN_XW, KITCHEN_XE], [KITCHEN_YS, KITCHEN_YE], [TAB_Z_START, TAB_Z_START+0.05], "Kitchen Floor", "sandybrown")
add_3d_wall(fig, [KITCHEN_XE - T, KITCHEN_XE], [KITCHEN_YS, KITCHEN_YE], [TAB_Z_START, TAB_Z_END], "Kitchen East Wall", KITCHEN_C)
add_3d_wall(fig, [KITCHEN_XW, KITCHEN_XE], [KITCHEN_YS - T, KITCHEN_YS], [TAB_Z_START, TAB_Z_END], "Kitchen South Wall", KITCHEN_C)

# Access door from hallway
add_3d_wall(fig, [HALL_END_X - T, HALL_END_X], [KITCHEN_YS + 1.0, KITCHEN_YS + 2.2], [TAB_Z_START+0.1, TAB_Z_START+2.1], "Kitchen Door", ENT_C)

# Bathroom: next to kitchen, two showers
BATH_XW = -1.79
BATH_XE = -3.97   # approx east edge of Room 5
BATH_YS = SLAB_Y_NORTH_EDGE + (SLAB_Y_SOUTH_EDGE - SLAB_Y_NORTH_EDGE) * 0.20
BATH_YE = KITCHEN_YS

add_3d_wall(fig, [BATH_XW, BATH_XE], [BATH_YS, BATH_YE], [TAB_Z_START, TAB_Z_END], "Bathroom North Wall", BATH_C)
add_3d_wall(fig, [BATH_XW, BATH_XE], [BATH_YS, BATH_YE], [TAB_Z_START, TAB_Z_START+0.05], "Bathroom Floor", "lightcyan")
add_3d_wall(fig, [BATH_XE - T, BATH_XE], [BATH_YS, BATH_YE], [TAB_Z_START, TAB_Z_END], "Bathroom East Wall", BATH_C)
add_3d_wall(fig, [BATH_XW, BATH_XE], [BATH_YE - T, BATH_YE], [TAB_Z_START, TAB_Z_END], "Bathroom South Wall", BATH_C)

# Internal partition + two showers
SHOWER_DIV_X = BATH_XW - 1.1
add_3d_wall(fig, [SHOWER_DIV_X, SHOWER_DIV_X + T], [BATH_YS, BATH_YE], [TAB_Z_START, TAB_Z_END], "Shower Divider", BATH_C)

# Shower 1 & 2 (simple boxes)
add_3d_wall(fig, [BATH_XW, SHOWER_DIV_X], [BATH_YS + 0.8, BATH_YS + 2.0], [TAB_Z_START + 0.1, TAB_Z_START + 2.1], "Shower 1", "teal")
add_3d_wall(fig, [SHOWER_DIV_X, BATH_XE], [BATH_YS + 0.8, BATH_YS + 2.0], [TAB_Z_START + 0.1, TAB_Z_START + 2.1], "Shower 2", "teal")

# Door to bathroom from hallway
add_3d_wall(fig, [HALL_END_X - T, HALL_END_X], [BATH_YS + 1.2, BATH_YS + 2.4], [TAB_Z_START+0.1, TAB_Z_START+2.1], "Bathroom Door", ENT_C)

# --- Staircase continuation (unchanged) ---
stair_z_start = TAB_Z_START - 0.3
curr_z = stair_z_start
curr_x = -1.1
for i, (rise, depth) in enumerate([(0.18, 0.40)] * 8):
    add_3d_wall(fig, [curr_x - depth, curr_x], [5.0, 6.4], [curr_z, curr_z + rise + 0.05], f"Upper Stair {i+1}", "silver")
    curr_z += rise
    curr_x -= depth
add_3d_wall(fig, [curr_x - 1.5, curr_x + 0.2], [4.4, 6.8], [TAB_Z_START, TAB_Z_START+0.05], "FF Stair Landing", "silver")

# --- Camera & Display ---
fig.update_layout(
    scene=dict(
        aspectmode='data',
        camera=dict(eye=dict(x=2.0, y=-2.5, z=1.2))
    ),
    margin=dict(l=0, r=0, b=0, t=50)
)

st.plotly_chart(fig, use_container_width=True)
