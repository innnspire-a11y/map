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

st.title("Digital Twin: Building (Rooms 1-5 Slab Focus)")

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

# Room 5 dimensions for slab calculation
R5_XE = -T - 3.75 # Easternmost boundary
R5_Z = 0.45

# --- 1. ROOMS 1-5 MESH GENERATION (Simplified Reference) ---
# Room 1 Walls
add_3d_wall(fig, [0, WEST_LIMIT_X], [-T, 0], [0, CEILING_H], "R1 North Wall", R1_C)
add_3d_wall(fig, [-T, 0], [0, R3_Y_DIVIDE], [0, CEILING_H], "R1/R5 Common Wall", R1_C)
add_3d_wall(fig, [0, WEST_LIMIT_X], [R3_Y_DIVIDE, R3_Y_DIVIDE+T], [0, CEILING_H], "R1 South Divider", R1_C)

# Room 2 Walls
R2_X_END = -1.79
add_3d_wall(fig, [R2_X_END, 0], [-T, 0], [0, CEILING_H], "R2 North", R2_C)
add_3d_wall(fig, [R2_X_END-T, R2_X_END], [-T, 2.42], [0, CEILING_H], "R2 East Wall", R2_C)

# Room 3 Walls
add_3d_wall(fig, [0, WEST_LIMIT_X], [R3_Y_END, R3_Y_END+T], [0, CEILING_H], "R3 South Wall", R3_C)

# Room 4 (Mezzanine area)
R4_X_LEFT = R2_X_END
add_3d_wall(fig, [R4_X_LEFT, 0], [2.42, 5.0], [0.77, 2.5], "R4 Area", R4_C)

# Room 5 (The Hub)
R5_YN, R5_YS = 6.46, R3_Y_END
add_3d_wall(fig, [-T, R5_XE], [R5_YN, R5_YS], [R5_Z, CEILING_H], "Room 5", R5_C)

# --- THE CONCRETE SLAB (Enforced over Rooms 1, 2, 3, 4 & 5 only) ---
# The slab needs to cover the rectangular bounding box of all ground rooms.
# X-range: From R5's Eastern Edge (R5_XE) to R1's Western Edge (WEST_LIMIT_X + T)
# Y-range: From the Northernmost wall (-T) to the Southernmost wall (R3_Y_END + T)

add_3d_wall(fig,
    [R5_XE, WEST_LIMIT_X + T], 
    [-T, R3_Y_END + T], 
    [CEILING_H, SLAB_TOP],
    "Concrete Slab (Rooms 1-5)",
    "rgba(80, 80, 80, 0.4)" # Semi-transparent grey
)

# --- FIRST FLOOR TENANT SPACES (Built atop the slab) ---
TAB_Z_START = SLAB_TOP
TAB_Z_END = TAB_Z_START + 2.50

# Outer boundary of First Floor (must not exceed slab)
add_3d_wall(fig, [R5_XE, WEST_LIMIT_X + T], [-T, R3_Y_END + T], [TAB_Z_START, TAB_Z_END], "FF Perimeter", TAB_C, opacity=0.3)

# --- Final view setup ---
fig.update_layout(
    scene=dict(
        aspectmode='data',
        xaxis_title="West (-) / East (+)",
        yaxis_title="North (-) / South (+)",
        zaxis_title="Height",
        camera=dict(eye=dict(x=1.8, y=-1.8, z=1.5))
    ),
    margin=dict(l=0, r=0, b=0, t=50),
    title="Structural View: Concrete Slab covering Rooms 1-5"
)

st.plotly_chart(fig, use_container_width=True)
