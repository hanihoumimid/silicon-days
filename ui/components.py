import unicodedata
from datetime import datetime, timedelta

from fpdf import FPDF
from fpdf.enums import XPos, YPos

from core.theme import (
    AMBER, CAPGEMINI_BLUE, CORAL, MINT, SLATE_300, SLATE_400, SLATE_600,
    SLATE_700, WHITE,
)
from data.mock_data import ATTACK_SCENARIOS
from data.ecs_logs import (
    ECS_LOGS_BY_SCENARIO, SOURCE_META, SRC_FIREWALL, SRC_AD, SRC_EDR,
    SRC_CLOUD, SEVERITY_CRITICAL, SEVERITY_HIGH, SEVERITY_MEDIUM,
    SEVERITY_LOW, SEVERITY_INFO,
)


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


def build_attack_timeline(scenario_idx=0):
    sc = ATTACK_SCENARIOS[scenario_idx]
    h, m, s = sc["attack_h"], sc["attack_m"], sc["attack_s"]
    base = datetime(2026, 3, 11, h, m, s)
    vector = sc["vector"]
    target = sc["target"]
    isolated = ", ".join(sorted(sc["isolated_nodes"]))

    return [
        (base, "critical",
         f"{vector} détecté sur {target.split('/')[0].strip()} (43 tentatives / 10 s)"),
        (base + timedelta(seconds=3), "critical",
         f"Compromission réussie : compte {target.split('/')[-1].strip()} (accès non autorisé)"),
        (base + timedelta(seconds=8), "warning",
         "Score Rs passe de 12 % à 67 % — Seuil d'alerte atteint"),
        (base + timedelta(seconds=11), "warning",
         "Shadow Proxy activé — Flux redirigé vers Mirage Sandbox"),
        (base + timedelta(seconds=12), "warning",
         "Latency Mimicry engagé (+500 ms d'injection)"),
        (base + timedelta(seconds=18), "critical",
         f"Mouvement latéral détecté depuis {list(sc['lateral_path'])[0]} (T1021)"),
        (base + timedelta(seconds=24), "warning",
         "Accès à des ressources sensibles — Mirage IA génère des leurres"),
        (base + timedelta(seconds=31), "warning",
         "Exfiltration de données leurres — balises de traçage injectées"),
        (base + timedelta(seconds=38), "critical",
         "Tentative d'exfiltration — Hash de traçage injecté dans le payload"),
        (base + timedelta(seconds=45), "critical",
         "Score Rs atteint 94 % — Isolation automatique déclenchée"),
        (base + timedelta(seconds=46), "success",
         f"Nœuds {isolated} isolés du réseau"),
        (base + timedelta(seconds=47), "success",
         "Session Mirage terminée — Données forensiques sauvegardées"),
        (base + timedelta(seconds=52), "success",
         "Rapport NIS2 généré automatiquement"),
    ]


