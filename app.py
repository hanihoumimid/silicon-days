"""
AEGIS AI — Système de Défense Active Cognitive
Hackathon Silicondays 2026 — Capgemini
Prototype de démonstration interactive
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
# Palette — Corporate Clean
# ---------------------------------------------------------------------------
CAPGEMINI_BLUE = "#0070AD"
SLATE_700 = "#1E293B"
SLATE_800 = "#0F172A"
SLATE_600 = "#475569"
SLATE_400 = "#94A3B8"
SLATE_300 = "#CBD5E1"
SLATE_200 = "#E2E8F0"
SLATE_100 = "#F1F5F9"
CARD_BG = "#1A2332"
SURFACE = "#131C2A"
CORAL = "#F87171"
AMBER = "#FBBF24"
MINT = "#34D399"
GOLD = "#D97706"
WHITE = "#F8FAFC"

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="AEGIS AI — Capgemini Cyber Defense",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# CSS — Corporate SaaS Theme
# ---------------------------------------------------------------------------
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    .stApp {{
        background-color: {SLATE_800};
    }}
    .block-container {{
        padding-top: 1rem;
    }}

    /* Header */
    .aegis-header {{
        background: linear-gradient(135deg, {SLATE_700}, {CARD_BG});
        border: 1px solid rgba(0,112,173,0.2);
        border-radius: 10px;
        padding: 1.2rem 2rem;
        margin-bottom: 1.5rem;
        text-align: center;
    }}
    .aegis-header h1 {{
        color: {WHITE};
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 1.6rem;
        margin: 0;
        letter-spacing: 2px;
    }}
    .aegis-header h1 span {{
        color: {CAPGEMINI_BLUE};
    }}
    .aegis-header p {{
        color: {SLATE_400};
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        margin: 0.4rem 0 0 0;
        font-weight: 400;
    }}

    /* Metric cards */
    .metric-card {{
        background: {CARD_BG};
        border: 1px solid rgba(148,163,184,0.1);
        border-radius: 10px;
        padding: 1.1rem 1.4rem;
        margin-bottom: 0.8rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.2);
    }}
    .metric-card .label {{
        color: {SLATE_400};
        font-family: 'Inter', sans-serif;
        font-size: 0.7rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.25rem;
    }}
    .metric-card .value {{
        color: {WHITE};
        font-size: 1.3rem;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
    }}

    /* Alert card — soft controlled warning, not panic */
    .alert-card {{
        background: rgba(251,191,36,0.06);
        border: 1px solid rgba(251,191,36,0.2);
        border-radius: 10px;
        padding: 1.1rem 1.4rem;
        margin-bottom: 0.8rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.2);
    }}
    .alert-card .label {{
        color: {AMBER};
        font-family: 'Inter', sans-serif;
        font-size: 0.7rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.25rem;
    }}
    .alert-card .value {{
        color: {AMBER};
        font-size: 1.3rem;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
    }}

    /* Audit console (ex-terminal) */
    .audit-console {{
        background: {SLATE_700};
        border: 1px solid rgba(148,163,184,0.15);
        border-radius: 8px;
        padding: 1.2rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
        color: {SLATE_300};
        line-height: 1.8;
        max-height: 500px;
        overflow-y: auto;
    }}
    .audit-console .prompt {{
        color: {CORAL};
        font-weight: 500;
    }}
    .audit-console .system {{
        color: {CAPGEMINI_BLUE};
    }}
    .audit-console .mirage {{
        color: {GOLD};
        font-weight: 500;
    }}
    .audit-console .output {{
        color: {SLATE_300};
    }}

    /* Timeline */
    .timeline-event {{
        border-left: 3px solid {CAPGEMINI_BLUE};
        padding: 0.7rem 1rem;
        margin-bottom: 0.7rem;
        background: {CARD_BG};
        border-radius: 0 8px 8px 0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.15);
    }}
    .timeline-event.critical {{
        border-left-color: {CORAL};
    }}
    .timeline-event.warning {{
        border-left-color: {AMBER};
    }}
    .timeline-event.success {{
        border-left-color: {MINT};
    }}
    .timeline-event .time {{
        color: {SLATE_400};
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
    }}
    .timeline-event .desc {{
        color: {SLATE_300};
        font-family: 'Inter', sans-serif;
        font-size: 0.88rem;
        margin-top: 0.2rem;
    }}

    /* NIS2 report */
    .nis2-report {{
        background: {CARD_BG};
        border: 1px solid rgba(0,112,173,0.2);
        border-radius: 10px;
        padding: 1.8rem;
        font-family: 'Inter', sans-serif;
        font-size: 0.88rem;
        color: {SLATE_300};
        line-height: 1.8;
    }}
    .nis2-report h3 {{
        color: {CAPGEMINI_BLUE};
        font-weight: 600;
        font-size: 1rem;
        border-bottom: 1px solid rgba(0,112,173,0.15);
        padding-bottom: 0.5rem;
        margin-top: 1.2rem;
    }}
    .nis2-report .field-label {{
        color: {SLATE_400};
        font-weight: 500;
    }}
    .nis2-report .field-value {{
        color: {WHITE};
    }}
    .nis2-report .critical-tag {{
        color: {CORAL};
        font-weight: 600;
    }}
    .nis2-report .ok-tag {{
        color: {MINT};
        font-weight: 600;
    }}
    .nis2-report code {{
        background: {SLATE_700};
        padding: 0.15rem 0.4rem;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
    }}

    /* Phase badges */
    .phase-badge {{
        display: inline-block;
        padding: 0.25rem 0.9rem;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        letter-spacing: 0.5px;
        margin-bottom: 1rem;
    }}
    .phase-avant {{
        background: rgba(0,112,173,0.12);
        color: {CAPGEMINI_BLUE};
        border: 1px solid rgba(0,112,173,0.3);
    }}
    .phase-pendant {{
        background: rgba(248,113,113,0.1);
        color: {CORAL};
        border: 1px solid rgba(248,113,113,0.3);
    }}
    .phase-apres {{
        background: rgba(52,211,153,0.1);
        color: {MINT};
        border: 1px solid rgba(52,211,153,0.3);
    }}

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 4px;
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: {CARD_BG};
        border-radius: 6px 6px 0 0;
        padding: 0.5rem 1.5rem;
        color: {SLATE_400};
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: rgba(0,112,173,0.15);
        border-bottom: 2px solid {CAPGEMINI_BLUE};
        color: {WHITE};
    }}

    /* Latency badge */
    .latency-badge {{
        background: rgba(251,191,36,0.08);
        border: 1px solid rgba(251,191,36,0.25);
        border-radius: 8px;
        padding: 0.6rem 1rem;
        text-align: center;
    }}

    /* Idle placeholder */
    .idle-placeholder {{
        text-align: center;
        padding: 3rem;
        color: {SLATE_400};
    }}
    .idle-placeholder .title {{
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        font-weight: 500;
        color: {SLATE_300};
        margin-bottom: 0.5rem;
    }}
    .idle-placeholder .subtitle {{
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
    }}

    /* Continuity success banner */
    .continuity-banner {{
        background: rgba(52,211,153,0.08);
        border: 1px solid rgba(52,211,153,0.25);
        border-radius: 10px;
        padding: 1.2rem 1.6rem;
        text-align: center;
        margin: 1rem 0;
    }}
    .continuity-banner .label {{
        color: {SLATE_400};
        font-family: 'Inter', sans-serif;
        font-size: 0.7rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.3rem;
    }}
    .continuity-banner .value {{
        color: {MINT};
        font-size: 1.6rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
    }}
    .continuity-banner .subtitle {{
        color: {SLATE_400};
        font-family: 'Inter', sans-serif;
        font-size: 0.8rem;
        margin-top: 0.3rem;
    }}

    /* Animations */
    @keyframes fadeInUp {{
        from {{ opacity: 0; transform: translateY(12px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}
    @keyframes pulseGlow {{
        0%, 100% {{ box-shadow: 0 0 0 0 rgba(248,113,113,0.3); }}
        50% {{ box-shadow: 0 0 16px 4px rgba(248,113,113,0.15); }}
    }}
    @keyframes pulseGlowMint {{
        0%, 100% {{ box-shadow: 0 0 0 0 rgba(52,211,153,0.3); }}
        50% {{ box-shadow: 0 0 16px 4px rgba(52,211,153,0.15); }}
    }}
    @keyframes slideInLeft {{
        from {{ opacity: 0; transform: translateX(-16px); }}
        to {{ opacity: 1; transform: translateX(0); }}
    }}
    .anim-fade-in-up {{
        animation: fadeInUp 0.5s ease-out both;
    }}
    .anim-fade-in {{
        animation: fadeIn 0.4s ease-out both;
    }}
    .anim-pulse {{
        animation: pulseGlow 2s ease-in-out infinite;
    }}
    .anim-pulse-mint {{
        animation: pulseGlowMint 2s ease-in-out infinite;
    }}
    .anim-slide-left {{
        animation: slideInLeft 0.4s ease-out both;
    }}
    .timeline-event {{
        animation: fadeInUp 0.35s ease-out both;
    }}

    /* Progress bar */
    .progress-container {{
        background: {SLATE_700};
        border-radius: 6px;
        height: 6px;
        overflow: hidden;
        margin: 0.6rem 0 1rem 0;
    }}
    .progress-bar {{
        height: 100%;
        border-radius: 6px;
        transition: width 0.3s ease;
        background: linear-gradient(90deg, {CAPGEMINI_BLUE}, {AMBER});
    }}
    .progress-bar.complete {{
        background: linear-gradient(90deg, {MINT}, {CAPGEMINI_BLUE});
    }}
    .progress-label {{
        color: {SLATE_400};
        font-family: 'Inter', sans-serif;
        font-size: 0.72rem;
        margin-bottom: 0.2rem;
        display: flex;
        justify-content: space-between;
    }}

    /* Navigation hint */
    .nav-hint {{
        background: rgba(0,112,173,0.08);
        border: 1px solid rgba(0,112,173,0.2);
        border-radius: 8px;
        padding: 0.8rem 1.2rem;
        margin: 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.7rem;
        animation: fadeInUp 0.5s ease-out both;
    }}
    .nav-hint .icon {{
        font-size: 1.2rem;
    }}
    .nav-hint .text {{
        color: {SLATE_300};
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
    }}
    .nav-hint .tab-name {{
        color: {CAPGEMINI_BLUE};
        font-weight: 600;
    }}

    /* Scenario selector styling */
    .scenario-selector {{
        background: {CARD_BG};
        border: 1px solid rgba(148,163,184,0.1);
        border-radius: 10px;
        padding: 1rem 1.4rem;
        margin-bottom: 1rem;
    }}
    .scenario-selector .label {{
        color: {SLATE_400};
        font-family: 'Inter', sans-serif;
        font-size: 0.7rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }}

    /* User profile cards */
    .profile-card {{
        background: {CARD_BG};
        border: 1px solid rgba(148,163,184,0.1);
        border-radius: 10px;
        padding: 1.2rem;
        animation: fadeInUp 0.4s ease-out both;
    }}
    .profile-card .avatar {{
        width: 42px;
        height: 42px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
        font-weight: 700;
        font-family: 'Inter', sans-serif;
        color: {WHITE};
        margin-bottom: 0.6rem;
    }}
    .profile-card .name {{
        color: {WHITE};
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 0.9rem;
    }}
    .profile-card .role {{
        color: {SLATE_400};
        font-family: 'Inter', sans-serif;
        font-size: 0.78rem;
        margin-bottom: 0.6rem;
    }}
    .profile-card .detail {{
        color: {SLATE_400};
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        display: flex;
        justify-content: space-between;
        padding: 0.25rem 0;
        border-bottom: 1px solid rgba(148,163,184,0.06);
    }}
    .profile-card .detail .val {{
        color: {SLATE_300};
        font-family: 'JetBrains Mono', monospace;
        font-weight: 500;
    }}
    .profile-card .risk-tag {{
        display: inline-block;
        padding: 0.15rem 0.5rem;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        margin-top: 0.6rem;
    }}
    .risk-low {{
        background: rgba(52,211,153,0.1);
        color: {MINT};
        border: 1px solid rgba(52,211,153,0.25);
    }}
    .risk-medium {{
        background: rgba(251,191,36,0.1);
        color: {AMBER};
        border: 1px solid rgba(251,191,36,0.25);
    }}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
if "intrusion_active" not in st.session_state:
    st.session_state.intrusion_active = False
if "attack_phase" not in st.session_state:
    st.session_state.attack_phase = 0
if "terminal_lines" not in st.session_state:
    st.session_state.terminal_lines = []
if "nis2_generated" not in st.session_state:
    st.session_state.nis2_generated = False
if "attack_timestamp" not in st.session_state:
    st.session_state.attack_timestamp = None
if "animating" not in st.session_state:
    st.session_state.animating = False
if "selected_scenario" not in st.session_state:
    st.session_state.selected_scenario = 0

# ---------------------------------------------------------------------------
# Scénarios d'attaque (même script, noms et descriptions différents)
# ---------------------------------------------------------------------------
ATTACK_SCENARIOS = [
    {
        "name": "Credential Stuffing — Portail Marketing",
        "vector": "Credential Stuffing",
        "target": "SRV-WEB / mkt-user01",
        "severity": "Critique",
        "desc": "Attaque par dictionnaire ciblant les identifiants marketing exposés sur le portail web.",
    },
    {
        "name": "Phishing ciblé — Spear Phishing RH",
        "vector": "Spear Phishing",
        "target": "Messagerie / rh-admin",
        "severity": "Critique",
        "desc": "E-mail de phishing hautement ciblé imitant un partenaire RH de confiance.",
    },
    {
        "name": "Supply Chain — Dépendance compromise",
        "vector": "Supply Chain Attack",
        "target": "SRV-APP / npm registry",
        "severity": "Élevée",
        "desc": "Package tiers compromis injectant un reverse shell lors du build CI/CD.",
    },
    {
        "name": "Insider Threat — Exfiltration lente",
        "vector": "Insider Threat",
        "target": "SRV-FILES / dev-user03",
        "severity": "Élevée",
        "desc": "Exfiltration progressive de documents sensibles par un compte interne légitime.",
    },
]

# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------

def build_network_nodes():
    """Nœuds et liens du réseau d'entreprise."""
    nodes = {
        "FW-01":      {"x": 0.5,  "y": 1.0,  "type": "firewall", "label": "Firewall\nPérimètre"},
        "SRV-WEB":    {"x": 0.2,  "y": 0.75, "type": "server",   "label": "Serveur\nWeb"},
        "SRV-APP":    {"x": 0.5,  "y": 0.75, "type": "server",   "label": "Serveur\nApp"},
        "SRV-DB":     {"x": 0.8,  "y": 0.75, "type": "server",   "label": "Base de\nDonnées"},
        "AD-DC":      {"x": 0.35, "y": 0.5,  "type": "critical", "label": "Active\nDirectory"},
        "SRV-FILES":  {"x": 0.65, "y": 0.5,  "type": "server",   "label": "Serveur\nFichiers"},
        "WS-ADMIN":   {"x": 0.15, "y": 0.25, "type": "endpoint", "label": "Poste\nAdmin IT"},
        "WS-MKT-01":  {"x": 0.4,  "y": 0.25, "type": "endpoint", "label": "Poste\nMarketing 1"},
        "WS-MKT-02":  {"x": 0.6,  "y": 0.25, "type": "endpoint", "label": "Poste\nMarketing 2"},
        "WS-DEV":     {"x": 0.85, "y": 0.25, "type": "endpoint", "label": "Poste\nDev"},
        "IOT-CAM":    {"x": 0.1,  "y": 0.5,  "type": "iot",      "label": "Caméra\nIP"},
        "IOT-PRINT":  {"x": 0.9,  "y": 0.5,  "type": "iot",      "label": "Imprimante\nRéseau"},
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
    compromised = {"WS-MKT-01", "AD-DC", "SRV-FILES"}
    isolated = {"WS-MKT-01", "AD-DC"}
    lateral_path = {"WS-MKT-01", "AD-DC", "SRV-FILES"}

    if not intrusion_active:
        return CAPGEMINI_BLUE
    if attack_phase == 1:
        return AMBER if node_id in lateral_path else CAPGEMINI_BLUE
    if attack_phase >= 2:
        if node_id in isolated:
            return CORAL
        if node_id in compromised:
            return AMBER
        return CAPGEMINI_BLUE
    return CAPGEMINI_BLUE


def get_node_symbol(node_info):
    mapping = {
        "firewall": "diamond", "server": "square", "critical": "star",
        "endpoint": "circle", "iot": "triangle-up",
    }
    return mapping.get(node_info["type"], "circle")


def get_node_size(node_info):
    mapping = {
        "firewall": 22, "server": 18, "critical": 24,
        "endpoint": 14, "iot": 12,
    }
    return mapping.get(node_info["type"], 14)


def build_network_figure(intrusion_active, attack_phase):
    nodes, edges = build_network_nodes()
    fig = go.Figure()

    compromised_edges = {
        ("WS-MKT-01", "AD-DC"), ("AD-DC", "WS-MKT-01"),
        ("AD-DC", "SRV-FILES"), ("SRV-FILES", "AD-DC"),
        ("SRV-APP", "AD-DC"), ("AD-DC", "SRV-APP"),
    }

    for src, dst in edges:
        n1, n2 = nodes[src], nodes[dst]
        edge_color = SLATE_600
        edge_width = 1
        if intrusion_active and attack_phase >= 1:
            if (src, dst) in compromised_edges or (dst, src) in compromised_edges:
                edge_color = CORAL if attack_phase >= 2 else AMBER
                edge_width = 2.5
        fig.add_trace(go.Scatter(
            x=[n1["x"], n2["x"]], y=[n1["y"], n2["y"]],
            mode="lines", line=dict(color=edge_color, width=edge_width),
            hoverinfo="none", showlegend=False,
        ))

    for nid, info in nodes.items():
        color = get_node_color(nid, info, intrusion_active, attack_phase)
        border_color = WHITE if color == CORAL else color
        isolated_nodes = {"WS-MKT-01", "AD-DC"}
        opacity = 0.35 if (intrusion_active and attack_phase >= 3
                           and nid in isolated_nodes) else 1.0
        fig.add_trace(go.Scatter(
            x=[info["x"]], y=[info["y"]],
            mode="markers+text",
            marker=dict(
                size=get_node_size(info), color=color,
                symbol=get_node_symbol(info),
                line=dict(width=2, color=border_color), opacity=opacity,
            ),
            text=info["label"], textposition="bottom center",
            textfont=dict(size=9, color=SLATE_400, family="Inter"),
            hovertext=f"<b>{nid}</b><br>Type : {info['type']}",
            hoverinfo="text", showlegend=False,
        ))

    if intrusion_active and attack_phase >= 3:
        fig.add_shape(
            type="rect", x0=0.05, y0=0.15, x1=0.5, y1=0.6,
            line=dict(color=CORAL, width=2, dash="dash"),
            fillcolor="rgba(248,113,113,0.04)",
        )
        fig.add_annotation(
            x=0.275, y=0.62, text="Zone isolée",
            font=dict(color=CORAL, size=11, family="Inter"), showarrow=False,
        )

    fig.update_layout(
        plot_bgcolor=SLATE_800, paper_bgcolor=SLATE_800,
        xaxis=dict(visible=False, range=[-0.05, 1.05]),
        yaxis=dict(visible=False, range=[0.05, 1.1]),
        margin=dict(l=10, r=10, t=10, b=10), height=420,
        hoverlabel=dict(bgcolor=CARD_BG, font_color=SLATE_300),
    )
    return fig


def build_risk_gauge(score):
    if score < 30:
        bar_color = MINT
    elif score < 70:
        bar_color = AMBER
    else:
        bar_color = CORAL

    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=score,
        number=dict(suffix="%", font=dict(size=42, color=WHITE,
                                          family="Inter")),
        gauge=dict(
            axis=dict(range=[0, 100], tickcolor=SLATE_600,
                      tickfont=dict(color=SLATE_400)),
            bar=dict(color=bar_color, thickness=0.7),
            bgcolor=CARD_BG, bordercolor=SLATE_600,
            steps=[
                dict(range=[0, 30], color="rgba(52,211,153,0.06)"),
                dict(range=[30, 70], color="rgba(251,191,36,0.06)"),
                dict(range=[70, 100], color="rgba(248,113,113,0.06)"),
            ],
            threshold=dict(
                line=dict(color=CORAL, width=3), thickness=0.8, value=80,
            ),
        ),
    ))
    fig.update_layout(
        paper_bgcolor=SLATE_800, plot_bgcolor=SLATE_800,
        height=250, margin=dict(l=30, r=30, t=30, b=10),
    )
    return fig


