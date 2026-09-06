# 1260. Shift 2D Grid

- **Difficulty:** Easy  
- **Pattern:** Math & Geometry  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/shift-2d-grid/>  
- **NeetCode:** <https://neetcode.io/problems/shift-2d-grid>  
- **Video:** <https://www.youtube.com/watch?v=nJYFh4Dl-as>  

[← Back to index](../INDEX.md)

## 1. Simulation (Extra Space)

Shifting a 2D grid is like rotating all elements forward by one position. Each element moves to the next column, and elements at the end of a row wrap around to the start of the next row. The last element of the grid wraps to position (0, 0).

By simulating this process k times, we can achieve the desired result. For each shift, we copy each element to its new position in a fresh grid.

```cpp
class Solution {
public:
    vector<vector<int>> shiftGrid(vector<vector<int>>& grid, int k) {
        int m = grid.size(), n = grid[0].size();

        while (k > 0) {
            vector<vector<int>> cur(m, vector<int>(n, 0));

            for (int r = 0; r < m; r++) {
                for (int c = 0; c < n - 1; c++) {
                    cur[r][c + 1] = grid[r][c];
                }
            }

            for (int r = 0; r < m; r++) {
                cur[(r + 1) % m][0] = grid[r][n - 1];
            }

            grid = cur;
            k--;
        }

        return grid;
    }
};
```

**Complexity**

- Time complexity: $O(k * m * n)$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows in the grid, $n$ is the number of columns in the grid, and $k$ is the shift count.

## 2. Simulation

Instead of creating a new grid each time, we can shift elements in place. The key insight is that shifting works like a rotation: each element takes the place of the previous one. By keeping track of the last element (which wraps to the first position), we can propagate values through the entire grid in a single pass.

```cpp
class Solution {
public:
    vector<vector<int>> shiftGrid(vector<vector<int>>& grid, int k) {
        int m = grid.size(), n = grid[0].size();

        while (k > 0) {
            int prev = grid[m - 1][n - 1];
            for (int r = 0; r < m; r++) {
                for (int c = 0; c < n; c++) {
                    swap(grid[r][c], prev);
                }
            }
            k--;
        }

        return grid;
    }
};
```

**Complexity**

- Time complexity: $O(k * m * n)$
- Space complexity: $O(m * n)$ for the output matrix.

> Where $m$ is the number of rows in the grid, $n$ is the number of columns in the grid, and $k$ is the shift count.

## 3. Convert to One Dimensional Array

A 2D grid can be viewed as a 1D array if we flatten it row by row. Shifting in a 1D array is simply rotating elements to the right. The classic way to rotate an array by k positions is to use three reversals: reverse the entire array, then reverse the first k elements, then reverse the remaining elements.

```cpp
class Solution {
public:
    vector<vector<int>> shiftGrid(vector<vector<int>>& grid, int k) {
        int m = grid.size(), n = grid[0].size();
        int N = m * n;
        k %= N;

        vector<int> arr(N);
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                arr[r * n + c] = grid[r][c];
            }
        }

        reverse(arr.begin(), arr.end());
        reverse(arr.begin(), arr.begin() + k);
        reverse(arr.begin() + k, arr.end());

        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                grid[r][c] = arr[r * n + c];
            }
        }

        return grid;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows in the grid and $n$ is the number of columns in the grid.

## 4. Iteration

Instead of actually shifting elements, we can compute where each element should go after k shifts. The position of an element in a flattened grid is `r * n + c`. After k shifts, this becomes `(r * n + c + k) % (m * n)`. We can then convert this back to 2D coordinates.

This approach processes each element exactly once, computing its final position directly.

```cpp
class Solution {
public:
    vector<vector<int>> shiftGrid(vector<vector<int>>& grid, int k) {
        int M = grid.size(), N = grid[0].size();
        vector<vector<int>> res(M, vector<int>(N));

        for (int r = 0; r < M; r++) {
            for (int c = 0; c < N; c++) {
                int newVal = (r * N + c + k) % (M * N);
                int newR = newVal / N, newC = newVal % N;
                res[newR][newC] = grid[r][c];
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows in the grid and $n$ is the number of columns in the grid.

## Standalone solution file (`cpp/1260-shift-2d-grid.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    vector<vector<int>> shiftGrid(vector<vector<int>>& grid, int k) {
        const int M = grid.size(), N = grid[0].size();
        
        auto posToVal = [&] (int r, int c) -> int {
            return r * N + c;};
        auto valToPos = [&] (int v) -> int* {
            return new int[] {v / N, v % N};};
        
        vector<vector<int>> res;
        for(int r = 0; r < M; r++) {
            vector<int> row;
            for(int c = 0; c < N; c++)
                row.push_back(0);
            res.push_back(row);
        }
        for(int r = 0; r < M; r++)
            for(int c = 0; c < N; c++) {
                int newVal = (posToVal(r, c) + k) % (M * N);
                int *newRC = valToPos(newVal);
                res[newRC[0]][newRC[1]] = grid[r][c];
            }
        return res;
    }
};
```
