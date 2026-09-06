# 986. Interval List Intersections

- **Difficulty:** Medium  
- **Pattern:** Intervals  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/interval-list-intersections/>  
- **NeetCode:** <https://neetcode.io/problems/interval-list-intersections>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The simplest way to find intersections is to check every interval in the first list against every interval in the second list. Two intervals overlap when one starts before the other ends and vice versa. If they do overlap, the intersection spans from the later start point to the earlier end point. This approach is straightforward but involves redundant comparisons since we ignore the fact that both lists are already sorted.

```cpp
class Solution {
public:
    vector<vector<int>> intervalIntersection(vector<vector<int>>& firstList, vector<vector<int>>& secondList) {
        vector<vector<int>> res;
        for (int i = 0; i < firstList.size(); i++) {
            int startA = firstList[i][0], endA = firstList[i][1];
            for (int j = 0; j < secondList.size(); j++) {
                int startB = secondList[j][0], endB = secondList[j][1];
                if ((startA <= startB && startB <= endA) || (startB <= startA && startA <= endB)) {
                    res.push_back({max(startA, startB), min(endA, endB)});
                }
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity:
    - $O(1)$ extra space.
    - $O(m + n)$ for the output list.

> Where $m$ and $n$ are the sizes of the arrays $firstList$ and $secondList$, respectively.

## 2. Line Sweep

Line sweep treats intervals as events on a number line. At each interval's start, we increment an "active" counter; at each interval's end plus one, we decrement it. When the active count equals `2`, it means both an interval from the first list and one from the second list are covering that point simultaneously. By processing all events in sorted order, we can identify exactly where overlaps occur without directly comparing pairs of intervals.

```cpp
class Solution {
public:
    vector<vector<int>> intervalIntersection(vector<vector<int>>& firstList, vector<vector<int>>& secondList) {
        map<int, int> mp;
        for (auto& f : firstList) {
            mp[f[0]] += 1;
            mp[f[1] + 1] -= 1;
        }
        for (auto& s : secondList) {
            mp[s[0]] += 1;
            mp[s[1] + 1] -= 1;
        }

        vector<vector<int>> res;
        int active = 0, prev = 0;
        bool started = false;
        for (auto& [x, v] : mp) {
            if (active == 2) {
                res.push_back({prev, x - 1});
            }
            active += v;
            prev = x;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O((m + n) \log (m + n))$
- Space complexity: $O(m + n)$

> Where $m$ and $n$ are the sizes of the arrays $firstList$ and $secondList$, respectively.

## 3. Two Pointers

Since both interval lists are sorted and disjoint within themselves, we can use two pointers to efficiently find intersections. At each step, we compare the current interval from each list. If they overlap, we record the intersection. Then we advance the pointer for whichever interval ends first, since that interval cannot intersect with any future intervals from the other list. This eliminates unnecessary comparisons and processes each interval exactly once.

```cpp
class Solution {
public:
    vector<vector<int>> intervalIntersection(vector<vector<int>>& firstList, vector<vector<int>>& secondList) {
        vector<vector<int>> res;
        int i = 0, j = 0;

        while (i < firstList.size() && j < secondList.size()) {
            int startA = firstList[i][0], endA = firstList[i][1];
            int startB = secondList[j][0], endB = secondList[j][1];

            int start = max(startA, startB);
            int end = min(endA, endB);

            if (start <= end) {
                res.push_back({start, end});
            }

            if (endA < endB) {
                i++;
            } else {
                j++;
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m + n)$
- Space complexity:
    - $O(1)$ extra space.
    - $O(m + n)$ for the output list.

> Where $m$ and $n$ are the sizes of the arrays $firstList$ and $secondList$, respectively.
