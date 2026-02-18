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

st.title("Digital Twin: Updated U-Turn Stairs & Full Structural Detail")

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
TAB_C, G_C, G_O = "plum", "skyblue", 0.4
ENT_C = "rgba(0, 255, 100, 0.4)"

R5_XW, R5_XE = -T, -T - 3.75 
R5_Z, R5_CEIL = 0.45, CEILING_H
R5_YN, R5_YS = 6.46, R3_Y_END

# --- 1. ROOM 1: MAIN HALL & ENTRANCES ---
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

# --- 2. HOLLOW PILLARS (Detail Retained) ---
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
W_END_X_R3, W_START_X_R3 = WEST_LIMIT_X - 0.35, WEST_LIMIT_X - 1.88
add_3d_wall(fig, [W_START_X_R3, W_END_X_R3], [R3_Y_END, R3_Y_END+T], [0, 0.43], "R3 S Sill", R3_C)
add_3d_wall(fig, [W_START_X_R3, W_END_X_R3], [R3_Y_END, R3_Y_END+T], [2.45, CEILING_H], "R3 S Header", R3_C)
add_3d_wall(fig, [W_START_X_R3, W_END_X_R3], [R3_Y_END+T/2, R3_Y_END+T/2], [0.43, 2.45], "Glass R3 S", G_C, G_O)
add_3d_wall(fig, [-T, 0], [R3_Y_DIVIDE, R3_Y_END], [0, CEILING_H], "R3 East Shared Wall", R3_C)
add_3d_wall(fig, [0, W_START_X_R3], [R3_Y_END, R3_Y_END+T], [0, CEILING_H], "R3 S Wall East", R3_C)
add_3d_wall(fig, [W_END_X_R3, WEST_LIMIT_X], [R3_Y_END, R3_Y_END+T], [0, CEILING_H], "R3 S Wall West", R3_C)
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [R3_Y_DIVIDE, R3_Y_DIVIDE+0.72], [0, CEILING_H], "R3 W Wall N", R3_C)
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [R3_Y_DIVIDE+2.71, R3_Y_END], [0, CEILING_H], "R3 W Wall S", R3_C)

# --- 6. ROOM 4: MEZZANINE ---
R4_X_LEFT, R4_Y_TOP, R4_FLOOR, R4_Y_BOTTOM_EDGE = R2_X_END, 2.42, 0.77, 5.0
add_3d_wall(fig, [R4_X_LEFT, 0], [R4_Y_TOP, R4_Y_BOTTOM_EDGE], [R4_FLOOR, R4_FLOOR+0.05], "R4 Floor", R4_C)
add_3d_wall(fig, [R4_X_LEFT, 0], [R4_Y_TOP, R4_Y_TOP+T], [R4_FLOOR, 2.5], "R4 North Shared Wall", R4_C)
add_3d_wall(fig, [-T, 0], [R4_Y_TOP, R4_Y_BOTTOM_EDGE], [R4_FLOOR, 2.5], "R4 West Shared Wall", R4_C)
add_3d_wall(fig, [R4_X_LEFT-T, R4_X_LEFT], [R4_Y_TOP, R4_Y_BOTTOM_EDGE], [R4_FLOOR, 2.5], "R4 East Wall", R4_C)
add_3d_wall(fig, [R4_X_LEFT + 0.82, 0], [R4_Y_BOTTOM_EDGE - T, R4_Y_BOTTOM_EDGE], [R4_FLOOR, 2.5], "R4 South Wall", R4_C)
add_3d_wall(fig, [R4_X_LEFT, R4_X_LEFT + 0.82], [R4_Y_BOTTOM_EDGE - T/2, R4_Y_BOTTOM_EDGE - T/2], [R4_FLOOR, 2.5], "R4 Entrance Glass", ENT_C)

# --- 7. ROOM 5: THE HUB ---
R5_XW, R5_XE = -T, -T - 3.75
R5_YN = 6.46
R5_YS = R3_Y_END
add_3d_wall(fig, [R5_XW, R5_XE], [R5_YN, R5_YS], [R5_Z-0.05, R5_Z], "R5 Floor", "tan")

