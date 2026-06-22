import urllib.request, urllib.parse, os, re, sys

username = os.environ.get('SF_USERNAME', '')
pw_only  = os.environ.get('SF_PASSWORD', '')
token    = os.environ.get('SF_SECURITY_TOKEN', '')
pw_token = os.environ.get('SF_PASSWORD_WITH_TOKEN', pw_only + token)

print(f"Username: {username}")
print(f"Trying 3 password combinations...")

def try_soap(password_str, label):
    soap = """<?xml version="1.0" encoding="utf-8"?>
<env:Envelope xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:env="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:urn="urn:partner.soap.sforce.com">
  <env:Body>
    <urn:login>
      <urn:username>""" + username + """</urn:username>
      <urn:password>""" + password_str + """</urn:password>
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
                session = re.search(r'<sessionId>(.*?)</sessionId>', body).group(1)
                server  = re.search(r'<serverUrl>(.*?)</serverUrl>', body).group(1)
                instance = re.search(r'https://([^/]+)', server).group(1)
                print(f"SUCCESS [{label}]: {instance}")
                sfdx_url = f"force://PlatformCLI::{session}@{instance}"
                with open('/tmp/sfdx_auth_url.txt', 'w') as f:
                    f.write(sfdx_url)
                return True
            else:
                fault = re.search(r'<faultstring>(.*?)</faultstring>', body)
                print(f"FAIL [{label}]: {fault.group(1) if fault else body[:200]}")
                return False
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        fault = re.search(r'<faultstring>(.*?)</faultstring>', body)
        print(f"HTTP {e.code} [{label}]: {fault.group(1) if fault else body[:200]}")
        return False
    except Exception as e:
        print(f"ERROR [{label}]: {type(e).__name__}: {e}")
        return False

if try_soap(pw_token, "password+token combined"):
    sys.exit(0)
if try_soap(pw_only, "password only"):
    sys.exit(0)
if try_soap(pw_only + token, "concatenated from separate secrets"):
    sys.exit(0)

print("All attempts failed")
sys.exit(1)
