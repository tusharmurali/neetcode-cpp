# 1198. Find Smallest Common Element in All Rows

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/find-smallest-common-element-in-all-rows/>  
- **NeetCode:** <https://neetcode.io/problems/find-smallest-common-element-in-all-rows>  

[← Back to index](../INDEX.md)

## 1. Count Elements

An element is common to all rows if it appears exactly `n` times across the matrix (once per row, since rows are sorted). We can count occurrences of each element and then scan from smallest to largest to find the first element with count equal to `n`. This works because each row contains distinct elements in sorted order.

```cpp
class Solution {
public:
    int smallestCommonElement(vector<vector<int>>& mat) {
        int count[10001] = {};
        int n = mat.size(), m = mat[0].size();
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < m; ++j) {
                ++count[mat[i][j]];
            }
        }
        for (int k = 1; k <= 10000; ++k) {
            if (count[k] == n) {
                return k;
            }
        }
        return -1;
    }
};
```

## 2. Count Elements (Improved)

We can improve the average time complexity if we count elements column-by-column. This way, smaller elements will be counted first, and we can exit as soon as we get to an element that repeats `n` times.

```cpp
class Solution {
public:
    int smallestCommonElement(vector<vector<int>>& mat) {
        int count[10001] = {};
        int n = mat.size(), m = mat[0].size();
        for (int j = 0; j < m; ++j) {
            for (int i = 0; i < n; ++i) {
                if (++count[mat[i][j]] == n) {
                    return mat[i][j];
                }
            }
        }
        return -1;
    }
};
```

## 3. Binary Search

Since each row is sorted, we can use binary search to check if an element exists in a row. We iterate through the first row (which is already sorted from smallest to largest) and for each element, we binary search for it in all other rows. The first element found in all rows is our answer.

```cpp
class Solution {
    int smallestCommonElement(vector<vector<int>>& mat) {
        int n = mat.size(), m = mat[0].size();
        for (int j = 0; j < m; ++j) {
            bool found = true;
            for (int i = 1; i < n && found; ++i) {
                found = binary_search(begin(mat[i]), end(mat[i]), mat[0][j]);
            }
            if (found) {
                return mat[0][j];
            }
        }
        return -1;
    }
};
```

## 4. Binary Search (Improved)

In the solution above, we always search the entire row. We can improve the average time complexity if we start the next search from the position returned by the previous search. We can also return `-1` if all elements in the row are smaller than value we searched for.

```cpp
class Solution {
    int smallestCommonElement(vector<vector<int>>& mat) {
        int n = mat.size(), m = mat[0].size();
        vector<int> pos(n);
        for (int j = 0; j < m; ++j) {
            bool found = true;
            for (int i = 1; i < n && found; ++i) {
                pos[i] = lower_bound(begin(mat[i]) + pos[i], end(mat[i]), mat[0][j]) - begin(mat[i]);
                if (pos[i] >= m) {
                    return -1;
                }
                found = mat[i][pos[i]] == mat[0][j];
            }
            if (found) {
                return mat[0][j];
            }
        }
        return -1;
    }
};
```

## 5. Row Positions

We can use a two-pointer style approach across all rows. We maintain a `pos` pointer for each row and track the current maximum value seen. When we find a value smaller than the current max, we advance that row's pointer. If all rows have the same value at their current positions, we found our answer. If any row's pointer goes out of bounds, no common element exists.

```cpp
class Solution {
public:
    int smallestCommonElement(vector<vector<int>>& mat) {
        int n = mat.size(), m = mat[0].size();
        int cur_max = 0, cnt = 0;
        vector<int> pos(n);
        while (true) {
            for (int i = 0; i < n; ++i) {
                while (pos[i] < m && mat[i][pos[i]] < cur_max) {
                    ++pos[i];
                }
                if (pos[i] >= m) {
                    return -1;
                }
                if (cur_max != mat[i][pos[i]]) {
                    cnt = 1;
                    cur_max = mat[i][pos[i]];
                } else if (++cnt == n) {
                    return cur_max;
                }
            }
        }
        return -1;
    }
};
```
