clean:
	find . -name "*.pyc" -type f -delete
	find . -name "*.pyo" -type f -delete
	find . -name "*.db" -type f -delete

test: clean
	python -m unittest discover tests/

build: clean test
	docker build -t "cynthek/robotrss:latest" .
