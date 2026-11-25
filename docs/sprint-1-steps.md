# Pododiab — Sprint 1 Step-by-Step Guide

**Sprint:** 1 — Foundation  
**Actual dates:** 7–28 November 2026 (with the midterm pause)  
**Sprint ends:** Saturday 28 November 2026  
**Team:** 5 beginners  
**Stack:** Python 3.12 + Django 5.2 + PostgreSQL 16 (Docker) + Git/GitHub

> **Purpose of this document:** explain exactly how we build the Sprint 1 foundation, who owns what, how we push code without blocking each other, and how we prove the sprint is done.

---

## 1. Sprint goal

> **Build the technical foundation of Pododiab:** a clean GitHub repository, a runnable Django 5.2 project on Python 3.12, a Dockerized PostgreSQL 16 database, the complete v1 database schema, repeatable seed data, model tests, and a green CI pipeline.

This sprint is a **foundation sprint**, not a feature sprint. We are not building login, dashboards, patient screens, or the visual shell yet. Those come in Sprint 2.

### In scope

- New GitHub repository and team access.
- Branch protection and pull-request workflow.
- Django project skeleton with separate apps.
- Python 3.12 virtual environment and pinned dependencies.
- PostgreSQL 16 running in Docker.
- All 8 v1 domain tables, created through Django migrations.
- Django admin registration for inspection.
- A repeatable `seed_demo` command with fictional data.
- At least 5 model/schema tests.
- GitHub Actions CI.
- README with clean-clone setup instructions.

### Out of scope for this sprint

- Login and logout.
- Doctor/assistant dashboards.
- Design shell and navigation.
- Permission decorators and 403 pages.
- Patient search and patient forms.
- Consultation, document, payment and print screens.
- Production deployment on the clinic network.

### Definition of Done

- [ ] A clean clone can be set up by following the README.
- [ ] `docker compose up -d db` starts PostgreSQL and reports healthy.
- [ ] `python manage.py migrate` creates the schema from an empty database.
- [ ] The 8 domain tables exist.
- [ ] `python manage.py seed_demo` creates 2 users, 10 fictional patients and 1 consultation.
- [ ] Running `seed_demo` twice does not duplicate data.
- [ ] `pytest` passes.
- [ ] `ruff check .` passes.
- [ ] CI is green on a pull request.
- [ ] `main` is protected and changes are merged through reviewed PRs.
- [ ] No `.env`, old database, real patient data, or `__pycache__` is committed.
- [ ] The GitHub board is updated and the sprint is demoed at the review.

### Cut line if the week slips

Keep, in this order:

1. Repository and Django skeleton.
2. Docker PostgreSQL and connection.
3. `User`, `Patient`, `AuditLog` models and migrations.
4. `seed_demo`.
5. Tests and CI.

If Saturday is close and something must move, move `Payment` and `Attachment` to Sprint 2. Do not fake the demo. Record the cut in the retrospective.

---

## 2. Team roles and ownership

Sprint 1 has one unavoidable dependency: the Day-1 bootstrap. P1 creates the repository and Django skeleton first. After that, everyone works in parallel on separate files.

| Person | Hat | Sprint 1 responsibility | Owns exclusively |
|---|---|---|---|
| **P1** | Scrum Master / platform | Repository, Django project, settings, Docker PostgreSQL, custom `User` | `config/`, `compose.yaml`, `requirements/`, `.env.example`, `.gitignore`, `README.md`, `apps/accounts/models.py` |
| **P2** | Product Owner / frontend | Design assets, static/templates skeleton, design tokens | `static/`, `templates/`, `docs/design/` |
| **P3** | Backend / data | `Patient`, `MedicalEntry`, `Consultation`, `PrescriptionItem` models and admin | `apps/patients/`, `apps/medical/`, `apps/consultations/models.py`, `apps/consultations/admin.py` |
| **P4** | Backend / auth | `Payment`, `Attachment`, `AuditLog` models and admin | `apps/billing/`, `apps/documents/`, `apps/audit/` |
| **P5** | QA / DevOps | Migrations integration, `seed_demo`, tests, CI, clean-clone check | `apps/core/management/commands/`, `tests/`, `pyproject.toml`, `.github/workflows/` |

### No-collision rules

1. **One file or app has one owner.** If you need a change in someone else’s file, open an issue and ask the owner. Do not edit it yourself.
2. **`main` is protected.** Nobody pushes directly to `main`.
3. **Every PR is reviewed by a non-owner.**
4. **Contract first.** The model fields come from `docs/03-data-model.md`. Do not invent fields or rename them silently. If the contract changes, announce it in the daily Scrum.
5. **Generated migration files are committed.** Do not delete migrations to “fix” a problem.

