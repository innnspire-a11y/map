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

st.title("Digital Twin: Full Building Integration")

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
TAB_C = "plum"
G_C, G_O = "skyblue", 0.4
ENT_C = "rgba(0, 255, 100, 0.4)"
KITCHEN_C = "lightsalmon"
BATH_C = "lightseagreen"

# Room 5 vertical datum
R5_Z = 0.45
R5_CEIL = CEILING_H
R5_XW, R5_XE = -T, -T - 3.75 # -3.97

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

# --- 2. HOLLOW PILLARS ---
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

# --- 3. WESTERN COLONNADE ---
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [0, 0.90], [0, CEILING_H], "West Corner Pillar", R1_C)
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [0.90, 2.99], [0, 0.17], "West Curb", R1_C)
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [2.99, 4.53], [0, CEILING_H], "West Mid Pillar", R1_C)
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [7.03, R3_Y_DIVIDE], [0, CEILING_H], "West Corner South", R1_C)

# --- 4. ROOM 2: EAST WING ---
R2_X_END = -1.79
add_3d_wall(fig, [-0.62, 0], [-T, 0], [0, CEILING_H], "R2 N Pillar", R2_C)
add_3d_wall(fig, [-1.325, -0.62], [-T, 0], [0, 1.46], "R2 N Sill", R2_C)
add_3d_wall(fig, [-1.325, -0.62], [-T, 0], [2.06, CEILING_H], "R2 N Header", R2_C)
add_3d_wall(fig, [-1.325, -0.62], [-T/2, -T/2], [1.46, 2.06], "Glass R2 N", G_C, G_O)
add_3d_wall(fig, [R2_X_END, -1.325], [-T, 0], [0, CEILING_H], "R2 N End", R2_C)
add_3d_wall(fig, [R2_X_END-T, R2_X_END], [-T, 2.42], [0, CEILING_H], "R2 East Wall", R2_C)
add_3d_wall(fig, [R2_X_END, 0], [2.42, 2.42+T], [0, CEILING_H], "R2 South Shared Wall", R2_C)

# --- 5. ROOM 3: SOUTH WING ---
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [R3_Y_DIVIDE+0.72, R3_Y_DIVIDE+2.71], [0, 0.86], "R3 W Sill", R3_C)
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [R3_Y_DIVIDE+0.72, R3_Y_DIVIDE+2.71], [2.46, CEILING_H], "R3 W Header", R3_C)
add_3d_wall(fig, [WEST_LIMIT_X+T/2, WEST_LIMIT_X+T/2], [R3_Y_DIVIDE+0.72, R3_Y_DIVIDE+2.71], [0.86, 2.46], "Glass R3 W", G_C, G_O)
add_3d_wall(fig, [-T, 0], [R3_Y_DIVIDE, R3_Y_END], [0, CEILING_H], "R3 East Shared Wall", R3_C)

# --- 6. ROOM 4: THE ENCLOSED MEZZANINE ---
R4_Y_TOP, R4_FLOOR, R4_Y_BOTTOM_EDGE = 2.42, 0.77, 5.0
add_3d_wall(fig, [R2_X_END, 0], [R4_Y_TOP, R4_Y_BOTTOM_EDGE], [R4_FLOOR, R4_FLOOR+0.05], "R4 Floor", R4_C)

# --- 7. ROOM 5: THE HUB (Ground Floor) ---
R5_YN, R5_YS = 6.46, R3_Y_END
add_3d_wall(fig, [R5_XW, R5_XE], [R5_YN, R5_YS], [R5_Z-0.05, R5_Z], "R5 Floor", "tan")
# Restoring all Ground Floor R5 details
S_D_X_START, S_D_X_END = R5_XW - 0.49, R5_XW - 1.38
add_3d_wall(fig, [R5_XW, S_D_X_START], [R5_YN, R5_YN+T], [R5_Z, R5_CEIL], "R5 N Wall W", R5_C)
add_3d_wall(fig, [S_D_X_START, S_D_X_END], [R5_YN, R5_YN+T], [R5_Z+2.03, R5_CEIL], "R5 N Header", R5_C)
add_3d_wall(fig, [S_D_X_START, S_D_X_END], [R5_YN+T/2, R5_YN+T/2], [R5_Z, R5_Z+2.03], "R5 N Door Glass", ENT_C)
add_3d_wall(fig, [R5_XE, R5_XE+T], [R5_YN, R5_YS], [R5_Z, R5_CEIL], "R5 E Wall", R5_C)

