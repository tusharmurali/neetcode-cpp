# 2597. The Number of Beautiful Subsets

- **Difficulty:** Medium  
- **Pattern:** Backtracking  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/the-number-of-beautiful-subsets/>  
- **NeetCode:** <https://neetcode.io/problems/the-number-of-beautiful-subsets>  
- **Video:** <https://www.youtube.com/watch?v=Dle_SpjHTio>  

[← Back to index](../INDEX.md)

## 1. Backtracking

A subset is beautiful if no two elements have an absolute difference of `k`. We can explore all possible subsets using backtracking. For each element, we decide whether to include it or skip it. Before including an element, we check if adding it would create a conflict with any element already in our current subset.

A hash map tracks the count of each number in the current subset. When considering `nums[i]`, we check if `nums[i] + k` or `nums[i] - k` exists in the map. If neither exists, we can safely include the element and recurse deeper.

```cpp
class Solution {
public:
    int beautifulSubsets(vector<int>& nums, int k) {
        unordered_map<int, int> count;
        return helper(0, count, nums, k) - 1;
    }

private:
    int helper(int i, unordered_map<int, int>& count, vector<int>& nums, int k) {
        if (i == nums.size()) {
            return 1;
        }

        int res = helper(i + 1, count, nums, k); // Skip nums[i]
        if (!count[nums[i] + k] && !count[nums[i] - k]) {
            count[nums[i]]++;
            res += helper(i + 1, count, nums, k);
            count[nums[i]]--;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ n)$
- Space complexity: $O(n)$

## 2. Dynamic Programming (Top-Down)

Numbers can only conflict if their difference is exactly `k`. This means numbers that differ by `k` form chains where adjacent elements cannot both appear in a beautiful subset. By grouping numbers into these chains, we transform the problem into independent subproblems.

For each chain, we solve a variation of the house robber problem: at each position, we either skip the current number or include some combination of its duplicates (if the number appears multiple times). If we include any copies of a number, we must skip the next number in the chain.

```cpp
class Solution {
public:
    int beautifulSubsets(vector<int>& nums, int k) {
        vector<unordered_map<int, int>> groups;
        cache.clear();
        cnt.clear();
        visit.clear();

        for (int& num : nums) {
            cnt[num]++;
        }

        for (auto it = cnt.begin(); it != cnt.end(); ++it) {
            int n = it->first;
            if (visit.count(n)) {
                continue;
            }
            unordered_map<int, int> g;
            while (cnt.count(n - k)) {
                n -= k;
            }
            while (cnt.count(n)) {
                g[n] = cnt[n];
                visit.insert(n);
                n += k;
            }
            groups.push_back(g);
        }

        int res = 1;
        for (auto& g : groups) {
            int n = min_element(g.begin(), g.end())->first;
            res *= helper(n, g, k);
        }
        return res - 1;
    }

private:
    unordered_map<int, int> cache;
    unordered_map<int, int> cnt;
    unordered_set<int> visit;

    int helper(int n, unordered_map<int, int>& g, int k) {
        if (!g.count(n)) {
            return 1;
        }
        if (cache.count(n)) {
            return cache[n];
        }

        int skip = helper(n + k, g, k);
        int include = (pow(2, g[n]) - 1) * helper(n + 2 * k, g, k);
        return cache[n] = skip + include;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Dynamic Programming (Bottom-Up)

Instead of using recursion with memoization, we can build the solution iteratively. After grouping numbers into chains, we process each chain from smallest to largest. At each step, we track the total number of valid subsets we can form using numbers up to the current position.

The key insight is that when processing a number, we need to know how many subsets were possible before the previous number (to combine with including the current number) and how many were possible including the previous number (which we cannot combine with the current number).

```cpp
class Solution {
public:
    int beautifulSubsets(vector<int>& nums, int k) {
        unordered_map<int, int> cnt;
        for (int num : nums) {
            cnt[num]++;
        }

        vector<unordered_map<int, int>> groups;
        unordered_set<int> visit;

        for (auto it = cnt.begin(); it != cnt.end(); ++it) {
            int n = it->first;
            if (visit.count(n)) {
                continue;
            }
            unordered_map<int, int> g;
            while (cnt.count(n - k)) {
                n -= k;
            }
            while (cnt.count(n)) {
                g[n] = cnt[n];
                visit.insert(n);
                n += k;
            }
            groups.push_back(g);
        }

        int res = 1;
        for (auto& g : groups) {
            unordered_map<int, int> dp;
            int prev = -1;

            vector<int> keys;
            for (auto& [num, _] : g) {
                keys.push_back(num);
            }
            sort(keys.begin(), keys.end());

            for (int num : keys) {
                int count = g[num];
                if (prev == -1 || prev + k != num) {
                    dp[num] = dp.count(prev) ? dp[prev] * (1 + (1 << count) - 1) :
                                               (1 + (1 << count) - 1);
                } else {
                    dp[num] = dp[prev] + ((1 << count) - 1) *
                              (dp.count(prev - k) ? dp[prev - k] : 1);
                }
                prev = num;
            }

            res *= dp[prev];
        }

        return res - 1;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 4. Dynamic Programming (Space Optimized)

We can optimize space by observing that we only need information from the previous two positions in each chain. Instead of storing results for all numbers in a DP map, we use two variables: one for subsets that include the previous number (`dp`) and one for subsets that do not include it (`ndp`).

By grouping numbers based on their remainder when divided by `k`, we naturally partition them into non-interacting groups. Numbers with different remainders can never conflict since their difference cannot be exactly `k`.

```cpp
class Solution {
public:
    int beautifulSubsets(vector<int>& nums, int k) {
        unordered_map<int, map<int, int>> groups;
        unordered_map<int, int> cnt;
        for (int& num : nums) {
            cnt[num]++;
        }

        // Group numbers based on remainder with k
        for (int num : nums) {
            groups[num % k][num] = cnt[num];
        }

        int res = 1;
        for (auto& [rem, g] : groups) {
            int prev = 0, dp = 0, ndp = 1;

            for (auto& [num, count] : g) {
                int have = (1 << count) - 1;
                int tmp = ndp;
                ndp += dp;

                if (prev == 0 || prev + k != num) {
                    dp = have * (tmp + dp);
                } else {
                    dp = tmp * have;
                }

                prev = num;
            }

            res *= (dp + ndp);
        }

        return res - 1;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$
