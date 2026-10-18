#!/bin/sh
# Regenerate test/fixtures/ from the PINNED contract (never hand-edit them).
set -eu
cd "$(dirname "$0")/.."
TOOL="python3 ../../tools/capitalix_contract.py"
$TOOL verify
mkdir -p test/fixtures
$TOOL sample owner.sales.customer-balances --status 200 > test/fixtures/customer-balances.200.json
$TOOL sample owner.sales.customer-balances --status 401 > test/fixtures/customer-balances.401.json
$TOOL sample owner.sales.customers.store   --status 201 > test/fixtures/customers.store.201.json
$TOOL sample owner.sales.customers.store   --status 422 > test/fixtures/customers.store.422.json
$TOOL sample owner.sales.customers.store   --status 409 > test/fixtures/customers.store.409.json
$TOOL sample owner.sales.customers.update  --status 200 > test/fixtures/customers.update.200.json
$TOOL sample owner.sales.customers.destroy --status 200 > test/fixtures/customers.destroy.200.json
$TOOL sample auth.login                    --status 201 > test/fixtures/auth.login.201.json
echo "fixtures regenerated from $(python3 -c 'import json;print(json.load(open(".capitalix-contract/contract.lock"))["version"])')"
