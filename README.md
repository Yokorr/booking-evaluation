# Booking Evaluation — Django Templates, ORM, DRF et JSON

Évaluation individuelle de développement backend, inspirée des notions M4 à M7 de DeskHive, mais indépendante du dépôt DeskHive.

**Durée indicative : 75 à 90 minutes. Barème : /20.** Le projet contient déjà le schéma SQLite, les migrations, les données de démonstration, les routes et les tests. Vous ne devez pas créer de nouveau projet Django.

## Objectifs et règles

- Compléter les quatre TODO dans les **quatre fichiers autorisés seulement** : `rooms/templates/rooms/catalogue.html`, `rooms/serializers.py`, `rooms/views.py` et `rooms/reports.py`.
- Ne pas modifier `rooms/tests.py`, `check.py`, `rooms/models.py`, les migrations, `booking_eval/settings.py`, ni les URLs.
- Ne pas coder les résultats en dur : utiliser les enregistrements ORM réellement fournis.
- Ne pas installer d'autres dépendances : Django et DRF suffisent.
- Le projet est volontairement **en lecture seule** : aucune création/modification/suppression de salle n'est demandée.
- Le rendu HTML du catalogue et le format JSON attendu est défini précisément ci-dessous. Les tests vérifient le comportement, pas la mise en forme du code.
- La remise consiste en un lien vers votre dépôt GitHub personnel et son commit final, selon la consigne du formateur.

## Pré-requis

- Git.
- Python **3.11 à 3.13**, conseillé : **3.12**.
- Connexion Internet pour installer les dépendances au premier lancement.
- Windows : PowerShell ; macOS : Terminal.
- Aucun compte cloud, émulateur ou serveur extérieur n'est nécessaire.

## 1. Récupérer le projet

Sur GitHub, créez votre propre fork du dépôt starter indiqué par le formateur, puis clonez **votre fork** (et non la solution). Remplacez `<VOTRE_COMPTE>` par votre compte GitHub et `<NOM_DU_REPO>` par le nom du dépôt publié :

```bash
git clone https://github.com/<VOTRE_COMPTE>/<NOM_DU_REPO>.git
cd <NOM_DU_REPO>
```

Si vous avez déjà cloné votre fork, ouvrez simplement son dossier et vérifiez `git status` avant de travailler. Ne supprimez pas vos changements existants.

## 2. Installation sous Windows (PowerShell)

Dans le dossier qui contient `manage.py` et `check.py` :

```powershell
# Vérifier Python
py -3.12 --version

# Environnement virtuel
py -3.12 -m venv .venv

# Installer les dépendances en utilisant le Python du venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# Créer la base de données ET charger les données de test
.\.venv\Scripts\python.exe manage.py migrate

# Vérification des fichiers et de la base
.\.venv\Scripts\python.exe manage.py check

# Lancer tous les tests (ils échouent initialement : TODO)
.\.venv\Scripts\python.exe check.py
```

Si `py -3.12` n'est pas disponible mais que `python --version` indique Python 3.11 à 3.13, utiliser `python -m venv .venv` à la place. L'activation (`Activate.ps1`) est **facultative** puisque les commandes utilisent directement le bon interpréteur. Pas besoin de modifier la politique d'exécution PowerShell.

## 3. Installation sous macOS (Terminal)

```bash
# Vérifier la version
python3 --version

# Si python3 pointe vers Python 3.11 à 3.13
python3 -m venv .venv

# Installer les dépendances
./.venv/bin/python -m pip install -r requirements.txt

# Créer la base et charger le catalogue
./.venv/bin/python manage.py migrate

# Vérifier la configuration
./.venv/bin/python manage.py check

# Lancer les tests (échecs attendus avant les TODO)
./.venv/bin/python check.py
```

Si `python3` n'est pas dans cette plage, installer Python 3.12 puis appeler explicitement `python3.12 -m venv .venv`. Xcode et l'émulateur iOS ne sont pas nécessaires pour cette évaluation backend.

## 4. Données de démonstration déjà installées

Les migrations créent automatiquement :

| Ville | Code salle | Nom | Capacité |
|---|---|---|---:|
| Lyon | `lyo-desk` | Open desk | 4 |
| Lyon | `lyo-room` | Meeting room | 6 |
| Paris | `par-desk` | Focus desk | 2 |
| Paris | `par-room` | Boardroom | 10 |
| Nantes | `nan-room` | Workshop room | 8 |

`Room` possède une relation `location` vers `Location`. Pour consulter ces modèles, voir `rooms/models.py` (lecture seulement).

## 5. TODO 0 — Template Django (M4 : 4 points)

**Fichier à modifier : `rooms/templates/rooms/catalogue.html`.**

Compléter le bloc TODO du template avec le langage de templates Django (DTL) :

- Utiliser la variable `rooms` transmise par la vue **déjà fournie** dans `rooms/web_views.py`.
- Afficher dynamiquement chaque salle : `code`, `name`, `capacity` et `location.city`.
- Pour chaque salle, afficher également la capacité au format `4 seats` (le nombre varie selon la salle).
- Si la liste est vide, afficher exactement `No rooms available.`.
- Utiliser `{% for %}` et `{% empty %}` ; les variables doivent être affichées via `{{ ... }}` pour bénéficier de l'échappement HTML Django.
- Ne modifier ni la vue HTML, ni les modèles, ni les routes. Ne pas écrire les données des cinq salles en dur.

Le catalogue HTML est disponible à **`GET /rooms/`** après `manage.py migrate` et `runserver`.

### Test ciblé

