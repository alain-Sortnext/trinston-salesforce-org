import urllib.request, urllib.parse, os, sys, json, subprocess

username        = os.environ.get("SF_USERNAME", "")
pw_token        = os.environ.get("SF_PASSWORD_WITH_TOKEN", "")
consumer_key    = os.environ.get("SF_CONSUMER_KEY", "")
consumer_secret = os.environ.get("SF_CONSUMER_SECRET", "")
summary         = os.environ.get("GITHUB_STEP_SUMMARY", "/dev/null")

def log(msg):
    print(msg)
    open(summary, "a").write(msg + "\n")

log(f"Username: {username}")
log(f"PW+Token len: {len(pw_token)}")

url = "https://orgfarm-709b3a2059-dev-ed.develop.my.salesforce.com/services/oauth2/token"
data = urllib.parse.urlencode({
    "grant_type":    "password",
    "client_id":     consumer_key,
    "client_secret": consumer_secret,
    "username":      username,
    "password":      pw_token,
}).encode()

try:
    with urllib.request.urlopen(urllib.request.Request(url, data=data), timeout=30) as r:
        resp = json.loads(r.read())
        if "access_token" in resp:
            token    = resp["access_token"]
            inst_url = resp["instance_url"]
            log(f"OAuth SUCCESS: {inst_url}")

            cmd = [
                "sf", "org", "login", "access-token",
                "--instance-url", inst_url,
                "--alias", "trinston-dev",
                "--set-default",
                "--no-prompt"
            ]
            env = os.environ.copy()
            env["SFDX_ACCESS_TOKEN"] = token
            result = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=60)
            log(f"SF CLI exit: {result.returncode}")
            if result.stdout: log(f"stdout: {result.stdout[:200]}")
            if result.stderr: log(f"stderr: {result.stderr[:200]}")
            
            if result.returncode == 0:
                log("SF CLI login SUCCESS")
                sys.exit(0)
            else:
                log("Trying sfdx-url fallback...")
                sfdx_url = f"force://{consumer_key}:{consumer_secret}:{token}@{inst_url.replace('https://','')}"
                open("/tmp/sfdx_auth_url.txt","w").write(sfdx_url)
                open("/tmp/use_sfdx_url","w").write("yes")
                log("sfdx url written")
                sys.exit(0)
        else:
            log(f"FAIL: {json.dumps(resp)}")
            sys.exit(1)
except urllib.error.HTTPError as e:
    log(f"HTTP {e.code}: {e.read().decode()[:300]}")
    sys.exit(1)
except Exception as ex:
    log(f"{type(ex).__name__}: {ex}")
    sys.exit(1)