---

## 3. How we push code (answer to “who pushes?”)

**Everyone pushes. Nobody pushes to `main` directly.**

The workflow is:

1. Each person creates a branch for their task.
2. They commit and push **their branch**.
3. They open a Pull Request (PR) into `main`.
4. A different person reviews it.
5. CI must be green.
6. The PR is squashed and merged.
7. The branch is deleted.

If you are the Scrum Master, you may be the person who clicks **Merge** after review. That does **not** mean you push other people’s code. Each author pushes their own branch.

### Branch names

Use the task ID:

```text
chore/S1-01-repo-bootstrap
feat/S1-02-django-skeleton
feat/S1-05-patient-model
test/S1-11-model-tests-ci
```

### Commit messages

Use short, clear messages in the imperative form:

```text
chore: initialize repository
feat: add Django project skeleton and app structure
feat(accounts): add custom User model with roles (S1-04)
feat(patients): add Patient model and admin (S1-05)
test: add audit log immutability tests (S1-11)
docs: add clean-clone setup instructions (S1-12)
```

### Daily Git commands

Start a task:

```bash
git switch main
git pull origin main
git switch -c feat/S1-05-patient-model
```

Save your work:

```bash
git status
git add apps/patients/models.py apps/patients/admin.py
git commit -m "feat(patients): add Patient model and admin (S1-05)"
git push -u origin feat/S1-05-patient-model
```

After the PR is merged:

```bash
git switch main
git pull origin main
git branch -d feat/S1-05-patient-model
```

### Pull request template

Create `.github/pull_request_template.md`:

```markdown
## What changed

## Why / related issue

Closes #<issue-number>

## How it was tested

- [ ] `python manage.py check`
- [ ] `python manage.py makemigrations --check --dry-run`
- [ ] `pytest`
- [ ] `ruff check .`

## Checklist

- [ ] Migrations are included
- [ ] No `.env`, secrets, database files or `__pycache__`
- [ ] No real patient data
- [ ] README/docs updated if setup changed
```

### Rules that prevent conflicts

- Pull `main` before starting a new branch.
- Keep PRs small.
- Do not edit files owned by someone else.
- Never commit `.env`.
- Never commit `db.sqlite3`, `__pycache__`, `.venv`, or `staticfiles/`.
- If you get a merge conflict, do not panic. Ask the owner of the file. Open the file, find `<<<<<<<`, choose the correct lines, then:

```bash
git add <file>
git commit
```

---

## 4. Before you start: prerequisites

Everyone needs:

- [ ] GitHub account with access to the new repository.
- [ ] Git installed.
- [ ] **Python 3.12** installed.
- [ ] **Docker Engine + Docker Compose v2** installed.
- [ ] SSH key added to GitHub, or an HTTPS personal access token.
- [ ] The project specification, especially `docs/03-data-model.md`.
- [ ] Their P-number and owned files from section 2.

### Ubuntu 24.04 setup

```bash
sudo apt update
sudo apt install -y python3.12-venv docker.io docker-compose-v2
sudo systemctl enable --now docker
sudo usermod -aG docker "$USER"
```

**Log out and log back in** after the `usermod` command.

Verify:

```bash
docker run hello-world
docker compose version
python3.12 --version
git --version
ssh -T git@github.com
```

If the SSH test fails, add the public key to GitHub:

```bash
cat ~/.ssh/id_ed25519.pub
```

GitHub → Settings → SSH and GPG keys → New SSH key.

### Windows setup

- Install **Python 3.12** from python.org. Do not use the Microsoft Store version.
- Install **Git for Windows**.
- Install **Docker Desktop** and enable the WSL2 backend.
- Use PowerShell:

```powershell
py -3.12 --version
docker --version
docker compose version
```

> **Important:** the Django app runs on the host. Only PostgreSQL runs in Docker. This keeps debugging simple.

### If a teammate cannot install Docker

They can still work on documentation, design assets, and templates. They cannot verify migrations or run the database tests until Docker works. Do not switch the project to SQLite just for one person; the schema must be tested on PostgreSQL.

---

## 5. Step 1 — Bootstrap the empty repository

### 5.1 Clone the empty repo

```bash
cd ~/projects
git clone <YOUR-EMPTY-REPO-URL> pododiab
cd pododiab
git switch -c main
```

