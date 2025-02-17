.PHONY: help run-scan run-summary

help:
	@echo "Targets: run-scan, run-summary"

run-scan:
	python -m loginsight scan scripts/sample.log --pattern ERROR

run-summary:
	python -m loginsight summary scripts/sample.log --bucket hour

