rb:
	python -m pip install .

test:
	python tests/test_bus.py

atest:
	python tests/async_test_bus.py
