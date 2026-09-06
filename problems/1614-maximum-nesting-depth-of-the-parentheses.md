# 1614. Maximum Nesting Depth of the Parentheses

- **Difficulty:** Easy  
- **Pattern:** Greedy  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/maximum-nesting-depth-of-the-parentheses/>  
- **NeetCode:** <https://neetcode.io/problems/maximum-nesting-depth-of-the-parentheses>  
- **Video:** <https://www.youtube.com/watch?v=FiQFJvCvWK4>  

[← Back to index](../INDEX.md)

## 1. Recursion

We can process the string from right to left using recursion. Each open parenthesis increases our depth count, and each close parenthesis decreases it. By tracking the maximum absolute value of this count at any point, we find the deepest nesting level. Processing from right to left means we encounter closing parentheses first, which decrement the counter, and opening parentheses later, which increment it.

```cpp
class Solution {
private:
    int res = 0;

    int dfs(const string& s, int i) {
        if (i == s.length()) {
            return 0;
        }

        int cur = dfs(s, i + 1);
        if (s[i] == '(') {
            cur += 1;
        } else if (s[i] == ')') {
            cur -= 1;
        }

        res = max(res, abs(cur));
        return cur;
    }

public:
    int maxDepth(string s) {
        dfs(s, 0);
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for recursion stack.

## 2. Stack

A stack naturally models nested structures. Each time we see an opening parenthesis, we push it onto the stack, increasing the current depth. Each closing parenthesis pops from the stack, decreasing the depth. The maximum stack size during traversal equals the maximum nesting depth.

```cpp
class Solution {
public:
    int maxDepth(string s) {
        int res = 0;
        stack<char> stack;

        for (char c : s) {
            if (c == '(') {
                stack.push(c);
                res = max(res, (int)stack.size());
            } else if (c == ')') {
                stack.pop();
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Iteration

We don't actually need to store the parentheses in a stack. Since we only care about the depth (stack size), we can replace the stack with a simple counter. This reduces space complexity to O(1) while maintaining the same logic.

```cpp
class Solution {
public:
    int maxDepth(string s) {
        int res = 0, cur = 0;

        for (char c : s) {
            if (c == '(') {
                cur++;
            } else if (c == ')') {
                cur--;
            }
            res = max(res, cur);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.