def _chart_layout(fig, y_title, y_range):
    fig.update_layout(
        paper_bgcolor=SLATE_800, plot_bgcolor=SLATE_800,
        xaxis=dict(title="Heure", gridcolor=SLATE_700, tickcolor=SLATE_400,
                   title_font=dict(color=SLATE_400, family="Inter"),
                   tickfont=dict(color=SLATE_400)),
        yaxis=dict(title=y_title, gridcolor=SLATE_700, range=y_range,
                   title_font=dict(color=SLATE_400, family="Inter"),
                   tickfont=dict(color=SLATE_400)),
        legend=dict(font=dict(color=SLATE_400, size=10, family="Inter"),
                    bgcolor="rgba(26,35,50,0.85)"),
        height=320, margin=dict(l=50, r=20, t=20, b=50),
    )


def build_confidence_budget_chart():
    hours = list(range(0, 24))
    np.random.seed(42)
    admin_baseline = [60 + 15 * np.sin(h / 3.8) for h in hours]
    admin_real = [v + np.random.uniform(-3, 5) for v in admin_baseline]
    mkt_baseline = [30 + 25 * np.sin((h - 4) / 3.8) for h in hours]
    mkt_real = [v + np.random.uniform(-2, 4) for v in mkt_baseline]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hours, y=admin_baseline, name="Admin IT — Référence",
        line=dict(color=CAPGEMINI_BLUE, width=2, dash="dash"), opacity=0.7,
    ))
    fig.add_trace(go.Scatter(
        x=hours, y=admin_real, name="Admin IT — Réel",
        line=dict(color=CAPGEMINI_BLUE, width=2),
        fill="tonexty", fillcolor="rgba(0,112,173,0.06)",
    ))
    fig.add_trace(go.Scatter(
        x=hours, y=mkt_baseline, name="Marketing — Référence",
        line=dict(color=SLATE_400, width=2, dash="dash"), opacity=0.7,
    ))
    fig.add_trace(go.Scatter(
        x=hours, y=mkt_real, name="Marketing — Réel",
        line=dict(color=SLATE_400, width=2),
        fill="tonexty", fillcolor="rgba(148,163,184,0.06)",
    ))
    _chart_layout(fig, "Budget confiance (%)", [0, 100])
    return fig