# --- 9. STEPS & STAIRCASE ---
add_3d_wall(fig, [-2.1, -1.1], [5.0, 6.4], [0, 0.45], "Step 2 (R5 Base)", "silver")

# --- CONCRETE SLAB (Level 1 Floor) ---
add_3d_wall(fig, [R5_XE, WEST_LIMIT_X + T], [-T, R3_Y_END + T], [CEILING_H, SLAB_TOP], "Level 1 Slab", "rgba(100,100,100,0.4)")

# --- 10. FIRST FLOOR (Improved Design) ---
Z_S, Z_E = SLAB_TOP, SLAB_TOP + 2.50
HALL_X_START, HALL_X_END = 0.0, 1.5

# FF North wall spanning full width from R5 east edge to West Limit
add_3d_wall(fig, [R5_XE, WEST_LIMIT_X], [-T, -T+T], [Z_S, Z_E], "FF North Outer", TAB_C)
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [-T, R3_Y_END], [Z_S, Z_E], "FF West Outer", TAB_C)
add_3d_wall(fig, [R5_XE, WEST_LIMIT_X], [R3_Y_END, R3_Y_END+T], [Z_S, Z_E], "FF South Outer", TAB_C)
add_3d_wall(fig, [R5_XE-T, R5_XE], [-T, R3_Y_END], [Z_S, Z_E], "FF East Outer", TAB_C)

# Hallway
add_3d_wall(fig, [HALL_X_START, HALL_X_END], [-T, R3_Y_END], [Z_S, Z_S+0.05], "FF Hall Floor", "lightgray")

# THREE ROOMS (West side)
y_room_divs = [-T, 3.5, 7.5, R3_Y_END]
for i in range(3):
    ys, ye = y_room_divs[i], y_room_divs[i+1]
    # Divider Walls
    if i > 0: add_3d_wall(fig, [HALL_X_END, WEST_LIMIT_X], [ys-T/2, ys+T/2], [Z_S, Z_E], f"Room Partition {i}", TAB_C)
    # Hall Wall
    add_3d_wall(fig, [HALL_X_END-T, HALL_X_END], [ys, ye], [Z_S, Z_E], f"Room {i+1} Hall Wall", TAB_C)
    # Door
    mid_y = (ys+ye)/2
    add_3d_wall(fig, [HALL_X_END-T, HALL_X_END], [mid_y-0.45, mid_y+0.45], [Z_S+0.1, Z_S+2.1], f"R{i+1} Door", ENT_C)

# KITCHEN & BATHROOM (East side, over Room 5)
KITCH_Y_SPLIT = 5.0
# Kitchen
add_3d_wall(fig, [R5_XE, HALL_X_START], [-T, KITCH_Y_SPLIT], [Z_S, Z_S+0.05], "Kitchen Floor", KITCHEN_C)
add_3d_wall(fig, [HALL_X_START, HALL_X_START+T], [-T, KITCH_Y_SPLIT], [Z_S, Z_E], "Kitchen Hall Partition", "silver")
add_3d_wall(fig, [R5_XE, HALL_X_START], [KITCH_Y_SPLIT-T, KITCH_Y_SPLIT], [Z_S, Z_E], "Kitchen/Bath Divider", "silver")
# Bathroom
add_3d_wall(fig, [R5_XE, HALL_X_START], [KITCH_Y_SPLIT, R3_Y_END], [Z_S, Z_S+0.05], "Bath Floor", BATH_C)
add_3d_wall(fig, [HALL_X_START, HALL_X_START+T], [KITCH_Y_SPLIT, R3_Y_END], [Z_S, Z_E], "Bath Hall Partition", "silver")
# Showers
add_3d_wall(fig, [R5_XE+0.5, R5_XE+1.8], [R3_Y_END-1.5, R3_Y_END-0.3], [Z_S, Z_S+2.1], "Shower 1", "teal", 0.5)
add_3d_wall(fig, [R5_XE+2.0, HALL_X_START-0.5], [R3_Y_END-1.5, R3_Y_END-0.3], [Z_S, Z_S+2.1], "Shower 2", "teal", 0.5)

# --- Final view ---
fig.update_layout(
    scene=dict(aspectmode='data', camera=dict(eye=dict(x=2.0, y=-2.0, z=1.5))),
    margin=dict(l=0, r=0, b=0, t=50)
)

st.plotly_chart(fig, use_container_width=True)
