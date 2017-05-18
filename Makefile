TEST_FILES=test_behavior.py

test:
	MODULE=docker mtf $(TEST_FILES)

all: test
