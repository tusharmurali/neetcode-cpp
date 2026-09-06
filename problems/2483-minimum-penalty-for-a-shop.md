# 2483. Minimum Penalty for a Shop

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/minimum-penalty-for-a-shop/>  
- **NeetCode:** <https://neetcode.io/problems/minimum-penalty-for-a-shop>  
- **Video:** <https://www.youtube.com/watch?v=0d7ShRoOFVE>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The shop can close at any hour from `0` to `n` (inclusive). If we close at hour `i`, we incur a penalty of `1` for each 'N' before hour `i` (shop was open but no customer) and `1` for each 'Y' from hour `i` onward (shop was closed but customer came). We try every possible closing time and pick the one with minimum penalty.

```cpp
class Solution {
public:
    int bestClosingTime(string customers) {
        int n = customers.size();
        int res = n, minPenalty = n;

        for (int i = 0; i <= n; i++) {
            int penalty = 0;
            for (int j = 0; j < i; j++) {
                if (customers[j] == 'N') {
                    penalty++;
                }
            }
            for (int j = i; j < n; j++) {
                if (customers[j] == 'Y') {
                    penalty++;
                }
            }

            if (penalty < minPenalty) {
                minPenalty = penalty;
                res = i;
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 2. Prefix & Suffix

Instead of recounting 'N' and 'Y' characters for each closing hour, we precompute prefix counts of 'N' and suffix counts of 'Y'. The prefix array tells us how many 'N' characters appear before each position, and the suffix array tells us how many 'Y' characters appear from each position onward. The penalty at any closing hour is simply the sum of these two precomputed values.

```cpp
class Solution {
public:
    int bestClosingTime(string customers) {
        int n = customers.size(), cnt = 0;

        vector<int> prefixN(n + 1);
        for (int i = 0; i < n; i++) {
            prefixN[i] = cnt;
            if (customers[i] == 'N') {
                cnt++;
            }
        }
        prefixN[n] = cnt;

        vector<int> suffixY(n + 1, 0);
        for (int i = n - 1; i >= 0; i--) {
            suffixY[i] = suffixY[i + 1];
            if (customers[i] == 'Y') {
                suffixY[i]++;
            }
        }

        int res = n, minPenalty = n;
        for (int i = 0; i <= n; i++) {
            int penalty = prefixN[i] + suffixY[i];
            if (penalty < minPenalty) {
                minPenalty = penalty;
                res = i;
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Iteration (Two Pass)

We can avoid storing arrays by computing on the fly. First, count all 'Y' characters. This represents the penalty if we close at hour `0` (we miss all customers). Then iterate through the string: each 'Y' we pass reduces the penalty (we served them), and each 'N' we pass increases it (we were open for nothing). Track the minimum penalty as we go.

```cpp
class Solution {
public:
    int bestClosingTime(string customers) {
        int cntY = count(customers.begin(), customers.end(), 'Y');

        int minPenalty = cntY, res = 0, cntN = 0;
        for (int i = 0; i < customers.size(); i++) {
            if (customers[i] == 'Y') {
                cntY--;
            } else {
                cntN++;
            }

            int penalty = cntN + cntY;
            if (penalty < minPenalty) {
                res = i + 1;
                minPenalty = penalty;
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 4. Iteration (One Pass)

We can solve this in a single pass using a clever observation. Instead of tracking absolute penalty, we track a relative score. Treat 'Y' as `+1` (benefit of staying open) and 'N' as `-1` (cost of staying open). As we iterate, we accumulate this score. The optimal closing time is right after the point where this cumulative score is maximized, meaning we captured the most value from being open.

```cpp
class Solution {
public:
    int bestClosingTime(string customers) {
        int res = 0, minPenalty = 0, penalty = 0;

        for (int i = 0; i < customers.size(); i++) {
            penalty += customers[i] == 'Y' ? 1 : -1;

            if (penalty > minPenalty) {
                minPenalty = penalty;
                res = i + 1;
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/2483-minimum-penalty-for-a-shop.cpp` in the NeetCode repo)

```cpp
/*
  You are given the customer visit log of a shop represented by a 0-indexed string customers consisting only of characters 'N' and 'Y':
      if the ith character is 'Y', it means that customers come at the ith hour
      whereas 'N' indicates that no customers come at the ith hour.
      
  If the shop closes at the jth hour (0 <= j <= n), the penalty is calculated as follows:
      For every hour when the shop is open and no customers come, the penalty increases by 1.
      For every hour when the shop is closed and customers come, the penalty increases by 1.
      
  Return the earliest hour at which the shop must be closed to incur a minimum penalty.
  Note that if a shop closes at the jth hour, it means the shop is closed at the hour j.

  Ex. Input: customers = "YYNY"
      Output: 2
      Explanation: 
      - Closing the shop at the 0th hour incurs in 1+1+0+1 = 3 penalty.
      - Closing the shop at the 1st hour incurs in 0+1+0+1 = 2 penalty.
      - Closing the shop at the 2nd hour incurs in 0+0+0+1 = 1 penalty.
      - Closing the shop at the 3rd hour incurs in 0+0+1+1 = 2 penalty.
      - Closing the shop at the 4th hour incurs in 0+0+1+0 = 1 penalty.
      Closing the shop at 2nd or 4th hour gives a minimum penalty. Since 2 is earlier, the optimal closing time is 2.

  Time  : O(N)
  Space : O(1)
*/

class Solution {
public:
    int bestClosingTime(string customers) {
        int res = -1, maxi = 0, pen = 0;
        for(int i = 0 ; i < customers.size() ; ++i) {
            if(customers[i] == 'Y')
                ++pen;
            else 
                --pen;
            if(pen > maxi) {
                maxi = pen;
                res = i;
            }
        }
        return ++res;
    }
};
```
