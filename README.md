# Silicon Days

Application Streamlit de démonstration pour le prototype AEGIS AI.

## Prérequis

- Python 3.10 ou plus recent
- `pip`

## Creer un environnement virtuel

Depuis la racine du projet, creez un venv :

```bash
python -m venv .venv
```

Activez-le ensuite selon votre environnement.

Sous Windows PowerShell :

```powershell
.venv\Scripts\Activate.ps1
```

Sous Windows CMD :

```bat
.venv\Scripts\activate.bat
```

Sous Linux, macOS ou WSL :

```bash
source .venv/bin/activate
```

## Installer les dependances

Une fois le venv active, installez les dependances du projet :

```bash
pip install -r requirements.txt
```

## Lancer l'application avec Streamlit

Depuis la racine du projet :

```bash
streamlit run app.py
```

Streamlit affichera ensuite une URL locale, en general :

```text
http://localhost:8501
```
