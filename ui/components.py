from datetime import datetime, timedelta

from core.theme import (
    CAPGEMINI_BLUE, CORAL, MINT, SLATE_300, SLATE_400, SLATE_600, SLATE_700,
    WHITE,
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
