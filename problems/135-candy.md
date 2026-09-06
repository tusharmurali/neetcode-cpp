# 135. Candy

- **Difficulty:** Hard  
- **Pattern:** Greedy  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/candy/>  
- **NeetCode:** <https://neetcode.io/problems/candy>  
- **Video:** <https://www.youtube.com/watch?v=1IzCRCcK17A>  

[← Back to index](../INDEX.md)

## 1. Brute Force

We process children left to right, adjusting candies to satisfy the constraint that higher-rated children get more candy than their neighbors. When we increase a child's candy count, we may violate the constraint with a previous child, so we propagate updates backward as needed. This approach ensures correctness but may revisit the same positions multiple times.

```cpp
class Solution {
public:
    int candy(vector<int>& ratings) {
        int n = ratings.size();
        vector<int> arr(n, 1);

        for (int i = 0; i < n - 1; i++) {
            if (ratings[i] == ratings[i + 1]) {
                continue;
            }
            if (ratings[i + 1] > ratings[i]) {
                arr[i + 1] = arr[i] + 1;
            } else if (arr[i] == arr[i + 1]) {
                arr[i + 1] = arr[i];
                arr[i]++;
                for (int j = i - 1; j >= 0; j--) {
                    if (ratings[j] > ratings[j + 1]) {
                        if (arr[j + 1] < arr[j]) {
                            break;
                        }
                        arr[j]++;
                    }
                }
            }
        }

        return accumulate(arr.begin(), arr.end(), 0);
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 2. Greedy (Two Pass)

We can handle left and right neighbors separately. First, scan left to right to ensure each child with a higher rating than their left neighbor gets more candy. Then, scan right to left to handle the right neighbor constraint. When adjusting for right neighbors, we take the maximum of the current value and what the right constraint requires, preserving the left constraint satisfaction.

```cpp
class Solution {
public:
    int candy(vector<int>& ratings) {
        int n = ratings.size();
        vector<int> arr(n, 1);

        for (int i = 1; i < n; i++) {
            if (ratings[i - 1] < ratings[i]) {
                arr[i] = arr[i - 1] + 1;
            }
        }

        for (int i = n - 2; i >= 0; i--) {
            if (ratings[i] > ratings[i + 1]) {
                arr[i] = max(arr[i], arr[i + 1] + 1);
            }
        }

        return accumulate(arr.begin(), arr.end(), 0);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Greedy (One Pass)

We can compute the result without storing candy counts for each child. The key insight is that ratings form a sequence of increasing and decreasing runs. For an increasing run of length `k`, we need 1+2+...+k extra candies above the base. For a decreasing run of length `k`, we also need 1+2+...+k extra candies. The peak between an increasing and decreasing run should belong to whichever run is longer.

```cpp
class Solution {
public:
    int candy(vector<int>& ratings) {
        int n = ratings.size();
        int res = n;

        int i = 1;
        while (i < n) {
            if (ratings[i] == ratings[i - 1]) {
                i++;
                continue;
            }

            int inc = 0;
            while (i < n && ratings[i] > ratings[i - 1]) {
                inc++;
                res += inc;
                i++;
            }

            int dec = 0;
            while (i < n && ratings[i] < ratings[i - 1]) {
                dec++;
                res += dec;
                i++;
            }

            res -= min(inc, dec);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.
