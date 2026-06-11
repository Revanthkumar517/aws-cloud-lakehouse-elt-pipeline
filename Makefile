.PHONY: setup generate validate upload terraform-init terraform-validate terraform-plan dbt-run dbt-test clean

setup:
	python -m venv .venv
	.venv\Scripts\pip install -r requirements.txt

generate:
	python data_generator/generate_mock_data.py

validate:
	python quality/validate_raw_orders.py

upload:
	python scripts/upload_to_s3.py

terraform-init:
	cd terraform && terraform init

terraform-validate:
	cd terraform && terraform validate

terraform-plan:
	cd terraform && terraform plan

dbt-run:
	cd dbt/aws_lakehouse_dbt_project && dbt run

dbt-test:
	cd dbt/aws_lakehouse_dbt_project && dbt test

clean:
	python -c "import shutil, pathlib; p=pathlib.Path('data/raw'); shutil.rmtree(p, ignore_errors=True)"
