# 254. Factor Combinations

- **Difficulty:** Medium  
- **Pattern:** Backtracking  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/factor-combinations/>  
- **NeetCode:** <https://neetcode.io/problems/factor-combinations>  

[← Back to index](../INDEX.md)

## 1. Backtracking

To find all unique factor combinations of `n`, we use backtracking. At each step, we take the last factor in our current list and try to split it into two smaller factors. By only considering factors greater than or equal to the previous one, we avoid generating duplicate combinations like `[2, 6]` and `[6, 2]`.

The key insight is that if we have a product, we only need to try factors up to the square root of that product. If `i` divides the product, then both `i` and `product/i` are factors, and we recursively continue with `product/i`.

```cpp
class Solution {
    void backtracking(vector<int>& factors, vector<vector<int>>& ans) {
        // Got a solution,
        if (factors.size() > 1) {
            ans.push_back(factors);
        }

        const int lastFactor = factors.back();
        factors.pop_back();

        for (int i = factors.empty() ? 2 : factors.back(); i <= lastFactor / i; ++i) {
            if (lastFactor % i == 0) {
                // Add i and lastFactor / i.
                factors.push_back(i);
                factors.push_back(lastFactor / i);
                backtracking(factors, ans);
                // Remove the last 2 elements in factors to restore it after the recursion returns
                factors.pop_back();
                factors.pop_back();
            }
        }

        // Add lastFactor back to factors to restore it.
        factors.push_back(lastFactor);
    }

public:
    vector<vector<int>> getFactors(int n) {
        vector<int> factors = {n};
        vector<vector<int>> ans;
        backtracking(factors, ans);

        return ans;
    }
};
```

**Complexity**

- Time complexity: $O(n^{1.5})$

- Space complexity: $O(\log (n))$

> Where $n$ is the input integer `n`.

## 2. Iterative DFS

The iterative approach uses an explicit stack instead of recursion. Each stack entry contains the current list of factors being built. We pop a state, extract its last factor, and try all valid ways to split it into two smaller factors.

This approach creates new factor lists for each branch rather than modifying and restoring a single list, which simplifies the logic but uses more memory.

```cpp
class Solution {
public:
    vector<vector<int>> getFactors(int n) {
        vector<vector<int>> ans;
        stack<vector<int>> stack;
        stack.push({n});

        while (!stack.empty()) {
            auto factors = stack.top();
            stack.pop();
            const int lastFactor = factors.back();
            factors.pop_back();

            for (int i = factors.empty() ? 2 : factors.back(); i <= lastFactor / i; ++i) {
                if (lastFactor % i == 0) {
                    vector<int> newFactors = factors;
                    newFactors.push_back(i);
                    newFactors.push_back(lastFactor / i);
                    stack.push(newFactors);
                    ans.push_back(newFactors);
                }
            }
        }

        return ans;
    }
};
```

**Complexity**

- Time complexity: $O(n^{1.5})$

- Space complexity: $O(n \cdot \log (n))$

> Where $n$ is the input integer `n`.