def build_confidence_budget_attack():
    hours = list(range(0, 24))
    np.random.seed(42)
    admin_baseline = [60 + 15 * np.sin(h / 3.8) for h in hours]
    admin_real = [v + np.random.uniform(-3, 5) for v in admin_baseline]
    mkt_baseline = [30 + 25 * np.sin((h - 4) / 3.8) for h in hours]
    mkt_real = list(mkt_baseline)
    for i in range(14, min(18, len(hours))):
        mkt_real[i] = mkt_baseline[i] + 35 + np.random.uniform(0, 10)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hours, y=admin_baseline, name="Admin IT — Référence",
        line=dict(color=CAPGEMINI_BLUE, width=2, dash="dash"), opacity=0.7,
    ))
    fig.add_trace(go.Scatter(
        x=hours, y=admin_real, name="Admin IT — Réel",
        line=dict(color=CAPGEMINI_BLUE, width=2),
        fill="tonexty", fillcolor="rgba(0,112,173,0.06)",
    ))
    fig.add_trace(go.Scatter(
        x=hours, y=mkt_baseline, name="Marketing — Référence",
        line=dict(color=SLATE_400, width=2, dash="dash"), opacity=0.7,
    ))
    fig.add_trace(go.Scatter(
        x=hours, y=mkt_real, name="Marketing — Réel (anomalie)",
        line=dict(color=CORAL, width=3),
        fill="tonexty", fillcolor="rgba(248,113,113,0.06)",
    ))
    fig.add_vrect(x0=14, x1=17, fillcolor=CORAL, opacity=0.06, line_width=0)
    fig.add_annotation(
        x=15.5, y=95, text="Anomalie détectée",
        font=dict(color=CORAL, size=12, family="Inter"), showarrow=False,
    )
    _chart_layout(fig, "Budget confiance (%)", [0, 110])
    return fig


