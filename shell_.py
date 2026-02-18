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

st.title("Digital Twin: Building (L-Shaped Slab & U-Turn Stairs)")

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

R5_XW, R5_XE = -T, -T - 3.75 # Eastern Edge ~ -3.97
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

# --- 4. ROOM 2: EAST WING ---
R2_X_END = -1.79
add_3d_wall(fig, [R2_X_END-T, R2_X_END], [-T, 2.42], [0, CEILING_H], "R2 East Wall", R2_C)
add_3d_wall(fig, [R2_X_END, 0], [2.42, 2.42+T], [0, CEILING_H], "R2 South Shared Wall", R2_C)

# --- 6. ROOM 4: THE ENCLOSED MEZZANINE ---
R4_X_LEFT, R4_Y_TOP, R4_FLOOR, R4_Y_BOTTOM_EDGE = R2_X_END, 2.42, 0.77, 5.0
add_3d_wall(fig, [R4_X_LEFT, 0], [R4_Y_TOP, R4_Y_BOTTOM_EDGE], [R4_FLOOR, R4_FLOOR+0.05], "R4 Floor", R4_C)
add_3d_wall(fig, [R4_X_LEFT-T, R4_X_LEFT], [R4_Y_TOP, R4_Y_BOTTOM_EDGE], [R4_FLOOR, 2.5], "R4 East Wall", R4_C)

# --- 7. ROOM 5: THE HUB ---
R5_YN, R5_YS = 6.46, R3_Y_END
add_3d_wall(fig, [-T, R5_XE], [R5_YN, R5_YS], [R5_Z-0.05, R5_Z], "R5 Floor", "tan")

# --- 9. STAIRCASE SYSTEM ---

# FLIGHT 1: West to East
curr_z, curr_x = 0.32, -1.1
y_range_f1 = [5.0, 6.4]
for i, (r, d) in enumerate([(0.19, 0.24), (0.21, 0.4), (0.19, 0.4), (0.18, 0.39), (0.18, 0.39), (0.18, 0.4), (0.18, 0.4), (0.18, 0.415)]):
    add_3d_wall(fig, [curr_x - d, curr_x], y_range_f1, [0, curr_z + r], f"Stair F1_{i+1}", "silver")
    curr_z += r
    curr_x -= d

# MID LANDING (at Z = 1.81)
# X spans the end of flight 1 to the start of flight 2
LANDING_X_START = curr_x - 1.2
add_3d_wall(fig, [LANDING_X_START, curr_x], [4.0, 6.4], [0, 1.81], "Mid Stair Landing", "darkgray")

# FLIGHT 2: East to West (Shifted 22cm North of Flight 1)
# Starts at Z = 1.81, ends at First Floor Slab (2.73)
y_range_f2 = [y_range_f1[0] - 1.4 - 0.22, y_range_f1[0] - 0.22] # 22cm gap north of F1
curr_z_f2 = 1.81
curr_x_f2 = LANDING_X_START # Starting from the landing
step_rise = (SLAB_TOP - 1.81) / 6
step_depth = 0.45

for i in range(6):
    add_3d_wall(fig, [curr_x_f2, curr_x_f2 + step_depth], y_range_f2, [0, curr_z_f2 + step_rise], f"Stair F2_{i+1}", "silver")
    curr_z_f2 += step_rise
    curr_x_f2 += step_depth

# FINAL LANDING on First Floor (above Room 4)
add_3d_wall(fig, [curr_x_f2, 0], y_range_f2, [SLAB_TOP, SLAB_TOP + 0.05], "FF Stair Arrival", "silver")

# --- CONCRETE SLAB (L-SHAPE) ---
SLAB_Y_N, SLAB_Y_S = -T, R3_Y_END + T

# 1. Western Slab (Rooms 1 & 3)
add_3d_wall(fig, [0, WEST_LIMIT_X + T], [SLAB_Y_N, SLAB_Y_S], [CEILING_H, SLAB_TOP], "Slab West", "rgba(100,100,100,0.5)")
# 2. Northern Strip (Room 2)
add_3d_wall(fig, [R2_X_END, 0], [SLAB_Y_N, 2.42 + T], [CEILING_H, SLAB_TOP], "Slab North-East", "rgba(100,100,100,0.5)")
# 3. Southern Strip (Room 5)
add_3d_wall(fig, [R5_XE, 0], [R5_YN - 0.2, SLAB_Y_S], [CEILING_H, SLAB_TOP], "Slab South-East", "rgba(100,100,100,0.5)")

# --- 10. FIRST FLOOR ---
TAB_Z_START, TAB_Z_END = SLAB_TOP, SLAB_TOP + 2.50
add_3d_wall(fig, [R2_X_END, WEST_LIMIT_X], [SLAB_Y_N, SLAB_Y_N+T], [TAB_Z_START, TAB_Z_END], "FF N Wall", TAB_C)
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [SLAB_Y_N, SLAB_Y_S], [TAB_Z_START, TAB_Z_END], "FF W Wall", TAB_C)
add_3d_wall(fig, [R5_XE, WEST_LIMIT_X], [SLAB_Y_S-T, SLAB_Y_S], [TAB_Z_START, TAB_Z_END], "FF S Wall", TAB_C)
add_3d_wall(fig, [R5_XE-T, R5_XE], [R5_YN, SLAB_Y_S], [TAB_Z_START, TAB_Z_END], "FF E Wall", TAB_C)

# --- Final view ---
fig.update_layout(
    scene=dict(
        aspectmode='data', 
        camera=dict(eye=dict(x=-2.0, y=-2.0, z=1.5)),
        xaxis=dict(title="East (-) / West (+)"),
        yaxis=dict(title="North (-) / South (+)")
    ),
    margin=dict(l=0, r=0, b=0, t=50)
)
st.plotly_chart(fig, use_container_width=True)
