clean:
	find . -name "*.pyc" -type f
	find . -name "*.pyo" -type f
	find . -name "*.pyc" -type f -delete
	find . -name "*.pyo" -type f -delete

test: clean
	python -m unittest discover tests/

build: clean test
	docker build -t "cynthek/robotrss:latest" .
