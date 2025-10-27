# Deployment Guide

## Azure Container Apps Deployment

### Prerequisites

1. **Azure CLI** installed and configured
2. **Docker** installed for building images
3. **Azure Container Registry (ACR)** created
4. **Azure Container Apps Environment** created
5. All **API keys** from `.env` file

### Step 1: Build and Push Docker Image

```bash
# Login to Azure Container Registry
az acr login --name novitaiacr

# Build the image
docker build -t novitaiacr.azurecr.io/novitai-patent-mcp-fastmcp:dev .

# Push to ACR
docker push novitaiacr.azurecr.io/novitai-patent-mcp-fastmcp:dev
```

### Step 2: Update Parameters File

Edit `azure-deployment/parameters.fastmcp.json`:

```json
{
  "containerRegistryName": {
    "value": "novitaiacr"  // Your ACR name
  },
  "azureOpenAIEndpoint": {
    "value": "https://your-resource.openai.azure.com/"
  },
  "azureOpenAIDeploymentName": {
    "value": "gpt-4"  // Or your deployment name
  },
  // ... add all other secrets
}
```

### Step 3: Deploy to Azure Container Apps

```bash
# Navigate to deployment directory
cd azure-deployment

# Deploy
az deployment group create \
  --resource-group novitai-patent-mcp-rg \
  --template-file azure-container-apps-fastmcp.yml \
  --parameters @parameters.fastmcp.json
```

### Step 4: Get the URL

After deployment, get the app URL:

```bash
az containerapp show \
  --name novitai-patent-mcp \
  --resource-group novitai-patent-mcp-rg \
  --query properties.configuration.ingress.fqdn \
  -o tsv
```

### Configuration Differences

#### FastMCP Server Changes:
- **Port**: 8003 (changed from 8001)
- **Environment Variables**: Added `AZURE_OPENAI_DEPLOYMENT_NAME`
- **Health Check**: Updated to use correct port
- **Image Tag**: `novitai-patent-mcp-fastmcp:dev`

### Health Check

The server includes a health check endpoint:

```bash
curl https://your-app.azurecontainerapps.io/health
```

### Monitoring

View logs in Azure Portal or via CLI:

```bash
# Get live logs
az containerapp logs show \
  --name novitai-patent-mcp \
  --resource-group novitai-patent-mcp-rg \
  --follow
```

## Local Testing

Test locally first:

```bash
# Build and run
docker build -t novitai-fastmcp:local .
docker run -p 8003:8003 --env-file .env novitai-fastmcp:local

# Test endpoint
curl http://localhost:8003/health
```

## Troubleshooting

### Common Issues

1. **Container won't start**
   - Check logs: `az containerapp logs show --name novitai-patent-mcp --resource-group novitai-patent-mcp-rg`
   - Verify all environment variables are set
   - Check API keys are correct

2. **Image pull failed**
   - Ensure ACR credentials are correct
   - Verify image exists: `az acr repository list --name novitaiacr`

3. **Connection refused**
   - Check targetPort matches container port (8003)
   - Verify ingress is enabled and external

### Environment Variables

Required variables (set in deployment):
- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_DEPLOYMENT_NAME`
- `GOOGLE_API_KEY`
- `GOOGLE_CSE_ID`
- `PATENTSVIEW_API_KEY`

Optional variables:
- `LOG_LEVEL` (default: INFO)
- `ENVIRONMENT` (dev/staging/prod)

