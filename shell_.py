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

R5_XW, R5_XE = -T, -T - 3.75   # ≈ -0.22 to -3.97

# (All ground floor sections unchanged: Room 1 → Pillars → Colonnade → Room 2 → Room 3 → Room 4 → Room 5 → Internal → Stairs → Slab)
# Paste your original ground floor code here (from Room 1 to Slab) as it was - no changes needed.

# For brevity in this message, assume the ground floor code is identical to your provided version up to the slab.

# --- 10. FIRST FLOOR — extended east over Room 5 up to its east edge ---

TAB_Z_START = SLAB_TOP          # ≈ 2.73
TAB_Z_END   = TAB_Z_START + 2.50

HALL_START_X   = 0.00
HALL_WIDTH     = 2.00
HALL_END_X     = HALL_START_X + HALL_WIDTH

# New eastern boundary: east edge of Room 5
FF_EAST_X      = R5_XE          # ≈ -3.97

# Outer walls — now extend east to FF_EAST_X
add_3d_wall(fig, [FF_EAST_X, WEST_LIMIT_X], [SLAB_Y_NORTH_EDGE, SLAB_Y_NORTH_EDGE+T], [TAB_Z_START, TAB_Z_END], "FF North Outer", TAB_C)
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [SLAB_Y_NORTH_EDGE, SLAB_Y_SOUTH_EDGE], [TAB_Z_START, TAB_Z_END], "FF West Outer", TAB_C)
add_3d_wall(fig, [FF_EAST_X, WEST_LIMIT_X], [SLAB_Y_SOUTH_EDGE-T, SLAB_Y_SOUTH_EDGE], [TAB_Z_START, TAB_Z_END], "FF South Outer", TAB_C)
add_3d_wall(fig, [FF_EAST_X-T, FF_EAST_X], [SLAB_Y_NORTH_EDGE, SLAB_Y_SOUTH_EDGE], [TAB_Z_START, TAB_Z_END], "FF East Outer (over R5)", TAB_C)

# Hallway floor (western part only)
add_3d_wall(fig, [HALL_START_X, HALL_END_X], [SLAB_Y_NORTH_EDGE, SLAB_Y_SOUTH_EDGE], [TAB_Z_START, TAB_Z_START+0.05], "FF Hallway Floor", "lightgray")

# Four tenant rooms — west of hallway (x = 0 → 4.84)
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
    add_3d_wall(fig, [HALL_START_X - T, HALL_START_X], [ys, ye], [TAB_Z_START, TAB_Z_END], f"{room_name} East Wall", TAB_C)
    if i > 0:
        add_3d_wall(fig, [HALL_START_X, WEST_LIMIT_X], [ys - T/2, ys + T/2], [TAB_Z_START, TAB_Z_END], f"Partition {i}", TAB_C)
    door_mid = (ys + ye) / 2
    add_3d_wall(fig, [HALL_START_X - T, HALL_START_X], [door_mid-0.45, door_mid+0.45], [TAB_Z_START+0.1, TAB_Z_START+2.1], f"{room_name} Door", ENT_C)

# ── Kitchen + Bathroom — placed in eastern extension (over Room 5), accessed from hallway ──
UTIL_XW = HALL_END_X            # start from hallway east side
UTIL_XE = FF_EAST_X             # up to east edge of Room 5
UTIL_YS = SLAB_Y_SOUTH_EDGE - 5.0   # southern part for stair proximity
UTIL_YE = SLAB_Y_SOUTH_EDGE

add_3d_wall(fig, [UTIL_XW, UTIL_XE], [UTIL_YS, UTIL_YE], [TAB_Z_START, TAB_Z_END], "Utility North Wall", "gray")
add_3d_wall(fig, [UTIL_XW, UTIL_XE], [UTIL_YS, UTIL_YE], [TAB_Z_START, TAB_Z_START+0.05], "Utility Floor", "lightgray")
add_3d_wall(fig, [UTIL_XE - T, UTIL_XE], [UTIL_YS, UTIL_YE], [TAB_Z_START, TAB_Z_END], "Utility East Wall", TAB_C)
add_3d_wall(fig, [UTIL_XW, UTIL_XE], [UTIL_YE - T, UTIL_YE], [TAB_Z_START, TAB_Z_END], "Utility South Wall", "gray")

# Split: kitchen (larger, south), bathroom (north)
PART_Y = UTIL_YS + 3.0   # more space for kitchen
add_3d_wall(fig, [UTIL_XW, UTIL_XE], [PART_Y - T/2, PART_Y + T/2], [TAB_Z_START, TAB_Z_END], "Kitchen/Bath Partition", "gray")

# Kitchen (south) — larger area
add_3d_wall(fig, [UTIL_XW + 0.5, UTIL_XE - 0.5], [UTIL_YS + 0.4, PART_Y - 0.4], [TAB_Z_START + 0.1, TAB_Z_START + 1.0], "Kitchen Area", KITCHEN_C)

# Bathroom (north) — two showers
add_3d_wall(fig, [UTIL_XW + 0.5, UTIL_XW + 2.0], [PART_Y + 0.5, PART_Y + 2.5], [TAB_Z_START + 0.1, TAB_Z_START + 2.1], "Shower 1", "teal")
add_3d_wall(fig, [UTIL_XW + 2.5, UTIL_XE - 0.5], [PART_Y + 0.5, PART_Y + 2.5], [TAB_Z_START + 0.1, TAB_Z_START + 2.1], "Shower 2", "teal")

# Doors from hallway into utility area
add_3d_wall(fig, [HALL_END_X - T, HALL_END_X], [UTIL_YS + 1.0, UTIL_YS + 2.5], [TAB_Z_START+0.1, TAB_Z_START+2.1], "Utility Access Door (Kitchen side)", ENT_C)
add_3d_wall(fig, [HALL_END_X - T, HALL_END_X], [PART_Y + 0.5, PART_Y + 1.8], [TAB_Z_START+0.1, TAB_Z_START+2.1], "Bathroom Door", ENT_C)

# --- Stair continuation (unchanged) ---
stair_z_start = TAB_Z_START - 0.3
curr_z = stair_z_start
curr_x = -1.1
for i, (rise, depth) in enumerate([(0.18, 0.40)] * 8):
    add_3d_wall(fig, [curr_x - depth, curr_x], [5.0, 6.4], [curr_z, curr_z + rise + 0.05], f"Upper Stair {i+1}", "silver")
    curr_z += rise
    curr_x -= depth
add_3d_wall(fig, [curr_x - 1.5, curr_x + 0.2], [4.4, 6.8], [TAB_Z_START, TAB_Z_START+0.05], "FF Stair Landing", "silver")

# --- Final view ---
fig.update_layout(
    scene=dict(
        aspectmode='data',
        camera=dict(eye=dict(x=2.0, y=-2.5, z=1.2))
    ),
    margin=dict(l=0, r=0, b=0, t=50)
)

st.plotly_chart(fig, use_container_width=True)
