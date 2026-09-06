# 645. Set Mismatch

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/set-mismatch/>  
- **NeetCode:** <https://neetcode.io/problems/set-mismatch>  
- **Video:** <https://www.youtube.com/watch?v=d-ulaeRBA64>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The array should contain each number from 1 to n exactly once, but one number is duplicated and one is missing. The most direct approach is to count how many times each number from 1 to n appears in the array. A number appearing twice is the duplicate, and a number appearing zero times is the missing one.

```cpp
class Solution {
public:
    vector<int> findErrorNums(vector<int>& nums) {
        vector<int> res(2, 0);
        int n = nums.size();

        for (int i = 1; i <= n; i++) {
            int cnt = 0;
            for (int num : nums) {
                if (num == i) {
                    cnt++;
                }
            }

            if (cnt == 0) {
                res[1] = i;
            } else if (cnt == 2) {
                res[0] = i;
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 2. Sorting

After sorting, consecutive elements should differ by exactly 1. If two adjacent elements are equal, we found the duplicate. If two adjacent elements differ by 2, the missing number lies between them. We also need to handle the edge case where the missing number is n (the last element after sorting is not n).

```cpp
class Solution {
public:
    vector<int> findErrorNums(vector<int>& nums) {
        vector<int> res = {0, 1};
        sort(nums.begin(), nums.end());

        for (int i = 1; i < nums.size(); i++) {
            if (nums[i] == nums[i - 1]) {
                res[0] = nums[i];
            } else if (nums[i] - nums[i - 1] == 2) {
                res[1] = nums[i] - 1;
            }
        }

        if (nums.back() != nums.size()) {
            res[1] = nums.size();
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 3. Frequency Count (Hash Table)

Using extra space, we can count occurrences in a single pass and then check each number's frequency. A frequency array of size n+1 lets us directly index by number value. The number with count 2 is the duplicate, and the number with count 0 is the missing one.

```cpp
class Solution {
public:
    vector<int> findErrorNums(vector<int>& nums) {
        int n = nums.size();
        vector<int> count(n + 1, 0);
        vector<int> res(2, 0);

        for (int num : nums) {
            count[num]++;
        }

        for (int i = 1; i <= n; i++) {
            if (count[i] == 0) {
                res[1] = i;
            }
            if (count[i] == 2) {
                res[0] = i;
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Negative Marking

We can use the input array itself as a hash table by marking visited indices. For each number, we negate the value at the corresponding index. If we try to negate an already negative value, we found the duplicate. After processing, any positive value indicates its index corresponds to the missing number.

```cpp
class Solution {
public:
    vector<int> findErrorNums(vector<int>& nums) {
        vector<int> res(2);

        for (int num : nums) {
            int absNum = abs(num);
            if (nums[absNum - 1] < 0) {
                res[0] = absNum;
            } else {
                nums[absNum - 1] *= -1;
            }
        }

        for (int i = 0; i < nums.size(); i++) {
            if (nums[i] > 0 && i + 1 != res[0]) {
                res[1] = i + 1;
                return res;
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 5. Math

Using sum formulas, we can set up equations to solve for the duplicate and missing numbers. Let the duplicate be `d` and the missing be `m`. The difference between actual sum and expected sum gives us `d - m`. The difference between actual sum of squares and expected sum of squares gives us `d^2 - m^2 = (d+m)(d-m)`. With these two equations, we can solve for both values.

```cpp
class Solution {
public:
    vector<int> findErrorNums(vector<int>& nums) {
        int N = nums.size();
        long long x = 0; // duplicate - missing
        long long y = 0; // duplicate^2 - missing^2

        for (int i = 1; i <= N; i++) {
            x += nums[i - 1] - i;
            y += (long long)nums[i - 1] * nums[i - 1] - (long long)i * i;
        }

        int missing = (y - x * x) / (2 * x);
        int duplicate = missing + x;
        return {duplicate, missing};
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 6. Bitwise XOR

XOR has the property that `a ^ a = 0`. If we XOR all numbers in the array with all numbers from 1 to n, pairs cancel out, leaving us with `duplicate ^ missing`. To separate them, we find a bit where they differ (using the rightmost set bit), then partition all numbers into two groups based on that bit. XORing within each group isolates the duplicate and missing values.

```cpp
class Solution {
public:
    vector<int> findErrorNums(vector<int>& nums) {
        int N = nums.size();
        // a ^ a = 0
        // xorr = (1 ^ 2 ^ ... N) ^ (nums[0] ^ nums[1] ^ ... nums[N - 1])
        // xorr = missing ^ duplicate
        int xorr = 0;
        for (int i = 1; i <= N; i++) {
            xorr ^= i;
            xorr ^= nums[i - 1];
        }

        // bit that is set in only one number among (duplicate, missing),
        // will be set in (duplicate ^ missing)
        // take rightMost set bit for simplicity
        int rightMostBit = xorr & ~(xorr - 1);

        // divide numbers (from nums, from [1, N]) into two sets w.r.t the rightMostBit
        // xorr the numbers of these sets independently
        int x = 0, y = 0;
        for (int i = 1; i <= N; i++) {
            if (i & rightMostBit) {
                x ^= i;
            } else {
                y ^= i;
            }

            if (nums[i - 1] & rightMostBit) {
                x ^= nums[i - 1];
            } else {
                y ^= nums[i - 1];
            }
        }

        // identify the duplicate number from x and y
        for (int num : nums) {
            if (num == x) {
                return {x, y};
            }
        }
        return {y, x};
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$
