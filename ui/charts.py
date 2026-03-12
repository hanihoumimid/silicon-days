import numpy as np
import plotly.graph_objects as go

from core.theme import (
    AMBER, CAPGEMINI_BLUE, CARD_BG, CORAL, MINT, SLATE_300, SLATE_400,
    SLATE_600, SLATE_700, SLATE_800, WHITE,
)
from data.mock_data import ATTACK_SCENARIOS


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


def get_node_color(node_id, node_info, intrusion_active, attack_phase,
                   scenario_idx=0):
    sc = ATTACK_SCENARIOS[scenario_idx]
    compromised = sc["compromised_nodes"]
    isolated = sc["isolated_nodes"]
    lateral_path = sc["lateral_path"]

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


def build_network_figure(intrusion_active, attack_phase, scenario_idx=0):
    nodes, edges = build_network_nodes()
    fig = go.Figure()

    sc = ATTACK_SCENARIOS[scenario_idx]
    compromised_edges = sc["compromised_edges"]

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
        color = get_node_color(nid, info, intrusion_active, attack_phase,
                               scenario_idx)
        border_color = WHITE if color == CORAL else color
        isolated_nodes = sc["isolated_nodes"]
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
        x0, y0, x1, y1 = sc["isolated_zone"]
        lx, ly, ltext = sc["isolated_zone_label"]
        fig.add_shape(
            type="rect", x0=x0, y0=y0, x1=x1, y1=y1,
            line=dict(color=CORAL, width=2, dash="dash"),
            fillcolor="rgba(248,113,113,0.04)",
        )
        fig.add_annotation(
            x=lx, y=ly, text=ltext,
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


def build_confidence_budget_attack(scenario_idx=0):
    sc = ATTACK_SCENARIOS[scenario_idx]
    a_start, a_end = sc["anomaly_window"]
    hours = list(range(0, 24))
    np.random.seed(42)
    admin_baseline = [60 + 15 * np.sin(h / 3.8) for h in hours]
    admin_real = [v + np.random.uniform(-3, 5) for v in admin_baseline]
    mkt_baseline = [30 + 25 * np.sin((h - 4) / 3.8) for h in hours]
    mkt_real = list(mkt_baseline)
    for i in range(a_start, min(a_end, len(hours))):
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
    mid = (a_start + a_end) / 2
    fig.add_vrect(x0=a_start, x1=a_end, fillcolor=CORAL, opacity=0.06,
                  line_width=0)
    fig.add_annotation(
        x=mid, y=95, text="Anomalie détectée",
        font=dict(color=CORAL, size=12, family="Inter"), showarrow=False,
    )
    _chart_layout(fig, "Budget confiance (%)", [0, 110])
    return fig
