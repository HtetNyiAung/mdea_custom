# Mdea Custom — Frappe Custom App

A custom [Frappe](https://frappeframework.com/) app for **Member Management** and **Member Subscriptions**, built for testing and extending with the `my-frappe-setup` Docker environment.

---

## 📦 Features

| Feature | Description |
|---|---|
| **Member** | Store member profiles — name, contact, type, status |
| **Member Subscription** | Track subscription plans, billing cycle, payment info |
| **Mdea Custom Workspace** | Dedicated home tile on Frappe desk with quick links |

---

## 🗂️ Project Structure

```
mdea_custom/
├── mdea_custom/                  ← Python package (app core)
│   ├── hooks.py                  ← Frappe lifecycle hooks
│   ├── modules.txt               ← Registered modules
│   ├── mdea_custom/              ← Module folder
│   │   ├── doctype/
│   │   │   ├── member/
│   │   │   │   ├── member.json   ← DocType schema (fields, permissions)
│   │   │   │   └── member.py     ← Python controller (validate, hooks)
│   │   │   └── member_subscription/
│   │   │       ├── member_subscription.json
│   │   │       └── member_subscription.py
│   │   └── workspace/
│   │       └── Mdea Custom/
│   │           └── Mdea Custom.json  ← Desk home tile
├── pyproject.toml
└── README.md
```

---

## 🚀 Setup — Using Docker (Recommended)

This app is designed to work with [`my-frappe-setup`](https://github.com/HtetNyiAung/my-frappe-setup).

### Prerequisites
- Docker & Docker Compose installed
- `jq` installed (`sudo apt install jq`)

### Step 1 — Clone the Docker setup repo

```bash
git clone https://github.com/HtetNyiAung/my-frappe-setup.git
cd my-frappe-setup/docker-setup
```

### Step 2 — Configure environment

```bash
cp .env.example .env
# Edit .env with your passwords and settings
```

### Step 3 — Check apps.json includes this app

```json
{
  "name": "mdea_custom",
  "url": "https://github.com/HtetNyiAung/mdea_custom.git",
  "branch": "main",
  "is_custom": true
}
```

### Step 4 — Run setup

```bash
./setup.sh
```

This will automatically:
- Clone `mdea_custom` to `../apps/mdea_custom` (volume mounted for hot-reload)
- Build a Docker image with all apps
- Create the Frappe site and install all apps
- Run database migration (DocTypes appear automatically)

### Step 5 — Access Frappe

Open **`http://localhost:8787`** in your browser.

- Username: `Administrator`
- Password: *(from your `.env` → `ADMIN_PASSWORD`)*

---

## 🛠️ Development Workflow

### Making changes to DocTypes or code

Since `apps/mdea_custom` is **volume-mounted** into Docker, your local file changes reflect instantly inside the container.

After editing files, run migrate to sync:

```bash
cd docker-setup
docker compose -f pwd-with-apps.yml -f docker-compose.override.yml \
  exec -T backend bench --site frontend migrate
```

### Adding a new DocType

1. Go to `localhost:8787/desk` → **Build → DocType → New**
2. Set **Module** = `Mdea Custom`
3. Add your fields and save
4. Export it to code (so it's version-controlled):

```bash
docker compose -f pwd-with-apps.yml -f docker-compose.override.yml \
  exec -T backend bench export-fixtures --app mdea_custom
```

5. The JSON will appear in `mdea_custom/mdea_custom/doctype/<doctype_name>/`

---

## 💾 Saving Changes to GitHub

All DocType files and app code live in **this repo** (`mdea_custom`).
Docker setup files (compose, `setup.sh`) live in the **`my-frappe-setup` repo**.

### Push app changes:

```bash
cd apps/mdea_custom
git add .
git commit -m "feat: describe your change"
git push origin main
```

> ✅ This pushes to `https://github.com/HtetNyiAung/mdea_custom`

---

## 📋 DocType Reference

### Member

| Field | Type | Description |
|---|---|---|
| `full_name` | Data | Member's full name (required) |
| `status` | Select | Active / Inactive / Suspended |
| `email` | Data (Email) | Contact email |
| `phone` | Phone | Contact phone |
| `member_type` | Select | Regular / Premium / VIP / Honorary |
| `member_since` | Date | Date of joining |
| `date_of_birth` | Date | Optional |
| `gender` | Select | Optional |
| `id_number` | Data | ID or Passport number |
| `address` | Small Text | Optional address |
| `notes` | Text Editor | Free-form notes |

Auto naming: `MEM-YYYY-00001`

### Member Subscription

| Field | Type | Description |
|---|---|---|
| `member` | Link → Member | Linked member (required) |
| `status` | Select | Active / Expired / Cancelled / Pending |
| `plan_name` | Select | Basic / Standard / Premium / VIP |
| `amount` | Currency | Subscription price |
| `billing_cycle` | Select | Monthly / Quarterly / Yearly |
| `start_date` | Date | Subscription start (required) |
| `end_date` | Date | Optional end date |
| `next_billing_date` | Date | Auto-calculated (read-only) |
| `auto_renew` | Check | Auto-renew flag |
| `payment_method` | Select | Cash / Bank Transfer / Credit Card / Mobile |
| `last_payment_date` | Date | Optional |
| `last_payment_amount` | Currency | Optional |

Auto naming: `SUB-YYYY-00001`

**Business logic:**
- `next_billing_date` is auto-calculated from `start_date` + billing cycle
- Subscription auto-marks as `Expired` if `end_date` is in the past on save

---

## 🔧 Manual Installation (Without Docker)

```bash
cd /path/to/frappe-bench
bench get-app https://github.com/HtetNyiAung/mdea_custom.git --branch main
bench --site your-site.local install-app mdea_custom
bench --site your-site.local migrate
```

---

## 📄 License

MIT — see [license.txt](license.txt)
