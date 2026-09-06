# 389. Find the Difference

- **Difficulty:** Easy  
- **Pattern:** Bit Manipulation  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/find-the-difference/>  
- **NeetCode:** <https://neetcode.io/problems/find-the-difference>  
- **Video:** <https://www.youtube.com/watch?v=oFmv4N4z00c>  

[← Back to index](../INDEX.md)

## 1. Two Hash Maps

String `t` is formed by shuffling string `s` and adding one extra character. By counting the frequency of each character in both strings, the added character will have a higher count in `t` than in `s`. We can compare these counts to find the difference.

```cpp
class Solution {
public:
    char findTheDifference(string s, string t) {
        vector<int> countS(26, 0), countT(26, 0);

        for (char c : s) countS[c - 'a']++;
        for (char c : t) countT[c - 'a']++;

        for (int i = 0; i < 26; i++) {
            if (countT[i] > countS[i]) {
                return i + 'a';
            }
        }
        return ' ';
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ since we have at most $26$ different characters.

## 2. One Hash Map

Instead of using two separate count arrays, we can use a single array. First count all characters from `t`, then subtract counts for characters in `s`. The character left with count `1` is the added character.

```cpp
class Solution {
public:
    char findTheDifference(string s, string t) {
        vector<int> count(26);

        for (char c : t) count[c - 'a']++;
        for (char c : s) count[c - 'a']--;

        for (int i = 0; i < 26; i++) {
            if (count[i] == 1) {
                return i + 'a';
            }
        }
        return ' ';
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ since we have at most $26$ different characters.

## 3. Sorting

After sorting both strings, corresponding characters at each position should match since `t` is a shuffled version of `s` plus one character. The first position where they differ reveals the added character. If all positions match, the added character is at the end of `t`.

```cpp
class Solution {
public:
    char findTheDifference(string s, string t) {
        sort(s.begin(), s.end());
        sort(t.begin(), t.end());
        for (int i = 0; i < s.size(); i++) {
            if (s[i] != t[i]) {
                return t[i];
            }
        }
        return t[t.size() - 1];
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 4. Difference Between ASCII Values

Each character has an ASCII value. If we sum the ASCII values of all characters in `t` and subtract the sum of ASCII values in `s`, the result equals the ASCII value of the added character. This works because all matching characters cancel out.

```cpp
class Solution {
public:
    char findTheDifference(string s, string t) {
        int sumS = 0, sumT = 0;
        for (char c : s) {
            sumS += c;
        }
        for (char c : t) {
            sumT += c;
        }
        return (char) (sumT - sumS);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## 5. Difference Between ASCII Values (Optimal)

We can optimize space by using a single variable instead of two separate sums. By subtracting ASCII values from `s` and adding ASCII values from `t` to the same variable, we compute the difference in one pass through both strings.

```cpp
class Solution {
public:
    char findTheDifference(string s, string t) {
        int res = 0;
        for (char c : s) {
            res -= c;
        }
        for (char c : t) {
            res += c;
        }
        return (char) (res);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## 6. Bitwise XOR

XOR has a useful property: `a ^ a = 0` and `a ^ 0 = a`. If we XOR all characters from both strings together, each character that appears in both `s` and `t` will cancel out (XOR with itself gives `0`). The only character remaining is the added one, since it appears an odd number of times total.

```cpp
class Solution {
public:
    char findTheDifference(string s, string t) {
        int res = 0;
        for (char c : s) {
            res ^= c;
        }
        for (char c : t) {
            res ^= c;
        }
        return (char) (res);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.
