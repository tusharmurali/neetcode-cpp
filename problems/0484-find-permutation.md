# 484. Find Permutation

- **Difficulty:** Medium  
- **Pattern:** Stack  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/find-permutation/>  
- **NeetCode:** <https://neetcode.io/problems/find-permutation>  

[← Back to index](../INDEX.md)

## 1. Using Stack

To produce the lexicographically smallest permutation, we want to place smaller numbers as early as possible. The string tells us the relationship between consecutive elements: 'I' means increasing, 'D' means decreasing. When we encounter a sequence of 'D's, we need to reverse the order of those numbers. A stack naturally handles this: push numbers onto the stack during 'D' sequences, then pop them all when we hit an 'I' (or the end), which reverses their order.

```cpp
class Solution {
public:
    vector<int> findPermutation(string s) {
        vector<int> res(s.length() + 1);
        stack<int> stk;
        int j = 0;

        for (int i = 1; i <= s.length(); i++) {
            if (s[i - 1] == 'I') {
                stk.push(i);
                while (!stk.empty()) {
                    res[j++] = stk.top();
                    stk.pop();
                }
            } else {
                stk.push(i);
            }
        }

        stk.push(s.length() + 1);
        while (!stk.empty()) {
            res[j++] = stk.top();
            stk.pop();
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

> Where $n$ is the number of elements in the resultant arrangement

## 2. Reversing the Subarray

Start with the identity permutation `[1, 2, ..., n+1]`, which is already the smallest possible arrangement. Whenever we see a sequence of consecutive 'D's, we need those corresponding elements to be in decreasing order. We can achieve this by reversing the subarray that spans those 'D's. This maintains the smallest possible values in earlier positions while satisfying the decrease constraints.

```cpp
class Solution {
public:
    vector<int> findPermutation(string s) {
        int n = s.length();
        vector<int> res(n + 1);

        for (int i = 0; i < res.size(); i++) {
            res[i] = i + 1;
        }

        int i = 1;

        while (i <= n) {
            int j = i;

            while (i <= n && s[i - 1] == 'D') {
                i++;
            }

            reverse(res, j - 1, i);
            i++;
        }

        return res;
    }

    void reverse(vector<int>& a, int start, int end) {
        for (int i = 0; i < (end - start) / 2; i++) {
            int temp = a[i + start];
            a[i + start] = a[end - i - 1];
            a[end - i - 1] = temp;
        }
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

> Where $n$ is the size of the resultant array

## 3. Two Pointers

We can build the result directly without explicitly reversing subarrays. For 'I' characters, we simply place the next available number. For 'D' sequences, we need to place a decreasing run of numbers. When we find a sequence of `k` consecutive 'D's, we fill those `k+1` positions with decreasing values starting from the highest value in that range. This is done by identifying the 'D' segment boundaries and filling values in reverse order.

```cpp
class Solution {
public:
    vector<int> findPermutation(string s) {
        int n = s.length();
        vector<int> res(n + 1);
        res[0] = 1;
        int i = 1;

        while (i <= n) {
            res[i] = i + 1;
            int j = i;

            if (s[i - 1] == 'D') {
                while (i <= n && s[i - 1] == 'D') {
                    i++;
                }

                for (int k = j - 1, c = i; k <= i - 1; k++, c--) {
                    res[k] = c;
                }
            } else {
                i++;
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

> Where $n$ is the size of the resultant array
