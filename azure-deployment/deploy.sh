#!/bin/bash

# Azure Container Apps deployment script for Novitai Patent MCP Server
# Usage: ./deploy.sh [environment] [resource-group] [location]

set -e

# Default values
ENVIRONMENT=${1:-dev}
RESOURCE_GROUP=${2:-novitai-patent-mcp-rg}
LOCATION=${3:-eastus2}
CONTAINER_REGISTRY=${4:-novitaiacr}
TEMPLATE_FILE="azure-container-apps.yml"
PARAMETERS_FILE="parameters.${ENVIRONMENT}.json"

echo "🚀 Deploying Novitai Patent MCP Server to Azure Container Apps"
echo "Environment: $ENVIRONMENT"
echo "Resource Group: $RESOURCE_GROUP"
echo "Location: $LOCATION"
echo "Container Registry: $CONTAINER_REGISTRY"
echo ""

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI is not installed. Please install it first."
    exit 1
fi

# Check if user is logged in
if ! az account show &> /dev/null; then
    echo "❌ Please log in to Azure CLI first: az login"
    exit 1
fi

# Create resource group if it doesn't exist
echo "📦 Creating resource group if it doesn't exist..."
az group create --name $RESOURCE_GROUP --location $LOCATION --output table

# Create container registry if it doesn't exist
echo "🐳 Creating container registry if it doesn't exist..."
az acr create --name $CONTAINER_REGISTRY --resource-group $RESOURCE_GROUP --sku Basic --admin-enabled true --output table

# Build and push Docker image
echo "🔨 Building and pushing Docker image..."
az acr build --registry $CONTAINER_REGISTRY --image novitai-patent-mcp:$ENVIRONMENT --file ../Dockerfile ../

# Deploy the container app
echo "🚀 Deploying container app..."
az deployment group create \
    --resource-group $RESOURCE_GROUP \
    --template-file $TEMPLATE_FILE \
    --parameters @$PARAMETERS_FILE \
    --parameters containerRegistryName=$CONTAINER_REGISTRY \
    --output table

# Get the app URL
echo "🔗 Getting application URL..."
APP_URL=$(az containerapp show --name novitai-patent-mcp-$ENVIRONMENT --resource-group $RESOURCE_GROUP --query "properties.configuration.ingress.fqdn" -o tsv)

echo ""
echo "✅ Deployment completed successfully!"
echo "🌐 Application URL: https://$APP_URL"
echo "🔍 Health check: https://$APP_URL/health"
echo "📚 MCP endpoint: https://$APP_URL/mcp"
echo ""
echo "📋 Next steps:"
echo "1. Update your MCP client to use: https://$APP_URL/mcp"
echo "2. Configure your environment variables in Azure Container Apps"
echo "3. Test the health endpoint to ensure the service is running"
echo ""
echo "🔧 To view logs:"
echo "az containerapp logs show --name novitai-patent-mcp-$ENVIRONMENT --resource-group $RESOURCE_GROUP --follow"




