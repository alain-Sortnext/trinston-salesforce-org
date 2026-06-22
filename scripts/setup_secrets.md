# GitHub Secrets Setup — Trinston Salesforce Deploy

Go to: https://github.com/alain-Sortnext/backend-simulation-starter/settings/secrets/actions

Add these 4 secrets:

## Secret 1: SF_SFDX_AUTH_URL
Run this command on your local machine (with sf cli installed):
```
sf org login web --instance-url https://orgfarm-709b3a2059-dev-ed.develop.my.salesforce.com --alias trinston-dev
sf org display --target-org trinston-dev --verbose --json
```
Copy the value of `sfdxAuthUrl` from the JSON output.
It looks like: `force://PlatformCLI::LONG_TOKEN@orgfarm-709b3a2059-dev-ed.develop.my.salesforce.com`

## Secret 2: SF_INSTANCE_URL
```
https://orgfarm-709b3a2059-dev-ed.develop.my.salesforce.com
```

## Secret 3: SF_USERNAME
```
mavadufashion.7880dc71777c@agentforce.com
```

## Secret 4: SF_CONSUMER_KEY
```
3MVG97L7PWbPq6UwlCtAjpkLOb9IMu3D2ZEMq0KSpMAcQoQRygtORv8ASzK1Ze0R0tt7ZV7TQmi9nrEQ3Qicf
```

Once all 4 secrets are added:
1. Go to: https://github.com/alain-Sortnext/backend-simulation-starter/actions
2. Click "Deploy Trinston Salesforce Org"
3. Click "Run workflow"
4. Select "true" for deploy_data
5. Click "Run workflow"

The workflow takes approximately 15-20 minutes to complete.