S_D_X_START = R5_XW - 0.49
S_D_X_END = S_D_X_START - 0.89
NW_WIN_Z_SILL, NW_WIN_Z_HEAD = R5_Z + 1.72, R5_Z + 1.72 + 0.29
NW_WIN_X_START = S_D_X_END - 0.335
NW_WIN_X_END = NW_WIN_X_START - 1.0

add_3d_wall(fig, [R5_XW, S_D_X_START], [R5_YN, R5_YN+T], [R5_Z, R5_CEIL], "R5 N Wall W", R5_C)
add_3d_wall(fig, [S_D_X_START, S_D_X_END], [R5_YN, R5_YN+T], [R5_Z+2.03, R5_CEIL], "R5 N Door Header", R5_C)
add_3d_wall(fig, [S_D_X_START, S_D_X_END], [R5_YN+T/2, R5_YN+T/2], [R5_Z, R5_Z+2.03], "Entrance R5 N Glass", ENT_C)
add_3d_wall(fig, [S_D_X_END, NW_WIN_X_START], [R5_YN, R5_YN+T], [R5_Z, R5_CEIL], "R5 N Wall Mid", R5_C)
add_3d_wall(fig, [NW_WIN_X_START, NW_WIN_X_END], [R5_YN, R5_YN+T], [R5_Z, NW_WIN_Z_SILL], "R5 N Win Sill", R5_C)
add_3d_wall(fig, [NW_WIN_X_START, NW_WIN_X_END], [R5_YN, R5_YN+T], [NW_WIN_Z_HEAD, R5_CEIL], "R5 N Win Header", R5_C)
add_3d_wall(fig, [NW_WIN_X_END, R5_XE], [R5_YN, R5_YN+T], [R5_Z, R5_CEIL], "R5 N Wall E", R5_C)
add_3d_wall(fig, [NW_WIN_X_START, NW_WIN_X_END], [R5_YN+T/2, R5_YN+T/2], [NW_WIN_Z_SILL, NW_WIN_Z_HEAD], "Glass R5 N", G_C, G_O)

# Room 5 East Wall
E_W_Y1, E_W_Y2 = R5_YN + 0.70, R5_YN + 1.68
E_WIN_Z_SILL, E_WIN_Z_HEAD = R5_Z + 1.22, R5_Z + 1.22 + 0.79
add_3d_wall(fig, [R5_XE, R5_XE+T], [R5_YN, E_W_Y1], [R5_Z, R5_CEIL], "R5 E Wall N", R5_C)
add_3d_wall(fig, [R5_XE, R5_XE+T], [E_W_Y1, E_W_Y2], [R5_Z, E_WIN_Z_SILL], "R5 E Sill", R5_C)
add_3d_wall(fig, [R5_XE, R5_XE+T], [E_W_Y1, E_W_Y2], [E_WIN_Z_HEAD, R5_CEIL], "R5 E Header", R5_C)
add_3d_wall(fig, [R5_XE, R5_XE+T], [E_W_Y2, R5_YS], [R5_Z, R5_CEIL], "R5 E Wall S", R5_C)
add_3d_wall(fig, [R5_XE+T/2, R5_XE+T/2], [E_W_Y1, E_W_Y2], [E_WIN_Z_SILL, E_WIN_Z_HEAD], "Glass R5 E", G_C, G_O)

