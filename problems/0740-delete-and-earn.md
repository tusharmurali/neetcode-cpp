# 740. Delete And Earn

- **Difficulty:** Medium  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/delete-and-earn/>  
- **NeetCode:** <https://neetcode.io/problems/delete-and-earn>  
- **Video:** <https://www.youtube.com/watch?v=7FCemBxvGw0>  

[← Back to index](../INDEX.md)

## 1. Recursion

When you pick a number `x`, you earn all points from every occurrence of `x`, but you must delete all instances of `x - 1` and `x + 1`. This creates a choice at each distinct value: either take it (and skip the next consecutive value) or skip it. Sorting helps group identical values together, making it easy to sum all occurrences. We recursively explore both choices at each group of identical numbers.

```cpp
class Solution {
public:
    int deleteAndEarn(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        return dfs(nums, 0);
    }

private:
    int dfs(const vector<int>& nums, int i) {
        if (i >= nums.size()) return 0;

        int cur = nums[i], pick = 0;
        while (i < nums.size() && nums[i] == cur) {
            pick += nums[i];
            i++;
        }

        int res = dfs(nums, i);
        while (i < nums.size() && nums[i] == cur + 1) {
            i++;
        }

        res = max(res, pick + dfs(nums, i));
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ n)$
- Space complexity: $O(n)$

## 2. Dynamic Programming (Top-Down)

The recursive solution has overlapping subproblems since we may revisit the same index multiple times. By precomputing the total value for each unique number (sum of all occurrences) and using memoization, we avoid redundant calculations. The problem reduces to: for each unique number, decide whether to take it (earning its total value but skipping the next consecutive number) or skip it.

```cpp
class Solution {
    unordered_map<int, int> val;
    vector<int> memo;

public:
    int deleteAndEarn(vector<int>& nums) {
        for (int num : nums) {
            val[num] += num;
        }

        vector<int> uniqueNums;
        for (auto& pair : val) {
            uniqueNums.push_back(pair.first);
        }
        sort(uniqueNums.begin(), uniqueNums.end());
        memo.resize(uniqueNums.size(), -1);

        return dfs(uniqueNums, 0);
    }

private:
    int dfs(vector<int>& nums, int i) {
        if (i >= nums.size()) return 0;
        if (memo[i] != -1) return memo[i];

        int res = val[nums[i]];
        if (i + 1 < nums.size() && nums[i] + 1 == nums[i + 1]) {
            res += dfs(nums, i + 2);
        } else {
            res += dfs(nums, i + 1);
        }

        res = max(res, dfs(nums, i + 1));
        memo[i] = res;
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 3. Dynamic Programming (Bottom-Up) - I

We can convert the top-down solution to bottom-up by processing unique numbers from right to left. At each position, we compute the maximum points achievable from that position onward. If the current and next numbers are consecutive, taking the current means skipping the next; otherwise, we can take the current and continue from the next.

```cpp
class Solution {
public:
    int deleteAndEarn(vector<int>& nums) {
        unordered_map<int, int> val;
        for (int num : nums) val[num] += num;
        vector<int> sortedNums;
        for (auto& [key, _] : val) sortedNums.push_back(key);
        sort(sortedNums.begin(), sortedNums.end());

        vector<int> dp(sortedNums.size() + 1);
        for (int i = sortedNums.size() - 1; i >= 0; i--) {
            int take = val[sortedNums[i]];
            if (i + 1 < sortedNums.size() && sortedNums[i + 1] == sortedNums[i] + 1) {
                take += dp[i + 2];
            } else {
                take += dp[i + 1];
            }
            dp[i] = max(dp[i + 1], take);
        }

        return dp[0];
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 4. Dynamic Programming (Bottom-Up) - II

Instead of working with unique sorted numbers, we can use an array indexed by the numbers themselves (`0` to max). Each index stores the total points for that number. This transforms the problem into the classic House Robber problem: you cannot take adjacent indices. We iterate backward, and at each position, choose the maximum of skipping it or taking it plus the result two positions ahead.

```cpp
class Solution {
public:
    int deleteAndEarn(vector<int>& nums) {
        int m = *max_element(nums.begin(), nums.end());
        vector<int> dp(m + 2);
        for (auto& num : nums) {
            dp[num] += num;
        }

        for (int i = m - 1; i > 0; i--) {
            dp[i] = max(dp[i + 1], dp[i + 2] + dp[i]);
        }
        return dp[1];
    }
};
```

**Complexity**

- Time complexity: $O(m + n)$
- Space complexity: $O(m)$

> Where $m$ is the maximum element in the array and $n$ is the size of the array.

## 5. Dynamic Programming (Space Optimized)

We only need to track the maximum earnings for the previous two positions, similar to the space-optimized House Robber solution. By iterating through sorted unique numbers and maintaining two variables, we can reduce space complexity. When consecutive numbers differ by more than `1`, there is no conflict, so we can add the current earnings directly.

```cpp
class Solution {
public:
    int deleteAndEarn(vector<int>& nums) {
        unordered_map<int, int> count;
        for (int num : nums) count[num] += num;
        vector<int> uniqueNums;
        for (auto& pair : count) uniqueNums.push_back(pair.first);
        sort(uniqueNums.begin(), uniqueNums.end());

        int earn1 = 0, earn2 = 0;
        for (int i = 0; i < uniqueNums.size(); i++) {
            int curEarn = count[uniqueNums[i]];
            if (i > 0 && uniqueNums[i] == uniqueNums[i - 1] + 1) {
                int temp = earn2;
                earn2 = max(curEarn + earn1, earn2);
                earn1 = temp;
            } else {
                int temp = earn2;
                earn2 = curEarn + earn2;
                earn1 = temp;
            }
        }
        return earn2;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/0740-delete-and-earn.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    int deleteAndEarn(vector<int>& nums) {
        int maxnum=0;
        int trans[10001]={0};
        for(int i:nums){
            trans[i]+=i;
            maxnum=max(maxnum,i);
        }
        int dp[maxnum+1];
        dp[0]=trans[0];
        dp[1]=max(trans[1],trans[0]);
        for(int i=2;i<=maxnum;i++){
            dp[i] = max(dp[i - 1], dp[i - 2] +trans[i]);
        }
        return dp[maxnum];
    }
};
```