def get_nis2_report_html(scenario_idx=0):
    sc = ATTACK_SCENARIOS[scenario_idx]
    ttps_rows = ""
    for code, name, phase in sc["ttps"]:
        tag = f'<span class="critical-tag">{phase}</span>' if phase in (
            "Initial Access", "Lateral Movement", "Persistence") else phase
        ttps_rows += f"""
<tr style="border-bottom:1px solid {SLATE_600};">
  <td style="padding:8px;"><code>{code}</code></td>
  <td style="padding:8px;">{name}</td>
  <td style="padding:8px;">{tag}</td>
</tr>"""

    aegis_items = "".join(
        f'<p><span class="ok-tag">&#10003;</span> {a}</p>'
        for a in sc["aegis_actions"]
    )
    fw_cmds = "".join(f"<code>{r}</code><br>" for r in sc["fw_rules"])
    iam_bullets = "".join(f"&bull; {r}<br>" for r in sc["iam_recs"])
    mon_bullets = "".join(f"&bull; {r}<br>" for r in sc["monitoring_recs"])

    return f"""
<div class="nis2-report">
<h3>Rapport d'incident NIS2 — AEGIS AI</h3>
<p style="color:{SLATE_400}; font-size:0.8rem;">
Référence : {sc['incident_ref']} &nbsp;|&nbsp; Classification : Critique &nbsp;|&nbsp;
Généré automatiquement le {sc['incident_date']}
</p>

<h3>1. Identification</h3>
<p><span class="field-label">Entité :</span>
   <span class="field-value">Capgemini — Division Cyber Défense</span></p>
<p><span class="field-label">Type d'incident :</span>
   <span class="critical-tag">{sc['incident_type']}</span></p>
<p><span class="field-label">Date de détection :</span>
   <span class="field-value">{sc['incident_date']}</span></p>
<p><span class="field-label">Durée totale :</span>
   <span class="field-value">{sc['incident_duration']}</span></p>
<p><span class="field-label">Impact métier :</span>
   <span class="ok-tag">Aucune interruption de service</span></p>

<h3>2. Patient zéro</h3>
<p><span class="field-label">Machine :</span>
   <span class="field-value">{sc['patient_zero_machine']}</span></p>
<p><span class="field-label">Compte compromis :</span>
   <span class="critical-tag">{sc['patient_zero_account']}</span></p>
<p><span class="field-label">Vecteur initial :</span>
   <span class="field-value">{sc['patient_zero_vector']}</span></p>
<p><span class="field-label">Cause racine :</span>
   <span class="field-value">{sc['patient_zero_cause']}</span></p>

<h3>3. TTPs détectées (MITRE ATT&amp;CK)</h3>
<table style="width:100%; color:{SLATE_300}; border-collapse:collapse;">
{ttps_rows}
</table>

<h3>4. Actions AEGIS automatiques</h3>
{aegis_items}

<h3>5. Recommandations de remédiation immédiate</h3>

<p style="margin-top:0.8rem;"><b>Firewall (Priorité : Critique)</b></p>
<p>{fw_cmds}</p>

<p style="margin-top:0.8rem;"><b>IAM / Active Directory (Priorité : Critique)</b></p>
<p>{iam_bullets}</p>

<p style="margin-top:0.8rem;"><b>Monitoring (Priorité : Haute)</b></p>
<p>{mon_bullets}</p>

<p style="text-align:center; color:{SLATE_400}; font-size:0.8rem; margin-top:1.5rem;
          border-top:1px solid {SLATE_600}; padding-top:1rem;">
AEGIS AI — Rapport généré automatiquement &nbsp;|&nbsp; Conforme NIS2 Art. 23 &nbsp;|&nbsp;
Capgemini Cyber Défense 2026
</p>
</div>
"""


