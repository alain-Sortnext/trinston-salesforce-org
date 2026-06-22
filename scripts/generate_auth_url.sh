#!/bin/bash
# Run this script LOCALLY on your machine to generate the SF_SFDX_AUTH_URL secret
# Prerequisites: sf cli installed (npm install -g @salesforce/cli)

echo "This script generates the Salesforce auth URL needed for GitHub Actions."
echo ""
echo "Step 1: Login to your Salesforce org"
sf org login web --instance-url https://orgfarm-709b3a2059-dev-ed.develop.my.salesforce.com --alias trinston-dev

echo ""
echo "Step 2: Your SFDX Auth URL (copy this EXACTLY for the GitHub secret SF_SFDX_AUTH_URL):"
sf org display --target-org trinston-dev --verbose --json | python3 -c "
import json, sys
data = json.load(sys.stdin)
url = data.get('result', {}).get('sfdxAuthUrl', 'NOT FOUND - try: sf org display --verbose')
print(url)
"

echo ""
echo "Step 3: Add this as GitHub Secret SF_SFDX_AUTH_URL at:"
echo "https://github.com/alain-Sortnext/backend-simulation-starter/settings/secrets/actions"
