# Atlus API Backend

FastAPI application deployed to AWS Lambda with API Gateway and custom domain.

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python lambda_handler.py

# API will be available at http://localhost:8000
# Docs at http://localhost:8000/docs
```

### Testing

```bash
# Run tests
python -m pytest

# Test specific endpoint locally
curl http://localhost:8000/meta
```

## Deployment

### Standard Deployment (After Initial Setup)

For routine code updates, use the simplified deployment:

```bash
# Build and deploy
sam build
sam deploy --stack-name atlus-api-prod --resolve-s3
```

This will update your existing Lambda function with new code while preserving all configuration.

### Full Deployment (With All Parameters)

Use this if you need to update domain or certificate settings:

```bash
sam build

sam deploy \
  --stack-name atlus-api-prod \
  --parameter-overrides \
    StageName=prod \
    CustomDomainName=api.atlus.dev \
    CertificateArn=arn:aws:acm:us-east-1:266672886316:certificate/74e50db6-6447-49e9-b63e-784a23343f6e \
  --capabilities CAPABILITY_IAM \
  --resolve-s3
```

### Using the Deploy Script

Alternatively, use the legacy deploy script (no custom domain parameters):

```bash
./deploy.sh prod
```

## API Endpoints

- **Production**: `https://api.atlus.dev`
- **Docs**: `https://api.atlus.dev/docs`
- **ReDoc**: `https://api.atlus.dev/redoc`
- **OpenAPI**: `https://api.atlus.dev/openapi.json`

### Main Endpoints

- `GET /meta` - API health check and version
- `POST /address/parse/` - Parse single address
- `POST /address/batch/` - Parse batch of addresses (max 10,000)
- `POST /phone/parse/` - Parse single phone number
- `POST /phone/batch/` - Parse batch of phone numbers (max 10,000)

## Common Tasks

### Viewing Logs

```bash
# Tail logs in real-time
sam logs --stack-name atlus-api-prod --tail

# View recent logs
sam logs --stack-name atlus-api-prod --start-time '10min ago'
```

### Testing Deployment

```bash
# Test meta endpoint
curl https://api.atlus.dev/meta

# Test address parsing
curl -X POST https://api.atlus.dev/address/parse/ \
  -H "Content-Type: application/json" \
  -d '{"address": "1600 Pennsylvania Ave NW, Washington, DC 20500"}'
```

### Updating Dependencies

```bash
# Update requirements.txt
pip install <package>
pip freeze > requirements.txt

# Deploy updated dependencies
sam build
sam deploy --stack-name atlus-api-prod --resolve-s3
```

### Updating Environment Variables

Edit `template.yaml` under the Lambda function's `Environment.Variables` section, then redeploy.

## Architecture

- **Lambda Function**: `atlus-api-prod` (512 MB, 30s timeout)
- **API Gateway**: REST API with CORS enabled
- **Custom Domain**: `api.atlus.dev` via CloudFront
- **Certificate**: ACM certificate in us-east-1
- **Runtime**: Python 3.12

## Custom Domain Configuration

### DNS Records (Namecheap)

| Type | Host | Value |
|------|------|-------|
| CNAME | api | `d3te59a4ae6p88.cloudfront.net` |
| CNAME | _validation | ACM validation record |

### Certificate

- **Domain**: `api.atlus.dev`
- **ARN**: `arn:aws:acm:us-east-1:266672886316:certificate/74e50db6-6447-49e9-b63e-784a23343f6e`
- **Region**: us-east-1 (required for API Gateway)

## Troubleshooting

### Deployment Fails

```bash
# Check CloudFormation events for errors
aws cloudformation describe-stack-events \
  --stack-name atlus-api-prod \
  --max-items 10

# Delete and recreate (last resort)
aws cloudformation delete-stack --stack-name atlus-api-prod
# Wait for deletion, then redeploy with full command
```

### Lambda Errors

```bash
# Check recent errors
sam logs --stack-name atlus-api-prod --filter "ERROR"

# Increase timeout or memory in template.yaml if needed
```

### CORS Issues

CORS is configured in `template.yaml` under `AtlusApiGateway.Cors` and in `app.py` via `CORSMiddleware`.

### Custom Domain Not Working

1. Verify DNS propagation: `dig api.atlus.dev`
2. Check certificate status in ACM console
3. Verify CloudFront distribution is deployed
4. Wait 15-30 minutes for DNS/CloudFront propagation

## Cost Monitoring

```bash
# Check Lambda invocations
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Invocations \
  --dimensions Name=FunctionName,Value=atlus-api-prod \
  --start-time $(date -u -d '7 days ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 86400 \
  --statistics Sum
```

## Stack Information

- **Stack Name**: `atlus-api-prod`
- **Region**: `us-east-1`
- **Template**: `template.yaml`
- **Handler**: `lambda_handler.handler`

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [AWS SAM Documentation](https://docs.aws.amazon.com/serverless-application-model/)
- [Mangum (ASGI adapter)](https://mangum.io/)
- [Atlus Python Package](https://github.com/whubsch/atlus/)
