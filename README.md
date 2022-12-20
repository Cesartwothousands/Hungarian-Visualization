# Hungarian Algorithm Visuallization
## Package Requirement
version (not required to be the same)
```
python>=3.7
numpy>=1.23.1
streamlit>=1.15.0
pandas>=1.4.3
networkx
matplotlib
```
install
```
pip install numpy 
pip install pandas
pip install streamlit
pip install networkx
pip install matplotlib
```
## Run Visualization
### Jonker-Volgenant algorithm
core algorithm at `algorithm\hungarian.py`, using `streamlit` for visualization.

open this project directory in command line
```
streamlit run .\visualization\hungarian_test.py
```
visit the application at `http://localhost:8501/`
### N3 Graph Solution
core algorithm at `algorithm\n3.py`, using `matplotlib` and `networkx` for visualization.

run `visualization\n3vis.py`
### N4 Graph Solution
core algorithm at `algorithm\n4.py`, using `matplotlib` and `networkx` for visualization.

run `visualization\n4vis.py`
## Test Algorithm
run `test\randomtest.py` for algorithm correctness

run `test\timetest.py` for time analysis

## To Do
- [x] compare performance with $n^3$ implementation and $n^4$ implementation
- [x] implement the $n^3$ implementation
- [x] compare the result with scipy's implementation, ensure that the code is bug-free
- [x] add more complex visualization support
- [x] add n3Graph implementation random test