If the repository already has a README commit, just clone it and continue on a branch.

### 5.2 Create the first files

Create `.gitignore`:

```gitignore
# Python
__pycache__/
*.py[cod]
*.egg-info/
.pytest_cache/
.ruff_cache/
.coverage
htmlcov/

# Virtual environments
.venv/
venv/
env/

# Environment files
.env
.env.*
!.env.example

# Django
db.sqlite3
db.sqlite3-journal
/staticfiles/
/media/
/private_media/

# OS and editors
.DS_Store
Thumbs.db
.idea/
.vscode/
```

Create `.env.example`:

```env
SECRET_KEY=replace-with-a-long-random-string
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

POSTGRES_DB=pododiab
POSTGRES_USER=pododiab
POSTGRES_PASSWORD=pododiab_dev
DATABASE_URL=postgres://pododiab:pododiab_dev@127.0.0.1:5432/pododiab
```

Create a short `README.md` placeholder for now. The full README comes in S1-12.

### 5.3 First commit

```bash
git add .gitignore .env.example README.md
git commit -m "chore: initialize repository"
git push -u origin main
```

> The very first commit on `main` is the only exception to the “no direct push” rule. After this commit, protect `main`.

### 5.4 GitHub settings

1. **Settings → Collaborators and teams** → add all 5 members with **Write** access.
2. **Settings → Branches** → add a branch protection rule for `main`:
   - Require a pull request before merging.
   - Require 1 approval.
   - Require status checks to pass (select CI after it exists).
   - Block force pushes.
   - Block deletions.
3. If branch protection is unavailable on a private repo, make the repo public (no real data) or use a ruleset. As a fallback, the team agrees never to push to `main`.

### 5.5 Copy the project documentation

Create a `docs/` folder in the new repo and copy the specification files from the old project:

- Project description.
- Functional specification.
- Data model (`03-data-model.md`).
- Permissions and security.
- Business rules.
- Acceptance criteria.
- Database schema image (`database-schema.png`).

Do **not** copy the old code or the old `.git` folder.

---

## 6. Step 2 — Create the Django skeleton

### 6.1 Requirements files

`requirements/base.txt`:

```text
Django>=5.2,<5.3
psycopg[binary]>=3.2,<4
django-environ>=0.12,<1
```

`requirements/dev.txt`:

```text
-r base.txt
pytest>=8,<9
pytest-django>=4.9,<5
ruff>=0.9,<1
```

### 6.2 Virtual environment and install

Linux/macOS:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements/dev.txt
```

Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements/dev.txt
```

### 6.3 Create the project and apps

```bash
django-admin startproject config .
mkdir -p apps
touch apps/__init__.py

python manage.py startapp core apps/core
python manage.py startapp accounts apps/accounts
python manage.py startapp patients apps/patients
python manage.py startapp medical apps/medical
python manage.py startapp consultations apps/consultations
python manage.py startapp billing apps/billing
python manage.py startapp documents apps/documents
python manage.py startapp audit apps/audit
```

The structure becomes:

```text
pododiab/
├── config/
├── apps/
│   ├── core/
│   ├── accounts/
│   ├── patients/
│   ├── medical/
│   ├── consultations/
│   ├── billing/
│   ├── documents/
│   └── audit/
├── templates/
├── static/
├── tests/
├── docs/
├── compose.yaml
├── manage.py
├── requirements/
│   ├── base.txt
│   └── dev.txt
├── .env.example
├── .gitignore
└── README.md
```

### 6.4 Fix every `apps.py`

`startapp` writes the short name. Change it to the full path. Example, `apps/patients/apps.py`:

```python
from django.apps import AppConfig


class PatientsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.patients"
```

Do the same for `apps.core`, `apps.accounts`, `apps.medical`, `apps.consultations`, `apps.billing`, `apps.documents`, `apps.audit`.

### 6.5 Configure `config/settings.py`

Add the environment reader and the apps:

```python
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.core",
    "apps.accounts",
    "apps.patients",
    "apps.medical",
    "apps.consultations",
    "apps.billing",
    "apps.documents",
    "apps.audit",
]

AUTH_USER_MODEL = "accounts.User"

DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

LANGUAGE_CODE = "fr"
TIME_ZONE = "Africa/Algiers"
USE_I18N = True
USE_TZ = True

TEMPLATES[0]["DIRS"] = [BASE_DIR / "templates"]
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
```

> **Critical:** `AUTH_USER_MODEL = "accounts.User"` must be set **before the first `migrate`**. If you migrate with Django’s default user first, reset the development database and start again.

