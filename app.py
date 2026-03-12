"""
AEGIS AI — Système de Défense Active Cognitive
Hackathon Silicondays 2026 — Capgemini
Prototype de démonstration interactive
"""

import time
from datetime import datetime

import streamlit as st

from core.theme import (
    AMBER, CAPGEMINI_BLUE, CARD_BG, CORAL, GOLD, MINT, SLATE_300, SLATE_400,
    SLATE_600, SLATE_700, SLATE_800, WHITE, inject_custom_css,
)
from core.state import init_session_state
from data.mock_data import ATTACK_SCENARIOS, TERMINAL_SEQUENCES
from ui.charts import (
    build_mitre_attack_matrix,
    build_confidence_budget_attack, build_confidence_budget_chart,
    build_network_figure, build_risk_gauge,
)
from ui.components import (
    build_attack_timeline, generate_nis2_pdf, get_nis2_report_html,
    get_terminal_html, build_ingestion_feed_html, build_source_stats_html,
)
from data.ecs_logs import SOURCE_META, SRC_FIREWALL, SRC_AD, SRC_EDR, SRC_CLOUD

# ---------------------------------------------------------------------------
# Page config — MUST be the first Streamlit command
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="AEGIS AI — Capgemini Cyber Defense",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Initialisation
# ---------------------------------------------------------------------------
init_session_state()
inject_custom_css()

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
tab_avant, tab_pendant, tab_apres, tab_ingestion = st.tabs([
    "Avant — Sentinel & Baseline",
    "Pendant — Riposte Active & Mirage",
    "Après — Forensics & Rapport NIS2",
    "Ingestion & ECS",
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
        uid = f"{phase}_{int(time.time() * 1000)}"
        sidx = st.session_state.selected_scenario

        net_color = AMBER if phase >= 1 else MINT
        net_text = ("Mouvement détecté — IA en réponse" if phase >= 1
                    else "Surveillance")
        net_label_ph.markdown(
            f"**Topologie réseau** &mdash; "
            f"<span style='color:{net_color};'>{net_text}</span>",
            unsafe_allow_html=True,
        )

        net_chart_ph.plotly_chart(
            build_network_figure(True, phase, sidx), width="stretch",
            key=f"net_chart_{uid}"
        )

        gauge_label_ph.markdown("**Score de risque global** $R_s$")

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

            behav_chart_ph.plotly_chart(
                build_confidence_budget_attack(sidx), width="stretch",
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
        sidx = st.session_state.selected_scenario
        terminal_seq = TERMINAL_SEQUENCES[sidx]
        total_steps = 3 + len(terminal_seq)

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

        for i, line in enumerate(terminal_seq):
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
        sidx = st.session_state.selected_scenario
        sc = ATTACK_SCENARIOS[sidx]
        events = build_attack_timeline(sidx)
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

        st.markdown("**Matrice MITRE ATT&CK interactive**")
        st.caption(
            "Cliquez et zoomez sur la matrice pour explorer les correspondances "
            "entre les 5 TTPs détectées et les tactiques ATT&CK."
        )
        st.plotly_chart(
            build_mitre_attack_matrix(sidx),
            width="stretch",
            key=f"mitre_matrix_{sc['incident_ref']}",
        )

        st.markdown("---")

        if st.button("Générer le rapport NIS2", type="primary",
                      width="stretch", key="nis2_btn"):
            st.session_state.nis2_generated = True
            st.rerun()

        if st.session_state.nis2_generated:
            st.markdown(get_nis2_report_html(sidx), unsafe_allow_html=True)

            # Build plain-text report from scenario data
            ttps_lines = "\n".join(
                f"- {code:12s}: {name} ({phase})"
                for code, name, phase in sc["ttps"]
            )
            aegis_lines = "\n".join(f"[OK] {a}" for a in sc["aegis_actions"])
            fw_lines = "\n  ".join(sc["fw_rules"])
            iam_lines = "\n  - ".join(sc["iam_recs"])
            mon_lines = "\n  - ".join(sc["monitoring_recs"])
            report_text = f"""RAPPORT D'INCIDENT NIS2 — AEGIS AI
========================================
Référence : {sc['incident_ref']}
Classification : Critique
Date : {sc['incident_date']}

1. IDENTIFICATION
Entité : Capgemini — Division Cyber Défense
Type : {sc['incident_type']}
Durée : {sc['incident_duration']}
Impact métier : Aucune interruption de service

2. PATIENT ZÉRO
Machine : {sc['patient_zero_machine']}
Compte : {sc['patient_zero_account']}
Vecteur : {sc['patient_zero_vector']}
Cause : {sc['patient_zero_cause']}

3. TTPs (MITRE ATT&CK)
{ttps_lines}

4. ACTIONS AEGIS
{aegis_lines}

5. RECOMMANDATIONS
Firewall (Critique) :
  {fw_lines}

IAM (Critique) :
  - {iam_lines}

Monitoring (Haute) :
  - {mon_lines}

========================================
AEGIS AI — Conforme NIS2 Art. 23
Capgemini Cyber Défense 2026
"""
            col_dl1, col_dl2 = st.columns(2)
            with col_dl1:
                st.download_button(
                    label="Télécharger le rapport (TXT)",
                    data=report_text,
                    file_name=f"AEGIS_NIS2_{sc['incident_ref']}.txt",
                    mime="text/plain",
                    width="stretch",
                )
            with col_dl2:
                pdf_bytes = generate_nis2_pdf(sidx)
                st.download_button(
                    label="Télécharger le rapport (PDF)",
                    data=pdf_bytes,
                    file_name=f"AEGIS_NIS2_{sc['incident_ref']}.pdf",
                    mime="application/pdf",
                    width="stretch",
                )


# ===== TAB 4 : INGESTION & ECS =====
with tab_ingestion:
    st.markdown(
        '<span class="phase-badge phase-avant">Ingestion Multi-Sources — ECS</span>',
        unsafe_allow_html=True,
    )
    st.markdown("""
    > **Ingestion multi-sources** : AEGIS collecte en temps réel les événements
    > de sécurité provenant de quatre types de capteurs —
    > **Firewall**, **Active Directory**, **EDR** et **Cloud** —
    > et les normalise automatiquement selon l'**Elastic Common Schema (ECS)**
    > avant corrélation et analyse.
    """)

    # ---- Scenario selector ----
    scenario_names = [s["name"] for s in ATTACK_SCENARIOS]
    col_sel_ecs, col_info_ecs = st.columns([1, 2])
    with col_sel_ecs:
        chosen_ecs = st.selectbox(
            "Scénario d'ingestion",
            scenario_names,
            index=st.session_state.selected_scenario,
            key="ecs_scenario_select",
        )
        ecs_sidx = scenario_names.index(chosen_ecs)

    with col_info_ecs:
        sc_ecs = ATTACK_SCENARIOS[ecs_sidx]
        st.markdown(f"""
        <div class="scenario-selector">
            <div class="label">Contexte du scénario</div>
            <div style="color:{SLATE_300}; font-family:'Inter',sans-serif;
                        font-size:0.85rem; margin-bottom:0.4rem;">
                {sc_ecs['desc']}
            </div>
            <div style="display:flex; gap:1.5rem; flex-wrap:wrap;">
                <span style="color:{SLATE_400}; font-size:0.78rem;">
                    Vecteur : <b style="color:{WHITE};">{sc_ecs['vector']}</b>
                </span>
                <span style="color:{SLATE_400}; font-size:0.78rem;">
                    Sévérité : <b style="color:{CORAL};">{sc_ecs['severity']}</b>
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ---- Source summary cards ----
    st.markdown("**Sources actives — Vue d'ensemble**")
    st.markdown(build_source_stats_html(ecs_sidx), unsafe_allow_html=True)

    st.markdown("---")

    # ---- ECS schema reference ----
    with st.expander("📋 Référence ECS (Elastic Common Schema) — champs utilisés", expanded=False):
        col_ecs1, col_ecs2 = st.columns(2)
        with col_ecs1:
            st.markdown(f"""
<div class="ecs-schema-box">
<b style="color:{CAPGEMINI_BLUE};">Champs communs</b><br>
<span class="ecs-field-name">@timestamp</span>
  <span class="ecs-field-type">date</span>
  <span class="ecs-field-desc">— Horodatage ISO 8601</span><br>
<span class="ecs-field-name">event.kind</span>
  <span class="ecs-field-type">keyword</span>
  <span class="ecs-field-desc">— event · alert · metric</span><br>
<span class="ecs-field-name">event.category</span>
  <span class="ecs-field-type">keyword[]</span>
  <span class="ecs-field-desc">— authentication · network · process · file · iam</span><br>
<span class="ecs-field-name">event.type</span>
  <span class="ecs-field-type">keyword[]</span>
  <span class="ecs-field-desc">— allowed · denied · start · end · access · admin</span><br>
<span class="ecs-field-name">event.action</span>
  <span class="ecs-field-type">keyword</span>
  <span class="ecs-field-desc">— Action déclenchante (ex. firewall-deny)</span><br>
<span class="ecs-field-name">event.outcome</span>
  <span class="ecs-field-type">keyword</span>
  <span class="ecs-field-desc">— success · failure · unknown</span><br>
<span class="ecs-field-name">log.level</span>
  <span class="ecs-field-type">keyword</span>
  <span class="ecs-field-desc">— info · warning · error · critical</span><br>
<span class="ecs-field-name">message</span>
  <span class="ecs-field-type">text</span>
  <span class="ecs-field-desc">— Description lisible de l'événement</span>
</div>
            """, unsafe_allow_html=True)
        with col_ecs2:
            st.markdown(f"""
<div class="ecs-schema-box">
<b style="color:{CAPGEMINI_BLUE};">Champs par source</b><br>
<span class="ecs-field-name">source.ip / destination.ip</span>
  <span class="ecs-field-type">ip</span>
  <span class="ecs-field-desc">— Firewall, EDR</span><br>
<span class="ecs-field-name">network.protocol / .direction</span>
  <span class="ecs-field-type">keyword</span>
  <span class="ecs-field-desc">— Firewall</span><br>
<span class="ecs-field-name">observer.type / .name</span>
  <span class="ecs-field-type">keyword</span>
  <span class="ecs-field-desc">— Firewall (firewall · ids)</span><br>
<span class="ecs-field-name">user.name / user.domain</span>
  <span class="ecs-field-type">keyword</span>
  <span class="ecs-field-desc">— AD, EDR, Cloud</span><br>
<span class="ecs-field-name">winlog.event_id / .logon.type</span>
  <span class="ecs-field-type">long / keyword</span>
  <span class="ecs-field-desc">— Active Directory</span><br>
<span class="ecs-field-name">process.name / .pid / .command_line</span>
  <span class="ecs-field-type">keyword / long</span>
  <span class="ecs-field-desc">— EDR</span><br>
<span class="ecs-field-name">cloud.provider / .region / .service.name</span>
  <span class="ecs-field-type">keyword</span>
  <span class="ecs-field-desc">— Cloud (aws · azure · gcp)</span><br>
<span class="ecs-field-name">file.path / file.name / file.size</span>
  <span class="ecs-field-type">keyword / long</span>
  <span class="ecs-field-desc">— EDR, AD</span>
</div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ---- Source filter tabs ----
    st.markdown("**Flux d'événements ECS normalisés**")
    src_all, src_fw, src_ad, src_edr, src_cloud = st.tabs([
        "Toutes les sources",
        f"🔥 {SRC_FIREWALL}",
        f"🗄️ {SRC_AD}",
        f"🛡️ {SRC_EDR}",
        f"☁️ {SRC_CLOUD}",
    ])

    with src_all:
        st.caption(
            "Tous les événements ingérés, triés par timestamp, "
            "normalisés selon ECS."
        )
        st.markdown(
            build_ingestion_feed_html(ecs_sidx),
            unsafe_allow_html=True,
        )

    with src_fw:
        meta_fw = SOURCE_META[SRC_FIREWALL]
        st.caption(meta_fw["description"])
        st.markdown(
            build_ingestion_feed_html(ecs_sidx, filter_source=SRC_FIREWALL),
            unsafe_allow_html=True,
        )

    with src_ad:
        meta_ad = SOURCE_META[SRC_AD]
        st.caption(meta_ad["description"])
        st.markdown(
            build_ingestion_feed_html(ecs_sidx, filter_source=SRC_AD),
            unsafe_allow_html=True,
        )

    with src_edr:
        meta_edr = SOURCE_META[SRC_EDR]
        st.caption(meta_edr["description"])
        st.markdown(
            build_ingestion_feed_html(ecs_sidx, filter_source=SRC_EDR),
            unsafe_allow_html=True,
        )

    with src_cloud:
        meta_cloud = SOURCE_META[SRC_CLOUD]
        st.caption(meta_cloud["description"])
        st.markdown(
            build_ingestion_feed_html(ecs_sidx, filter_source=SRC_CLOUD),
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown(f"""
    <div class="nav-hint">
        <div class="icon">&#10145;</div>
        <div class="text">
            Les événements ECS sont corrélés par AEGIS AI dans l'onglet
            <span class="tab-name">Pendant — Riposte Active & Mirage</span>
            pour déclencher la réponse automatique.
        </div>
    </div>
    """, unsafe_allow_html=True)
