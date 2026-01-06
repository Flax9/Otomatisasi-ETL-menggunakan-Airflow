#User Metadata
CREATE USER 'airflow_sys'@'%' IDENTIFIED BY 'sys_password_123';
GRANT ALL PRIVILEGES ON airflow_metadata.* TO 'airflow_sys'@'%';

#User ETL Worker
CREATE USER 'etl_worker_bpom'@'%' IDENTIFIED BY 'etl_password_456';
-- Akses Baca di Sumber
GRANT SELECT ON db_monitoring_bpom.* TO 'etl_worker_bpom'@'%';
-- Akses Tulis di Staging
GRANT ALL PRIVILEGES ON db_dashboard_bpom_staging.* TO 'etl_worker_bpom'@'%';

-- Terapkan perubahan
FLUSH PRIVILEGES;