# Room 5 South Wall
S_W_X1, S_W_X2 = R5_XE + 0.36, R5_XE + 1.26
S_WIN_Z_SILL, S_WIN_Z_HEAD = R5_Z + 1.31, R5_Z + 1.31 + 0.72
add_3d_wall(fig, [R5_XW, S_D_X_START], [R5_YS, R5_YS+T], [R5_Z, R5_CEIL], "R5 S Wall W", R5_C)
add_3d_wall(fig, [S_D_X_START, S_D_X_END], [R5_YS, R5_YS+T], [R5_Z+2.03, R5_CEIL], "R5 S Door Header", R5_C)
add_3d_wall(fig, [S_D_X_START, S_D_X_END], [R5_YS+T/2, R5_YS+T/2], [R5_Z, R5_Z+2.03], "Entrance R5 S Glass", ENT_C)
add_3d_wall(fig, [S_D_X_END, S_W_X2], [R5_YS, R5_YS+T], [R5_Z, R5_CEIL], "R5 S Wall Mid", R5_C)
add_3d_wall(fig, [S_W_X2, S_W_X1], [R5_YS, R5_YS+T], [R5_Z, S_WIN_Z_SILL], "R5 S Win Sill", R5_C)
add_3d_wall(fig, [S_W_X2, S_W_X1], [R5_YS, R5_YS+T], [S_WIN_Z_HEAD, R5_CEIL], "R5 S Win Header", R5_C)
add_3d_wall(fig, [S_W_X1, R5_XE], [R5_YS, R5_YS+T], [R5_Z, R5_CEIL], "R5 S Wall E", R5_C)
add_3d_wall(fig, [S_W_X2, S_W_X1], [R5_YS+T/2, R5_YS+T/2], [S_WIN_Z_SILL, S_WIN_Z_HEAD], "Glass R5 S", G_C, G_O)

# --- 8. INTERNAL PARTITION (Room 5) ---
INT_X = S_D_X_END - 0.36
INT_Y1, INT_Y2, INT_Y3 = R5_YS - 0.35, R5_YS - 1.15, R5_YS - 2.15
W_INT_X1, W_INT_X2 = INT_X - 0.11, INT_X - 1.10
add_3d_wall(fig, [INT_X, INT_X+0.05], [R5_YS, INT_Y1], [R5_Z, R5_CEIL], "Int Vert 1", "silver")
add_3d_wall(fig, [INT_X, INT_X+0.05], [INT_Y1, INT_Y2], [R5_Z+2.01, R5_CEIL], "Int Door Header", "silver")
add_3d_wall(fig, [INT_X+0.025, INT_X+0.025], [INT_Y1, INT_Y2], [R5_Z, R5_Z+2.01], "Int Entrance Glass", ENT_C)
add_3d_wall(fig, [INT_X, INT_X+0.05], [INT_Y2, INT_Y3], [R5_Z, R5_CEIL], "Int Vert 2", "silver")
I_WIN_Z_SILL, I_WIN_Z_HEAD = R5_Z + 1.29, R5_Z + 1.29 + 0.71
add_3d_wall(fig, [INT_X, W_INT_X1], [INT_Y3, INT_Y3+0.05], [R5_Z, R5_CEIL], "Int Horiz 1", "silver")
add_3d_wall(fig, [W_INT_X1, W_INT_X2], [INT_Y3, INT_Y3+0.05], [R5_Z, I_WIN_Z_SILL], "Int Win Sill", "silver")
add_3d_wall(fig, [W_INT_X1, W_INT_X2], [INT_Y3, INT_Y3+0.05], [I_WIN_Z_HEAD, R5_CEIL], "Int Win Header", "silver")
add_3d_wall(fig, [W_INT_X2, R5_XE], [INT_Y3, INT_Y3+0.05], [R5_Z, R5_CEIL], "Int Horiz 2", "silver")
add_3d_wall(fig, [W_INT_X1, W_INT_X2], [INT_Y3+0.025, INT_Y3+0.025], [I_WIN_Z_SILL, I_WIN_Z_HEAD], "Glass Int", G_C, G_O)

# --- 9. STAIRCASE SYSTEM (INTEGRATED U-TURN) ---

# Flight 1: West to East (Starting at Z=0.32, climbing to Z=1.81)
curr_z, curr_x = 0.32, -1.1
y_f1_start, y_f1_end = 5.0, 6.4
f1_steps = [(0.19, 0.24), (0.21, 0.4), (0.19, 0.4), (0.18, 0.39), (0.18, 0.39), (0.18, 0.4), (0.18, 0.4), (0.18, 0.415)]

