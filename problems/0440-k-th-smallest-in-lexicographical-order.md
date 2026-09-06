# 440. K-th Smallest in Lexicographical Order

- **Difficulty:** Hard  
- **Pattern:** Math & Geometry  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/k-th-smallest-in-lexicographical-order/>  
- **NeetCode:** <https://neetcode.io/problems/k-th-smallest-in-lexicographical-order>  
- **Video:** <https://www.youtube.com/watch?v=wRubz1zhVqk>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The simplest approach converts all numbers from `1` to `n` into strings and sorts them lexicographically. In lexicographical order, "10" comes before "2" because '1' < '2'. After sorting, we simply return the `k`-th element. This is straightforward but inefficient for large `n`.

```cpp
class Solution {
public:
    int findKthNumber(int n, int k) {
        vector<string> nums;
        for (int num = 1; num <= n; ++num) {
            nums.push_back(to_string(num));
        }
        sort(nums.begin(), nums.end());
        return stoi(nums[k - 1]);
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 2. Prefix Count

Numbers in lexicographical order form a tree structure where each prefix leads to its extensions. For example, prefix "1" leads to "10", "11", ..., "19", "100", etc. We can count how many numbers exist under any prefix without enumerating them. Starting at "1", we count how many numbers lie in the subtree rooted at the current prefix. If this count is less than or equal to the remaining `k`, we skip this entire subtree and move to the next sibling. Otherwise, we descend into the subtree by appending a digit.

```cpp
class Solution {
public:
    int findKthNumber(int n, int k) {
        long long cur = 1;
        long long i = 1;
        while (i < k) {
            long long steps = count(cur, n);
            if (i + steps <= k) {
                cur++;
                i += steps;
            } else {
                cur *= 10;
                i++;
            }
        }
        return (int)cur;
    }

private:
    long long count(long long cur, int n) {
        long long res = 0;
        long long nei = cur + 1;
        while (cur <= n) {
            res += min(nei, (long long)n + 1) - cur;
            cur *= 10;
            nei *= 10;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O((\log n) ^ 2)$
- Space complexity: $O(1)$
