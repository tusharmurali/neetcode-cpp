# 1769. Minimum Number of Operations to Move All Balls to Each Box

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/minimum-number-of-operations-to-move-all-balls-to-each-box/>  
- **NeetCode:** <https://neetcode.io/problems/minimum-number-of-operations-to-move-all-balls-to-each-box>  
- **Video:** <https://www.youtube.com/watch?v=ZmH3gHiIqfI>  

[← Back to index](../INDEX.md)

## 1. Brute Force

For each box position, we want to know the total number of moves needed to bring all balls to that position. A move shifts a ball one position left or right. The cost to move a ball from position `i` to position `pos` is simply the absolute difference `|pos - i|`.

We can compute this directly by iterating through all boxes for each target position and summing up the distances from each `ball`.

```cpp
class Solution {
public:
    vector<int> minOperations(string boxes) {
        int n = boxes.size();
        vector<int> res(n, 0);

        for (int pos = 0; pos < n; pos++) {
            for (int i = 0; i < n; i++) {
                if (boxes[i] == '1') {
                    res[pos] += abs(pos - i);
                }
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity:
    - $O(1)$ extra space.
    - $O(n)$ space for the output list.

## 2. Prefix Sum

We can split the total cost for each position into contributions from the left and the right. For `balls` on the left, the cost is `i * count_left - sum_of_indices_left`. For `balls` on the right, the cost is `sum_of_indices_right - i * count_right`. Using prefix sums for both the `count` of `balls` and the sum of their `indices`, we can compute both parts efficiently.

```cpp
class Solution {
public:
    vector<int> minOperations(string boxes) {
        int n = boxes.size();
        vector<int> res(n), prefixCount(n + 1, 0), indexSum(n + 1, 0);

        for (int i = 0; i < n; i++) {
            prefixCount[i + 1] = prefixCount[i] + (boxes[i] == '1' ? 1 : 0);
            indexSum[i + 1] = indexSum[i] + (boxes[i] == '1' ? i : 0);
        }

        for (int i = 0; i < n; i++) {
            int left = prefixCount[i];
            int leftSum = indexSum[i];
            int right = prefixCount[n] - prefixCount[i + 1];
            int rightSum = indexSum[n] - indexSum[i + 1];
            res[i] = i * left - leftSum + (rightSum - i * right);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Prefix Sum (Optimal)

Instead of storing prefix arrays, we can compute the contribution incrementally using two passes. In the left-to-right pass, we track how many `balls` are to the left and accumulate the `moves` needed to shift them one position right. In the right-to-left pass, we do the same for `balls` on the right. The sum of both passes gives the final answer.

```cpp
class Solution {
public:
    vector<int> minOperations(string boxes) {
        int n = boxes.size();
        vector<int> res(n, 0);

        int balls = 0, moves = 0;
        for (int i = 0; i < n; i++) {
            res[i] = balls + moves;
            moves += balls;
            balls += boxes[i] - '0';
        }

        balls = moves = 0;
        for (int i = n - 1; i >= 0; i--) {
            res[i] += balls + moves;
            moves += balls;
            balls += boxes[i] - '0';
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity:
    - $O(1)$ extra space.
    - $O(n)$ space for the output list.
