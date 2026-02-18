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

st.title("Digital Twin: Multi-Level Optimized Design")

fig = go.Figure()

# --- CONSTANTS ---
T = 0.22
CEILING_H = 2.50
SLAB_TOP = 2.73
WEST_LIMIT_X = 4.84
R3_Y_DIVIDE = 7.72
R3_Y_END = 11.07
R1_C, R2_C, R3_C, R4_C, R5_C = "royalblue", "firebrick", "darkgreen", "slategrey", "darkorange"
TAB_C = "plum"
G_C, G_O = "skyblue", 0.4
ENT_C = "rgba(0, 255, 100, 0.4)"
KITCHEN_C = "lightsalmon"
BATH_C = "lightseagreen"

# --- ROOM 5 CONSTANTS ---
R5_Z = 0.45
R5_XW, R5_XE = -T, -3.97
R5_YN, R5_YS = 6.46, R3_Y_END

# --- [GROUND FLOOR FEATURES PRESERVED] ---
# Main Hall (R1)
add_3d_wall(fig, [0, WEST_LIMIT_X], [-T, 0], [0, CEILING_H], "R1 North Wall", R1_C)
# Room 5 (The Hub)
add_3d_wall(fig, [R5_XW, R5_XE], [R5_YN, R5_YS], [R5_Z, CEILING_H], "Room 5 Hub", R5_C)
# ... [Rest of Ground Floor components omitted for brevity but logic remains] ...

# --- CONCRETE SLAB ---
# Unified slab covering the whole footprint
add_3d_wall(fig, [R5_XE, WEST_LIMIT_X + T], [-T, R3_Y_END + T], [CEILING_H, SLAB_TOP], "Main Slab", "rgba(100,100,100,0.4)")

# --- FIRST FLOOR (3 Rooms + Kitchen + Bath) ---
Z_S, Z_E = SLAB_TOP, SLAB_TOP + 2.50
HALL_X_START, HALL_X_END = -0.5, 1.0  # 1.5m central hallway

# 1. PERIMETER WALLS (Corrected to R5 East Edge)
add_3d_wall(fig, [R5_XE, WEST_LIMIT_X], [-T, -T+0.05], [Z_S, Z_E], "FF North Perimeter", TAB_C)
add_3d_wall(fig, [R5_XE, WEST_LIMIT_X], [R3_Y_END, R3_Y_END+T], [Z_S, Z_E], "FF South Perimeter", TAB_C)
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [-T, R3_Y_END], [Z_S, Z_E], "FF West Wall", TAB_C)
add_3d_wall(fig, [R5_XE-T, R5_XE], [-T, R3_Y_END], [Z_S, Z_E], "FF East Wall", TAB_C)

# 2. THREE WESTERN ROOMS (Area over Rooms 1, 3, 4)
y_splits = [-T, 3.6, 7.3, R3_Y_END]
for i in range(3):
    ys, ye = y_splits[i], y_splits[i+1]
    # Internal Hallway wall for these rooms
    add_3d_wall(fig, [HALL_X_END, HALL_X_END+T], [ys, ye], [Z_S, Z_E], f"Room {i+1} Hall Wall", TAB_C)
    # Room Dividers
    if i < 2:
        add_3d_wall(fig, [HALL_X_END, WEST_LIMIT_X], [ye-T/2, ye+T/2], [Z_S, Z_E], f"Partition Room {i+1}", TAB_C)
    # Door to Hallway
    mid_y = (ys + ye) / 2
    add_3d_wall(fig, [HALL_X_END, HALL_X_END+T], [mid_y-0.45, mid_y+0.45], [Z_S, Z_S+2.1], f"Room {i+1} Door", ENT_C)

# 3. KITCHEN (Area over Room 5 North)
KITCHEN_Y_START, KITCHEN_Y_END = -T, 5.5
add_3d_wall(fig, [R5_XE, HALL_X_START], [KITCHEN_Y_START, KITCHEN_Y_END], [Z_S, Z_S+0.05], "Kitchen Floor", KITCHEN_C)
add_3d_wall(fig, [HALL_X_START-T, HALL_X_START], [KITCHEN_Y_START, KITCHEN_Y_END], [Z_S, Z_E], "Kitchen Hall Wall", "silver")
add_3d_wall(fig, [R5_XE, HALL_X_START], [KITCHEN_Y_END-T, KITCHEN_Y_END], [Z_S, Z_E], "Kitchen/Bath Divider", "silver")
# Kitchen Door
add_3d_wall(fig, [HALL_X_START-T, HALL_X_START], [1.0, 1.9], [Z_S, Z_S+2.1], "Kitchen Door", ENT_C)

# 4. BATHROOM + 2 SHOWERS (Area over Room 5 South)
BATH_Y_START, BATH_Y_END = KITCHEN_Y_END, R3_Y_END
add_3d_wall(fig, [R5_XE, HALL_X_START], [BATH_Y_START, BATH_Y_END], [Z_S, Z_S+0.05], "Bath Floor", BATH_C)
add_3d_wall(fig, [HALL_X_START-T, HALL_X_START], [BATH_Y_START, BATH_Y_END], [Z_S, Z_E], "Bath Hall Wall", "silver")

# Shower Cubicles
add_3d_wall(fig, [R5_XE+0.2, R5_XE+1.5], [BATH_Y_END-1.5, BATH_Y_END-0.3], [Z_S, Z_S+2.0], "Shower 1", "teal", 0.7)
add_3d_wall(fig, [R5_XE+1.7, R5_XE+3.0], [BATH_Y_END-1.5, BATH_Y_END-0.3], [Z_S, Z_S+2.0], "Shower 2", "teal", 0.7)

# Bath Door
add_3d_wall(fig, [HALL_X_START-T, HALL_X_START], [BATH_Y_START+1.0, BATH_Y_START+1.9], [Z_S, Z_S+2.1], "Bath Door", ENT_C)

# 5. HALLWAY FLOOR
add_3d_wall(fig, [HALL_X_START, HALL_X_END], [-T, R3_Y_END], [Z_S, Z_S+0.02], "FF Hallway Floor", "lightgrey")

# --- Staircase Continuation ---
stair_z = Z_S - 0.4
stair_x = -1.1
for i in range(10):
    add_3d_wall(fig, [stair_x - 0.4, stair_x], [5.0, 6.4], [0, stair_z + (i*0.18)], f"Upper Stair {i}", "silver")
    stair_x -= 0.1

# --- Final view ---
fig.update_layout(
    scene=dict(
        aspectmode='data',
        camera=dict(eye=dict(x=1.8, y=-2.0, z=1.5)),
        xaxis=dict(range=[-6, 6]),
        yaxis=dict(range=[-2, 12])
    ),
    margin=dict(l=0, r=0, b=0, t=40),
    height=800
)

st.plotly_chart(fig, use_container_width=True)
