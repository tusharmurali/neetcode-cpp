# 439. Ternary Expression Parser

- **Difficulty:** Medium  
- **Pattern:** Stack  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/ternary-expression-parser/>  
- **NeetCode:** <https://neetcode.io/problems/ternary-expression-parser>  

[← Back to index](../INDEX.md)

## 1. Find Rightmost Atomic Expression

A ternary expression like `T?a:b` consists of a condition (`T` or `F`), followed by `?`, then the true branch, `:`, and the false branch. When expressions are nested, we can evaluate from the inside out.

The key insight is that the rightmost atomic expression (a simple `B?E1:E2` where both `E1` and `E2` are single characters) can always be evaluated first without affecting the rest. By repeatedly finding and reducing these atomic expressions from right to left, we eventually collapse the entire expression to a single result.

```cpp
class Solution {
public:
    string parseTernary(string expression) {

        // Checks if the string s is a valid atomic expression
        auto isValidAtomic = [](string s) {
            return (s[0] == 'T' || s[0] == 'F') && s[1] == '?' && ((s[2] >= '0' && s[2] <= '9') || s[2] == 'T' || s[2] == 'F') && s[3] == ':' && ((s[4] >= '0' && s[4] <= '9') || s[4] == 'T' || s[4] == 'F');
        };

        // Returns the value of the atomic expression
        auto solveAtomic = [](string s) {
            return s[0] == 'T' ? s[2] : s[4];
        };

        // Reduce expression until we are left with a single character
        while (expression.size() != 1) {
            int j = expression.size() - 1;
            while (!isValidAtomic(expression.substr(j-4, 5))) {
                j--;
            }
            expression = expression.substr(0, j-4) + solveAtomic(expression.substr(j-4, 5)) + expression.substr(j+1);
        }

        // Return the final character
        return expression;
    }
};
```

**Complexity**

- Time complexity: $O(N^2)$
- Space complexity: $O(N)$

> Where $N$ is the length of `expression`

## 2. Reverse Polish Notation

Instead of validating the full atomic expression pattern, we can simplify by just finding the rightmost `?` operator. The character immediately before `?` is the condition, and the characters at positions `+1` and `+3` relative to `?` are the true and false values respectively.

This works because the rightmost `?` is always part of the innermost (deepest nested) ternary that can be evaluated. After each reduction, the next rightmost `?` becomes evaluable.

```cpp
class Solution {
public:
    string parseTernary(string expression) {

        // Reduce expression until we are left with a single character
        while (expression.size() != 1) {
            int questionMarkIndex = expression.size() - 1;
            while (expression[questionMarkIndex] != '?') {
                questionMarkIndex--;
            }

            // Find the value of the expression.
            char value;
            if (expression[questionMarkIndex - 1] == 'T') {
                value = expression[questionMarkIndex + 1];
            } else {
                value = expression[questionMarkIndex + 3];
            }

            // Replace the expression with the value
            expression = expression.substr(0, questionMarkIndex - 1) + value + expression.substr(questionMarkIndex + 4);
        }

        // Return the final character
        return expression;
    }
};
```

**Complexity**

- Time complexity: $O(N^2)$
- Space complexity: $O(N)$

> Where $N$ is the length of `expression`

## 3. Reverse Polish Notation using Stack

Processing from right to left with a stack eliminates the need for string manipulation. When we encounter a `?`, we know the stack contains the true value, `:`, and false value (in that order from top). The current character is the condition, so we can immediately resolve which value to keep.

This approach processes each character exactly once and avoids expensive substring operations, achieving linear time complexity.

```cpp
class Solution {
public:
    string parseTernary(string expression) {

        // Initialize a stack
        stack<char> stack;

        // Traverse the expression from right to left
        for (int i = expression.length() - 1; i >= 0; i--) {

            // If stack top is ?, then replace next four characters
            // with E1 or E2 depending on the value of B
            if (!stack.empty() && stack.top() == '?') {
                stack.pop();
                char onTrue = stack.top();
                stack.pop();
                stack.pop();
                char onFalse = stack.top();
                stack.pop();
                stack.push(expression[i] == 'T' ? onTrue : onFalse);
            }

            // Otherwise, push this character
            else {
                stack.push(expression[i]);
            }
        }

        // Return the final character
        return string(1, stack.top());
    }
};
```

