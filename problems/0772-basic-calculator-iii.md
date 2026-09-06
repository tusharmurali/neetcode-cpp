# 772. Basic Calculator III

- **Difficulty:** Hard  
- **Pattern:** Stack  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/basic-calculator-iii/>  
- **NeetCode:** <https://neetcode.io/problems/basic-calculator-iii>  

[← Back to index](../INDEX.md)

## 1. Stack

This problem adds parentheses to the basic calculator, which introduces nested sub-expressions. We handle this by using a stack that can hold both numbers and operators. When we see an opening parenthesis, we save the current operator and reset our state. When we see a closing parenthesis, we evaluate everything inside, then retrieve the saved operator to continue. The stack essentially lets us pause the outer expression, fully evaluate the inner one, and resume.

```cpp
class Solution {
public:
    int calculate(string s) {
        auto evaluate = [](int x, int y, char op) -> int {
            if (op == '+') {
                return x;
            }
            if (op == '-') {
                return -x;
            }
            if (op == '*') {
                return x * y;
            }
            return x / y;
        };

        vector<pair<int, bool>> stack;  // {value, isInt}
        int curr = 0;
        char previousOperator = '+';
        s += "@";

        for (char c : s) {
            if (isdigit(c)) {
                curr = curr * 10 + (c - '0');
            } else if (c == '(') {
                stack.push_back({previousOperator, false});
                previousOperator = '+';
            } else {
                if (previousOperator == '*' || previousOperator == '/') {
                    int top = stack.back().first;
                    stack.pop_back();
                    stack.push_back({evaluate(top, curr, previousOperator), true});
                } else {
                    stack.push_back({evaluate(curr, 0, previousOperator), true});
                }

                curr = 0;
                previousOperator = c;

                if (c == ')') {
                    while (!stack.empty() && stack.back().second) {
                        curr += stack.back().first;
                        stack.pop_back();
                    }
                    previousOperator = stack.back().first;
                    stack.pop_back();
                }
            }
        }

        int ans = 0;
        for (auto& p : stack) {
            ans += p.first;
        }

        return ans;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

> Where $n$ is the length of the expression

## 2. Solve Isolated Expressions With Recursion

Parentheses naturally suggest recursion. When we encounter an opening parenthesis, we can recursively evaluate everything inside it and treat the result as a single number. This makes the problem cleaner since each recursive call handles one level of nesting. The base case is a simple expression without parentheses, which we evaluate using the same logic as Basic Calculator II.

```cpp
class Solution {
public:
    int calculate(string s) {
        s += "@";
        int i = 0;
        return solve(s, i);
    }

private:
    int evaluate(char op, int x, int y) {
        if (op == '+') {
            return x;
        } else if (op == '-') {
            return -x;
        } else if (op == '*') {
            return x * y;
        }

        return x / y;
    }

    int solve(string& s, int& i) {
        stack<int> stk;
        int curr = 0;
        char previousOperator = '+';

        while (i < s.length()) {
            char c = s[i];

            if (c == '(') {
                i++;
                curr = solve(s, i);
            } else if (isdigit(c)) {
                curr = curr * 10 + (c - '0');
            } else {
                if (previousOperator == '*' || previousOperator == '/') {
                    int top = stk.top();
                    stk.pop();
                    stk.push(evaluate(previousOperator, top, curr));
                } else {
                    stk.push(evaluate(previousOperator, curr, 0));
                }

                if (c == ')') {
                    break;
                }

                curr = 0;
                previousOperator = c;
            }

            i++;
        }

        int ans = 0;
        while (!stk.empty()) {
            ans += stk.top();
            stk.pop();
        }

        return ans;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

> Where $n$ is the length of the expression
