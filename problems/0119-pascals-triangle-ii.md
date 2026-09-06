# 119. Pascal's Triangle II

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/pascals-triangle-ii/>  
- **NeetCode:** <https://neetcode.io/problems/pascals-triangle-ii>  
- **Video:** <https://www.youtube.com/watch?v=k1DNTyal77I>  

[← Back to index](../INDEX.md)

## 1. Dynamic Programming (Top-Down)

To get row `n`, we need row `n - 1` first. Each row depends on the previous one, with interior elements being the sum of two adjacent elements from above. Recursion naturally models this dependency: we compute the previous row, then build the current row from it.

```cpp
class Solution {
public:
    vector<int> getRow(int rowIndex) {
        if (rowIndex == 0) return {1};

        vector<int> curRow = {1};
        vector<int> prevRow = getRow(rowIndex - 1);

        for (int i = 1; i < rowIndex; i++) {
            curRow.push_back(prevRow[i - 1] + prevRow[i]);
        }

        curRow.push_back(1);
        return curRow;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 2. Dynamic Programming (Bottom-Up)

We build the entire triangle iteratively from row 0 up to the target row. Each row is constructed using values from the previous row. Though we store all rows, we only need the last one as our answer.

```cpp
class Solution {
public:
    vector<int> getRow(int rowIndex) {
        vector<vector<int>> res(rowIndex + 1);
        for (int i = 0; i <= rowIndex; i++) {
            res[i] = vector<int>(i + 1, 1);
            for (int j = 1; j < i; j++) {
                res[i][j] = res[i - 1][j - 1] + res[i - 1][j];
            }
        }
        return res[rowIndex];
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## 3. Dynamic Programming (Space Optimized - I)

We only need the previous row to compute the current row, so we don't need to store the entire triangle. We keep one row at a time and build the next row by adding contributions from adjacent elements.

```cpp
class Solution {
public:
    vector<int> getRow(int rowIndex) {
        vector<int> res = {1};
        for (int i = 0; i < rowIndex; i++) {
            vector<int> nextRow(res.size() + 1, 0);
            for (int j = 0; j < res.size(); j++) {
                nextRow[j] += res[j];
                nextRow[j + 1] += res[j];
            }
            res = nextRow;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 4. Dynamic Programming (Space Optimized - II)

We can update the row in place by iterating from right to left. This ensures we don't overwrite values we still need. Each element becomes the sum of itself and the element to its left, which matches how Pascal's Triangle is built.

```cpp
class Solution {
public:
    vector<int> getRow(int rowIndex) {
        vector<int> row(rowIndex + 1, 1);
        for (int i = 1; i < rowIndex; i++) {
            for (int j = i; j > 0; j--) {
                row[j] += row[j - 1];
            }
        }
        return row;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 5. Combinatorics

The values in row `n` of Pascal's Triangle are the binomial coefficients `C(n, 0)`, `C(n, 1)`, ..., `C(n, n)`. We can compute each coefficient incrementally from the previous one using the formula: `C(n, k) = C(n, k - 1) * (n - k + 1) / k`.

```cpp
class Solution {
public:
    vector<int> getRow(int rowIndex) {
        vector<int> row = {1};
        for (int i = 1; i <= rowIndex; i++) {
            row.push_back(int(row.back() * 1LL * (rowIndex - i + 1) / i));
        }
        return row;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$