**Complexity**

- Time complexity: $O(N)$
- Space complexity: $O(N)$

> Where $N$ is the length of `expression`

## 4. Binary Tree

A ternary expression naturally maps to a binary tree structure. Each condition becomes a node, with its true branch as the left child and false branch as the right child. Leaf nodes hold the final values (digits or `T`/`F`).

Once the tree is built, evaluating the expression is straightforward: start at the root and traverse left for `T` conditions, right for `F` conditions, until reaching a leaf.

```cpp
struct TreeNode {
    char val;
    TreeNode* left;
    TreeNode* right;

    TreeNode(char val) : val(val), left(nullptr), right(nullptr) {}
};

class Solution {
private:
    int index = 0;

    TreeNode* constructTree(string& expression) {

        // Storing current character of expression
        TreeNode* root = new TreeNode(expression[index]);
        // If last character of expression, return
        if (index == expression.length() - 1) {
            return root;
        }

        // Check next character
        index++;
        if (expression[index] == '?') {
            index++;
            root->left = constructTree(expression);
            index++;
            root->right = constructTree(expression);
        }

        return root;
    }

public:
    string parseTernary(string expression) {

        // Construct Binary Tree
        TreeNode* root = constructTree(expression);

        // Parse the binary tree till we reach the leaf node
        while (root->left != nullptr && root->right != nullptr) {
            if (root->val == 'T') {
                root = root->left;
            } else {
                root = root->right;
            }
        }

        return string(1, root->val);
    }
};
```

**Complexity**

- Time complexity: $O(N)$
- Space complexity: $O(N)$

> Where $N$ is the length of `expression`

## 5. Recursion

We can evaluate the expression top-down by recursively processing subexpressions. The key challenge is finding where the true branch ends and the false branch begins, since branches can contain nested ternaries.

By counting `?` and `:` characters, we can find the matching `:` for any given `?`. Each `?` increments a counter, each `:` decrements it. When the counter reaches zero, we have found the boundary between the true and false branches.

```cpp
class Solution {
private:
    string expression;

    // To analyze the expression between two indices
    string solve(int i, int j) {
        // If expression is a single character, return it
        if (i == j) {
            return string(1, expression[i]);
        }

        // Find the index of ?
        int questionMarkIndex = i;
        while (expression[questionMarkIndex] != '?') {
            questionMarkIndex++;
        }

        // Find one index after corresponding :
        int aheadColonIndex = questionMarkIndex + 1;
        int count = 1;
        while (count != 0) {
            if (expression[aheadColonIndex] == '?') {
                count++;
            } else if (expression[aheadColonIndex] == ':') {
                count--;
            }
            aheadColonIndex++;
        }

        // Check the value of B and recursively solve
        if (expression[i] == 'T') {
            return solve(questionMarkIndex + 1, aheadColonIndex - 2);
        } else {
            return solve(aheadColonIndex, j);
        }
    }

public:
    string parseTernary(string expr) {
        expression = expr;
        // Solve for the entire expression
        return solve(0, expression.length() - 1);
    }
};
```

**Complexity**

- Time complexity: $O(N^2)$
- Space complexity: $O(N)$

> Where $N$ is the length of `expression`

## 6. Constant Space Solution

We can evaluate the expression iteratively without recursion or extra space by simulating the evaluation process directly. Starting from the beginning, we repeatedly decide whether to take the true or false branch based on each condition.

When the condition is `T`, we simply skip past the `?` to the true branch. When it is `F`, we must skip the entire true branch (which may contain nested ternaries) by counting `?` and `:` to find where the false branch starts.

```cpp
class Solution {
public:
    string parseTernary(string expression) {
        int i = 0;
        for ( ; i < expression.length(); ) {

            if (expression[i] != 'T' && expression[i] != 'F'
            || i == expression.length() - 1 || expression[i + 1] == ':') {
                break;
            }
            if (expression[i] == 'T') {
                i += 2;
            } else {
                int count;
                for (count = 1, i += 2; count != 0; i++) {
                    if (expression[i] == ':') {
                        count--;
                    } else if (expression[i] == '?') {
                        count++;
                    }
                }
            }
        }

        return expression.substr(i, 1);
    }
};
```

**Complexity**

- Time complexity: $O(N)$
- Space complexity: $O(1)$

> Where $N$ is the length of `expression`
