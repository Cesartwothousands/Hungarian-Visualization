import numpy as np
from pointset import PointSet


class Hungarian:
    def __init__(self, matrix) -> None:
        self.matrix = np.array(matrix)
        self.sequence = []
        self.covered_colums = set()
        self.covered_row = set()
        self.starred_point = PointSet()
        self.primed_point_x2y = {}

    def full_covered(self):
        matrix = self.matrix
        for x in range(len(matrix)):
            for y in range(len(matrix[0])):
                if matrix[x][y] == 0:
                    if x not in self.covered_row and y not in self.covered_colums:
                        return False
        return True

    def snapshot(self):
        starred = []
        for tuple in self.starred_point:
            starred.append(tuple)
        primed = []
        for key in self.primed_point_x2y:
            primed.append((key, self.primed_point_x2y[key]))
        self.sequence.append({
            "matrix": self.matrix.copy(),
            "covered rows": self.covered_row.copy(),
            "covered colums": self.covered_colums.copy(),
            "starred_point": starred,
            "primed_point": primed,
        })
        # print(self.sequence[len(self.sequence)-1])

    def get_seq(self):
        return self.sequence

    def calculate(self):
        matrix = self.matrix
        cost = 0
        n = len(matrix)
        # Step 1 & 2
        min_rows = np.amin(matrix, axis=1, keepdims=True)
        matrix -= min_rows
        min_cols = np.amin(matrix, axis=0, keepdims=True)
        matrix -= min_cols
        cost += np.sum(min_cols)
        cost += np.sum(min_rows)
        self.snapshot()
        while len(self.covered_row) + len(self.covered_colums) < n:
            # Step 3
            # All zeros in the matrix must be covered by marking as few rows and/or columns as possible
            # assign as many as possible
            self.starred_point = PointSet()
            # primed point can be on the same column cannot use pointset
            # but primed point only has a x->y mapping, so can use a dict to replace
            self.primed_point_x2y = {}
            self.covered_colums = set()
            self.covered_row = set()
            find = False
            while not find:
                for x in range(n):
                    for y in range(n):
                        if matrix[x][y] == 0 and not self.starred_point.contains_x(
                                x) and not self.starred_point.contains_y(y):
                            self.starred_point.add_point((x, y))
                            self.covered_colums.add(y)
                            break
                self.snapshot()
                # check if it is full covered
                if self.full_covered():
                    break
                # find a non-converted zero and prime it
                # if the zero is on the same row as the starred zero,cover the corresponding row and uncover the column of
                # the starred zero
                for x in range(n):
                    for y in range(n):
                        if matrix[x][y] == 0 and x not in self.covered_row and y not in self.covered_colums:
                            # prime it
                            self.primed_point_x2y[x] = y
                            self.snapshot()
                            # if a non covered zero is on the same row as a starred zero
                            if self.starred_point.contains_x(x):
                                # uncover the column
                                subx, suby = self.starred_point.get_by_x(x)
                                self.covered_colums.remove(suby)
                                # cover the row
                                self.covered_row.add(x)
                                self.snapshot()
                                # check if it is full covered
                                if self.full_covered():
                                    ## change the flag to break
                                    find = True
                                    break
                            else:
                                # has no assignment on its row
                                px = x
                                py = y
                                primed_on_path = []
                                starred_on_path = []
                                primed_on_path.append((px, py))
                                while True:
                                    # step1
                                    # find a starred zero on column
                                    if self.starred_point.contains_y(py):
                                        px, _ = self.starred_point.get_by_y(py)
                                        starred_on_path.append((px, py))
                                    else:
                                        break
                                    # step2
                                    # find a primed zero on row, there will always be one on row
                                    # if not px in self.primed_point_x2y:
                                    #    print(self.sequence)
                                    py = self.primed_point_x2y[px]
                                    primed_on_path.append((px, py))
                                # star all prime zero and remove all covered lines and prime zeros
                                self.covered_row = set()
                                self.covered_colums = set()
                                for px, py in starred_on_path:
                                    self.starred_point.remove_point((px, py))
                                for px, py in primed_on_path:
                                    self.starred_point.add_point((px, py))
                                self.primed_point_x2y = {}
                                # cover the columns of all prime zero
                                for px, py in self.starred_point:
                                    self.covered_colums.add(py)
                            if len(self.covered_row) + len(self.covered_colums) >= n:
                                # find the result
                                return self.starred_point

            # Step 4
            # for the left values, find the lowest , subtract from every unmarked element and add to every 
            # element covered by two lines
            if len(self.covered_row) + len(self.covered_colums) >= n:
                # find the result
                return self.starred_point
            min_val = matrix.max()
            for x in range(n):
                for y in range(n):
                    if x not in self.covered_row and y not in self.covered_colums:
                        min_val = min(min_val, matrix[x][y])
            cost += min_val
            for x in range(n):
                for y in range(n):
                    if x not in self.covered_row and y not in self.covered_colums:
                        matrix[x][y] -= min_val
                    if x in self.covered_row and y in self.covered_colums:
                        matrix[x][y] += min_val
            self.snapshot()
        return self.starred_point
