#!/usr/bin/bash
pre-commit install

# MinIO Iceberg Warehouse bucket and user
mc alias set local http://minio:9000 minio_root_user minio_root_password
mc admin info local
mc mb --ignore-existing local/iceberg-warehouse
mc admin user add local iceberg_user iceberg_password
mc admin policy attach local readwrite --user iceberg_user || echo "NOTE: mc command shows error if policy is re-attached, so don't worry."
