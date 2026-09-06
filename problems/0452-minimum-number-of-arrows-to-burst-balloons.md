# 452. Minimum Number of Arrows to Burst Balloons

- **Difficulty:** Medium  
- **Pattern:** Intervals  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/>  
- **NeetCode:** <https://neetcode.io/problems/minimum-number-of-arrows-to-burst-balloons>  
- **Video:** <https://www.youtube.com/watch?v=lPmkKnvNPrw>  

[← Back to index](../INDEX.md)

## 1. Greedy (Sort By Start Value)

Think of each balloon as a horizontal range on a number line. If two balloons overlap, a single arrow can pop both. The key insight is that by sorting balloons by their starting position, we can process them left to right and greedily merge overlapping intervals.

When we encounter a new balloon, we check if it overlaps with the previous group. If it does, we shrink the overlap region by taking the minimum of the end values. If not, we need a new arrow. We start by assuming each balloon needs its own arrow, then subtract one for each overlap we find.

```cpp
class Solution {
public:
    int findMinArrowShots(vector<vector<int>>& points) {
        sort(points.begin(), points.end());
        int res = points.size(), prevEnd = points[0][1];

        for (int i = 1; i < points.size(); i++) {
            vector<int>& curr = points[i];
            if (curr[0] <= prevEnd) {
                res--;
                prevEnd = min(curr[1], prevEnd);
            } else {
                prevEnd = curr[1];
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 2. Greedy (Sort By End Value)

Sorting by end position offers a cleaner greedy approach. By shooting an arrow at the end of the first balloon, we maximize the chance of hitting subsequent balloons. Each balloon that starts after our current arrow position requires a new arrow.

This is a classic interval scheduling pattern: always pick the earliest finishing interval first. When we shoot at the end of a balloon, any other balloon that overlaps must have started before or at that point.

```cpp
class Solution {
public:
    int findMinArrowShots(vector<vector<int>>& points) {
        sort(points.begin(), points.end(), [](const auto& a, const auto& b) {
            return a[1] < b[1];
        });
        int res = 1, prevEnd = points[0][1];

        for (int i = 1; i < points.size(); i++) {
            if (points[i][0] > prevEnd) {
                prevEnd = points[i][1];
                res++;
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.
