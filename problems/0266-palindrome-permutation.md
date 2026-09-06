# 266. Palindrome Permutation

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/palindrome-permutation/>  
- **NeetCode:** <https://neetcode.io/problems/palindrome-permutation>  

[← Back to index](../INDEX.md)

## 1. Brute Force

A string can form a palindrome if at most one character has an odd count. In a palindrome, characters mirror around the center, so pairs must exist for every character except possibly one in the middle.

The brute force approach counts occurrences of each possible ASCII character by iterating through the string for each character code. If more than one character has an odd frequency, no palindrome permutation is possible.

```cpp
class Solution {
public:
    bool canPermutePalindrome(string s) {
        int count[128] = {0};
        for (int j = 0; j < s.length(); j++) {
            count[s[j]]++;
        }
        int odd = 0;
        for (int i = 0; i < 128 && odd <= 1; i++) {
            odd += count[i] % 2;
        }
        return odd <= 1;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
    - If we generalize the solution to handle any Unicode character (no hardcoding): $O(k \cdot n)$. <br> $O(n^2)$ In the worst case, if all characters are unique $(k = n)$
- Space complexity: $O(1)$ If the we assume the input contains only ASCII characters.
    - $O(1)$ If the implementation is modiifed to handle Unicode characters.

> Where $n$ is the size of the input string `s` and where $k$ is the number of unique characters in `s`

## 2. Using HashMap

Instead of iterating through all possible ASCII characters, we can use a hash map to only track characters that actually appear in the string. This is more efficient when the string uses a small subset of the character set.

We count the frequency of each character, then check how many have odd counts. The palindrome condition remains the same: at most one odd frequency.

```cpp
class Solution {
public:
    bool canPermutePalindrome(string s) {
        unordered_map<char, int> map;
        for (int i = 0; i < s.length(); i++) {
            +map[s[i]]++;
        }
        int count = 0;
        for (auto& pair : map) {
            count += pair.second % 2;
        }
        return count <= 1;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
    - $O(n + k)$ If we generalize the solution to handle any Unicode character. In the worst case $(k = n)$, this becomes $O(n)$.
- Space complexity: $O(1)$ If the we assume the input contains only ASCII characters.
    - $O(k)$ If the implementation is modiifed to handle Unicode characters, the space complexity would depend on the number of unique characters in the string. $O(n)$ in the worst case (if all characters are unique).

> Where $n$ is the size of the input string `s` and where $k$ is the number of unique characters in `s`

## 3. Using Array

Since we know the input contains only ASCII characters (128 possible values), we can replace the hash map with a fixed-size array. Array access is faster than hash map lookups, and we avoid the overhead of hashing.

The logic is identical to the hash map approach, but we use the character's ASCII value as the array index.

```cpp
class Solution {
public:
    bool canPermutePalindrome(string s) {
        int map[128] = {0};
        for (char c : s) {
            map[int(c)]++;
        }
        int count = 0;
        for (int i = 0; i < 128 && count <= 1; i++) {
            count += map[i] % 2;
        }
        return count <= 1;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ If the we assume the input contains only ASCII characters.
    - $O(k)$ If the implementation is modiifed to handle Unicode characters, the space complexity would depend on the number of unique characters in the string. $O(n)$ in the worst case (if all characters are unique).

> Where $n$ is the size of the input string `s` and where $k$ is the number of unique characters in `s`

## 4. Single Pass

We can optimize further by tracking the odd count dynamically as we process each character. When a character's frequency becomes even, we decrement the odd count. When it becomes odd, we increment. This way, we know the final answer immediately after one pass without needing a second loop.

```cpp
class Solution {
public:
    bool canPermutePalindrome(string s) {
        int map[128] = {0};
        int count = 0;
        for (int i = 0; i < s.length(); i++) {
            map[int(s[i])]++;
            if (map[int(s[i])] % 2 == 0)
                count--;
            else
                count++;
        }
        return count <= 1;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ If the we assume the input contains only ASCII characters.
    - $O(k)$ If the implementation is modiifed to handle Unicode characters, the space complexity would depend on the number of unique characters in the string. $O(n)$ in the worst case (if all characters are unique).

> Where $n$ is the size of the input string `s` and where $k$ is the number of unique characters in `s`

## 5. Using Set

A set provides an elegant way to track characters with odd frequencies. When we see a character for the first time, we add it to the set. When we see it again, we remove it. Characters that appear an even number of times cancel out and leave the set. Only characters with odd frequencies remain.

At the end, if the set has at most one element, a palindrome permutation is possible.

```cpp
class Solution {
public:
    bool canPermutePalindrome(string s) {
        unordered_set<char> char_set;
        for (char c : s) {
            if (char_set.find(c) != char_set.end())
                char_set.erase(c);
            else
                char_set.insert(c);
        }
        return char_set.size() <= 1;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ If the we assume the input contains only ASCII characters.
    - $O(k)$ If the implementation is modiifed to handle Unicode characters, the space complexity would depend on the number of unique characters in the string. $O(n)$ in the worst case (if all characters are unique)

> Where $n$ is the size of the input string `s` and where $k$ is the number of unique characters in `s`