def generate_nis2_pdf(scenario_idx=0):
    """Generate a PDF bytes buffer for the NIS2 report using fpdf2."""

    def _safe(text):
        """Transliterate non-latin-1 characters to their closest ASCII equivalent.

        fpdf2's built-in fonts (Helvetica) only support latin-1. We use NFD
        Unicode normalisation followed by a latin-1 encode/decode round-trip so
        that accented characters (é → e, à → a, etc.) are preserved as their
        base letters while any truly unrepresentable code-points are dropped.
        """
        return (
            unicodedata.normalize("NFD", text)
            .encode("latin-1", "ignore")
            .decode("latin-1")
        )

    sc = ATTACK_SCENARIOS[scenario_idx]

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    lm = pdf.l_margin

    def reset_x():
        pdf.set_x(lm)

    def write_line(text, font="Helvetica", style="", size=9,
                   color=(30, 30, 30), indent=0):
        pdf.set_font(font, style, size)
        pdf.set_text_color(*color)
        pdf.set_x(lm + indent)
        pdf.multi_cell(0, 5, _safe(text),
                       new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def section(title):
        pdf.ln(2)
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(0, 112, 173)
        pdf.set_x(lm)
        pdf.cell(0, 8, _safe(title),
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_draw_color(0, 112, 173)
        y = pdf.get_y()
        pdf.line(lm, y, lm + 180, y)
        pdf.ln(3)

    def field(label, value):
        write_line(label + " :", style="B", size=9, color=(100, 100, 100))
        write_line(value, size=9, color=(30, 30, 30), indent=4)
        pdf.ln(1)

    # Title
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(0, 112, 173)
    pdf.set_x(lm)
    pdf.cell(0, 10, _safe("Rapport d'incident NIS2 - AEGIS AI"),
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(2)

    # Subtitle
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(100, 100, 100)
    pdf.set_x(lm)
    pdf.multi_cell(
        0, 6,
        _safe(f"Ref : {sc['incident_ref']}  |  Classification : Critique  |  {sc['incident_date']}"),
        align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT,
    )
    pdf.ln(4)

    # Section 1 — Identification
    section("1. Identification")
    field("Entite", "Capgemini - Division Cyber Defense")
    field("Type d'incident", sc['incident_type'])
    field("Date de detection", sc['incident_date'])
    field("Duree totale", sc['incident_duration'])
    field("Impact metier", "Aucune interruption de service")

    # Section 2 — Patient zero
    section("2. Patient zero")
    field("Machine", sc['patient_zero_machine'])
    field("Compte compromis", sc['patient_zero_account'])
    field("Vecteur initial", sc['patient_zero_vector'])
    field("Cause racine", sc['patient_zero_cause'])

    # Section 3 — TTPs
    section("3. TTPs detectees (MITRE ATT&CK)")
    col_w = [30, 90, 55]
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(80, 80, 80)
    reset_x()
    pdf.cell(col_w[0], 7, "Code", border=1)
    pdf.cell(col_w[1], 7, "Technique", border=1)
    pdf.cell(col_w[2], 7, "Phase", border=1,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(30, 30, 30)
    for code, name, phase in sc["ttps"]:
        reset_x()
        pdf.cell(col_w[0], 6, _safe(code), border=1)
        pdf.cell(col_w[1], 6, _safe(name), border=1)
        pdf.cell(col_w[2], 6, _safe(phase), border=1,
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)

    # Section 4 — AEGIS actions
    section("4. Actions AEGIS automatiques")
    for action in sc["aegis_actions"]:
        write_line(f"[OK] {action}", size=9, color=(30, 30, 30))

    # Section 5 — Recommendations
    section("5. Recommandations de remediation")
    write_line("Firewall (Priorite : Critique)", style="B", size=9,
               color=(50, 50, 50))
    for rule in sc["fw_rules"]:
        write_line(rule, font="Courier", size=8, color=(40, 40, 40), indent=4)
    pdf.ln(2)
    write_line("IAM / Active Directory (Priorite : Critique)", style="B",
               size=9, color=(50, 50, 50))
    for rec in sc["iam_recs"]:
        write_line(f"- {rec}", size=9, color=(30, 30, 30), indent=4)
    pdf.ln(2)
    write_line("Monitoring (Priorite : Haute)", style="B", size=9,
               color=(50, 50, 50))
    for rec in sc["monitoring_recs"]:
        write_line(f"- {rec}", size=9, color=(30, 30, 30), indent=4)
    pdf.ln(6)

    # Footer
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(120, 120, 120)
    reset_x()
    pdf.multi_cell(
        0, 6,
        "AEGIS AI - Rapport genere automatiquement | Conforme NIS2 Art. 23 | Capgemini Cyber Defense 2026",
        align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT,
    )

    return bytes(pdf.output())


# ---------------------------------------------------------------------------
# ECS Ingestion feed helpers
# ---------------------------------------------------------------------------

_SEVERITY_STYLES = {
    SEVERITY_CRITICAL: (CORAL,    "rgba(248,113,113,0.08)", "rgba(248,113,113,0.3)"),
    SEVERITY_HIGH:     (AMBER,    "rgba(251,191,36,0.08)",  "rgba(251,191,36,0.3)"),
    SEVERITY_MEDIUM:   ("#FCD34D","rgba(252,211,77,0.06)",  "rgba(252,211,77,0.25)"),
    SEVERITY_LOW:      (MINT,     "rgba(52,211,153,0.06)",  "rgba(52,211,153,0.25)"),
    SEVERITY_INFO:     (SLATE_400,"rgba(148,163,184,0.05)", "rgba(148,163,184,0.15)"),
}

_SOURCE_COLORS = {
    SRC_FIREWALL: "#F97316",  # orange
    SRC_AD:       CAPGEMINI_BLUE,
    SRC_EDR:      MINT,
    SRC_CLOUD:    "#A78BFA",  # violet
}


def _ecs_field_badge(label, value):
    """Render a small ECS field pill."""
    if value is None:
        return ""
    return (
        f'<span class="ecs-field">'
        f'<span class="ecs-key">{label}</span>'
        f'<span class="ecs-val">{value}</span>'
        f'</span>'
    )


def build_ingestion_feed_html(scenario_idx=0, filter_source=None):
    """Return HTML for the multi-source ECS ingestion feed panel.

    Parameters
    ----------
    scenario_idx : int
        Index into ECS_LOGS_BY_SCENARIO.
    filter_source : str or None
        If set, only logs with matching source_type are shown.
    """
    logs = ECS_LOGS_BY_SCENARIO[scenario_idx]
    if filter_source:
        logs = [l for l in logs if l["source_type"] == filter_source]

    rows = ""
    for log in logs:
        sev = log.get("_severity", SEVERITY_INFO)
        text_col, bg_col, border_col = _SEVERITY_STYLES.get(
            sev, _SEVERITY_STYLES[SEVERITY_INFO]
        )
        src = log["source_type"]
        src_color = _SOURCE_COLORS.get(src, SLATE_400)
        meta = SOURCE_META.get(src, {})
        icon = meta.get("icon", "📄")

        # ECS pills — show the most relevant fields
        pills = ""
        for field, key in [
            ("source.ip",            "source.ip"),
            ("destination.ip",       "destination.ip"),
            ("network.protocol",     "network.protocol"),
            ("user.name",            "user.name"),
            ("host.hostname",        "host.hostname"),
            ("process.name",         "process.name"),
            ("cloud.service.name",   "cloud.service.name"),
            ("cloud.provider",       "cloud.provider"),
            ("winlog.event_id",      "winlog.event_id"),
            ("event.action",         "event.action"),
        ]:
            v = log.get(key)
            if v is not None:
                pills += _ecs_field_badge(field, v)

        rows += f"""
<div class="ecs-log-row" style="border-left:3px solid {border_col};
     background:{bg_col};">
  <div class="ecs-row-header">
    <span class="ecs-source-badge" style="color:{src_color};">
      {icon} {src}
    </span>
    <span class="ecs-timestamp">{log.get('@timestamp','')}</span>
    <span class="ecs-severity" style="color:{text_col};">{sev.upper()}</span>
    <span class="ecs-level">{log.get('log.level','')}</span>
  </div>
  <div class="ecs-message">{log['message']}</div>
  <div class="ecs-pills">{pills}</div>
</div>"""

    if not rows:
        rows = f'<div style="color:{SLATE_400}; padding:1rem; text-align:center;">Aucun événement pour cette source.</div>'

    return f'<div class="ecs-feed">{rows}</div>'


def build_source_stats_html(scenario_idx=0):
    """Return HTML for per-source event-count summary cards."""
    logs = ECS_LOGS_BY_SCENARIO[scenario_idx]
    cards = ""
    for src in [SRC_FIREWALL, SRC_AD, SRC_EDR, SRC_CLOUD]:
        src_logs = [l for l in logs if l["source_type"] == src]
        meta = SOURCE_META[src]
        icon = meta["icon"]
        label = meta["label"]
        description = meta["description"]
        src_color = _SOURCE_COLORS[src]
        count = len(src_logs)
        crit = sum(1 for l in src_logs if l["_severity"] == SEVERITY_CRITICAL)
        high = sum(1 for l in src_logs if l["_severity"] == SEVERITY_HIGH)

        alert_txt = ""
        if crit:
            alert_txt += (
                f'<span class="src-stat-pill" style="color:{CORAL};">'
                f'{crit} CRITICAL</span>'
            )
        if high:
            alert_txt += (
                f'<span class="src-stat-pill" style="color:{AMBER};">'
                f'{high} HIGH</span>'
            )
        if not crit and not high:
            alert_txt = (
                f'<span class="src-stat-pill" style="color:{MINT};">Normal</span>'
            )

        cards += f"""
<div class="src-stat-card" style="border-top:3px solid {src_color};">
  <div class="src-stat-icon">{icon}</div>
  <div class="src-stat-label" style="color:{src_color};">{label}</div>
  <div class="src-stat-desc">{description}</div>
  <div class="src-stat-count">{count} événements</div>
  <div class="src-stat-alerts">{alert_txt}</div>
</div>"""

    return f'<div class="src-stats-row">{cards}</div>'
