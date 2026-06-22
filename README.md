# Trinston Salesforce Org — Deployment Package

Automated Salesforce configuration for the **Project Lab — Trinston Ltd CRM PM Simulation**.

## What this deploys
- 9 roles (full 6-tier hierarchy)
- 2 profiles (Operations Read-Only + Trinston Candidate)  
- 6 regional queues (4 sales + 2 CS)
- 14 custom fields across 6 objects
- 4 validation rules
- 4 reports + 1 dashboard
- 1 automation flow (Close Date Reminder)
- 2,850 data records (250 Accounts + 1,000 Contacts + 500 Leads + 100 Campaigns + 400 Opportunities + 600 Cases)

---

## One-time setup — 4 steps in Salesforce, 4 secrets in GitHub

### STEP 1 — Upload certificate to your Connected App in Salesforce

Go to your org:  
`https://orgfarm-709b3a2059-dev-ed.develop.my.salesforce.com/lightning/setup/ConnectedApplication/home`

Find the Connected App you created → Click **Edit** → Scroll to **API (Enable OAuth Settings)**

Enable **"Use digital signatures"** → Upload this certificate file:

```
-----BEGIN CERTIFICATE-----
MIIDwTCCAqmgAwIBAgIUBAiPQHOzplQ8RGJPkLIwYfGNS/YwDQYJKoZIhvcNAQEL
BQAwcDELMAkGA1UEBhMCR0IxEDAOBgNVBAgMB0VuZ2xhbmQxEzARBgNVBAcMCkJp
cm1pbmdoYW0xFTATBgNVBAoMDFRyaW5zdG9uIEx0ZDEjMCEGA1UEAwwadHJpbnN0
b24tc2FsZXNmb3JjZS1kZXBsb3kwHhcNMjYwNjIyMTU0OTQwWhcNMjcwNjIyMTU0
OTQwWjBwMQswCQYDVQQGEwJHQjEQMA4GA1UECAwHRW5nbGFuZDETMBEGA1UEBwwK
QmlybWluZ2hhbTEVMBMGA1UECgwMVHJpbnN0b24gTHRkMSMwIQYDVQQDDBp0cmlu
c3Rvbi1zYWxlc2ZvcmNlLWRlcGxveTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCC
AQoCggEBAM/jKbcu/4phCzBdXnBQi9wdR2CNO+WqGid8jIzOI/PawF37GKNRGVcQ
iM/55+OeWZxa8Y4p6frl7j/uRCSMgtDROxUeDTpdlSP+PfmD8v4e1ZF+hzR1o9m9
4jCQ/58kYn9lhN97mAmItZqdWJYIX/PKWQ92fvE0hSiZZTJ4Tb3A6ljnXte+adzr
Zm+xQEJYQ+GUB0W62n3SxlOcRRp/FhifhRYWJkw+EVAnD3a+hqnJGv6R1GuCqDdW
InuR0BuMDhMKfki/HLmSWHVyYNICQLnU0DXzKFnBz3peAgcXNh+uST3a+JGVHNCr
fkU4W3WGZc3o5kpQa9nFUtd/eU1vnc0CAwEAAaNTMFEwHQYDVR0OBBYEFPad9pz+
vDyjUY0ZHqHIOluKfodrMB8GA1UdIwQYMBaAFPad9pz+vDyjUY0ZHqHIOluKfodr
MA8GA1UdEwEB/wQFMAMBAf8wDQYJKoZIhvcNAQELBQADggEBAA07sr0ewBYeTkno
ML8It0p9RxwPcTPwggvp2feg9TvuX4nshe2PNslGKBmDxZQ+e3PgfJnvrU0UA3qq
Guq9v4Ylal7b1pprJYTpOnjOZ1FOxZkYZ3ZMYMFYzxGKNHN+7R1SZIuz+PtZbKfa
i4RxdQ7hfi3voPy2dTN1y/NEfd1OEY+HJb8EyqTfq1cFnikW6gTGCGzQvtkhIcKD
Q6yWBc5oFFnqywQNAUuCjWAEUh/Fzd4hHlglLGCJeoAW9TfI0iAsBEbOYLhQ5qBK
RJB4nA7HktxUfprV/3CJl7lP2yh5oqiW/InY9VajlkldIBLSWTcOG0MPFdcCjCZg
KPUE15I=
-----END CERTIFICATE-----

```

Save it as a `.crt` file and upload it.

### STEP 2 — Pre-authorise JWT in Salesforce

In Setup → search **"OAuth and OpenID Connect Settings"**  
→ Enable **"Allow OAuth Username-Password Flows"**

Also go to Setup → **Manage Connected Apps** → find your app → **Edit Policies**  
→ Set **"IP Relaxation"** to `Relax IP restrictions`  
→ Set **"Permitted Users"** to `Admin approved users are pre-authorized`  
→ Save

Then go to Setup → **Permission Sets** → find or create one → **Manage Assignments** → add your user

### STEP 3 — Add 4 GitHub Secrets

Go to: `https://github.com/alain-Sortnext/trinston-salesforce-org/settings/secrets/actions`

| Secret Name | Value |
|---|---|
| `SF_USERNAME` | `mavadufashion.7880dc71777c@agentforce.com` |
| `SF_CONSUMER_KEY` | `3MVG97L7PWbPq6UwlCtAjpkLOb9IMu3D2ZEMq0KSpMAcQoQRygtORv8ASzK1Ze0R0tt7ZV7TQmi9nrEQ3Qicf` |
| `SF_INSTANCE_URL` | `https://orgfarm-709b3a2059-dev-ed.develop.my.salesforce.com` |
| `SF_JWT_PRIVATE_KEY` | *(see scripts/jwt_private_key.txt in this repo)* |

### STEP 4 — Run the workflow

Go to: `https://github.com/alain-Sortnext/trinston-salesforce-org/actions`  
→ Click **Deploy Trinston Salesforce Org**  
→ Click **Run workflow**  
→ Set `deploy_data = true`  
→ Click **Run workflow**

Everything deploys automatically in ~15 minutes. ✅

---

## Repo structure
```
├── .github/workflows/deploy-trinston-org.yml  # GitHub Actions workflow
├── force-app/main/default/
│   ├── objects/          # Custom fields + validation rules (6 objects)
│   ├── roles/            # 9 roles — full hierarchy
│   ├── profiles/         # Operations Read-Only + Trinston Candidate
│   ├── queues/           # 4 sales + 2 CS queues
│   ├── flows/            # Close Date Reminder automation
│   ├── reports/          # 4 key programme reports
│   └── dashboards/       # Programme KPI dashboard
├── data/                 # 2,850 records ready to load
└── scripts/              # Setup guides
```
