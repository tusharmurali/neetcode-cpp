# 1422. Maximum Score After Splitting a String

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/maximum-score-after-splitting-a-string/>  
- **NeetCode:** <https://neetcode.io/problems/maximum-score-after-splitting-a-string>  
- **Video:** <https://www.youtube.com/watch?v=mc_eSStDrWw>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The score at any split point is the sum of zeros in the left substring plus the sum of ones in the right substring. The simplest approach is to try every valid split position and count directly. For each split, we scan the left portion to count zeros and the right portion to count ones, then track the maximum score found.

```cpp
class Solution {
public:
    int maxScore(string s) {
        int n = s.size(), res = 0;
        for (int i = 1; i < n; i++) {
            int leftZero = 0, rightOne = 0;
            for (int j = 0; j < i; j++) {
                if (s[j] == '0') {
                    leftZero++;
                }
            }
            for (int j = i; j < n; j++) {
                if (s[j] == '1') {
                    rightOne++;
                }
            }
            res = max(res, leftZero + rightOne);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 2. Prefix & Suffix Arrays

Instead of recounting zeros and ones for every split position, we can precompute cumulative counts. A prefix array stores the count of zeros up to each index, while a suffix array stores the count of ones from each index to the end. This way, evaluating any split becomes an O(1) lookup.

```cpp
class Solution {
public:
    int maxScore(string s) {
        int n = s.size();
        vector<int> leftZero(n, 0), rightOne(n, 0);

        if (s[0] == '0') {
            leftZero[0] = 1;
        }
        for (int i = 1; i < n; i++) {
            leftZero[i] = leftZero[i - 1];
            if (s[i] == '0') {
                leftZero[i]++;
            }
        }

        if (s[n - 1] == '1') {
            rightOne[n - 1] = 1;
        }
        for (int i = n - 2; i >= 0; i--) {
            rightOne[i] = rightOne[i + 1];
            if (s[i] == '1') {
                rightOne[i]++;
            }
        }

        int res = 0;
        for (int i = 1; i < n; i++) {
            res = max(res, leftZero[i - 1] + rightOne[i]);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Iteration (Two Pass)

We can avoid storing full arrays by maintaining running counts. First, count all ones in the string. Then iterate through the string, incrementing zeros and decrementing ones as we move the split point. At each position, the current counts represent exactly what we need for the score calculation.

```cpp
class Solution {
public:
    int maxScore(string s) {
        int zero = 0, one = 0, res = 0;

        for (char c : s) {
            if (c == '1') {
                one++;
            }
        }

        for (int i = 0; i < s.size() - 1; i++) {
            if (s[i] == '0') {
                zero++;
            } else {
                one--;
            }
            res = max(res, zero + one);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 4. Iteration (One Pass)

We can derive a single-pass solution using algebra. The score at position `i` equals `left_zeros + right_ones`. Since `right_ones = total_ones - left_ones`, the score becomes `left_zeros + total_ones - left_ones`, or equivalently `total_ones + (left_zeros - left_ones)`. Since `total_ones` is constant, we only need to maximize `(left_zeros - left_ones)` while iterating, then add the total ones at the end.

```cpp
class Solution {
public:
    int maxScore(string s) {
        // res = Max of all (leftZeros + rightOnes)
        // res = Max of all (leftZeros + (totalOnes - leftOnes))
        // res = totalOnes (constant) + Max of all (leftZeros - leftOnes)

        int zeros = 0, ones = 0, res = INT_MIN;

        if (s[0] == '0') {
            zeros++;
        } else {
            ones++;
        }

        for (int i = 1; i < s.size(); i++) {
            res = max(res, zeros - ones);
            if (s[i] == '0') {
                zeros++;
            } else {
                ones++;
            }
        }

        return res + ones;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$
