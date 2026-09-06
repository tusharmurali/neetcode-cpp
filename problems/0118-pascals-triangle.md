# 118. Pascals Triangle

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/pascals-triangle/>  
- **NeetCode:** <https://neetcode.io/problems/pascals-triangle>  
- **Video:** <https://www.youtube.com/watch?v=nPVEaB3AjUM>  

[← Back to index](../INDEX.md)

## 1. Combinatorics

Each element in Pascal's Triangle corresponds to a binomial coefficient. The value at row `n` and position `k` is `C(n, k)`. Rather than computing each coefficient from scratch using factorials, we can compute them incrementally. Starting from `1`, each subsequent value in a row can be derived by multiplying by `(n - k + 1) / k`.

```cpp
class Solution {
public:
    vector<vector<int>> generate(int numRows) {
        vector<vector<int>> res;
        for (int n = 0; n < numRows; n++) {
            vector<int> row;
            row.push_back(1);
            int val = 1;
            for (int k = 1; k <= n; k++) {
                val = val * (n - k + 1) / k;
                row.push_back(val);
            }
            res.push_back(row);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## 2. Dynamic Programming - I

Each element in Pascal's Triangle (except the edges) is the sum of the two elements directly above it. We can simulate this by padding the previous row with zeros on both ends, then summing adjacent pairs to generate the next row.

```cpp
class Solution {
public:
    vector<vector<int>> generate(int numRows) {
        vector<vector<int>> res = {{1}};

        for (int i = 0; i < numRows - 1; i++) {
            vector<int> temp = {0};
            temp.insert(temp.end(), res.back().begin(), res.back().end());
            temp.push_back(0);
            vector<int> row;
            for (size_t j = 0; j < res.back().size() + 1; j++) {
                row.push_back(temp[j] + temp[j + 1]);
            }
            res.push_back(row);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## 3. Dynamic Programming - II

We directly apply the defining property of Pascal's Triangle: each interior element equals the sum of the two elements above it. The first and last elements of every row are always `1`. We build row by row, referencing the previous row for the sums.

```cpp
class Solution {
public:
    vector<vector<int>> generate(int numRows) {
        vector<vector<int>> res(numRows);

        for (int i = 0; i < numRows; i++) {
            res[i].resize(i + 1);
            res[i][0] = res[i][i] = 1;
            for (int j = 1; j < i; j++){
                res[i][j] = res[i - 1][j - 1] + res[i - 1][j];
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## Standalone solution file (`cpp/0118-pascals-triangle.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    vector<vector<int>> generate(int numRows)
    {
        vector<vector<int>> ret;

        for(int i = 0; i < numRows ; i++){
            vector<int> row(i+1, 1);
            for(int j = 1; j < i ; j++){
                row[j] = ret[i-1][j] + ret[i-1][j-1];
            }
            ret.push_back(row);
        }

        return ret;
    }
};
```
