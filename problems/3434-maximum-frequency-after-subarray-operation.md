# 3434. Maximum Frequency After Subarray Operation

- **Difficulty:** Medium  
- **Pattern:** Greedy  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/maximum-frequency-after-subarray-operation/>  
- **NeetCode:** <https://neetcode.io/problems/maximum-frequency-after-subarray-operation>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The operation lets us pick a subarray and add a constant to every element in it. Our goal is to maximize how often some value `k` appears. The key insight is that we want to convert elements of some value `num` into `k` by choosing the right constant. For each candidate `num`, we try every possible subarray, count how many `num` values we convert to `k`, and subtract any `k` values that get changed to something else within the subarray.

```cpp
class Solution {
public:
    int maxFrequency(vector<int>& nums, int k) {
        int n = nums.size();
        int cntK = 0;
        for (int x : nums) if (x == k) cntK++;
        int res = cntK;

        for (int num = 1; num <= 50; num++) {
            if (num == k) continue;
            for (int i = 0; i < n; i++) {
                int tmp = cntK, cnt = 0;
                for (int j = i; j < n; j++) {
                    if (nums[j] == num) {
                        cnt++;
                    } else if (nums[j] == k) {
                        cntK--;
                    }
                    res = max(res, cnt + cntK);
                }
                cntK = tmp;
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(50 * n ^ 2)$
- Space complexity: $O(1)$

## 2. Kadane's Algorithm - I

The brute force tries all subarrays, but we can use Kadane's algorithm to find the best subarray in linear time. For a fixed target value `num`, we want to find a subarray where converting `num` to `k` gives the maximum net gain. Treat each `num` as `+1` (we gain a `k`) and each `k` as `-1` (we lose a `k`). Kadane's algorithm finds the maximum sum subarray, giving us the best gain for that target.

```cpp
class Solution {
public:
    int maxFrequency(vector<int>& nums, int k) {
        int cntK = 0;
        for (int num : nums) {
            if (num == k) cntK++;
        }
        int res = 0;

        for (int i = 1; i <= 50; i++) {
            if (i == k) continue;
            int cnt = 0;
            for (int num : nums) {
                if (num == i) cnt++;
                if (num == k) cnt--;
                cnt = max(cnt, 0);
                res = max(res, cntK + cnt);
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(50 * n)$
- Space complexity: $O(1)$

## 3. Kadane's Algorithm - II

We can process all target values simultaneously in a single pass. For each number, we track the best running sum ending at the current position. When we see a number, its count can either extend from its previous best or start fresh from `k`'s position (since we could start our subarray here). The maximum difference between any count and `k`'s count represents the best gain achievable.

```cpp
class Solution {
public:
    int maxFrequency(vector<int>& nums, int k) {
        unordered_map<int,int> cnt;
        int res = 0;
        for (int num : nums) {
            int prev = max(cnt[num], cnt[k]);
            cnt[num] = prev + 1;
            res = max(res, cnt[num] - cnt[k]);
        }
        return cnt[k] + res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(50)$