Check the project:

```bash
python manage.py check
```

### 6.6 First PR

```bash
git switch -c feat/S1-02-django-skeleton
git add .
git commit -m "feat: add Django project skeleton and app structure"
git push -u origin feat/S1-02-django-skeleton
```

Open a PR, request a review, wait for the review, and squash-merge.

---

## 7. Step 3 — PostgreSQL 16 with Docker

### 7.1 Create `compose.yaml`

```yaml
services:
  db:
    image: postgres:16
    container_name: pododiab-db
    restart: unless-stopped
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-pododiab}
      POSTGRES_USER: ${POSTGRES_USER:-pododiab}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-pododiab_dev}
    ports:
      - "127.0.0.1:5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-pododiab} -d ${POSTGRES_DB:-pododiab}"]
      interval: 5s
      timeout: 5s
      retries: 10

volumes:
  postgres_data:
```

Why these choices:

- `postgres:16` matches the project specification.
- `127.0.0.1:5432:5432` exposes the database only to your machine, not the local network.
- The named volume keeps data when the container is recreated.
- The healthcheck tells you when PostgreSQL is ready.

### 7.2 Create your local `.env`

```bash
cp .env.example .env
```

Generate a secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Put the generated value in `.env` as `SECRET_KEY`.

`.env` is ignored by Git. Never commit it.

### 7.3 Start the database

```bash
docker compose up -d db
docker compose ps
docker compose logs db
```

Wait until the state is `healthy`.

### 7.4 Run the first migration

```bash
python manage.py migrate
```

This creates Django’s built-in tables in PostgreSQL. If it connects successfully, the Docker bridge works.

Useful commands:

```bash
docker compose exec db psql -U pododiab -d pododiab -c "\dt"
docker compose exec db psql -U pododiab -d pododiab
docker compose down        # stop, keep data
docker compose down -v     # stop and DELETE all data
```

> Never use `docker compose down -v` unless you want a completely fresh database.

If port `5432` is already in use, change the compose mapping to `"127.0.0.1:5433:5432"` and update `DATABASE_URL` to port `5433`.

---

## 8. Step 4 — Write the database models

The full field list is in `docs/03-data-model.md`. That document is the contract. The summary below tells you which model belongs in which app.

| App | Model | Main content |
|---|---|---|
| `accounts` | `User` | `AbstractUser` + `role` (`doctor`/`assistant`), `must_change_password`, `created_by`, deactivation fields |
| `patients` | `Patient` | `reference` (`PAT-000001`), names, phone, birth date, sex, address, creator, archive fields |
| `medical` | `MedicalEntry` | patient, category (5 types), title, details, dates, active flag, recorder |
| `consultations` | `Consultation` | patient, doctor, date, complaint, examination, diagnosis, notes, treatment, analysis fields, orientation letter, status, fee |
| `consultations` | `PrescriptionItem` | consultation, medication, dosage, frequency, duration, instructions, position, soft removal |
| `billing` | `Payment` | consultation, amount, method, paid date, reference, note, receipt number, recorder |
| `documents` | `Attachment` | consultation, private file, original name, MIME type, size, caption, uploader, soft removal |
| `audit` | `AuditLog` | actor, role, action, patient, entity type/id, summary, JSON changes, masked IP |

### Model rules

- Use `settings.AUTH_USER_MODEL` for every user foreign key. Do not import `User` directly in models.
- Use `on_delete=models.PROTECT` for users, patients and consultations.
- Use `models.TextChoices` for every enum.
- Use `DecimalField(max_digits=12, decimal_places=2)` for money. Never `FloatField`.
- Add `created_at` / `updated_at` where the data model requires them.
- Add the indexes listed in `docs/03`.
- No hard deletes for medical or financial records. The fields support archive, void, deactivate or soft removal.
- `AuditLog` is append-only.

### 8.1 `apps/accounts/models.py`

```python
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        DOCTOR = "doctor", "Médecin"
        ASSISTANT = "assistant", "Assistant(e)"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.ASSISTANT)
    must_change_password = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="created_users",
    )
    deactivated_at = models.DateTimeField(null=True, blank=True)
    deactivated_by = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="deactivated_users",
    )

    @property
    def full_name(self):
        return self.get_full_name() or self.username
```

Django already provides `first_name`, `last_name`, `is_active`, `last_login` and `date_joined`. Use them instead of duplicating fields from the document.

### 8.2 `apps/patients/models.py` — reference generation

