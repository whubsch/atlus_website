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

# Check if SAM CLI is installed
if ! command -v sam &> /dev/null; then
    echo "Error: AWS SAM CLI is not installed. Please install it first."
    echo "Install with: pip install aws-sam-cli"
    exit 1
fi

# Validate AWS credentials
echo "Validating AWS credentials..."
aws sts get-caller-identity --region ${REGION} > /dev/null
echo "✓ AWS credentials validated"

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
    echo "  curl ${API_URL}api/meta"
else
    echo "Note: Retrieve your API URL with:"
    echo "  aws cloudformation describe-stacks --stack-name ${STACK_NAME} --region ${REGION}"
fi

echo ""
echo "View logs with:"
echo "  sam logs --stack-name ${STACK_NAME} --region ${REGION} --tail"
