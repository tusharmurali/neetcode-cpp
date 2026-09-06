# 2028. Find Missing Observations

- **Difficulty:** Medium  
- **Pattern:** Math & Geometry  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/find-missing-observations/>  
- **NeetCode:** <https://neetcode.io/problems/find-missing-observations>  
- **Video:** <https://www.youtube.com/watch?v=86yKkaNi3sU>  

[← Back to index](../INDEX.md)

## 1. Math - I

We know the target mean and the sum of the existing rolls. From this, we can calculate the total sum needed for all `n + m` dice, and therefore the sum required for the `n` missing dice. If this required sum is impossible (less than `n` or greater than `6 * n`), no valid solution exists. Otherwise, we greedily assign values to each die, giving each one as high a value as possible while ensuring the remaining dice can still reach at least `1` each.

```cpp
class Solution {
public:
    vector<int> missingRolls(vector<int>& rolls, int mean, int n) {
        int m = rolls.size();
        int nTotal = (mean * (n + m)) - accumulate(rolls.begin(), rolls.end(), 0);

        if (nTotal < n || nTotal > n * 6) {
            return {};
        }

        vector<int> res;
        for (int i = 0; i < n; ++i) {
            int dice = min(nTotal - (n - i - 1), 6);
            res.push_back(dice);
            nTotal -= dice;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m + n)$
- Space complexity:
    - $O(1)$ extra space.
    - $O(n)$ space for the output array.

> Where $m$ is the size of the array $rolls$ and $n$ is the number of missing observations.

## 2. Math - II

Instead of greedily assigning values one at a time, we can distribute the required sum more evenly. First, compute the average value each die should have by dividing the total needed by `n`. The remainder tells us how many dice need to be one higher than the average. This produces a cleaner distribution where most dice have the same value.

```cpp
class Solution {
public:
    vector<int> missingRolls(vector<int>& rolls, int mean, int n) {
        int m = rolls.size();
        int nTotal = (mean * (n + m)) - accumulate(rolls.begin(), rolls.end(), 0);

        if (nTotal < n || nTotal > n * 6) {
            return {};
        }

        int avg = nTotal / n;
        int rem = nTotal - (avg * n);
        vector<int> res;

        for (int i = 0; i < n - rem; ++i) {
            res.push_back(avg);
        }
        for (int i = 0; i < rem; ++i) {
            res.push_back(avg + 1);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m + n)$
- Space complexity:
    - $O(1)$ extra space.
    - $O(n)$ space for the output array.

> Where $m$ is the size of the array $rolls$ and $n$ is the number of missing observations.
