run:
	python3 src/main.py -d ${ARGS}

test:
	cd test && python3 run_tests.py --verbose ${ARGS}

benchmark:
	cd test && python3 run_tests.py BenchmarkTest --verbose ${ARGS}

save-benchmark:
	mv test/benchmark-summary.json test/benchmark.json

zip:
	zip -r life-and-death-bot.zip src
	open https://starapple.riddles.io/competitions/game-of-life-and-death

profile:
	cd test && python3 profiler.py
	snakeviz profile

.PHONY: run test benchmark save-benchmark zip profile
