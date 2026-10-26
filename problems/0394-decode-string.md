# 394. Decode String

- **Difficulty:** Medium  
- **Pattern:** Stack  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/decode-string/>  
- **NeetCode:** <https://neetcode.io/problems/decode-string>  
- **Video:** <https://www.youtube.com/watch?v=qB0zZpBJlh8>  
- **Video approach:** 2. One Stack  

[← Back to index](../INDEX.md)

## 1. Recursion

The encoded string has a nested structure where patterns like `k[encoded_string]` can contain other encoded patterns inside. This naturally maps to recursion. When we encounter an opening bracket, we recursively decode the inner content, then repeat it `k` times. The recursion handles arbitrary nesting depth automatically.

```cpp
class Solution {
private:
    string helper(int& i, string& s) {
        string res;
        int k = 0;

        while (i < s.size()) {
            char c = s[i];

            if (isdigit(c)) {
                k = k * 10 + (c - '0');
            } else if (c == '[') {
                i++;
                string subRes = helper(i, s);
                while (k-- > 0) res += subRes;
                k = 0;
            } else if (c == ']') {
                return res;
            } else {
                res += c;
            }

            i++;
        }

        return res;
    }

public:
    string decodeString(string s) {
        int i = 0;
        return helper(i, s);
    }
};
```

**Complexity**

- Time complexity: $O(nN)$, using the problem's fixed upper bound of $300$ on repeat counts

    - The Java, C++, Kotlin, Swift, and Rust versions use growing string buffers and have the tighter bound $O(n + (d + 1)N)$. A decoded substring can be copied at every enclosing bracket, even when the repeat count is $1$. For example, nesting the pattern `1[a...]` $d$ times produces $d$ letters but builds intermediate results of lengths $1, 2, \ldots, d$, requiring $\Theta(d^2)$ character copying. Thus $O(n + N)$ is not a general time bound.
    - The $O(nN)$ bound also accounts for copying accumulated prefixes during string concatenation. Python and JavaScript runtimes may optimize some of these copies. The C# and Go versions additionally concatenate immutable strings inside their repetition loops: for `k[a]`, they build strings of lengths $1$ through $k$. If repeat counts are allowed to grow without the problem's cap, a conservative bound for those two versions is $O(nN + N^2)$.

- Space complexity: $O(n + N)$

> Where $n$ is the length of the input string, $N$ is the length of the output string, and $d$ is the maximum bracket nesting depth.

## 2. One Stack ▶ video

We can convert the recursive approach to an iterative one using a single stack. Push every character onto the stack until we hit a closing bracket `]`. At that point, pop characters to extract the substring inside the brackets, then pop the digits to get the repeat count `k`. Multiply the substring and push the result back onto the stack. This simulates the recursive call stack.

```cpp
class Solution {
public:
    string decodeString(string s) {
        vector<string> stack;

        for (char& c : s) {
            if (c != ']') {
                stack.push_back(string(1, c));
            } else {
                string substr = "";
                while (stack.back() != "[") {
                    substr = stack.back() + substr;
                    stack.pop_back();
                }
                stack.pop_back();

                string k = "";
                while (!stack.empty() && isdigit(stack.back()[0])) {
                    k = stack.back() + k;
                    stack.pop_back();
                }
                int repeatCount = stoi(k);

                string repeated = "";
                for (int i = 0; i < repeatCount; ++i) {
                    repeated += substr;
                }
                stack.push_back(repeated);
            }
        }

        string res = "";
        for (const string& part : stack) {
            res += part;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(nN)$

    - There are $O(n)$ stack pushes and pops because each closing bracket pushes one decoded block, not its individual characters. Prepending a popped block or expanding a bracket can copy up to $O(N)$ characters. This accounts for both repeated front concatenation and copying the same decoded block through nested brackets. An $O(n + N^2)$ bound alone misses the latter when the nesting depth is much larger than the output length.

- Space complexity: $O(n + N)$

> Where $n$ is the length of the input string and $N$ is the length of the output string.

## 3. Two Stacks

Using two separate stacks provides cleaner logic: one stack for accumulated strings and another for repeat counts. When we see `[`, we save the current string and count, then start fresh. When we see `]`, we pop the previous string and count, repeat the current string, and concatenate. This approach avoids the overhead of extracting digits and substrings from a mixed stack.

```cpp
class Solution {
public:
    string decodeString(string s) {
        vector<string> stringStack;
        vector<int> countStack;
        string cur = "";
        int k = 0;

        for (char c : s) {
            if (isdigit(c)) {
                k = k * 10 + (c - '0');
            } else if (c == '[') {
                stringStack.push_back(cur);
                countStack.push_back(k);
                cur = "";
                k = 0;
            } else if (c == ']') {
                string temp = cur;
                cur = stringStack.back();
                stringStack.pop_back();
                int count = countStack.back();
                countStack.pop_back();
                for (int i = 0; i < count; i++) {
                    cur += temp;
                }
            } else {
                cur += c;
            }
        }

        return cur;
    }
};
```

**Complexity**

- Time complexity: $O(nN)$, using the problem's fixed upper bound of $300$ on repeat counts

    - The Java, C++, Swift, and Rust versions use growing string buffers and have the tighter bound $O(n + (d + 1)N)$. Closing a bracket copies the decoded inner string into its parent's result, so the same characters can be copied at each of the $d$ levels, including levels with repeat count $1$.
    - The $O(nN)$ bound also allows for copying accumulated prefixes; Python and JavaScript runtimes may optimize some copies. Unlike the recursive Kotlin version, this Kotlin version uses immutable strings, as do the C# and Go versions. Their repetition loops repeatedly copy the growing result. Without the fixed cap on repeat counts, a conservative bound for these three versions is $O(nN + N^2)$.

- Space complexity: $O(n + N)$

> Where $n$ is the length of the input string, $N$ is the length of the output string, and $d$ is the maximum bracket nesting depth.

## Standalone solution file (`cpp/0394-decode-string.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    string decodeString(string s) {
        stack<string> stack;
        string result;

        for (int i = 0; i < s.length(); i++) {
            if (s[i] != ']') {
                stack.push(string(1, s[i]));
            } else {
                string substr;
                while (!stack.empty() && stack.top() != "[") {
                    substr = stack.top() + substr;
                    stack.pop();
                }
                stack.pop();

                string k;
                while (!stack.empty() && isdigit(stack.top()[0])) {
                    k = stack.top() + k;
                    stack.pop();
                }
                int kInt = stoi(k);

                string temp;
                for (int j = 0; j < kInt; j++) {
                    temp += substr;
                }
                stack.push(temp);
            }
        }

        while (!stack.empty()) {
            result = stack.top() + result;
            stack.pop();
        }

        return result;
    }
};
```