# ---------------------------------------------------------------------------
# Console d'audit — séquence de logs
# ---------------------------------------------------------------------------
TERMINAL_SEQUENCE = [
    ("system", "[AEGIS] Shadow Proxy activé — Flux redirigé vers Mirage Sandbox"),
    ("system", "[AEGIS] Latency Mimicry engagé : injection +500 ms"),
    ("system", "[AEGIS] Enregistrement forensique démarré…"),
    ("", ""),
    ("prompt", "attacker@compromised:~$ whoami"),
    ("output", "mkt-user01"),
    ("prompt", "attacker@compromised:~$ uname -a"),
    ("output", "Linux SRV-FILES 5.15.0-generic #1 SMP x86_64 GNU/Linux"),
    ("prompt", "attacker@compromised:~$ ls /etc/"),
    ("output", "passwd  shadow  hosts  hostname  resolv.conf  ssl/  ssh/"),
    ("prompt", "attacker@compromised:~$ cat /etc/shadow"),
    ("mirage", "[MIRAGE IA] Génération de faux hashes en cours…"),
    ("output", "root:$6$xK9vQ2mZ$fAk3hAsH7rGn8Tq...truncated:19847:0:99999:7:::"),
    ("output", "admin:$6$pL4wN8rT$m1R4g3HaSh9Bx2...truncated:19847:0:99999:7:::"),
    ("output", "mkt-user01:$6$qW3eR5tY$d3c0YcOnT3nT...truncated:19847:0:99999:7:::"),
    ("prompt", "attacker@compromised:~$ cat /home/admin/passwords.txt"),
    ("mirage", "[MIRAGE IA] Génération de faux identifiants…"),
    ("output", "# Admin Password Vault — CONFIDENTIEL"),
    ("output", "aws_prod     : Xk9$mP2!vL7@nQ4w"),
    ("output", "db_master    : Rj5#hN8&bY3*fT6e"),
    ("output", "vpn_gateway  : Wm2%kD9!pA6^sG1c"),
    ("output", "ssh_bastion  : Qz7&nL4$vH8@jR5t"),
    ("prompt", "attacker@compromised:~$ scp passwords.txt ext-relay:/tmp/"),
    ("mirage", "[MIRAGE IA] Simulation d'exfiltration — données tracées"),
    ("output", "passwords.txt    100%  412    52.1KB/s   00:00"),
    ("system", "[AEGIS] Exfiltration capturée — Hash de traçage injecté"),
    ("system", "[AEGIS] Empreinte attaquant enregistrée : TTP T1003, T1078, T1021"),
    ("", ""),
    ("prompt", "attacker@compromised:~$ ssh admin@AD-DC"),
    ("system", "[AEGIS] Tentative de déplacement latéral détectée"),
    ("system", "[AEGIS] Isolation déclenchée — Nœuds WS-MKT-01, AD-DC coupés"),
    ("output", "ssh: connect to host AD-DC port 22: Connection refused"),
    ("system", "[AEGIS] Session Mirage terminée — Données forensiques sauvegardées"),
]


def get_terminal_html(lines):
    html = '<div class="audit-console">'
    for kind, text in lines:
        if kind == "prompt":
            html += f'<div class="prompt">{text}</div>'
        elif kind == "system":
            html += f'<div class="system">{text}</div>'
        elif kind == "mirage":
            html += f'<div class="mirage">{text}</div>'
        elif kind == "output":
            html += f'<div class="output">{text}</div>'
        elif kind == "" and text == "":
            html += "<br>"
    html += "</div>"
    return html