```python
from django.conf import settings
from django.db import models


class Patient(models.Model):
    class Sex(models.TextChoices):
        MALE = "M", "Masculin"
        FEMALE = "F", "Féminin"

    reference = models.CharField(
        max_length=10,
        unique=True,
        null=True,
        blank=True,
        editable=False,
    )
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=1, choices=Sex.choices, blank=True)
    address = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="patients_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    archived_at = models.DateTimeField(null=True, blank=True)
    archived_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="patients_archived",
    )

    class Meta:
        ordering = ["last_name", "first_name"]
        indexes = [
            models.Index(fields=["last_name", "first_name"]),
            models.Index(fields=["phone"]),
            models.Index(fields=["archived_at"]),
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.reference:
            self.reference = f"PAT-{self.pk:06d}"
            super().save(update_fields=["reference"])

    def __str__(self):
        return f"{self.reference} — {self.last_name} {self.first_name}"
```

This is a simple Sprint 1 implementation. A database sequence can replace it later when the patient workflow is built.

### 8.3 `apps/audit/models.py` — append-only

```python
from django.conf import settings
from django.db import models


class AuditLog(models.Model):
    class Action(models.TextChoices):
        RECORD_VIEW = "record_view", "Consultation du dossier"
        CREATE = "create", "Création"
        UPDATE = "update", "Modification"
        ARCHIVE = "archive", "Archivage"
        RESTORE = "restore", "Restauration"
        PAYMENT_CREATE = "payment_create", "Paiement"
        PAYMENT_UPDATE = "payment_update", "Modification de paiement"
        UPLOAD = "upload", "Téléversement"
        DOCUMENT_REMOVE = "document_remove", "Suppression de document"
        USER_CREATE = "user_create", "Création d'utilisateur"
        USER_UPDATE = "user_update", "Modification d'utilisateur"
        USER_DEACTIVATE = "user_deactivate", "Désactivation d'utilisateur"
        USER_REACTIVATE = "user_reactivate", "Réactivation d'utilisateur"
        PASSWORD_RESET = "password_reset", "Réinitialisation de mot de passe"

    occurred_at = models.DateTimeField(auto_now_add=True)
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="audit_entries",
    )
    actor_role = models.CharField(max_length=20, blank=True)
    action = models.CharField(max_length=30, choices=Action.choices)
    patient = models.ForeignKey(
        "patients.Patient",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="audit_entries",
    )
    entity_type = models.CharField(max_length=50)
    entity_id = models.BigIntegerField(null=True, blank=True)
    summary = models.CharField(max_length=255)
    changes = models.JSONField(null=True, blank=True)
    ip_masked = models.CharField(max_length=45, blank=True)

    class Meta:
        ordering = ["-occurred_at"]
        indexes = [
            models.Index(fields=["occurred_at"]),
            models.Index(fields=["actor"]),
            models.Index(fields=["patient"]),
            models.Index(fields=["action"]),
        ]

    def save(self, *args, **kwargs):
        if self.pk and AuditLog.objects.filter(pk=self.pk).exists():
            raise ValueError("AuditLog is append-only")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValueError("AuditLog cannot be deleted")

    def __str__(self):
        return f"{self.occurred_at:%Y-%m-%d %H:%M} — {self.summary}"
```

The application-level check is enough for Sprint 1. For stronger protection later, add database triggers or revoke update/delete permissions on the table.

### 8.4 Admin registration

Register every model so the team can inspect the data. Example for a patient:

```python
from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("reference", "last_name", "first_name", "phone", "archived_at")
    search_fields = ("reference", "last_name", "first_name", "phone")
    list_filter = ("sex", "archived_at")
    readonly_fields = ("reference", "created_at", "updated_at")
```

For `AuditLog`, make the admin read-only:

```python
@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("occurred_at", "actor", "action", "entity_type", "summary")
    list_filter = ("action", "actor_role")
    search_fields = ("summary", "entity_type")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
```

---

## 9. Step 5 — Migrations and seed data

### 9.1 Create and apply migrations

```bash
python manage.py makemigrations accounts patients medical consultations billing documents audit
python manage.py migrate
```

`core` has no models in Sprint 1, so it does not need a migration.

Verify the tables:

```bash
docker compose exec db psql -U pododiab -d pododiab -c "\dt"
```

You should see these domain tables:

```text
accounts_user
patients_patient
medical_medicalentry
consultations_consultation
consultations_prescriptionitem
billing_payment
documents_attachment
audit_auditlog
```

Django’s own tables (`django_migrations`, `auth_group`, etc.) will also be present. That is normal.

