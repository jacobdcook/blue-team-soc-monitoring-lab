#!/bin/bash
# Setup script for Wazuh - generates certificates

echo "Setting up Wazuh certificates..."

# Create directories for certificates
mkdir -p ./config/wazuh_indexer/certs
mkdir -p ./config/wazuh_dashboard/certs
mkdir -p ./config/wazuh_manager/certs

echo "Certificate directories created."
echo "Note: The Wazuh containers will generate their own certificates on first run."