Windows :
```powershell
.\.venv\Scripts\python.exe check.py --todo0
```
macOS :
```bash
./.venv/bin/python check.py --todo0
```

## 6. TODO 1 — Serializer DRF (M6 : 5 points)

**Fichier à modifier : `rooms/serializers.py`.**

Compléter `RoomSerializer(serializers.ModelSerializer)` pour exposer exactement **quatre champs en lecture seule** :

- `code` (chaîne)
- `name` (chaîne)
- `capacity` (entier)
- `location_city` (chaîne correspondant à `location.city`)

Les objets doivent provenir du modèle `Room` existant. Ne pas créer de nouvelles tables. Un tableau d'objets doit pouvoir être sérialisé avec `many=True`.

### Test ciblé

Windows :
```powershell
.\.venv\Scripts\python.exe check.py --todo1
```
macOS :
```bash
./.venv/bin/python check.py --todo1
```

## 7. TODO 2 — Endpoint REST (M5/M6 : 6 points)

**Fichier à modifier : `rooms/views.py`.**

Compléter `RoomListView` pour exposer `GET /api/rooms/` :

- Sans paramètre, retourner toutes les salles triées par `code`.
- Avec `?city=Lyon`, retourner uniquement les salles de cette ville (comparaison insensible à la casse, et ignorer les espaces autour du paramètre).
- Avec `?city=Rennes`, retourner un tableau JSON vide et un statut **200**.
- Avec `?city=` ou une valeur constituée uniquement d'espaces, retourner **400**.
- `POST /api/rooms/` n'est pas autorisé : **405**.
- Éviter des requêtes répétées pour les données de localisation.

### Test ciblé

Windows :
```powershell
.\.venv\Scripts\python.exe check.py --todo2
```
macOS :
```bash
./.venv/bin/python check.py --todo2
```

## 8. TODO 3 — Rapport JSON (M5/M7 : 5 points)

**Fichier à modifier : `rooms/reports.py`.**

Compléter la fonction `export_city_summary(city) -> str` :

- `city` doit être une chaîne non vide après suppression des espaces en début/fin ; sinon lever `ValueError`.
- Comparaison de ville insensible à la casse, avec suppression des espaces autour du nom.
- Une ville connue doit être restituée avec son orthographe enregistrée dans la base (`Lyon` et non `lyon`).
- Une ville inconnue doit produire un rapport vide avec le nom demandé nettoyé.
- Les codes doivent être triés par ordre alphabétique.
- Calculer réellement le nombre de salles et la somme de leurs capacités depuis l'ORM.
- Retourner **une chaîne JSON valide** via `json.dumps()`, pas un dictionnaire Python.
- Ne faire aucune écriture en base.

### Exemple de sortie attendue pour Lyon

```json
{
  "city": "Lyon",
  "total_rooms": 2,
  "total_capacity": 10,
  "room_codes": ["lyo-desk", "lyo-room"]
}
```

Pour `Rennes` (ville absente), les nombres doivent valoir `0` et `room_codes` doit être `[]`.

### Test ciblé

Windows :
```powershell
.\.venv\Scripts\python.exe check.py --todo3
```
macOS :
```bash
./.venv/bin/python check.py --todo3
```

## 9. Vérification finale

Windows :
```powershell
.\.venv\Scripts\python.exe check.py
```
macOS :
```bash
./.venv/bin/python check.py
```

Les **16 tests** doivent réussir après implémentation (4 TODO et vérifications transversales). Avant réalisation, plusieurs tests échouent volontairement : c'est attendu.

## 10. Tester les pages dans le navigateur (facultatif)

Windows :
```powershell
.\.venv\Scripts\python.exe manage.py runserver 8001
```
macOS :
```bash
./.venv/bin/python manage.py runserver 8001
```

Ouvrir `http://127.0.0.1:8001/rooms/` (HTML), puis `http://127.0.0.1:8001/api/rooms/` et `http://127.0.0.1:8001/api/rooms/?city=Lyon`. Arrêter avec `Ctrl+C`.

## 11. Enregistrer et rendre le travail

```bash
git status
git add rooms/templates/rooms/catalogue.html rooms/serializers.py rooms/views.py rooms/reports.py
git commit -m "Complete booking evaluation TODOs"
git push origin HEAD
```

Communiquer le lien de votre dépôt/fork au formateur, ainsi que le hash du dernier commit (`git log -1 --oneline`). Il n'est pas nécessaire de joindre `.venv` ou `db.sqlite3` : ils sont exclus par `.gitignore`.

## En cas de problème

- `ModuleNotFoundError: django` : vérifier l'installation avec le Python de `.venv`.
- `no such table: rooms_room` : relancer `manage.py migrate`.
- `python3` absent : vérifier l'installation Python ; sur macOS, un Python 3.12 installé séparément peut s'appeler `python3.12`.
- Les tests échouent au départ : normal, tant que les TODO ne sont pas complétés.
- Ne pas modifier les tests pour obtenir un résultat artificiellement vert.


## Récapitulatif du barème

| Compétence | Fichier modifié | Note |
|---|---|---:|
| M4 : affichage HTML avec DTL, boucle, cas vide et échappement | `rooms/templates/rooms/catalogue.html` | 4 |
| M6 : sérialisation du modèle Django | `rooms/serializers.py` | 5 |
| M5/M6 : lecture ORM et API REST avec filtrage | `rooms/views.py` | 6 |
| M5/M7 : agrégation ORM et export JSON | `rooms/reports.py` | 5 |
| **Total** | **4 fichiers** | **20** |

Les tests mesurent les comportements attendus ; le barème reste attribué par le formateur et n'est pas nécessairement un point par test.
