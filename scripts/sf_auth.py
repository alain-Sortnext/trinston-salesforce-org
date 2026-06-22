import urllib.request, re, os, sys

USERNAME = os.environ.get('SF_USERNAME', '')
PW_WITH_TOK = os.environ.get('SF_PASSWORD_WITH_TOKEN', '')

soap = """<?xml version="1.0" encoding="utf-8"?>
<env:Envelope xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:env="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:urn="urn:partner.soap.sforce.com">
  <env:Body>
    <urn:login>
      <urn:username>""" + USERNAME + """</urn:username>
      <urn:password>""" + PW_WITH_TOK + """</urn:password>
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
        if '<sessionId>' in body:
            session  = re.search(r'<sessionId>(.*?)</sessionId>', body).group(1)
            server   = re.search(r'<serverUrl>(.*?)</serverUrl>', body).group(1)
            instance = re.search(r'https://([^/]+)', server).group(1)
            sfdx_url = f"force://PlatformCLI::{session}@{instance}"
            with open('/tmp/sfdx_auth_url.txt', 'w') as f:
                f.write(sfdx_url)
            print(f"SUCCESS: {instance}")
            sys.exit(0)
        else:
            fault = re.search(r'<faultstring>(.*?)</faultstring>', body)
            msg = fault.group(1) if fault else body[:300]
            print(f"FAIL: {msg}")
            with open('auth_debug.txt', 'w') as f:
                f.write(f"User: {USERNAME}\nPW len: {len(PW_WITH_TOK)}\nError: {msg}\nFull: {body}")
            sys.exit(1)
except urllib.error.HTTPError as e:
    body = e.read().decode()
    fault = re.search(r'<faultstring>(.*?)</faultstring>', body)
    msg = fault.group(1) if fault else body[:300]
    print(f"HTTP {e.code}: {msg}")
    with open('auth_debug.txt', 'w') as f:
        f.write(f"User: {USERNAME}\nPW len: {len(PW_WITH_TOK)}\nHTTP {e.code}: {msg}\nBody: {body}")
    sys.exit(1)
except Exception as e:
    print(f"{type(e).__name__}: {e}")
    with open('auth_debug.txt', 'w') as f:
        f.write(f"Exception: {type(e).__name__}: {e}")
    sys.exit(1)
