# 2390. Removing Stars From a String

- **Difficulty:** Medium  
- **Pattern:** Stack  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/removing-stars-from-a-string/>  
- **NeetCode:** <https://neetcode.io/problems/removing-stars-from-a-string>  
- **Video:** <https://www.youtube.com/watch?v=pRyFZIaKegA>  

[← Back to index](../INDEX.md)

## 1. Brute Force

Each star removes the closest non-star character to its left. The simplest approach is to simulate this process directly: scan for a star, remove it along with the character before it, then repeat until no more removals are possible. This is straightforward but inefficient because each removal requires rebuilding the string. In the loop, we iterate with index `i` to find each star.

```cpp
class Solution {
public:
    string removeStars(string s) {
        while (true) {
            bool flag = false;
            for (int i = 1; i < s.size(); ++i) {
                if (s[i] == '*' && s[i - 1] != '*') {
                    s = s.substr(0, i - 1) + s.substr(i + 1);
                    flag = true;
                    break;
                }
            }
            if (!flag) {
                break;
            }
        }
        return s;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 2. Brute Force (Optimized)

Instead of restarting the scan from the beginning after each removal, we can continue from where we left off, adjusting our position backward after removing characters. This avoids redundant scanning of already-processed portions, though string manipulation still takes linear time per removal. We track the current position with `i` and the length with `n`.

```cpp
class Solution {
public:
    string removeStars(string s) {
        int n = s.length();
        int i = 0;
        while (i < n) {
            if (i > 0 && s[i] == '*' && s[i - 1] != '*') {
                s = s.substr(0, i - 1) + s.substr(i + 1);
                n -= 2;
                i -= 2;
            }
            i++;
        }
        return s;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 3. Stack

A star removes the most recently added non-star character, which is exactly what a stack does with pop operations. As we scan the string with index `i`, we push non-star characters `c` onto the `stack`. When we encounter a star, we pop the top element. The remaining `stack` contents form the answer.

```cpp
class Solution {
public:
    string removeStars(string s) {
        stack<char> stack;
        for (char c : s) {
            if (c == '*') {
                if (!stack.empty()) stack.pop();
            } else {
                stack.push(c);
            }
        }
        string res;
        while (!stack.empty()) {
            res += stack.top();
            stack.pop();
        }
        reverse(res.begin(), res.end());
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Two Pointers

We can avoid extra space by using the input array itself. A left pointer `l` tracks where the next valid character should be placed, while a right pointer `r` scans through the string. For stars, we decrement `l` to "undo" the last character. For regular characters, we write them at position `l` and increment `l`. The result is the substring from `0` to `l`.

```cpp
class Solution {
public:
    string removeStars(string s) {
        int l = 0;

        for (int r = 0; r < s.size(); r++) {
            if (s[r] == '*') {
                l--;
            } else {
                s[l] = s[r];
                l++;
            }
        }
        return s.substr(0, l);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the language.

## Standalone solution file (`cpp/2390-removing-stars-from-a-string.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    string removeStars(string s) {
        stack<char> stk;
        for(int i=0;i<s.size();i++){
            if(s[i]=='*'){
                stk.pop();
            }else stk.push(s[i]);
        }
        string res = "";
        while(!stk.empty()){
            res += stk.top();
            stk.pop();
        }
         reverse(res.begin(), res.end());
         return res;
    }
};
```
