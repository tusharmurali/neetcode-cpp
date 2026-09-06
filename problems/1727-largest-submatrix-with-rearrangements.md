# 1727. Largest Submatrix With Rearrangements

- **Difficulty:** Medium  
- **Pattern:** Math & Geometry  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/largest-submatrix-with-rearrangements/>  
- **NeetCode:** <https://neetcode.io/problems/largest-submatrix-with-rearrangements>  
- **Video:** <https://www.youtube.com/watch?v=NYyIVuSCfOA>  

[← Back to index](../INDEX.md)

## 1. Brute Force

We can rearrange columns in any order, so the key is to find which columns can form a rectangle of all `1`s. For each starting row, we track which columns have continuous `1`s from that row downward. As we extend the rectangle row by row, columns with a `0` are eliminated. The area at each step is the number of surviving columns multiplied by the current height.

```cpp
class Solution {
public:
    int largestSubmatrix(vector<vector<int>>& matrix) {
        int ROWS = matrix.size(), COLS = matrix[0].size();
        int res = 0;

        for (int startRow = 0; startRow < ROWS; startRow++) {
            queue<int> ones;
            for (int c = 0; c < COLS; c++) {
                ones.push(c);
            }

            for (int r = startRow; r < ROWS; r++) {
                if (ones.empty()) break;

                for (int i = ones.size(); i > 0; i--) {
                    int c = ones.front(); ones.pop();
                    if (matrix[r][c] == 1) {
                        ones.push(c);
                    }
                }

                res = max(res, (int)ones.size() * (r - startRow + 1));
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * n ^ 2)$
- Space complexity: $O(n)$

> Where $m$ is the number of rows and $n$ is the number of columns.

## 2. Greedy + Sorting

Think of each cell as the height of a bar extending upward through consecutive `1`s. For each row, compute these heights based on the previous row. Since we can rearrange columns, sort the heights in descending order. Then greedily compute the largest rectangle: the first column can use its full height, the first two columns are limited by the second height, and so on.

```cpp
class Solution {
public:
    int largestSubmatrix(vector<vector<int>>& matrix) {
        int ROWS = matrix.size(), COLS = matrix[0].size();
        int res = 0;
        vector<int> prevHeights(COLS);

        for (int r = 0; r < ROWS; r++) {
            vector<int> heights = matrix[r];
            vector<int> sortedHgts = matrix[r];

            for (int c = 0; c < COLS; c++) {
                if (heights[c] > 0) {
                    heights[c] += prevHeights[c];
                    sortedHgts[c] = heights[c];
                }
            }

            sort(sortedHgts.begin(), sortedHgts.end(), greater<int>());
            for (int i = 0; i < COLS; i++) {
                res = max(res, (i + 1) * sortedHgts[i]);
            }

            prevHeights = heights;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * n \log n)$
- Space complexity: $O(n)$

> Where $m$ is the number of rows and $n$ is the number of columns.

## 3. Greedy + Sorting (Overwriting the Input)

This is the same approach as above but optimizes space by modifying the input matrix directly. Each cell stores the cumulative height of consecutive `1`s ending at that cell. This eliminates the need for a separate heights array.

```cpp
class Solution {
public:
    int largestSubmatrix(vector<vector<int>>& matrix) {
        int ROWS = matrix.size(), COLS = matrix[0].size();
        int res = 0;

        for (int r = 1; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                if (matrix[r][c] > 0) {
                    matrix[r][c] += matrix[r - 1][c];
                }
            }
        }

        for (int r = 0; r < ROWS; r++) {
            sort(matrix[r].begin(), matrix[r].end(), greater<int>());
            for (int i = 0; i < COLS; i++) {
                res = max(res, (i + 1) * matrix[r][i]);
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algoirhtm.

> Where $m$ is the number of rows and $n$ is the number of columns.

## 4. Greedy

We can avoid sorting entirely by maintaining a sorted order implicitly. Track the column indices that had continuous `1`s from the previous row. For the current row, first process columns from the previous list (they have taller heights), then add new columns that just started with a `1`. This naturally keeps columns ordered by height in descending order.

```cpp
class Solution {
public:
    int largestSubmatrix(vector<vector<int>>& matrix) {
        int ROWS = matrix.size(), COLS = matrix[0].size(), res = 0;
        vector<int> prevHeights;

        for (int r = 0; r < ROWS; r++) {
            vector<int> heights;

            for (int c : prevHeights) {
                if (matrix[r][c] == 1) {
                    matrix[r][c] += matrix[r - 1][c];
                    heights.push_back(c);
                }
            }

            for (int c = 0; c < COLS; c++) {
                if (matrix[r][c] == 1) {
                    heights.push_back(c);
                }
            }

            for (int i = 0; i < heights.size(); i++) {
                res = max(res, (i + 1) * matrix[r][heights[i]]);
            }

            prevHeights = heights;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(n)$

> Where $m$ is the number of rows and $n$ is the number of columns.
