import urllib.request, os, re, sys

username = os.environ.get('SF_USERNAME', '')
pw_token = os.environ.get('SF_PASSWORD_WITH_TOKEN', '')

print(f"Username: {username}")
print(f"Password+token length: {len(pw_token)}")

soap = """<?xml version="1.0" encoding="utf-8"?>
<env:Envelope xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:env="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:urn="urn:partner.soap.sforce.com">
  <env:Body>
    <urn:login>
      <urn:username>""" + username + """</urn:username>
      <urn:password>""" + pw_token + """</urn:password>
    </urn:login>
  </env:Body>
</env:Envelope>"""

req = urllib.request.Request(
    "https://login.salesforce.com/services/Soap/u/59.0",
    data=soap.encode(),
    headers={"Content-Type": "text/xml; charset=UTF-8", "SOAPAction": "login"}
)

try:
    with urllib.request.urlopen(req, timeout=30) as r:
        body = r.read().decode()
        print("HTTP 200 response received")
        print(body[:2000])
        
        if "<sessionId>" in body:
            session  = re.search(r"<sessionId>(.*?)</sessionId>", body).group(1)
            srv_url  = re.search(r"<serverUrl>(.*?)</serverUrl>", body).group(1)
            instance = re.search(r"https://([^/]+)", srv_url).group(1)
            print(f"SUCCESS: {instance}")
            sfdx_url = f"force://PlatformCLI::{session}@{instance}"
            with open("/tmp/sfdx_auth_url.txt", "w") as f:
                f.write(sfdx_url)
            
            # Write success marker
            with open("auth_result.txt", "w") as f:
                f.write(f"SUCCESS:{instance}")
            sys.exit(0)
        else:
            with open("auth_result.txt", "w") as f:
                f.write("FAIL:" + body[:500])
            sys.exit(1)

except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f"HTTP {e.code}: {body[:500]}")
    with open("auth_result.txt", "w") as f:
        f.write(f"HTTP{e.code}:{body[:500]}")
    sys.exit(1)
except Exception as ex:
    msg = f"{type(ex).__name__}: {ex}"
    print(msg)
    with open("auth_result.txt", "w") as f:
        f.write(f"EXCEPT:{msg}")
    sys.exit(1)