def build_attack_timeline():
    base = datetime(2026, 3, 11, 14, 23, 12)
    return [
        (base, "critical",
         "Credential Stuffing détecté sur SRV-WEB (43 tentatives / 10 s)"),
        (base + timedelta(seconds=3), "critical",
         "Compromission réussie : compte mkt-user01 (mot de passe faible)"),
        (base + timedelta(seconds=8), "warning",
         "Score Rs passe de 12 % à 67 % — Seuil d'alerte atteint"),
        (base + timedelta(seconds=11), "warning",
         "Shadow Proxy activé — Flux redirigé vers Mirage Sandbox"),
        (base + timedelta(seconds=12), "warning",
         "Latency Mimicry engagé (+500 ms d'injection)"),
        (base + timedelta(seconds=18), "critical",
         "Déplacement latéral WS-MKT-01 → AD-DC détecté (T1021)"),
        (base + timedelta(seconds=24), "warning",
         "Lecture /etc/shadow — Mirage IA génère de faux hashes"),
        (base + timedelta(seconds=31), "warning",
         "Lecture passwords.txt — Faux identifiants injectés"),
        (base + timedelta(seconds=38), "critical",
         "Tentative d'exfiltration — Hash de traçage injecté dans le payload"),
        (base + timedelta(seconds=45), "critical",
         "Score Rs atteint 94 % — Isolation automatique déclenchée"),
        (base + timedelta(seconds=46), "success",
         "Nœuds WS-MKT-01 et AD-DC isolés du réseau"),
        (base + timedelta(seconds=47), "success",
         "Session Mirage terminée — Données forensiques sauvegardées"),
        (base + timedelta(seconds=52), "success",
         "Rapport NIS2 généré automatiquement"),
    ]


