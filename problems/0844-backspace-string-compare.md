# 844. Backspace String Compare

- **Difficulty:** Easy  
- **Pattern:** Two Pointers  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/backspace-string-compare/>  
- **NeetCode:** <https://neetcode.io/problems/backspace-string-compare>  
- **Video:** <https://www.youtube.com/watch?v=k2qrymM_DOo>  

[← Back to index](../INDEX.md)

## 1. Stack

The backspace character `#` removes the previous character, which is exactly what a stack does well. We can simulate typing each string by pushing regular characters onto a stack and popping when we see a `#`. After processing both strings this way, we just compare the resulting stacks.

```cpp
class Solution {
public:
    bool backspaceCompare(string s, string t) {
        return convert(s) == convert(t);
    }

private:
    string convert(const string& s) {
        string res = "";
        for (char c : s) {
            if (c == '#') {
                if (!res.empty()) {
                    res.pop_back();
                }
            } else {
                res += c;
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(n + m)$

> Where $n$ is the length of the string $s$ and $m$ is the length of the string $t$.

## 2. Reverse iteration

Instead of building the result from the beginning, we can iterate from the end. When we encounter a `#`, we know we need to skip the next valid character. By counting backspaces as we go backward, we can skip the right number of characters before adding one to our result. This still uses extra space for storing the result, but gives us a different perspective on the problem.

```cpp
class Solution {
public:
    bool backspaceCompare(string s, string t) {
        return convert(s) == convert(t);
    }

private:
    string convert(string s) {
        string res;
        int backspace = 0;
        for (int i = s.size() - 1; i >= 0; i--) {
            if (s[i] == '#') {
                backspace++;
            } else if (backspace > 0) {
                backspace--;
            } else {
                res += s[i];
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(n + m)$

> Where $n$ is the length of the string $s$ and $m$ is the length of the string $t$.

## 3. Two Pointers - I

We can compare the strings character by character without building the full result. Starting from the end of both strings, we find the next valid character in each (skipping over characters deleted by backspaces). If at any point these characters differ, the strings are not equal. This approach uses O(1) extra space since we only track pointers and counts.

```cpp
class Solution {
public:
    bool backspaceCompare(string s, string t) {
        int indexS = s.size() - 1, indexT = t.size() - 1;

        while (indexS >= 0 || indexT >= 0) {
            indexS = nextValidChar(s, indexS);
            indexT = nextValidChar(t, indexT);

            char charS = indexS >= 0 ? s[indexS] : '\0';
            char charT = indexT >= 0 ? t[indexT] : '\0';

            if (charS != charT) return false;

            indexS--;
            indexT--;
        }

        return true;
    }

private:
    int nextValidChar(string &str, int index) {
        int backspace = 0;

        while (index >= 0) {
            if (str[index] == '#') {
                backspace++;
            } else if (backspace > 0) {
                backspace--;
            } else {
                break;
            }
            index--;
        }

        return index;
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(1)$

> Where $n$ is the length of the string $s$ and $m$ is the length of the string $t$.

## 4. Two Pointers - II

This is a more compact version of the two-pointer approach. Instead of using a helper function, we inline the logic for skipping characters. The core idea remains the same: iterate backward through both strings simultaneously, skip characters that would be deleted by backspaces, and compare the remaining characters one by one.

```cpp
class Solution {
public:
    bool backspaceCompare(string s, string t) {
        int indexS = s.size() - 1, indexT = t.size() - 1;
        int backspaceS = 0, backspaceT = 0;

        while (true) {

            while (indexS >= 0 && (backspaceS > 0 || s[indexS] == '#')) {
                backspaceS += (s[indexS] == '#') ? 1 : -1;
                indexS--;
            }

            while (indexT >= 0 && (backspaceT > 0 || t[indexT] == '#')) {
                backspaceT += (t[indexT] == '#') ? 1 : -1;
                indexT--;
            }

            if (!(indexS >= 0 && indexT >= 0 && s[indexS] == t[indexT])) {
                return indexS == -1 && indexT == -1;
            }
            indexS--;
            indexT--;
        }
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(1)$

> Where $n$ is the length of the string $s$ and $m$ is the length of the string $t$.
