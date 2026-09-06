# 1572. Matrix Diagonal Sum

- **Difficulty:** Easy  
- **Pattern:** Math & Geometry  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/matrix-diagonal-sum/>  
- **NeetCode:** <https://neetcode.io/problems/matrix-diagonal-sum>  
- **Video:** <https://www.youtube.com/watch?v=WliTu6gIK7o>  

[← Back to index](../INDEX.md)

## 1. Iteration

The matrix has two diagonals: the primary diagonal (top-left to bottom-right) and the secondary diagonal (top-right to bottom-left). We can collect elements from both diagonals by reversing each row after processing the primary diagonal, then processing it again. The center element appears on both diagonals for odd-sized matrices, so we subtract it once to avoid double-counting.

```cpp
class Solution {
public:
    int diagonalSum(vector<vector<int>>& mat) {
        int n = mat.size();
        return helper(mat) + helper(mat) - (n % 2 == 1 ? mat[n / 2][n / 2] : 0);
    }

private:
    int helper(vector<vector<int>>& matrix) {
        int res = 0, n = matrix.size();
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                if (i == j) {
                    res += matrix[i][j];
                }
            }
            reverse(matrix[i].begin(), matrix[i].end());
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$ extra space.

## 2. Iteration (Optimal)

We can directly compute both diagonal sums in a single pass. For row `r`, the primary diagonal element is at column `r`, and the secondary diagonal element is at column `n - r - 1`. We simply add both for each row. When `n` is odd, the center element (at row `n / 2`, column `n / 2`) is counted twice, so we subtract it once at the end.

```cpp
class Solution {
public:
    int diagonalSum(vector<vector<int>>& mat) {
        int res = 0, n = mat.size();

        for (int r = 0; r < n; r++) {
            res += mat[r][r];
            res += mat[r][n - r - 1];
        }

        return res - (n % 2 == 1 ? mat[n / 2][n / 2] : 0);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.
