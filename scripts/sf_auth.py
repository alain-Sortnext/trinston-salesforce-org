import subprocess, os, sys, json

username     = os.environ.get("SF_USERNAME", "")
consumer_key = os.environ.get("SF_CONSUMER_KEY", "")
instance_url = "https://orgfarm-709b3a2059-dev-ed.develop.my.salesforce.com"

summary = os.environ.get("GITHUB_STEP_SUMMARY", "/dev/null")

def log(msg):
    print(msg)
    with open(summary, "a") as f:
        f.write(msg + "\n")

# Write the JWT private key to a temp file
key_content = os.environ.get("SF_JWT_PRIVATE_KEY", "")
with open("/tmp/server.key", "w") as f:
    f.write(key_content)

log(f"Username: {username}")
log(f"Instance: {instance_url}")
log(f"Consumer key: {consumer_key[:20]}...")
log(f"Key file size: {len(key_content)} chars")

# Try JWT auth via sf cli directly
cmd = [
    "sf", "org", "login", "jwt",
    "--username", username,
    "--jwt-key-file", "/tmp/server.key",
    "--client-id", consumer_key,
    "--instance-url", instance_url,
    "--alias", "trinston-dev",
    "--set-default",
    "--no-prompt",
    "--json"
]

log(f"\nRunning: sf org login jwt...")
result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
log(f"Exit code: {result.returncode}")
log(f"Stdout: {result.stdout[:500]}")
if result.stderr:
    log(f"Stderr: {result.stderr[:500]}")

if result.returncode == 0:
    log("**JWT AUTH SUCCESS**")
    sys.exit(0)
else:
    log("**JWT AUTH FAILED**")
    # Try parsing the error
    try:
        d = json.loads(result.stdout)
        log(f"Error: {d.get('message', d)}")
    except:
        pass
    sys.exit(1)
