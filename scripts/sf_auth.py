import urllib.request, os, re, sys

username = os.environ['SF_USERNAME']
password = os.environ['SF_PASSWORD'] + os.environ['SF_SECURITY_TOKEN']

print(f"Authenticating: {username}")

soap_body = """<?xml version="1.0" encoding="utf-8"?>
<env:Envelope xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:env="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:urn="urn:partner.soap.sforce.com">
  <env:Body>
    <urn:login>
      <urn:username>{username}</urn:username>
      <urn:password>{password}</urn:password>
    </urn:login>
  </env:Body>
</env:Envelope>""".format(username=username, password=password)

req = urllib.request.Request(
    "https://login.salesforce.com/services/Soap/u/59.0",
    data=soap_body.encode(),
    headers={"Content-Type": "text/xml; charset=UTF-8", "SOAPAction": "login"}
)

try:
    with urllib.request.urlopen(req, timeout=30) as r:
        body = r.read().decode()
        session = re.search(r'<sessionId>(.*?)</sessionId>', body)
        server  = re.search(r'<serverUrl>(.*?)</serverUrl>', body)
        if session and server:
            sid      = session.group(1)
            srv_url  = server.group(1)
            instance = re.search(r'https://([^/]+)', srv_url).group(1)
            print(f"SUCCESS: {instance}")
            sfdx_url = f"force://PlatformCLI::{sid}@{instance}"
            with open('/tmp/sfdx_auth_url.txt', 'w') as f:
                f.write(sfdx_url)
            print("Auth file written")
            sys.exit(0)
        else:
            print(f"No session in response: {body[:300]}")
            sys.exit(1)
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}: {e.read().decode()[:300]}")
    sys.exit(1)
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
    sys.exit(1)
