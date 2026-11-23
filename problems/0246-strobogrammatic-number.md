# 246. Strobogrammatic Number

- **Difficulty:** Easy  
- **Pattern:** Two Pointers  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/strobogrammatic-number/>  
- **NeetCode:** <https://neetcode.io/problems/strobogrammatic-number>  

[← Back to index](../INDEX.md)

## 1. Reverse String

```cpp
class Solution {
public:
    bool isStrobogrammatic(string num) {
        unordered_map<char, char> rotated = {
            {'0', '0'}, {'1', '1'}, {'6', '9'}, {'8', '8'}, {'9', '6'}
        };
        string res;
        for (int i = num.size() - 1; i >= 0; i--) {
            if (!rotated.count(num[i])) {
                return false;
            }
            res += rotated[num[i]];
        }
        return res == num;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

> Where $n$ is the length of the string $num$.

## 2. Recursion

```cpp
class Solution {
public:
    bool isStrobogrammatic(string num) {
        return dfs(num, 0, num.size() - 1);
    }

private:
    unordered_map<char, char> rotated = {
        {'0', '0'}, {'1', '1'}, {'6', '9'}, {'8', '8'}, {'9', '6'}
    };

    bool dfs(const string& num, int l, int r) {
        if (l > r) {
            return true;
        }
        auto it = rotated.find(num[l]);
        if (it == rotated.end() || it->second != num[r]) {
            return false;
        }
        return dfs(num, l + 1, r - 1);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for the recursion stack.

> Where $n$ is the length of the string $num$.

## 3. Two Pointers

```cpp
class Solution {
public:
    bool isStrobogrammatic(string num) {
        unordered_map<char, char> rotated = {
            {'0', '0'}, {'1', '1'}, {'6', '9'}, {'8', '8'}, {'9', '6'}
        };
        int l = 0, r = num.size() - 1;
        while (l <= r) {
            auto it = rotated.find(num[l]);
            if (it == rotated.end() || it->second != num[r]) {
                return false;
            }
            l++;
            r--;
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

> Where $n$ is the length of the string $num$.
