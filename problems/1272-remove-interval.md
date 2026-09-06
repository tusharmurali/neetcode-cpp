# 1272. Remove Interval

- **Difficulty:** Medium  
- **Pattern:** Intervals  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/remove-interval/>  
- **NeetCode:** <https://neetcode.io/problems/remove-interval>  

[← Back to index](../INDEX.md)

## 1. Sweep Line, One Pass

Each interval in the input can relate to the removal interval in one of three ways: completely outside (no overlap), completely inside (fully removed), or partially overlapping.
If there is no overlap, we keep the interval unchanged.
If there is overlap, we need to preserve any portions that fall outside the removal range.
This could mean keeping a left portion, a right portion, or both if the removal interval sits in the middle.

```cpp
class Solution {
public:
    vector<vector<int>> removeInterval(vector<vector<int>>& intervals, vector<int>& toBeRemoved) {
        vector<vector<int>> result;

        for (auto& interval : intervals) {
            // If there are no overlaps, add the interval to the list as is.
            if (interval[0] > toBeRemoved[1] || interval[1] < toBeRemoved[0]) {
                result.push_back({interval[0], interval[1]});
            } else {
                // Is there a left interval we need to keep?
                if (interval[0] < toBeRemoved[0]) {
                    result.push_back({interval[0], toBeRemoved[0]});
                }
                // Is there a right interval we need to keep?
                if (interval[1] > toBeRemoved[1]) {
                    result.push_back({toBeRemoved[1], interval[1]});
                }
            }
        }

        return result;
    }
};
```

**Complexity**

- Time complexity: $O(N)$
- Space complexity: $O(1)$ without considering $O(N)$ space for the output list.

> Where $N$ is the number of intervals in `intervals`
