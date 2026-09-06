# 1209. Remove All Adjacent Duplicates In String II

- **Difficulty:** Medium  
- **Pattern:** Stack  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/remove-all-adjacent-duplicates-in-string-ii/>  
- **NeetCode:** <https://neetcode.io/problems/remove-all-adjacent-duplicates-in-string-ii>  
- **Video:** <https://www.youtube.com/watch?v=w6LcypDgC4w>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The most direct approach is to repeatedly scan the string looking for `k` consecutive identical characters. When found, we remove them and restart the scan from the beginning since the removal might create new groups of `k` adjacent duplicates.

This process continues until a full scan completes without finding any group to remove. While straightforward, this approach is inefficient because each removal requires rescanning from the start.

```cpp
class Solution {
public:
    string removeDuplicates(string s, int k) {
        while (s.length()) {
            bool flag = false;
            char cur = s[0];
            int cnt = 1;

            for (int i = 1; i < s.size(); i++) {
                if (cur != s[i]) {
                    cnt = 0;
                    cur = s[i];
                }
                cnt++;
                if (cnt == k) {
                    s = s.substr(0, i - cnt + 1) + s.substr(i + 1);
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

- Time complexity: $O(\frac {n ^ 2}{k})$
- Space complexity: $O(n)$

## 2. Stack

To avoid rescanning the entire string after each removal, we can use a stack to track consecutive counts as we process each character. When we encounter a character, we check if it matches the previous one. If so, we increment the count; otherwise, we start a new count.

When the count reaches `k`, we remove those `k` characters and continue from where we left off. The stack helps us remember the count before the removal so we can correctly continue counting if the characters before and after the removed segment match.

```cpp
class Solution {
public:
    string removeDuplicates(string s, int k) {
        vector<int> stack;
        int n = s.length(), i = 0;

        while (i < n) {
            if (i == 0 || s[i] != s[i - 1]) {
                stack.push_back(1);
            } else {
                stack.back()++;
                if (stack.back() == k) {
                    stack.pop_back();
                    s.erase(i - k + 1, k);
                    i -= k;
                    n -= k;
                }
            }
            i++;
        }

        return s;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Stack (Optimal)

Instead of modifying the string and tracking counts separately, we can store both the character and its count together in the stack. This eliminates the need for in-place string manipulation and index adjustments.

Each stack entry is a pair of (character, count). When we encounter a new character, we either increment the count of the top entry (if it matches) or push a new entry. When a count reaches `k`, we simply pop that entry. Building the result at the end involves expanding each entry back into its characters.

```cpp
class Solution {
public:
    string removeDuplicates(string s, int k) {
        vector<pair<char, int>> stack;

        for (char c : s) {
            if (!stack.empty() && stack.back().first == c) {
                stack.back().second++;
            } else {
                stack.push_back({c, 1});
            }
            if (stack.back().second == k) {
                stack.pop_back();
            }
        }

        string res;
        for (auto& p : stack) {
            res.append(p.second, p.first);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Two Pointers

This approach uses the input array itself as both the working space and the result, avoiding the need for a separate stack data structure. We use two pointers: `j` reads through the original string while `i` writes the result.

A separate count array tracks consecutive occurrences at each write position. When we write a character, we check if it matches the previous written character to determine its count. If the count reaches `k`, we "rewind" the write pointer by `k` positions, effectively removing those characters.

```cpp
class Solution {
public:
    string removeDuplicates(string s, int k) {
        int i = 0, n = s.length();
        vector<int> count(n);
        for (int j = 0; j < n; i++, j++) {
            s[i] = s[j];
            count[i] = 1;
            if (i > 0 && s[i - 1] == s[j]) {
                count[i] += count[i - 1];
            }
            if (count[i] == k) i -= k;
        }
        return s.substr(0, i);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/1209-remove-all-adjacent-duplicates-in-string-ii.cpp` in the NeetCode repo)

```cpp
// Time and space complexity is O(n) where n is the size of the input string.
class Solution {
public:
    string removeDuplicates(string s, int k) {
      stack<pair<char , int>> st;
      
      for(int i = 0 ; i < s.size(); i++)
      {
        int count = 1;
        if(!st.empty() && st.top().first == s[i])
        {
          count += st.top().second;
          st.pop();
        }
        
        st.push({s[i] , count});
        
        if(count == k) st.pop();
        
      }
      
      string ans = "";
      while(!st.empty())
      {
        int freq = st.top().second;
        int c = st.top().first;
        while(freq > 0)
        {
           ans += c;
           freq--;
        }
        
        st.pop();
      }
      
      reverse(ans.begin() , ans.end());
      return ans;
    }
};
```
