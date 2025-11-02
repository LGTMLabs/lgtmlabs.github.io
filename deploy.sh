#!/bin/bash

# LGTM Labs SFTP Deployment Script
# Configure these variables with your Gandi.net SFTP credentials

SFTP_HOST="your-sftp-host.gandi.net"
SFTP_USER="your-username"
SFTP_PORT="22"
REMOTE_DIR="/path/to/web/root"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}LGTM Labs Deployment Script${NC}"
echo "================================"

# Check if credentials are configured
if [ "$SFTP_HOST" = "your-sftp-host.gandi.net" ]; then
    echo -e "${RED}Error: Please configure your SFTP credentials in deploy.sh${NC}"
    echo "Edit the following variables:"
    echo "  SFTP_HOST - Your Gandi.net SFTP hostname"
    echo "  SFTP_USER - Your SFTP username"
    echo "  REMOTE_DIR - Remote directory path"
    exit 1
fi

# Files to deploy
FILES=(
    "index.html"
    "style.css"
    "favicon.svg"
)

echo -e "${YELLOW}Deploying to: $SFTP_HOST${NC}"
echo -e "${YELLOW}Remote directory: $REMOTE_DIR${NC}"
echo ""

# Create SFTP batch file
BATCH_FILE=$(mktemp)
echo "cd $REMOTE_DIR" > $BATCH_FILE

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "put $file" >> $BATCH_FILE
        echo -e "  Uploading: ${GREEN}$file${NC}"
    else
        echo -e "  ${RED}Warning: $file not found${NC}"
    fi
done

echo "bye" >> $BATCH_FILE

# Execute SFTP upload
echo ""
echo "Starting SFTP transfer..."
sftp -P $SFTP_PORT -b $BATCH_FILE $SFTP_USER@$SFTP_HOST

# Check if deployment was successful
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓ Deployment completed successfully!${NC}"
    echo -e "Your site should be live at your configured domain."
else
    echo ""
    echo -e "${RED}✗ Deployment failed. Please check your credentials and connection.${NC}"
fi

# Clean up temp file
rm -f $BATCH_FILE

echo ""
echo "================================"
echo -e "${GREEN}LGTM Labs - Quality Engineering${NC}"