# 1235. Maximum Profit in Job Scheduling

- **Difficulty:** Hard  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/maximum-profit-in-job-scheduling/>  
- **NeetCode:** <https://neetcode.io/problems/maximum-profit-in-job-scheduling>  
- **Video:** <https://www.youtube.com/watch?v=JLoWc3v0SiE>  

[← Back to index](../INDEX.md)

## 1. Dynamic Programming (Top-Down)

This is a classic interval scheduling problem. For each job, we have two choices: skip it or take it. If we take a job, we earn its profit but must skip all overlapping jobs. By sorting jobs by start time and using memoization, we can efficiently explore all valid schedules.

```cpp
class Solution {
public:
    vector<vector<int>> intervals;
    vector<int> cache;

    int jobScheduling(vector<int>& startTime, vector<int>& endTime, vector<int>& profit) {
        int n = startTime.size();
        intervals.resize(n, vector<int>(3));
        cache.assign(n, -1);

        for (int i = 0; i < n; i++) {
            intervals[i] = {startTime[i], endTime[i], profit[i]};
        }
        sort(intervals.begin(), intervals.end());

        return dfs(0);
    }

private:
    int dfs(int i) {
        if (i == intervals.size()) {
            return 0;
        }
        if (cache[i] != -1) {
            return cache[i];
        }

        // Don't include
        int res = dfs(i + 1);

        // Include
        int j = i + 1;
        while (j < intervals.size() && intervals[i][1] > intervals[j][0]) {
            j++;
        }

        return cache[i] = max(res, intervals[i][2] + dfs(j));
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 2. Dynamic Programming (Top-Down) + Binary Search

The linear scan to find the next non-overlapping job can be optimized using binary search. Since jobs are sorted by start time, we can binary search for the first job whose start time is at least the current job's end time.

```cpp
class Solution {
public:
    vector<vector<int>> intervals;
    vector<int> cache;

    int jobScheduling(vector<int>& startTime, vector<int>& endTime, vector<int>& profit) {
        int n = startTime.size();
        intervals.resize(n, vector<int>(3));
        cache.assign(n, -1);

        for (int i = 0; i < n; i++) {
            intervals[i] = {startTime[i], endTime[i], profit[i]};
        }
        sort(intervals.begin(), intervals.end());

        return dfs(0);
    }

private:
    int dfs(int i) {
        if (i == intervals.size()) {
            return 0;
        }
        if (cache[i] != -1) {
            return cache[i];
        }

        int res = dfs(i + 1);

        int left = i + 1, right = intervals.size(), j = intervals.size();
        while (left < right) {
            int mid = left + (right - left) / 2;
            if (intervals[mid][0] >= intervals[i][1]) {
                j = mid;
                right = mid;
            } else {
                left = mid + 1;
            }
        }

        return cache[i] = max(res, intervals[i][2] + dfs(j));
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 3. Dynamic Programming (Top-Down) + Binary Search (Optimal)

Instead of creating new interval objects, we can sort indices by start time and work with the original arrays. This reduces memory allocations while maintaining the same algorithmic approach.

```cpp
class Solution {
public:
    vector<int> startTime, endTime, profit, index, cache;
    int n;

    int jobScheduling(vector<int>& startTime, vector<int>& endTime, vector<int>& profit) {
        this->n = startTime.size();
        this->startTime = startTime;
        this->endTime = endTime;
        this->profit = profit;
        this->index.resize(n);
        this->cache.assign(n, -1);

        for (int i = 0; i < n; i++) {
            index[i] = i;
        }
        sort(index.begin(), index.end(), [&](int i, int j) {
            return startTime[i] < startTime[j];
        });

        return dfs(0);
    }

private:
    int dfs(int i) {
        if (i == n) {
            return 0;
        }
        if (cache[i] != -1) {
            return cache[i];
        }

        int res = dfs(i + 1);

        int left = i + 1, right = n, j = n;
        while (left < right) {
            int mid = left + (right - left) / 2;
            if (startTime[index[mid]] >= endTime[index[i]]) {
                j = mid;
                right = mid;
            } else {
                left = mid + 1;
            }
        }

        return cache[i] = max(res, profit[index[i]] + dfs(j));
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 4. Dynamic Programming (Bottom-Up) + Binary Search

We can convert the top-down approach to bottom-up by iterating from the last job to the first. At each position, we compute the maximum profit considering all jobs from that point onwards. This eliminates recursion overhead.

```cpp
class Solution {
public:
    int jobScheduling(vector<int>& startTime, vector<int>& endTime, vector<int>& profit) {
        int n = startTime.size();
        vector<int> index(n), dp(n + 1, 0);
        for (int i = 0; i < n; i++) index[i] = i;
        sort(index.begin(), index.end(), [&](int i, int j) {
            return startTime[i] < startTime[j];
        });

        for (int i = n - 1; i >= 0; i--) {
            int left = i + 1, right = n, j = n;
            while (left < right) {
                int mid = left + (right - left) / 2;
                if (startTime[index[mid]] >= endTime[index[i]]) {
                    j = mid;
                    right = mid;
                } else {
                    left = mid + 1;
                }
            }
            dp[i] = max(dp[i + 1], profit[index[i]] + dp[j]);
        }

        return dp[0];
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$
