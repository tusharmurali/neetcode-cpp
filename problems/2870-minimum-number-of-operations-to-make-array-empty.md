# 2870. Minimum Number of Operations to Make Array Empty

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/minimum-number-of-operations-to-make-array-empty/>  
- **NeetCode:** <https://neetcode.io/problems/minimum-number-of-operations-to-make-array-empty>  
- **Video:** <https://www.youtube.com/watch?v=_AcO35R0fss>  

[← Back to index](../INDEX.md)

## 1. Recursion

We can only delete elements in groups of 2 or 3, and all elements in a group must be identical. This means we need to count the frequency of each element and figure out how to reduce each frequency to zero using the minimum number of deletions.

For any `count`, we try both options: subtract 2 or subtract 3, and recursively solve for the remaining `count`. If we reach exactly `0`, we are done. If we go negative, that path is invalid. The `min` of both branches gives us the answer.

```cpp
class Solution {
public:
    int minOperations(vector<int>& nums) {
        unordered_map<int, int> count;
        for (int num : nums) {
            count[num]++;
        }

        int res = 0;
        for (auto& [num, cnt] : count) {
            int op = dfs(cnt);
            if (op == INT_MAX) {
                return -1;
            }
            res += op;
        }

        return res;
    }

private:
    int dfs(int cur) {
        if (cur < 0) {
            return INT_MAX;
        }
        if (cur == 0) {
            return 0;
        }

        int ops = min(dfs(cur - 2), dfs(cur - 3));
        return ops == INT_MAX ? ops : 1 + ops;
    }
};
```

**Complexity**

- Time complexity: $O(n * 2 ^ m)$
- Space complexity: $O(n + m)$

> Where $n$ is the size of the array $nums$ and $m$ is the average frequency of the array elements.

## 2. Dynamic Programming (Top-Down)

The recursive solution has overlapping subproblems. When computing the minimum operations for a `count`, we may revisit the same `count` multiple times. By caching results, we avoid redundant computation and make the solution efficient.

```cpp
class Solution {
    unordered_map<int, int> cache;
public:
    int minOperations(vector<int>& nums) {
        unordered_map<int, int> count;
        for (int num : nums) {
            count[num]++;
        }

        int res = 0;
        for (auto& [num, cnt] : count) {
            int op = dfs(cnt);
            if (op == INT_MAX) {
                return -1;
            }
            res += op;
        }

        return res;
    }

private:
    int dfs(int cur) {
        if (cur < 0) {
            return INT_MAX;
        }
        if (cur == 2 || cur == 3) {
            return 1;
        }
        if (cache.count(cur)) {
            return cache[cur];
        }

        int res = min(dfs(cur - 2), dfs(cur - 3));
        cache[cur] = res == INT_MAX ? res : res + 1;
        return cache[cur];
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(n + m)$

> Where $n$ is the size of the array $nums$ and $m$ is the average frequency of the array elements.

## 3. Dynamic Programming (Bottom-Up)

Instead of solving recursively from larger counts down to zero, we can build up solutions from smaller counts. We precompute the minimum operations for all counts from 0 up to the maximum frequency, using the recurrence relation derived earlier.

```cpp
class Solution {
public:
    int minOperations(vector<int>& nums) {
        unordered_map<int, int> count;
        for (int num : nums) {
            count[num]++;
        }

        int maxf = 0;
        for (auto& [num, freq] : count) {
            maxf = max(maxf, freq);
        }

        vector<int> minOps(maxf + 1, 0);
        minOps[1] = INT_MAX;

        for (int i = 2; i <= maxf; i++) {
            minOps[i] = minOps[i - 2];
            if (i - 3 >= 0) {
                minOps[i] = min(minOps[i], minOps[i - 3]);
            }
            if (minOps[i] != INT_MAX) {
                minOps[i] += 1;
            }
        }

        int res = 0;
        for (auto& [num, cnt] : count) {
            int op = minOps[cnt];
            if (op == INT_MAX) {
                return -1;
            }
            res += op;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(n + m)$

> Where $n$ is the size of the array $nums$ and $m$ is the average frequency of the array elements.

## 4. Greedy

There is a mathematical pattern: for any `count` greater than `1`, the minimum operations is the ceiling of `count / 3`. This works because we prioritize groups of `3`, and any remainder can be handled by converting some `3`s to `2`s. For example, `count = 4` uses two `2`s, `count = 5` uses one `2` and one `3`.

The only impossible case is when `count` equals `1`, since we need at least `2` identical elements to perform any deletion.

```cpp
class Solution {
public:
    int minOperations(vector<int>& nums) {
        unordered_map<int, int> count;
        for (int num : nums) {
            count[num]++;
        }

        int res = 0;
        for (auto& [num, cnt] : count) {
            if (cnt == 1) {
                return -1;
            }
            res += (cnt + 2) / 3;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$
