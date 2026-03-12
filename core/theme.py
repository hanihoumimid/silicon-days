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


def inject_custom_css():
    """Inject the full CSS theme into the Streamlit app."""
    import streamlit as st

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

    /* Ingestion source badges */
    .source-badge {{
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.2rem 0.65rem;
        border-radius: 12px;
        font-size: 0.72rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        letter-spacing: 0.3px;
    }}
    .source-firewall {{
        background: rgba(248,113,113,0.12);
        color: {CORAL};
        border: 1px solid rgba(248,113,113,0.3);
    }}
    .source-ad {{
        background: rgba(0,112,173,0.12);
        color: {CAPGEMINI_BLUE};
        border: 1px solid rgba(0,112,173,0.3);
    }}
    .source-edr {{
        background: rgba(251,191,36,0.12);
        color: {AMBER};
        border: 1px solid rgba(251,191,36,0.3);
    }}
    .source-cloud {{
        background: rgba(52,211,153,0.12);
        color: {MINT};
        border: 1px solid rgba(52,211,153,0.3);
    }}

    /* Log level pill */
    .loglevel-info {{
        color: {SLATE_400};
        background: rgba(148,163,184,0.1);
        border: 1px solid rgba(148,163,184,0.2);
        padding: 0.1rem 0.45rem;
        border-radius: 4px;
        font-size: 0.68rem;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
    }}
    .loglevel-warning {{
        color: {AMBER};
        background: rgba(251,191,36,0.1);
        border: 1px solid rgba(251,191,36,0.25);
        padding: 0.1rem 0.45rem;
        border-radius: 4px;
        font-size: 0.68rem;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
    }}
    .loglevel-critical {{
        color: {CORAL};
        background: rgba(248,113,113,0.1);
        border: 1px solid rgba(248,113,113,0.25);
        padding: 0.1rem 0.45rem;
        border-radius: 4px;
        font-size: 0.68rem;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
    }}

    /* ECS event card */
    .ecs-event {{
        background: {CARD_BG};
        border: 1px solid rgba(148,163,184,0.1);
        border-radius: 8px;
        padding: 0.9rem 1.1rem;
        margin-bottom: 0.6rem;
        animation: fadeInUp 0.3s ease-out both;
    }}
    .ecs-event.ecs-alert {{
        border-left: 3px solid {CORAL};
    }}
    .ecs-event.ecs-event-kind {{
        border-left: 3px solid {CAPGEMINI_BLUE};
    }}
    .ecs-event-header {{
        display: flex;
        align-items: center;
        gap: 0.6rem;
        margin-bottom: 0.5rem;
        flex-wrap: wrap;
    }}
    .ecs-timestamp {{
        color: {SLATE_400};
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
    }}
    .ecs-message {{
        color: {SLATE_300};
        font-family: 'Inter', sans-serif;
        font-size: 0.82rem;
        margin-top: 0.2rem;
    }}
    .ecs-field-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
        gap: 0.3rem 1rem;
        margin-top: 0.5rem;
    }}
    .ecs-field {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: {SLATE_400};
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }}
    .ecs-field .ecs-key {{
        color: {CAPGEMINI_BLUE};
    }}
    .ecs-field .ecs-val {{
        color: {SLATE_300};
    }}

    /* Ingestion pipeline header */
    .ingestion-header {{
        background: linear-gradient(135deg, {SLATE_700}, {CARD_BG});
        border: 1px solid rgba(0,112,173,0.15);
        border-radius: 8px;
        padding: 0.8rem 1.2rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.8rem;
    }}
    .ingestion-header .source-name {{
        color: {WHITE};
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 0.95rem;
    }}
    .ingestion-header .source-vendor {{
        color: {SLATE_400};
        font-family: 'Inter', sans-serif;
        font-size: 0.78rem;
    }}
    .ingestion-header .source-desc {{
        color: {SLATE_400};
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
    }}

    /* Raw log block */
    .raw-log {{
        background: {SLATE_700};
        border: 1px solid rgba(148,163,184,0.12);
        border-radius: 6px;
        padding: 0.8rem 1rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: {SLATE_300};
        line-height: 1.7;
        overflow-x: auto;
    }}
    .raw-log .rk {{ color: {GOLD}; }}
    .raw-log .rv {{ color: {SLATE_300}; }}

    /* Pipeline arrow */
    .pipeline-arrow {{
        text-align: center;
        font-size: 1.2rem;
        color: {CAPGEMINI_BLUE};
        padding: 0.2rem 0;
        font-family: 'Inter', sans-serif;
    }}

    /* Stats pill row */
    .stats-row {{
        display: flex;
        gap: 0.8rem;
        flex-wrap: wrap;
        margin-bottom: 1rem;
    }}
    .stat-pill {{
        background: {CARD_BG};
        border: 1px solid rgba(148,163,184,0.1);
        border-radius: 8px;
        padding: 0.5rem 0.9rem;
        font-family: 'Inter', sans-serif;
    }}
    .stat-pill .sp-label {{
        color: {SLATE_400};
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 0.4px;
    }}
    .stat-pill .sp-value {{
        color: {WHITE};
        font-family: 'JetBrains Mono', monospace;
        font-size: 1rem;
        font-weight: 600;
    }}
</style>
""", unsafe_allow_html=True)
