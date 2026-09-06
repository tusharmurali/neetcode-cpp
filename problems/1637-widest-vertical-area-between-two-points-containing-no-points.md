# 1637. Wildest Vertical Area Between Two Points Containing No Points

- **Difficulty:** Easy  
- **Pattern:** Math & Geometry  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/widest-vertical-area-between-two-points-containing-no-points/>  
- **NeetCode:** <https://neetcode.io/problems/widest-vertical-area-between-two-points-containing-no-points>  
- **Video:** <https://www.youtube.com/watch?v=6XnvNCTyJP4>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The most straightforward approach is to check every pair of points and determine if the vertical area between them contains any other points. For each pair, we compute the horizontal distance and verify that no other point lies strictly between them in the x-coordinate. This gives us the correct answer but is inefficient for large inputs.

```cpp
class Solution {
public:
    int maxWidthOfVerticalArea(vector<vector<int>>& points) {
        int n = points.size(), res = 0;

        for (int i = 1; i < n; i++) {
            int x1 = points[i][0];
            for (int j = 0; j < i; j++) {
                int x2 = points[j][0];
                bool hasPoints = false;

                for (int k = 0; k < n; k++) {
                    if (k == i || k == j) continue;

                    int x3 = points[k][0];
                    if (x3 > min(x1, x2) && x3 < max(x1, x2)) {
                        hasPoints = true;
                        break;
                    }
                }

                if (!hasPoints) {
                    res = max(res, abs(x1 - x2));
                }
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 3)$
- Space complexity: $O(1)$

## 2. Sorting

The key insight is that a vertical area containing no points must exist between two consecutive points when sorted by x-coordinate. If we sort all points by their x-values, the widest gap between adjacent points gives us the answer directly. This works because any non-adjacent pair would have at least one point between them, making that area invalid.

```cpp
class Solution {
public:
    int maxWidthOfVerticalArea(vector<vector<int>>& points) {
        sort(points.begin(), points.end(), [](const auto& a, const auto& b) {
            return a[0] < b[0];
        });

        int res = 0;
        for (int i = 0; i < points.size() - 1; i++) {
            res = max(res, points[i + 1][0] - points[i][0]);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.
