# 531. Lonely Pixel I

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/lonely-pixel-i/>  
- **NeetCode:** <https://neetcode.io/problems/lonely-pixel-i>  

[← Back to index](../INDEX.md)

## 1. Counting with Arrays

A pixel is "lonely" if it's the only black pixel in both its row and its column. Instead of checking the entire row and column for each black pixel (which would be slow), we can precompute the count of black pixels in every row and every column. Then, a black pixel at position `(i, j)` is lonely if and only if both `row_count[i]` and `column_count[j]` equal `1`.

```cpp
class Solution {
public:
    int findLonelyPixel(vector<vector<char>>& picture) {
        int n = int(picture.size());
        int m = int(picture[0].size());

        // Arrays to store the count of black cells in rows and columns.
        vector<int> rowCount(n, 0);
        vector<int> columnCount(m, 0);
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                if (picture[i][j] == 'B') {
                    rowCount[i]++;
                    columnCount[j]++;
                }
            }
        }

        int answer = 0;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                // Its a lonely cell, if the current cell is black and,
                // the count of black cells in its row and column is 1.
                if (picture[i][j] == 'B' && rowCount[i] == 1 && columnCount[j] == 1) {
                    answer++;
                }
            }
        }

        return answer;
    }
};
```

**Complexity**

- Time complexity: $O(M \cdot N)$
- Space complexity: $O(M + N)$

> Where $M$ is the number of rows in the given matrix `picture`, and $N$ is the number of columns in it.

## 2. Space Optimized Counting

We can avoid using extra arrays by reusing the first row and first column of the grid itself to store the counts. However, we must first handle lonely pixels in the first row and first column separately, since those cells will be overwritten. After that, we convert the border cells to store counts and use them to check interior cells.

```cpp

class Solution {
public:
    // Returns true if the cell at (x, y) is lonely.
    // There should not be any other black cell
    // In the first row and column except (x, y) itself.
    bool check(vector<vector<char>>& picture, int x, int y) {
        int n = int(picture.size());
        int m = int(picture[0].size());

        int cnt = 0;
        for (int i = 0; i < n; i++) {
            cnt += (picture[i][y] == 'B');
        }

        for (int j = 0; j < m; j++) {
            // avoid double count (x, y)
            if (j != y) cnt += (picture[x][j] == 'B');
        }
        return picture[x][y] == 'B' && cnt == 1;
    }

    int findLonelyPixel(vector<vector<char>>& picture) {
        int n = int(picture.size());
        int m = int(picture[0].size());

        int answer = 0;
        // Lonely cells in the first row
        for (int j = 0; j < m; j++) {
            answer += check(picture, 0, j);
        }
        //Lonely cells in the first column
        for (int i = 1; i < n; i++) {
            answer += check(picture, i, 0);
        }

        // Convert cell 'B' to '1' and 'W' to '0'
        for (int j = 0; j < m; j++) {
            picture[0][j] = (picture[0][j] == 'B' ? '1' : '0');
        }

        for (int i = 0; i < n; i++) {
            picture[i][0] = (picture[i][0] == 'B' ? '1' : '0');
        }

        // If the cell is black increment the count of corresponding row and column by 1
        for (int i = 1; i < n; i++) {
            for (int j = 1; j < m; j++) {
                if (picture[i][j] == 'B') {
                    picture[i][0]++;
                    picture[0][j]++;
                }
            }
        }

        for (int i = 1; i < n; i++) {
            for (int j = 1; j < m; j++) {
                if (picture[i][j] == 'B') {
                    if (picture[0][j] == '1' && picture[i][0] == '1') {
                        answer++;
                    }
                }
            }
        }

        return answer;
    }
};
```

**Complexity**

- Time complexity: $O(M \cdot N)$
- Space complexity: $O(1)$ constant space

> Where $M$ is the number of rows in the given matrix `picture`, and $N$ is the number of columns in it.
