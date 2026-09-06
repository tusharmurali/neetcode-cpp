# 227. Basic Calculator II

- **Difficulty:** Medium  
- **Pattern:** Stack  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/basic-calculator-ii/>  
- **NeetCode:** <https://neetcode.io/problems/basic-calculator-ii>  

[← Back to index](../INDEX.md)

## 1. Stack

The challenge with evaluating expressions is handling operator precedence. Multiplication and division must be done before addition and subtraction. We can use a `stack` to defer the addition and subtraction while immediately computing multiplication and division. For `+` and `-`, we push numbers onto the `stack` (negative for subtraction). For `*` and `/`, we pop the previous number, compute the result, and push it back. At the end, summing the `stack` gives us the answer.

```cpp
class Solution {
public:
    int calculate(string s) {
        s.erase(remove(s.begin(), s.end(), ' '), s.end());
        vector<int> stack;
        int num = 0;
        char op = '+';
        for (int i = 0; i < s.size(); i++) {
            char ch = s[i];
            if (isdigit(ch)) {
                num = num * 10 + (ch - '0');
            }
            if (!isdigit(ch) || i == s.size() - 1) {
                if (op == '+') {
                    stack.push_back(num);
                } else if (op == '-') {
                    stack.push_back(-num);
                } else if (op == '*') {
                    int prev = stack.back(); stack.pop_back();
                    stack.push_back(prev * num);
                } else {
                    int prev = stack.back(); stack.pop_back();
                    stack.push_back(prev / num);
                }
                op = ch;
                num = 0;
            }
        }
        int res = 0;
        for (int x : stack) res += x;
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Without Stack

We can avoid using a `stack` by realizing that we only need to track two values: the running `total` of all fully computed terms, and the `prev` term that might still be involved in a multiplication or division. When we see `+` or `-`, we can add the `prev` term to our `total` and start a new term. When we see `*` or `/`, we update the `prev` term directly. This reduces space complexity to `O(1)`.

```cpp
class Solution {
public:
    int calculate(string s) {
        int total = 0, prev = 0, num = 0;
        char op = '+';
        int n = s.size(), i = 0;
        while (i <= n) {
            char ch = i < n ? s[i] : '+';
            if (ch == ' ') {
                i++;
                continue;
            }
            if (isdigit(ch)) {
                num = num * 10 + (ch - '0');
            } else {
                if (op == '+') {
                    total += prev;
                    prev = num;
                } else if (op == '-') {
                    total += prev;
                    prev = -num;
                } else if (op == '*') {
                    prev = prev * num;
                } else {
                    prev = prev / num;
                }
                op = ch;
                num = 0;
            }
            i++;
        }
        total += prev;
        return total;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$
