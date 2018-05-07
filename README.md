# Life and Death Bot

[Riddles.io API](https://docs.riddles.io/game-of-life-and-death/api)


## To install
This project recommends using `pipenv`

In the project folder, simply run
```
pipenv install
```


### Commands
```
./bin/run.sh
./bin/test.sh
./bin/benchmark.sh
./bin/build.sh
```
##  TODO

### Optimize and Benchmark
Numpy needs to be utilized wherever possible to speed up everything
A numpy method in place of a native python iterator over the board sped up
the function call by **1000%**

### Prune getMoves to not count useless actions:

#### Ignore 'kill' actions where it's neighbors neighbor count is less than 3.

for example, the one in the middle need not be explored to kill:

Board:
```
0 1 0 0 1
0 0 0 0 0
0 0 1 0 0
1 0 0 0 1
0 0 0 0 0
```

Neighbors:
```
1 0 1 1 0
1 2 2 2 1
1 2 0 2 1
0 2 1 2 0
1 1 0 1 1
```

Since the cell only neighbors cells with a 2 max, it can have no effect on the board.

Another Scenario:
Board:
```
0 0 0 0 0
0 0 0 0 1
0 0 1 0 0
0 0 0 0 1
0 0 0 0 0
```

Neighbors:
```
0 0 0 1 1
0 1 1 2 0
0 1 0 3 2
0 1 1 2 0
0 0 0 1 1
```

Since this cell has max 3 on it's surrounding neighbors, it must be considered to be killed or not

#### Birth Optimizing
Likewise, cells that have max neighbor count of 2 do not need to be considered to birth to.
Cells that are in these regions should be first picks for sacrificing.