for i, (r, d) in enumerate(f1_steps):
    add_3d_wall(fig, [curr_x - d, curr_x], [y_f1_start, y_f1_end], [0, curr_z + r], f"Stair F1_{i+1}", "silver")
    curr_z += r
    curr_x -= d

# Mid Landing (Fixed exactly at Z = 1.81)
# Depth set to 1.3 to bridge back to the second flight start
landing_depth = 1.3
add_3d_wall(fig, [curr_x - landing_depth, curr_x], [y_f1_start - 1.5, y_f1_end], [0, 1.81], "Mid Landing", "darkgray")

# Flight 2: East to West (Shifted 22cm North of Flight 1)
# Starts from Landing North side at Z=1.81, ending at Slab Top Z=2.73
y_f2_start, y_f2_end = y_f1_start - 1.4 - 0.22, y_f1_start - 0.22 
curr_z_f2 = 1.81
curr_x_f2 = curr_x - landing_depth 
f2_step_count = 6
rise_per_step = (SLAB_TOP - 1.81) / f2_step_count
run_per_step = 0.5

for i in range(f2_step_count):
    add_3d_wall(fig, [curr_x_f2, curr_x_f2 + run_per_step], [y_f2_start, y_f2_end], [0, curr_z_f2 + rise_per_step], f"Stair F2_{i+1}", "silver")
    curr_z_f2 += rise_per_step
    curr_x_f2 += run_per_step

# Final Arrival Platform on top of Room 4 (Z=2.73)
add_3d_wall(fig, [curr_x_f2, 0], [y_f2_start, y_f2_end], [SLAB_TOP - 0.05, SLAB_TOP], "FF Arrival", "silver")

# --- CONCRETE SLAB (MATCHING L-SHAPE PHOTO) ---
SLAB_Y_N, SLAB_Y_S = -T, R3_Y_END + T
# Segmented to leave the stairwell hollow
add_3d_wall(fig, [0, WEST_LIMIT_X + T], [SLAB_Y_N, SLAB_Y_S], [CEILING_H, SLAB_TOP], "Slab West", "rgba(100,100,100,0.5)")
add_3d_wall(fig, [R2_X_END, 0], [SLAB_Y_N, 2.42 + T], [CEILING_H, SLAB_TOP], "Slab North-East", "rgba(100,100,100,0.5)")
add_3d_wall(fig, [R5_XE, 0], [R5_YN - 0.2, SLAB_Y_S], [CEILING_H, SLAB_TOP], "Slab South-East", "rgba(100,100,100,0.5)")

# --- 10. FIRST FLOOR (Built on top of Slab) ---
TAB_Z_START, TAB_Z_END = SLAB_TOP, SLAB_TOP + 2.50
add_3d_wall(fig, [R2_X_END, WEST_LIMIT_X], [SLAB_Y_N, SLAB_Y_N+T], [TAB_Z_START, TAB_Z_END], "FF N Wall", TAB_C)
add_3d_wall(fig, [WEST_LIMIT_X, WEST_LIMIT_X+T], [SLAB_Y_N, SLAB_Y_S], [TAB_Z_START, TAB_Z_END], "FF W Wall", TAB_C)
add_3d_wall(fig, [R5_XE, WEST_LIMIT_X], [SLAB_Y_S-T, SLAB_Y_S], [TAB_Z_START, TAB_Z_END], "FF S Wall", TAB_C)
add_3d_wall(fig, [R5_XE-T, R5_XE], [R5_YN, SLAB_Y_S], [TAB_Z_START, TAB_Z_END], "FF E Wall", TAB_C)

# --- Final view ---
fig.update_layout(
    scene=dict(
        aspectmode='data', 
        camera=dict(eye=dict(x=-1.8, y=-1.8, z=1.5)),
        xaxis=dict(title="East-West (X)"),
        yaxis=dict(title="North-South (Y)")
    ),
    margin=dict(l=0, r=0, b=0, t=50)
)
st.plotly_chart(fig, use_container_width=True)

