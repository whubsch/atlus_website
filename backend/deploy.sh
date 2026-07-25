#!/bin/bash

# Atlus API Deployment Script for AWS Lambda
# Usage: ./deploy.sh [stage]
# Example: ./deploy.sh prod

set -e  # Exit on error

STAGE=${1:-prod}
REGION="us-east-1"
STACK_NAME="atlus-api-${STAGE}"

echo "=========================================="
echo "Deploying Atlus API to AWS Lambda"
echo "Stage: ${STAGE}"
echo "Region: ${REGION}"
echo "=========================================="

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "Error: AWS CLI is not installed. Please install it first."
    exit 1
fi

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "Error: uv is not installed. Please install it first."
    echo "Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Ensure SAM CLI is available, installing it via uv if necessary.
#
# We use `uv tool` rather than relying on a pre-installed global `sam` (or
# plain `pip install aws-sam-cli`) because it manages an isolated environment
# for the CLI without touching the project's own dependencies. We also pin
# `cryptography<44` here: aws-sam-cli's dependency chain (via pyopenssl) can
# otherwise resolve to a `cryptography` release with no prebuilt wheel for
# some platforms (notably macOS x86_64), which forces a from-source build
# that requires a fully licensed Xcode toolchain. Pinning to an older,
# widely-wheeled release avoids that entirely. We also add `botocore[crt]`,
# which SAM's "login" credential provider requires for `sam deploy`.
if ! command -v sam &> /dev/null; then
    echo "SAM CLI not found. Installing via uv..."
    uv tool install aws-sam-cli --with "cryptography<44" --with "botocore[crt]"
    export PATH="$(uv tool dir --bin):$PATH"
    if ! command -v sam &> /dev/null; then
        echo "Error: SAM CLI installation via uv did not put 'sam' on PATH."
        echo "Run 'uv tool update-shell' (or add ~/.local/bin to PATH) and re-run this script."
        exit 1
    fi
    echo "✓ SAM CLI installed"
elif uv tool list 2>/dev/null | grep -q '^aws-sam-cli'; then
    # SAM CLI is already on PATH via `uv tool`, but if it was installed by
    # an older version of this script (before `botocore[crt]` was added),
    # `sam deploy` fails with a missing dependency error. Re-run the
    # install to make sure the extra is present; this is a fast no-op if
    # it already is.
    uv tool install aws-sam-cli --with "cryptography<44" --with "botocore[crt]" &> /dev/null
fi

# Validate AWS credentials
echo "Validating AWS credentials..."
aws sts get-caller-identity --region ${REGION} > /dev/null
echo "✓ AWS credentials validated"

# Regenerate requirements.txt from the uv lockfile for the Lambda build
echo ""
echo "Exporting dependencies from uv.lock..."
(cd "$(dirname "$0")/.." && uv export --package backend --no-hashes --no-dev --no-editable -o backend/requirements.txt)
echo "✓ requirements.txt updated"

# Build the application
echo ""
echo "Building application..."
sam build --region ${REGION}
echo "✓ Build complete"

# Deploy the application
echo ""
echo "Deploying to AWS..."
sam deploy \
    --stack-name ${STACK_NAME} \
    --region ${REGION} \
    --capabilities CAPABILITY_IAM \
    --parameter-overrides StageName=${STAGE} \
    --no-fail-on-empty-changeset \
    --resolve-s3

echo ""
echo "=========================================="
echo "✓ Deployment complete!"
echo "=========================================="
echo ""
echo "Getting API URL..."
API_URL=$(aws cloudformation describe-stacks --stack-name ${STACK_NAME} --region ${REGION} --query "Stacks[0].Outputs[?OutputKey=='ApiUrl'].OutputValue" --output text 2>/dev/null || echo "")

if [ -n "$API_URL" ]; then
    echo "API URL: ${API_URL}"
    echo ""
    echo "Test your API with:"
    echo "  curl ${API_URL}meta"
else
    echo "Note: Retrieve your API URL with:"
    echo "  aws cloudformation describe-stacks --stack-name ${STACK_NAME} --region ${REGION}"
fi

echo ""
echo "View logs with:"
echo "  sam logs --stack-name ${STACK_NAME} --region ${REGION} --tail"
