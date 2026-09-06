# 48. Rotate Image

- **Difficulty:** Medium  
- **Pattern:** Math & Geometry  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/rotate-image/>  
- **NeetCode:** <https://neetcode.io/problems/rotate-matrix>  
- **Video:** <https://www.youtube.com/watch?v=fMSJSS7eO1w>  

[← Back to index](../INDEX.md)

## 1. Brute Force

We are given an `n x n` matrix and need to rotate it **90 degrees clockwise**.

A direct and beginner-friendly way to think about this is:

- create a **new matrix** where each element from the original matrix is placed in its rotated position
- after building this rotated version, copy it back into the original matrix

The key observation for a 90° clockwise rotation is:

- an element at position `(i, j)` in the original `matrix`
- moves to position `(j, n - 1 - i)` in the rotated `matrix`

By applying this rule to every cell, we can construct the rotated matrix easily.

```cpp
class Solution {
public:
    void rotate(vector<vector<int>>& matrix) {
        int n = matrix.size();
        vector<vector<int>> rotated(n, vector<int>(n));

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                rotated[j][n - 1 - i] = matrix[i][j];
            }
        }

        matrix = rotated;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## 2. Rotate By Four Cells

We want to rotate an `n x n` matrix **90 degrees clockwise**, but this time **in-place**, without using extra space.

A useful way to visualize this is to rotate the matrix **layer by layer**, starting from the outermost layer and moving inward.

For each square layer:

- elements move in groups of **four**
- each element in the group shifts to its new rotated position

Specifically, for a given layer:

- **`top-left` → `top-right`**
- **`top-right` → `bottom-right`**
- **`bottom-right` → `bottom-left`**
- **`bottom-left` → `top-left`**

By rotating these four cells at a time, we complete the rotation without needing an extra `matrix`.

```cpp
class Solution {
public:
    void rotate(vector<vector<int>>& matrix) {
        int l = 0;
        int r = matrix.size() - 1;

        while ( l < r ) {
            for(int i = 0; i < r - l; i++) {
                int top = l;
                int bottom = r;

                //save the topleft
                int topLeft = matrix[top][l + i];

                //move bottom left into top left
                matrix[top][l + i] = matrix[bottom - i][l];

                // move bottom right into bottom left
                matrix[bottom - i][l] = matrix[bottom][r - i];

                // move top right into bottom right
                matrix[bottom][r - i] = matrix[top + i][r];

                // move top left into top right
                matrix[top + i][r] = topLeft;

            }
            r--;
            l++;
        }
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 3. Reverse And Transpose

We want to rotate an `n x n` `matrix` **90 degrees clockwise** in-place.

A very clean way to do this is to break the rotation into **two simple operations**:

1. **Reverse the `matrix` vertically**
2. **Transpose the `matrix`**

Why this works:

- Reversing the `matrix` flips it upside down
- Transposing swaps rows with columns
- Doing both together results in a 90° clockwise rotation

This method is elegant, easy to remember, and avoids extra space.

```cpp
class Solution {
public:
    void rotate(vector<vector<int>>& matrix) {
        // Reverse the matrix vertically
        reverse(matrix.begin(), matrix.end());

        // Transpose the matrix
        for (int i = 0; i < matrix.size(); ++i) {
            for (int j = i + 1; j < matrix[i].size(); ++j)
                swap(matrix[i][j], matrix[j][i]);
        }
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0048-rotate-image.cpp` in the NeetCode repo)

```cpp
/*
    Given a 2D image matrix, rotate image 90 deg CW

    Transpose + reflect (rev on diag then rev left to right)

    Time: O(n^2)
    Space: O(1)
*/

class Solution {
public:
    void rotate(vector<vector<int>>& matrix) {
        int n = matrix.size();
        for (int i = 0; i < n; i++) {
            for (int j = i; j < n; j++) {
                swap(matrix[i][j], matrix[j][i]);
            }
            reverse(matrix[i].begin(), matrix[i].end());
        }
    }
};
```
