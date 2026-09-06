# 907. Sum of Subarray Minimums

- **Difficulty:** Medium  
- **Pattern:** Stack  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/sum-of-subarray-minimums/>  
- **NeetCode:** <https://neetcode.io/problems/sum-of-subarray-minimums>  
- **Video:** <https://www.youtube.com/watch?v=aX1F2-DrBkQ>  

[← Back to index](../INDEX.md)

## 1. Brute Force

For each subarray, we need to find its minimum element and add it to the total sum. The straightforward approach is to enumerate all possible subarrays by their start and end positions, tracking the running minimum as we extend each subarray.

```cpp
class Solution {
public:
    int sumSubarrayMins(vector<int>& arr) {
        int n = arr.size(), res = 0;
        const int MOD = 1000000007;

        for (int i = 0; i < n; i++) {
            int minVal = arr[i];
            for (int j = i; j < n; j++) {
                minVal = min(minVal, arr[j]);
                res = (res + minVal) % MOD;
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 2. Monotonically Increasing Stack (Two Pass)

Instead of computing minimums for each subarray, we can ask: for each element, how many subarrays is it the minimum of? An element `arr[i]` is the minimum of all subarrays that start after the previous smaller element and end before the next smaller element. A monotonically increasing stack helps us efficiently find these boundaries.

```cpp
class Solution {
public:
    int sumSubarrayMins(vector<int>& arr) {
        const int MOD = 1e9 + 7;
        int n = arr.size();

        // Compute previous smaller
        vector<int> prevSmaller(n, -1);
        stack<int> stack;
        for (int i = 0; i < n; i++) {
            while (!stack.empty() && arr[stack.top()] > arr[i]) {
                stack.pop();
            }
            prevSmaller[i] = stack.empty() ? -1 : stack.top();
            stack.push(i);
        }

        // Compute next smaller
        vector<int> nextSmaller(n, n);
        stack = {};
        for (int i = n - 1; i >= 0; i--) {
            while (!stack.empty() && arr[stack.top()] >= arr[i]) {
                stack.pop();
            }
            nextSmaller[i] = stack.empty() ? n : stack.top();
            stack.push(i);
        }

        // Calculate result
        long long res = 0;
        for (int i = 0; i < n; i++) {
            long long left = i - prevSmaller[i];
            long long right = nextSmaller[i] - i;
            res = (res + arr[i] * left * right) % MOD;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Monotonically Increasing Stack (One Pass)

We can combine finding the previous smaller and next smaller into a single pass. By adding sentinel values (negative infinity) at both ends of the array, we ensure every element gets processed. When we pop an element from the stack upon finding a smaller value, we immediately know both its left boundary (from the new stack top) and right boundary (the current index).

```cpp
class Solution {
public:
    int sumSubarrayMins(vector<int>& arr) {
        const int MOD = 1e9 + 7;
        int res = 0;
        vector<int> newArr(arr.size() + 2, INT_MIN);
        copy(arr.begin(), arr.end(), newArr.begin() + 1);

        stack<pair<int, int>> stack;

        for (int i = 0; i < newArr.size(); i++) {
            while (!stack.empty() && newArr[i] < stack.top().second) {
                auto [j, m] = stack.top();
                stack.pop();
                int left = stack.empty() ? j + 1 : j - stack.top().first;
                int right = i - j;
                res = (res + (long long) m * left * right % MOD) % MOD;
            }
            stack.emplace(i, newArr[i]);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Monotonically Increasing Stack (Optimal)

We can eliminate the sentinel values by handling the edge cases explicitly. Instead of padding the array, we iterate one position past the end and use a conditional check to treat the out-of-bounds position as having a smaller value than any element. This triggers final processing of remaining stack elements.

```cpp
class Solution {
public:
    int sumSubarrayMins(vector<int>& arr) {
        const int MOD = 1e9 + 7;
        int n = arr.size();
        stack<int> stack;
        long long res = 0;

        for (int i = 0; i <= n; i++) {
            while (!stack.empty() && (i == n || arr[i] < arr[stack.top()])) {
                int j = stack.top();
                stack.pop();
                int left = j - (stack.empty() ? -1 : stack.top());
                int right = i - j;
                res = (res + (long long) arr[j] * left * right) % MOD;
            }
            stack.push(i);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 5. Dynamic Programming + Stack

We can think of this problem dynamically. Let `dp[i]` represent the sum of minimums of all subarrays ending at index `i`. When we add element `arr[i]`, we need to consider: for subarrays where `arr[i]` is not the minimum, we can reuse previously computed values; for subarrays where `arr[i]` is the minimum, we count how many such subarrays exist. The stack helps us find where `arr[i]` stops being the minimum.

```cpp
class Solution {
public:
    int sumSubarrayMins(vector<int>& arr) {
        const int MOD = 1e9 + 7;
        int n = arr.size();
        vector<int> dp(n, 0);
        stack<int> stack;
        long long res = 0;

        for (int i = 0; i < n; i++) {
            while (!stack.empty() && arr[stack.top()] > arr[i]) {
                stack.pop();
            }

            int j = stack.empty() ? -1 : stack.top();
            dp[i] = ((j != -1 ? dp[j] : 0) + arr[i] * (i - j)) % MOD;
            res = (res + dp[i]) % MOD;
            stack.push(i);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$