### 9.2 Common migration mistake

If you already ran `migrate` before setting `AUTH_USER_MODEL`, the user table is wrong. Reset the development database:

```bash
docker compose down -v
docker compose up -d db
python manage.py migrate
```

Do not delete migration files. Do not do this on a database that contains real data.

### 9.3 Create the seed command

Create `apps/core/management/commands/seed_demo.py`. Create the `management/` and `management/commands/` folders with `__init__.py` files.

The command must:

- Create one doctor and one assistant.
- Create 10 fictional patients.
- Create one consultation for the first patient.
- Create one prescription line and one payment.
- Create one or two audit entries.
- Use `get_or_create` so it is repeatable.
- Print the demo credentials.

Use clearly fake data. Example names and phone numbers:

```text
Benali, Amina, 0550 00 00 01
Khelifi, Yacine, 0550 00 00 02
...
```

Never use real patient information.

Run it:

```bash
python manage.py seed_demo
python manage.py seed_demo
```

The second run must not create duplicates.

---

## 10. Step 6 — Tests, CI and README

### 10.1 `pyproject.toml`

```toml
[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "config.settings"
python_files = ["test_*.py", "*_tests.py"]

[tool.ruff]
target-version = "py312"
line-length = 100
exclude = ["migrations"]

[tool.ruff.lint]
select = ["E", "F", "I", "DJ"]
```

### 10.2 Five required tests

Create `tests/test_models.py` with at least these tests:

1. A new patient receives a reference in the `PAT-000001` format.
2. An audit log cannot be updated.
3. An audit log cannot be deleted.
4. A user who created a patient cannot be deleted (`ProtectedError`).
5. Consultations are ordered by most recent first.

Example pattern:

```python
import pytest
from django.db.models import ProtectedError

from apps.accounts.models import User
from apps.audit.models import AuditLog
from apps.patients.models import Patient


@pytest.fixture
def doctor(db):
    return User.objects.create_user(
        username="doctor.demo",
        password="test-only",
        role=User.Role.DOCTOR,
    )


@pytest.mark.django_db
def test_patient_reference_is_generated(doctor):
    patient = Patient.objects.create(
        last_name="Test",
        first_name="Patient",
        phone="0550000001",
        created_by=doctor,
    )
    assert patient.reference == f"PAT-{patient.pk:06d}"


@pytest.mark.django_db
def test_audit_log_cannot_be_updated(doctor):
    log = AuditLog.objects.create(
        actor=doctor,
        actor_role=User.Role.DOCTOR,
        action=AuditLog.Action.CREATE,
        entity_type="patient",
        summary="Test audit entry",
    )
    log.summary = "Changed"
    with pytest.raises(ValueError):
        log.save()


@pytest.mark.django_db
def test_audit_log_cannot_be_deleted(doctor):
    log = AuditLog.objects.create(
        actor=doctor,
        actor_role=User.Role.DOCTOR,
        action=AuditLog.Action.CREATE,
        entity_type="patient",
        summary="Test audit entry",
    )
    with pytest.raises(ValueError):
        log.delete()


@pytest.mark.django_db
def test_user_with_patients_cannot_be_deleted(doctor):
    Patient.objects.create(
        last_name="Test",
        first_name="Patient",
        phone="0550000002",
        created_by=doctor,
    )
    with pytest.raises(ProtectedError):
        doctor.delete()
```

Add the consultation ordering test in the same file or in `tests/test_consultations.py`.

Run:

```bash
pytest
```

### 10.3 CI workflow

Create `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  pull_request:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: pododiab
          POSTGRES_USER: pododiab
          POSTGRES_PASSWORD: pododiab
        ports:
          - 5432:5432
        options: >-
          --health-cmd "pg_isready -U pododiab -d pododiab"
          --health-interval 5s
          --health-timeout 5s
          --health-retries 10

    env:
      SECRET_KEY: ci-only-secret-key-not-for-production
      DEBUG: "False"
      ALLOWED_HOSTS: localhost,127.0.0.1,testserver
      DATABASE_URL: postgres://pododiab:pododiab@127.0.0.1:5432/pododiab

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
          cache-dependency-path: requirements/*.txt

      - name: Install dependencies
        run: pip install -r requirements/dev.txt

      - name: Lint
        run: ruff check .

      - name: Django check
        run: python manage.py check

      - name: Check migrations
        run: python manage.py makemigrations --check --dry-run

      - name: Tests
        run: pytest
```

After the first PR, go back to the branch protection rule and select the CI check.

