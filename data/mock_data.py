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
