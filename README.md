# Pododiab — Clinic Management System

Pododiab is a web-based clinic management system for a private podiatry and
diabetic-foot clinic. It replaces paper patient files with a centralised,
role-separated system for the clinic's doctor and assistant.



## Sprint status

**Sprint 1 — Foundation** · 7–28 November 2026

In progress:
- repeatable seed data, tests and CI.

Not in this sprint:

- login and dashboards;
- design shell and navigation;
- patient and consultation screens;
- permission UI.

## Stack

| Layer | Choice |
|---|---|
| Language | Python 3.12 |
| Framework | Django 5.2 LTS |
| Database | PostgreSQL 16 (Docker for development) |
| Frontend | Django templates + Bootstrap 5.3 (Sprint 2) |
| Tests | pytest + pytest-django |
| Lint | ruff |
| CI | GitHub Actions |

## Quick start


```bash
cp .env.example .env
# generate a SECRET_KEY and put it in .env

docker compose up -d db
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements/dev.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

Windows: use `py -3.12 -m venv .venv` and `.venv\Scripts\Activate.ps1`.

## Repository layout (target)

```text
pododiab/
├── config/                 # Django project settings and URLs
├── apps/
│   ├── core/               # shared helpers and seed command
│   ├── accounts/           # custom User and roles
│   ├── patients/           # Patient
│   ├── medical/            # MedicalEntry
│   ├── consultations/      # Consultation and PrescriptionItem
│   ├── billing/            # Payment
│   ├── documents/          # Attachment
│   └── audit/              # AuditLog
├── templates/              # Django templates
├── static/                 # locally hosted CSS, JS, fonts, icons
├── tests/                  # pytest tests
├── docs/                   # specification and sprint documentation
├── compose.yaml            # PostgreSQL 16 development container
├── manage.py
├── requirements/
│   ├── base.txt
│   └── dev.txt
├── .env.example
├── .gitignore
└── README.md
```

## Workflow

- `main` is protected.
- One branch per task, for example `feat/S1-05-patient-model`.
- Open a pull request, get a review from a non-owner, wait for CI, then
  squash-merge.
- Never commit `.env`, database files, or real patient information.


## Data safety

Use fictional data only. Never commit real patient information, screenshots of
real records, `.env` files or database dumps. The clinic's production data must
stay on the clinic's own infrastructure.