### 10.4 README

The README must let a new person start from a clean clone. Include:

- Project summary.
- Stack.
- Prerequisites.
- Linux and Windows setup commands.
- How to start Docker, migrate and seed.
- Demo accounts.
- How to run tests.
- Project structure.
- Git workflow.
- “Synthetic data only” warning.

Linux quick start:

```bash
cp .env.example .env
# generate and paste SECRET_KEY into .env
docker compose up -d db
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements/dev.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

Windows quick start:

```powershell
copy .env.example .env
# generate and paste SECRET_KEY into .env
docker compose up -d db
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements/dev.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

### 10.5 Clean-clone test

Before the review, test the README from a fresh clone:

```bash
cd /tmp
git clone <YOUR-REPO-URL> pododiab-clean
cd pododiab-clean
cp .env.example .env
# put a secret key in .env
docker compose up -d db
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements/dev.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

If this works, the sprint demo is ready.

---

## 11. Sprint 1 board

These are **enablers**, not user stories. Keep the 29 product stories in a separate Product Backlog view.

| ID | Task | Owner | Points | Done when |
|---|---|---|---|---|
| **S1-01** | Repo, README, `.gitignore`, `.env.example`, PR template, branch protection | P1 | 2 | `main` protected; clean clone documented |
| **S1-02** | Python 3.12, requirements, Django project, apps | P1 | 3 | `manage.py check` passes |
| **S1-03** | Docker PostgreSQL + settings + `.env` | P1 | 2 | `migrate` connects from a clean clone |
| **S1-04** | Custom `User` + roles + admin | P1 / P4 | 2 | `accounts_user` exists; roles work |
| **S1-05** | `Patient` model + reference + indexes + admin | P3 | 2 | `patients_patient`; reference format works |
| **S1-06** | `MedicalEntry` model + categories + admin | P3 | 2 | `medical_medicalentry` exists |
| **S1-07** | `Consultation` + `PrescriptionItem` models + admin | P3 | 3 | both tables; ordering and `PROTECT` work |
| **S1-08** | `Payment` + `Attachment` models + admin | P4 | 2 | both tables and fields exist |
| **S1-09** | `AuditLog` model + append-only + read-only admin | P4 / P5 | 2 | update/delete blocked by tests |
| **S1-10** | Migrations from zero + `seed_demo` | P5 | 3 | `migrate` + `seed_demo` work twice |
| **S1-11** | 5 model tests + CI | P5 | 3 | CI green; `pytest` green |
| **S1-12** | Clean-clone check + demo evidence | P1 / P5 | 2 | clean clone runs; screenshots ready |
| **S1-13** | Design assets, `static/` and `templates/` skeleton | P2 | 2 | tokens and folders ready for Sprint 2 |

**Total:** about 30 points.

### Board columns

```text
To Do  →  In Progress  →  Done
```

Keep a separate table view called **Product Backlog** for the 29 user stories.

### Labels

```text
must
should
could
enabler
sprint:1
role:doctor
role:assistant
db
```

---

## 12. Three-day schedule

| Day | Focus | Checkpoint |
|---|---|---|
| **Wednesday 25 Nov** | P1: repo, skeleton, Docker, PostgreSQL, settings. P2: design assets and static/templates folders. P3/P4: read the data model and draft models. P5: CI and test skeleton. | First PRs merged; `migrate` connects to PostgreSQL |
| **Thursday 26 Nov** | `User`, `Patient`, `MedicalEntry` models, migrations, admin. | These tables exist; admin opens |
| **Friday 27 Nov** | `Consultation`, `PrescriptionItem`, `Payment`, `Attachment`, `AuditLog`, seed, tests, CI. | Full schema; `seed_demo` works; tests pass |
| **Saturday 28 Nov** | Clean-clone test, README, fix CI, merge, board update, sprint review and retrospective. | Sprint demo ready; board Done column updated |

Suggested ceremonies:

- **Daily Scrum:** 15 minutes, same time every day.
  - What did I do?
  - What will I do?
  - What is blocking me?
- **Sprint review:** Saturday 28 November, 60 minutes. Demo from the app, not screenshots.
- **Retrospective:** after the review, 45 minutes.

---

## 13. Sprint review demo script

Show this in order:

1. GitHub repository, branch protection, and PR history.
2. One merged PR with review and green CI.
3. Clean clone from the README.
4. `docker compose up -d db` and `docker compose ps` showing healthy.
5. `python manage.py migrate` on the empty database.
6. `docker compose exec db psql -U pododiab -d pododiab -c "\dt"` showing the domain tables.
7. `python manage.py seed_demo` and the demo accounts.
8. Django admin: show the seeded users, patients, consultation, payment and audit entry.
9. `pytest` and the green CI run.
10. The GitHub board with the Done items.

### Evidence checklist

- [ ] Board screenshot with **To Do / In Progress / Done** and real cards.
- [ ] GitHub **Insights → Commits** screenshot showing all contributors.
- [ ] Screenshot of the Docker database healthy.
- [ ] Screenshot of `\dt` with the domain tables.
- [ ] Screenshot of the seeded data in Django admin.
- [ ] Screenshot of green CI.
- [ ] Sprint review notes and attendance.

---

## 14. Using the old AI-built project

The old project is a **prototype and reference**. The new repository is the final deliverable. You may copy small, understood pieces to save time, but do not copy the whole project.

### Allowed

- Model field definitions.
- Validation rules and business logic.
- CSS/theme and template fragments.
- Documentation and database schema images.

### Not allowed

- The old `.git` folder.
- The old `.env`.
- `db.sqlite3` or any real data.
- `__pycache__`, `staticfiles/`, or the old virtual environment.
- A single giant commit containing the whole old project.

If you copy a piece, adapt it to the new structure and write an honest commit message:

```text
feat(patients): add Patient model adapted from prototype (S1-05)
```

You can read the old code without cloning it:

```bash
git remote add prototype <OLD-REPO-URL>
git fetch prototype
git show prototype/main:clinic/models.py
```

If you cannot explain a line to the teacher, do not commit it.

---

## 15. Decisions log for Sprint 1

Record these decisions in the repository or in the project documentation:

| Decision | Choice |
|---|---|
| Repository | New empty repo; old repo is reference only |
| Python | 3.12 |
| Django | 5.2 LTS |
| Database | PostgreSQL 16 in Docker |
| Django runtime | Host virtual environment, not Docker |
| App layout | `apps/` package with one app per domain |
| Settings | Single `config/settings.py` + `.env` for now; split later if needed |
| Sprint dates | 7–28 November 2026, with the midterm pause |
| Sprint scope | Repo, skeleton, schema, seed, tests, CI |
| Out of scope | Login, dashboards, design shell, permission UI |
| Frontend for Sprint 2 | To be confirmed by the team (Bootstrap is simpler for beginners and matches the prototype; Tailwind needs a Node build step) |

Also update the old `docs/13-sprint-1-plan-and-form-guide.md` (or the copy in the new repo) so it does not claim that login, the shell and permission tests were delivered in this sprint.

---

## 16. Common beginner errors

| Error | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'apps'` | `apps.py` uses the short name | Set `name = "apps.<app>"` and use `apps.<app>` in `INSTALLED_APPS` |
| `AUTH_USER_MODEL` error or wrong user table | Migrated before setting the custom user | `docker compose down -v`, `up -d db`, `migrate` |
| `connection refused` on port 5432 | Docker is not running or the container is unhealthy | `docker compose ps`, `docker compose logs db` |
| `SECRET_KEY` error | `.env` is missing | `cp .env.example .env` and fill the key |
| `psycopg` install fails | Using Python 3.14 | Create the venv with `python3.12` |
| `pytest` finds no tests | Tests are not under `tests/` | Create `tests/test_models.py` |
| CI fails on `makemigrations --check` | A model changed and the migration was not committed | Run `makemigrations`, commit the file |
| `git push` to `main` is rejected | Branch protection is working | Push a branch and open a PR |
| Port 5432 is busy | Another PostgreSQL is running | Map `127.0.0.1:5433:5432` and update `DATABASE_URL` |
| Seed creates duplicates | Using `create()` instead of `get_or_create()` | Make the command idempotent |

---

## 17. Quick command sheet

```bash
# Start the database
docker compose up -d db

# Activate the environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements/dev.txt

# Create migrations
python manage.py makemigrations accounts patients medical consultations billing documents audit

# Apply migrations
python manage.py migrate

# Seed fictional data
python manage.py seed_demo

# Run checks and tests
python manage.py check
python manage.py makemigrations --check --dry-run
pytest
ruff check .

# Start the app
python manage.py runserver

# Inspect the tables
docker compose exec db psql -U pododiab -d pododiab -c "\dt"

# Stop the database
docker compose down

# Reset the development database (destroys data)
docker compose down -v
docker compose up -d db
python manage.py migrate
```

---

**End of Sprint 1 guide.**
