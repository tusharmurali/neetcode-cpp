# 387. First Unique Character in a String

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/first-unique-character-in-a-string/>  
- **NeetCode:** <https://neetcode.io/problems/first-unique-character-in-a-string>  
- **Video:** <https://www.youtube.com/watch?v=rBENYgWy3xU>  

[← Back to index](../INDEX.md)

## 1. Brute Force

For each character in the string, we check if it appears anywhere else. If a character has no duplicate, it is unique. The first such character we find (going left to right) is our answer.

```cpp
class Solution {
public:
    int firstUniqChar(string s) {
        for (int i = 0; i < s.size(); i++) {
            bool flag = true;
            for (int j = 0; j < s.size(); j++) {
                if (i == j) continue;
                if (s[i] == s[j]) {
                    flag = false;
                    break;
                }
            }
            if (flag) return i;
        }
        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 2. Hash Map

Instead of checking every pair of characters, we can count the frequency of each character in a single pass. Then, in a second pass, we find the first character whose count is exactly 1. This trades space for time.

```cpp
class Solution {
public:
    int firstUniqChar(string s) {
        unordered_map<char, int> count;
        for (char c : s) {
            count[c]++;
        }

        for (int i = 0; i < s.size(); i++) {
            if (count[s[i]] == 1) {
                return i;
            }
        }
        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ since we have at most $26$ different characters.

## 3. Hash Map (Optimal)

We can optimize the second pass by iterating over the hash map instead of the string. For each character, we store its first occurrence index. If the character appears again, we mark it as non-unique by setting its index to `n` (string length). Finally, we find the minimum index among all unique characters.

```cpp
class Solution {
public:
    int firstUniqChar(string s) {
        int n = s.size();
        unordered_map<char, int> count;

        for (int i = 0; i < n; i++) {
            if (count.find(s[i]) == count.end()) {
                count[s[i]] = i;
            } else {
                count[s[i]] = n;
            }
        }

        int res = n;
        for (auto& [key, index] : count) {
            res = min(res, index);
        }

        return res == n ? -1 : res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ since we have at most $26$ different characters.

## 4. Iteration

Since the string contains only lowercase letters, we can iterate through all 26 characters and find the first occurrence of each. If a character's first and last occurrence are the same index, it appears exactly once. We track the minimum such index across all characters.

```cpp
class Solution {
public:
    int firstUniqChar(string s) {
        int res = s.size();

        for (char ch = 'a'; ch <= 'z'; ch++) {
            int firstIndex = s.find(ch);
            if (firstIndex != string::npos && s.rfind(ch) == firstIndex) {
                res = min(res, firstIndex);
            }
        }

        return res == s.size() ? -1 : res;
    }
};
```

**Complexity**

- Time complexity: $O(26 * n)$ since we have at most $26$ different characters.
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0387-first-unique-character-in-a-string.cpp` in the NeetCode repo)

```cpp
class Solution{    
    public:    
        unordered_map<char, int> Map = {};    
        int firstUniqChar(string s){            
            char c;            
            int Min;            
            for(int i = 0; i < s.length(); i++){                
                if(Map.find(s[i]) != Map.end()){                    
                    Map[s[i]]++;                    
                }
                else{                    
                    Map.insert(make_pair(s[i], 1));                    
                }                
            }            
            Min = s.length();            
            for(auto & m : Map){                
                if((m.second == 1) && (s.find(m.first) < Min)){                    
                    c = m.first;                    
                    Min = s.find(m.first);                    
                }                
            }            
            return Min == s.length() ? -1 : Min;
        }       
};
```
