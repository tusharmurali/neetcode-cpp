# 1498. Number of Subsequences That Satisfy The Given Sum Condition

- **Difficulty:** Medium  
- **Pattern:** Two Pointers  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/number-of-subsequences-that-satisfy-the-given-sum-condition/>  
- **NeetCode:** <https://neetcode.io/problems/number-of-subsequences-that-satisfy-the-given-sum-condition>  
- **Video:** <https://www.youtube.com/watch?v=xCsIkPLS4Ls>  

[← Back to index](../INDEX.md)

## 1. Brute Force (Recursion)

We generate all possible subsequences using recursion, tracking the minimum and maximum values chosen so far. If a non-empty subsequence has `min + max <= target`, we count it. This explores the full power set of the array.

```cpp
class Solution {
public:
    const int MOD = 1e9 + 7;

    int numSubseq(vector<int>& nums, int target) {
        return dfs(nums, INT_MIN, INT_MAX, 0, target);
    }

private:
    int dfs(vector<int>& nums, int maxi, int mini, int i, int target) {
        if (i == nums.size()) {
            if (mini != INT_MAX && (maxi + mini) <= target) {
                return 1;
            }
            return 0;
        }

        int skip = dfs(nums, maxi, mini, i + 1, target);
        int include = dfs(nums, max(maxi, nums[i]), min(mini, nums[i]), i + 1, target);
        return (skip + include) % MOD;
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ n)$
- Space complexity: $O(n)$ for recursion stack.

## 2. Binary Search

After sorting, for each element as the minimum, we use binary search to find the rightmost element that can serve as the maximum (where `min + max <= target`). All elements between these two positions can freely be included or excluded, giving `2^(count)` valid subsequences with this minimum.

```cpp
class Solution {
public:
    int numSubseq(vector<int>& nums, int target) {
        sort(nums.begin(), nums.end());
        int MOD = 1000000007;
        int res = 0;

        for (int i = 0; i < nums.size(); i++) {
            if (nums[i] * 2 > target) break;

            int l = i, r = nums.size() - 1;
            while (l <= r) {
                int mid = l + (r - l) / 2;
                if (nums[i] + nums[mid] <= target) {
                    l = mid + 1;
                } else {
                    r = mid - 1;
                }
            }

            long long count = powMod(2, r - i, MOD);
            res = (res + count) % MOD;
        }
        return res;
    }

private:
    long long powMod(int base, int exp, int mod) {
        long long result = 1, b = base;
        while (exp > 0) {
            if (exp & 1) result = (result * b) % mod;
            b = (b * b) % mod;
            exp >>= 1;
        }
        return result;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 3. Two Pointers

After sorting, we use two pointers. The left pointer represents the minimum element we must include. The right pointer starts at the end and shrinks inward until the sum constraint is satisfied. Since the array is sorted, once the right pointer moves left, it never needs to go back.

```cpp
class Solution {
public:
    int numSubseq(vector<int>& nums, int target) {
        sort(nums.begin(), nums.end());
        int res = 0, mod = 1000000007;
        int r = nums.size() - 1;

        for (int i = 0; i < nums.size(); i++) {
            while (i <= r && nums[i] + nums[r] > target) {
                r--;
            }
            if (i <= r) {
                res = (res + power(2, r - i, mod)) % mod;
            }
        }
        return res;
    }

private:
    long long power(int base, int exp, int mod) {
        long long result = 1, b = base;
        while (exp > 0) {
            if (exp & 1) result = (result * b) % mod;
            b = (b * b) % mod;
            exp >>= 1;
        }
        return result;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 4. Two Pointers (Optimal)

We precompute all powers of `2` up to `n` to avoid repeated exponentiation. The two pointer logic moves inward from both ends: if the current pair satisfies the constraint, count the subsequences and advance the left pointer; otherwise, shrink the right pointer.

```cpp
class Solution {
public:
    int numSubseq(vector<int>& nums, int target) {
        sort(nums.begin(), nums.end());
        int MOD = 1000000007;
        int res = 0, l = 0, r = nums.size() - 1;
        vector<int> power(nums.size(), 1);

        for (int i = 1; i < nums.size(); i++) {
            power[i] = (power[i - 1] * 2) % MOD;
        }

        while (l <= r) {
            if (nums[l] + nums[r] <= target) {
                res = (res + power[r - l]) % MOD;
                l++;
            } else {
                r--;
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/1498-number-of-subsequences-that-satisfy-the-given-sum-condition.cpp` in the NeetCode repo)

```cpp
// Time Complexity - O(nlogn)
// Space Complexity - O(n)

class Solution {
public:
    int numSubseq(vector<int>& nums, int target) {
        sort(nums.begin(), nums.end());
        int n = nums.size();

        int left = 0, right = n - 1;
        int res = 0, mod = 1e9 + 7;
        while (left <= right) {
            if (nums[left] + nums[right] > target) {
                right--;
            } 
            else {
                res = (res + fastPower(2, right - left, mod)) % mod;
                left++;
            }
        }
        return res;
    }
    
    int fastPower(int a, int b, int mod) {
        long long ans = 1;
        long long base = a;
        while (b != 0) {
            if (b % 2 == 1) {
                ans = (ans * base) % mod;
            }
            base = (base * base) % mod;
            b /= 2;
        }
        return ans;
    }
};
```
