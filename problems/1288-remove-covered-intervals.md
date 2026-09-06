# 1288. Remove Covered Intervals

- **Difficulty:** Medium  
- **Pattern:** Intervals  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/remove-covered-intervals/>  
- **NeetCode:** <https://neetcode.io/problems/remove-covered-intervals>  
- **Video:** <https://www.youtube.com/watch?v=nhAsMabiVkM>  

[← Back to index](../INDEX.md)

## 1. Brute Force

An interval is "covered" if another interval completely contains it. We check every pair of intervals to see if one covers the other. For interval `i` to be covered by interval `j`, we need `j`'s start to be at or before `i`'s start, and `j`'s end to be at or after `i`'s end. We count how many intervals are not covered by any other.

```cpp
class Solution {
public:
    int removeCoveredIntervals(vector<vector<int>>& intervals) {
        int n = intervals.size();
        int res = n;

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                if (i != j && intervals[j][0] <= intervals[i][0] &&
                    intervals[j][1] >= intervals[i][1]) {
                    res--;
                    break;
                }
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$ extra space.

## 2. Sorting - I

Sorting helps us process intervals in an order where we can easily detect covered intervals. By sorting by start time (ascending) and then by end time (descending), intervals that share the same start will have the longest one first. This means when we encounter a new interval, we only need to check if it's covered by the most recent "dominant" interval we've seen.

```cpp
class Solution {
public:
    int removeCoveredIntervals(vector<vector<int>>& intervals) {
        sort(intervals.begin(), intervals.end(), [](const auto& a, const auto& b) {
            return a[0] == b[0] ? b[1] < a[1] : a[0] < b[0];
        });

        int res = 1, prevL = intervals[0][0], prevR = intervals[0][1];
        for (const auto& interval : intervals) {
            int l = interval[0], r = interval[1];
            if (prevL <= l && prevR >= r) {
                continue;
            }
            res++;
            prevL = l;
            prevR = r;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n\log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 3. Sorting - II

With a simpler sort by start time only, we track the maximum end point seen so far. An interval is covered if both its start is greater than or equal to a previous start AND its end is within the maximum end we've tracked. By keeping the maximum end updated, we efficiently determine coverage in a single pass.

```cpp
class Solution {
public:
    int removeCoveredIntervals(vector<vector<int>>& intervals) {
        sort(intervals.begin(), intervals.end());
        int res = 1, start = intervals[0][0], end = intervals[0][1];

        for (const auto& interval : intervals) {
            int l = interval[0], r = interval[1];
            if (start < l && end < r) {
                start = l;
                res++;
            }
            end = max(end, r);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.