def get_nis2_report_html():
    return f"""
<div class="nis2-report">
<h3>Rapport d'incident NIS2 — AEGIS AI</h3>
<p style="color:{SLATE_400}; font-size:0.8rem;">
Référence : AEGIS-INC-2026-0311-001 &nbsp;|&nbsp; Classification : Critique &nbsp;|&nbsp;
Généré automatiquement le 11/03/2026 à 14:24:04 UTC
</p>

<h3>1. Identification</h3>
<p><span class="field-label">Entité :</span>
   <span class="field-value">Capgemini — Division Cyber Défense</span></p>
<p><span class="field-label">Type d'incident :</span>
   <span class="critical-tag">Intrusion active avec déplacement latéral</span></p>
<p><span class="field-label">Date de détection :</span>
   <span class="field-value">11/03/2026 14:23:12 UTC</span></p>
<p><span class="field-label">Durée totale :</span>
   <span class="field-value">52 secondes (détection à remédiation)</span></p>
<p><span class="field-label">Impact métier :</span>
   <span class="ok-tag">Aucune interruption de service</span></p>

<h3>2. Patient zéro</h3>
<p><span class="field-label">Machine :</span>
   <span class="field-value">WS-MKT-01 (10.0.2.47)</span></p>
<p><span class="field-label">Compte compromis :</span>
   <span class="critical-tag">mkt-user01</span></p>
<p><span class="field-label">Vecteur initial :</span>
   <span class="field-value">Credential Stuffing via SRV-WEB (port 443)</span></p>
<p><span class="field-label">Cause racine :</span>
   <span class="field-value">Mot de passe faible, absence de MFA sur le portail marketing</span></p>

<h3>3. TTPs détectées (MITRE ATT&amp;CK)</h3>
<table style="width:100%; color:{SLATE_300}; border-collapse:collapse;">
<tr style="border-bottom:1px solid {SLATE_600};">
  <td style="padding:8px;"><code>T1110.004</code></td>
  <td style="padding:8px;">Credential Stuffing</td>
  <td style="padding:8px;"><span class="critical-tag">Initial Access</span></td>
</tr>
<tr style="border-bottom:1px solid {SLATE_600};">
  <td style="padding:8px;"><code>T1078</code></td>
  <td style="padding:8px;">Valid Accounts</td>
  <td style="padding:8px;"><span class="critical-tag">Persistence</span></td>
</tr>
<tr style="border-bottom:1px solid {SLATE_600};">
  <td style="padding:8px;"><code>T1021</code></td>
  <td style="padding:8px;">Remote Services (SSH)</td>
  <td style="padding:8px;"><span class="critical-tag">Lateral Movement</span></td>
</tr>
<tr style="border-bottom:1px solid {SLATE_600};">
  <td style="padding:8px;"><code>T1003</code></td>
  <td style="padding:8px;">OS Credential Dumping</td>
  <td style="padding:8px;">Credential Access</td>
</tr>
<tr>
  <td style="padding:8px;"><code>T1048</code></td>
  <td style="padding:8px;">Exfiltration Over Alternative Protocol</td>
  <td style="padding:8px;">Exfiltration</td>
</tr>
</table>

<h3>4. Actions AEGIS automatiques</h3>
<p><span class="ok-tag">&#10003;</span> Redirection vers Mirage Sandbox (Shadow Proxying L7)</p>
<p><span class="ok-tag">&#10003;</span> Injection de faux identifiants (Mirage IA génératif)</p>
<p><span class="ok-tag">&#10003;</span> Injection de hash de traçage dans le payload exfiltré</p>
<p><span class="ok-tag">&#10003;</span> Isolation réseau des nœuds WS-MKT-01 et AD-DC</p>
<p><span class="ok-tag">&#10003;</span> Capture forensique complète de la session attaquant</p>

<h3>5. Recommandations de remédiation immédiate</h3>

<p style="margin-top:0.8rem;"><b>Firewall (Priorité : Critique)</b></p>
<p><code>iptables -A INPUT -s 10.0.2.0/24 -d 10.0.1.10 -p tcp --dport 22 -j DROP</code><br>
<code>iptables -A INPUT -p tcp --dport 443 -m connlimit --connlimit-above 10 -j REJECT</code></p>

<p style="margin-top:0.8rem;"><b>IAM / Active Directory (Priorité : Critique)</b></p>
<p>&bull; Forcer la réinitialisation du mot de passe pour mkt-user01<br>
&bull; Activer le MFA obligatoire sur tous les portails web exposés<br>
&bull; Appliquer une politique de mot de passe (min. 14 caractères, complexité)<br>
&bull; Restreindre les connexions SSH inter-segments au strict nécessaire</p>

<p style="margin-top:0.8rem;"><b>Monitoring (Priorité : Haute)</b></p>
<p>&bull; Ajouter une alerte SIEM pour &gt; 10 échecs auth / 10 s par IP source<br>
&bull; Activer le logging SSH détaillé sur AD-DC et SRV-FILES<br>
&bull; Déployer un EDR sur les endpoints du segment Marketing</p>

<p style="text-align:center; color:{SLATE_400}; font-size:0.8rem; margin-top:1.5rem;
          border-top:1px solid {SLATE_600}; padding-top:1rem;">
AEGIS AI — Rapport généré automatiquement &nbsp;|&nbsp; Conforme NIS2 Art. 23 &nbsp;|&nbsp;
Capgemini Cyber Défense 2026
</p>
</div>
"""


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown("""
<div class="aegis-header">
    <h1><span>AEGIS</span> AI</h1>
    <p>Système de Défense Active Cognitive &mdash; Capgemini Cyber Défense</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center; padding:0.5rem 0 1rem 0;">
        <span style="color:{CAPGEMINI_BLUE}; font-family:'Inter',sans-serif;
                     font-size:0.9rem; font-weight:600; letter-spacing:1px;">
        Panneau de contrôle
        </span>
    </div>
    """, unsafe_allow_html=True)

    is_attack = st.session_state.intrusion_active

    if is_attack:
        st.markdown(f"""
        <div class="alert-card anim-pulse">
            <div class="label">Statut système</div>
            <div class="value">Test en cours</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="metric-card">
            <div class="label">Statut système</div>
            <div class="value" style="color:{MINT};">Nominal</div>
        </div>
        """, unsafe_allow_html=True)

    rs = 94 if is_attack else 12
    rs_color = CORAL if is_attack else MINT
    card_class = "alert-card" if is_attack else "metric-card"
    st.markdown(f"""
    <div class="{card_class}">
        <div class="label">Score de risque Rs</div>
        <div class="value" style="color:{rs_color};">{rs} %</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="metric-card">
        <div class="label">Nœuds surveillés</div>
        <div class="value">12 / 12</div>
    </div>
    """, unsafe_allow_html=True)

    isolated_count = 2 if is_attack and st.session_state.attack_phase >= 3 else 0
    iso_color = CORAL if isolated_count > 0 else MINT
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">Nœuds isolés</div>
        <div class="value" style="color:{iso_color};">{isolated_count}</div>
    </div>
    """, unsafe_allow_html=True)

    mirage_status = "Actif" if is_attack and st.session_state.attack_phase >= 2 else "Veille"
    mirage_color = GOLD if mirage_status == "Actif" else SLATE_400
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">Mirage génératif</div>
        <div class="value" style="color:{mirage_color};">{mirage_status}</div>
    </div>
    """, unsafe_allow_html=True)

    if is_attack and st.session_state.attack_phase >= 2:
        st.markdown(f"""
        <div class="latency-badge">
            <span style="color:{AMBER}; font-family:'JetBrains Mono',monospace;
                         font-size:0.82rem;">
            Injection de latence active<br>
            <b style="font-size:1.2rem;">+500 ms</b>
            </span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="metric-card">
        <div class="label">Uptime service métier</div>
        <div class="value" style="color:{MINT};">99,97 %</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"""
    <div style="text-align:center; color:{SLATE_400}; font-size:0.7rem;
                font-family:'Inter',sans-serif;">
        AEGIS AI v2.1 &mdash; Silicondays 2026<br>
        Capgemini Cyber Défense
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------
tab_avant, tab_pendant, tab_apres = st.tabs([
    "Avant — Sentinel & Baseline",
    "Pendant — Riposte Active & Mirage",
    "Après — Forensics & Rapport NIS2",
])

# ===== TAB 1 : AVANT =====
with tab_avant:
    st.markdown(
        '<span class="phase-badge phase-avant">Phase 1 — Mode Sentinel</span>',
        unsafe_allow_html=True,
    )
    st.markdown("""
    > **Mode Sentinel** : AEGIS surveille en continu le réseau, établit des
    > baselines comportementales et calcule un score de risque dynamique
    > pour chaque entité.
    """)

    col_map, col_gauge = st.columns([3, 2])
    with col_map:
        st.markdown(
            f"**Topologie réseau** &mdash; "
            f"<span style='color:{MINT};'>Tous les nœuds nominaux</span>",
            unsafe_allow_html=True,
        )
        st.plotly_chart(build_network_figure(False, 0),
                        width="stretch", key="net_avant")

    with col_gauge:
        st.markdown("**Score de risque global** $R_s$")
        st.plotly_chart(build_risk_gauge(12),
                        width="stretch", key="gauge_avant")
        st.markdown(f"""
        <div class="metric-card" style="text-align:center;">
            <div class="label">Verdict</div>
            <div class="value" style="color:{MINT}; font-size:1rem;">
            Aucune menace détectée</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**Profils comportementaux surveillés**")
    prof1, prof2, prof3, prof4 = st.columns(4)
    with prof1:
        st.markdown(f"""
        <div class="profile-card">
            <div class="avatar" style="background:{CAPGEMINI_BLUE};">JD</div>
            <div class="name">Jean Dupont</div>
            <div class="role">Admin IT — Infrastructure</div>
            <div class="detail"><span>Accès</span><span class="val">Privilégié</span></div>
            <div class="detail"><span>Segments</span><span class="val">Tous</span></div>
            <div class="detail"><span>Sessions / jour</span><span class="val">18</span></div>
            <div class="detail"><span>Budget confiance</span><span class="val">87 %</span></div>
            <div class="risk-tag risk-low">Risque bas</div>
        </div>
        """, unsafe_allow_html=True)
    with prof2:
        st.markdown(f"""
        <div class="profile-card" style="animation-delay:0.1s;">
            <div class="avatar" style="background:{SLATE_600};">ML</div>
            <div class="name">Marie Lefèvre</div>
            <div class="role">Marketing — Chef de projet</div>
            <div class="detail"><span>Accès</span><span class="val">Standard</span></div>
            <div class="detail"><span>Segments</span><span class="val">MKT, Web</span></div>
            <div class="detail"><span>Sessions / jour</span><span class="val">12</span></div>
            <div class="detail"><span>Budget confiance</span><span class="val">92 %</span></div>
            <div class="risk-tag risk-low">Risque bas</div>
        </div>
        """, unsafe_allow_html=True)
    with prof3:
        st.markdown(f"""
        <div class="profile-card" style="animation-delay:0.2s;">
            <div class="avatar" style="background:{GOLD};">PT</div>
            <div class="name">Pierre Tran</div>
            <div class="role">Dev — Backend Lead</div>
            <div class="detail"><span>Accès</span><span class="val">Élevé</span></div>
            <div class="detail"><span>Segments</span><span class="val">Dev, Prod</span></div>
            <div class="detail"><span>Sessions / jour</span><span class="val">24</span></div>
            <div class="detail"><span>Budget confiance</span><span class="val">78 %</span></div>
            <div class="risk-tag risk-medium">Risque modéré</div>
        </div>
        """, unsafe_allow_html=True)
    with prof4:
        st.markdown(f"""
        <div class="profile-card" style="animation-delay:0.3s;">
            <div class="avatar" style="background:{SLATE_400};">SB</div>
            <div class="name">Sophie Bernard</div>
            <div class="role">Marketing — Stagiaire</div>
            <div class="detail"><span>Accès</span><span class="val">Restreint</span></div>
            <div class="detail"><span>Segments</span><span class="val">MKT</span></div>
            <div class="detail"><span>Sessions / jour</span><span class="val">6</span></div>
            <div class="detail"><span>Budget confiance</span><span class="val">95 %</span></div>
            <div class="risk-tag risk-low">Risque bas</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**Tableau comportemental** &mdash; Consommation du budget confiance")
    st.plotly_chart(build_confidence_budget_chart(),
                    width="stretch", key="behavior_avant")
    st.info(
        "Les profils **Admin IT** et **Marketing** restent dans les limites "
        "de leur baseline. Le budget confiance est respecté."
    )
    st.markdown(f"""
    <div class="nav-hint">
        <div class="icon">&#10145;</div>
        <div class="text">Passez à l'onglet <span class="tab-name">Pendant — Riposte Active & Mirage</span> pour lancer une simulation d'attaque et observer la réponse d'AEGIS AI.</div>
    </div>
    """, unsafe_allow_html=True)


# ===== TAB 2 : PENDANT =====
with tab_pendant:
    st.markdown(
        '<span class="phase-badge phase-pendant">Phase 2 — Mode Mirage</span>',
        unsafe_allow_html=True,
    )
    st.markdown("""
    > **Mode Mirage** : Lorsqu'une menace est détectée, AEGIS redirige
    > invisiblement l'attaquant vers un environnement sandbox (Shadow Proxying)
    > et génère de faux contenus via IA pour maintenir l'illusion.
    """)

    # ---- Scénario selector ----
    scenario = ATTACK_SCENARIOS[st.session_state.selected_scenario]
    col_sel, col_info = st.columns([1, 2])
    with col_sel:
        scenario_names = [s["name"] for s in ATTACK_SCENARIOS]
        chosen = st.selectbox(
            "Scénario de test",
            scenario_names,
            index=st.session_state.selected_scenario,
            disabled=st.session_state.intrusion_active,
            key="scenario_select",
        )
        st.session_state.selected_scenario = scenario_names.index(chosen)
        scenario = ATTACK_SCENARIOS[st.session_state.selected_scenario]
    with col_info:
        st.markdown(f"""
        <div class="scenario-selector anim-fade-in">
            <div class="label">Détails du scénario</div>
            <div style="color:{SLATE_300}; font-family:'Inter',sans-serif; font-size:0.85rem; margin-bottom:0.4rem;">
                {scenario['desc']}
            </div>
            <div style="display:flex; gap:1.5rem; flex-wrap:wrap;">
                <span style="color:{SLATE_400}; font-size:0.78rem;">Vecteur : <b style="color:{WHITE};">{scenario['vector']}</b></span>
                <span style="color:{SLATE_400}; font-size:0.78rem;">Cible : <b style="color:{WHITE};">{scenario['target']}</b></span>
                <span style="color:{SLATE_400}; font-size:0.78rem;">Sévérité : <b style="color:{CORAL};">{scenario['severity']}</b></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    col_btn, col_status = st.columns([1, 2])
    with col_btn:
        intrusion_btn = st.button(
            f"Lancer le test — {scenario['vector']}",
            type="primary", width="stretch",
            disabled=st.session_state.intrusion_active,
        )
    with col_status:
        status_ph = st.empty()

    if st.session_state.intrusion_active and not st.session_state.animating:
        phase_names = {
            1: "Analyse en cours…",
            2: "Mirage actif — Menace contenue par l'IA",
            3: "Isolation terminée — Continuité maintenue",
        }
        phase_text = phase_names.get(
            st.session_state.attack_phase, "Traitement…"
        )
        status_ph.markdown(f"""
        <div class="alert-card" style="text-align:center;">
            <div class="value" style="font-size:1rem;">{phase_text}</div>
        </div>
        """, unsafe_allow_html=True)

    # Layout containers
    progress_ph = st.empty()
    col_net2, col_gauge2 = st.columns([3, 2])
    with col_net2:
        net_label_ph = st.empty()
        net_chart_ph = st.empty()
    with col_gauge2:
        gauge_label_ph = st.empty()
        gauge_chart_ph = st.empty()
        verdict_ph = st.empty()

    sep1_ph = st.empty()
    behav_label_ph = st.empty()
    behav_chart_ph = st.empty()
    sep2_ph = st.empty()
    latency_ph = st.empty()
    continuity_ph = st.empty()
    expander_container = st.expander(
        "Voir les détails techniques de l'isolation (Logs IA)",
        expanded=False,
    )
    with expander_container:
        terminal_ph = st.empty()
    reset_ph = st.empty()
    def _render_panels(phase, score, term_lines):
        # Création d'une clé unique dynamique pour Streamlit
        uid = f"{phase}_{int(time.time() * 1000)}"
        
        net_color = AMBER if phase >= 1 else MINT
        net_text = ("Mouvement détecté — IA en réponse" if phase >= 1
                    else "Surveillance")
        net_label_ph.markdown(
            f"**Topologie réseau** &mdash; "
            f"<span style='color:{net_color};'>{net_text}</span>",
            unsafe_allow_html=True,
        )
        
        # Ajout de l'argument 'key' unique ici
        net_chart_ph.plotly_chart(
            build_network_figure(True, phase), width="stretch",
            key=f"net_chart_{uid}"
        )
        
        gauge_label_ph.markdown("**Score de risque global** $R_s$")
        
        # Ajout de l'argument 'key' unique ici
        gauge_chart_ph.plotly_chart(
            build_risk_gauge(score), width="stretch",
            key=f"gauge_chart_{uid}"
        )
        
        if phase >= 2:
            verdict_ph.markdown(f"""
            <div class="alert-card" style="text-align:center;">
                <div class="label">Verdict</div>
                <div class="value" style="font-size:1rem;">
                Menace contenue — Mirage engagé</div>
            </div>
            """, unsafe_allow_html=True)
            sep1_ph.markdown("---")
            behav_label_ph.markdown(
                "**Tableau comportemental** &mdash; Anomalie détectée"
            )
            
            # Ajout de l'argument 'key' unique ici
            behav_chart_ph.plotly_chart(
                build_confidence_budget_attack(), width="stretch",
                key=f"behav_chart_{uid}"
            )
            
            sep2_ph.markdown("---")
            latency_ph.markdown(f"""
            <div class="latency-badge" style="margin-bottom:1rem;">
                <span style="color:{AMBER}; font-family:'JetBrains Mono',monospace;
                             font-size:0.85rem;">
                Injection de latence active &mdash;
                <b>+500 ms</b> sur chaque réponse Mirage
                (simulation de la production réelle)
                </span>
            </div>
            """, unsafe_allow_html=True)
            
        if term_lines:
            terminal_ph.markdown(
                get_terminal_html(term_lines), unsafe_allow_html=True,
            )

        # Continuity of service banner — the most reassuring metric
        if phase >= 1:
            continuity_ph.markdown(f"""
            <div class="continuity-banner anim-fade-in-up anim-pulse-mint">
                <div class="label">Continuité de service</div>
                <div class="value">100 % Maintenue</div>
                <div class="subtitle">Les services métier n'ont subi aucune interruption</div>
            </div>
            """, unsafe_allow_html=True)

            
    # ---- ANIMATION ----
    if intrusion_btn and not st.session_state.intrusion_active:
        st.session_state.intrusion_active = True
        st.session_state.animating = True
        st.session_state.attack_timestamp = datetime.now()
        st.session_state.terminal_lines = []
        total_steps = 3 + len(TERMINAL_SEQUENCE)  # 3 phases + terminal lines

        def _update_progress(step, label):
            pct = min(int((step / total_steps) * 100), 100)
            css_class = "complete" if pct >= 100 else ""
            progress_ph.markdown(f"""
            <div>
                <div class="progress-label">
                    <span>{label}</span>
                    <span>{pct} %</span>
                </div>
                <div class="progress-container">
                    <div class="progress-bar {css_class}" style="width:{pct}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Phase 1
        st.session_state.attack_phase = 1
        _update_progress(1, "Phase 1/3 — Détection & Analyse")
        status_ph.markdown(f"""
        <div class="alert-card anim-fade-in" style="text-align:center;">
            <div class="value" style="font-size:1rem;">Analyse en cours…</div>
        </div>
        """, unsafe_allow_html=True)
        _render_panels(1, 67, [])
        time.sleep(2)

        # Phase 2
        st.session_state.attack_phase = 2
        _update_progress(2, "Phase 2/3 — Mirage actif")
        status_ph.markdown(f"""
        <div class="alert-card anim-fade-in" style="text-align:center;">
            <div class="value" style="font-size:1rem;">Mirage actif — Menace contenue par l'IA</div>
        </div>
        """, unsafe_allow_html=True)
        _render_panels(2, 85, [])

        for i, line in enumerate(TERMINAL_SEQUENCE):
            st.session_state.terminal_lines.append(line)
            terminal_ph.markdown(
                get_terminal_html(st.session_state.terminal_lines),
                unsafe_allow_html=True,
            )
            _update_progress(3 + i, "Phase 2/3 — Audit console")
            time.sleep(0.3)

        # Phase 3
        st.session_state.attack_phase = 3
        _update_progress(total_steps, "Phase 3/3 — Isolation terminée")
        status_ph.markdown(f"""
        <div class="alert-card anim-fade-in" style="text-align:center;">
            <div class="value" style="font-size:1rem;">Isolation terminée — Continuité maintenue</div>
        </div>
        """, unsafe_allow_html=True)
        _render_panels(3, 94, st.session_state.terminal_lines)
        time.sleep(1)

        st.session_state.animating = False
        st.rerun()

    # ---- FINAL STATE ----
    elif st.session_state.intrusion_active and not st.session_state.animating:
        _render_panels(
            st.session_state.attack_phase, 94,
            st.session_state.terminal_lines,
        )
        st.markdown(f"""
        <div class="nav-hint">
            <div class="icon">&#10145;</div>
            <div class="text">Simulation terminée. Consultez l'onglet <span class="tab-name">Après — Forensics & Rapport NIS2</span> pour voir la timeline et générer le rapport d'incident.</div>
        </div>
        """, unsafe_allow_html=True)
        if reset_ph.button("Réinitialiser la simulation", key="reset_btn"):
            st.session_state.intrusion_active = False
            st.session_state.attack_phase = 0
            st.session_state.terminal_lines = []
            st.session_state.nis2_generated = False
            st.session_state.attack_timestamp = None
            st.session_state.animating = False
            st.rerun()

    # ---- IDLE ----
    else:
        net_label_ph.empty()
        net_chart_ph.empty()
        gauge_label_ph.empty()
        gauge_chart_ph.empty()
        verdict_ph.empty()
        st.markdown(f"""
        <div class="idle-placeholder">
            <div class="title">Système prêt</div>
            <div class="subtitle">Cliquez sur le bouton ci-dessus pour lancer
            un test de résilience par <b>Credential Stuffing</b> et observer la
            réponse d'AEGIS AI en temps réel.</div>
        </div>
        """, unsafe_allow_html=True)


# ===== TAB 3 : APRÈS =====
with tab_apres:
    st.markdown(
        '<span class="phase-badge phase-apres">Phase 3 — Mode Forensics</span>',
        unsafe_allow_html=True,
    )
    st.markdown("""
    > **Mode Forensics** : Après neutralisation, AEGIS génère automatiquement
    > une timeline de l'incident et un rapport conforme à la directive NIS2.
    """)

    if not st.session_state.intrusion_active:
        st.markdown(f"""
        <div class="idle-placeholder">
            <div class="title">Aucun incident à analyser</div>
            <div class="subtitle">Lancez d'abord une simulation dans l'onglet
            <b>Pendant</b> pour générer des données forensiques.</div>
        </div>
        <div class="nav-hint">
            <div class="icon">&#10145;</div>
            <div class="text">Rendez-vous dans l'onglet <span class="tab-name">Pendant — Riposte Active & Mirage</span> pour lancer un test de résilience.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("**Timeline de l'incident**")
        events = build_attack_timeline()
        for idx, (ts, severity, desc) in enumerate(events):
            time_str = (ts.strftime("%H:%M:%S.")
                        + f"{ts.microsecond // 1000:03d}")
            delay = idx * 0.06
            st.markdown(f"""
            <div class="timeline-event {severity}" style="animation-delay:{delay}s;">
                <div class="time">{time_str}</div>
                <div class="desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

        duration = events[-1][0] - events[0][0]
        st.markdown(f"""
        <div class="metric-card" style="text-align:center; margin:1rem 0;">
            <div class="label">Durée totale de l'incident</div>
            <div class="value" style="color:{CAPGEMINI_BLUE};">
            {duration.seconds} s &mdash; Détection à remédiation</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        if st.button("Générer le rapport NIS2", type="primary",
                      width="stretch", key="nis2_btn"):
            st.session_state.nis2_generated = True
            st.rerun()

        if st.session_state.nis2_generated:
            st.markdown(get_nis2_report_html(), unsafe_allow_html=True)

            report_text = """RAPPORT D'INCIDENT NIS2 — AEGIS AI
========================================
Référence : AEGIS-INC-2026-0311-001
Classification : Critique
Date : 11/03/2026 14:23:12 UTC

1. IDENTIFICATION
Entité : Capgemini — Division Cyber Défense
Type : Intrusion active avec déplacement latéral
Durée : 52 secondes (détection à remédiation)
Impact métier : Aucune interruption de service

2. PATIENT ZÉRO
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
[OK] Injection de faux identifiants (Mirage IA génératif)
[OK] Hash de traçage injecté dans le payload exfiltré
[OK] Isolation réseau WS-MKT-01 et AD-DC
[OK] Capture forensique complète

5. RECOMMANDATIONS
Firewall (Critique) :
  iptables -A INPUT -s 10.0.2.0/24 -d 10.0.1.10 -p tcp --dport 22 -j DROP
  iptables -A INPUT -p tcp --dport 443 -m connlimit --connlimit-above 10 -j REJECT

IAM (Critique) :
  - Réinitialisation du mot de passe mkt-user01
  - MFA obligatoire sur portails web
  - Politique mot de passe min. 14 car.
  - Restreindre SSH inter-segments

Monitoring (Haute) :
  - Alerte SIEM > 10 échecs auth / 10 s
  - Logging SSH sur AD-DC et SRV-FILES
  - EDR sur endpoints Marketing

========================================
AEGIS AI — Conforme NIS2 Art. 23
Capgemini Cyber Défense 2026
"""
            st.download_button(
                label="Télécharger le rapport (TXT)",
                data=report_text,
                file_name="AEGIS_NIS2_Report_2026-03-11.txt",
                mime="text/plain",
                width="stretch",
            )
