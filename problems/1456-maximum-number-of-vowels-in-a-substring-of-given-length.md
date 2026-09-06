# 1456. Maximum Number of Vowels in a Substring of Given Length

- **Difficulty:** Medium  
- **Pattern:** Sliding Window  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/maximum-number-of-vowels-in-a-substring-of-given-length/>  
- **NeetCode:** <https://neetcode.io/problems/maximum-number-of-vowels-in-a-substring-of-given-length>  
- **Video:** <https://www.youtube.com/watch?v=kEfPSzgL-Ss>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The most straightforward approach is to check every possible substring of length `k`. For each starting position, count the vowels in the window and track the maximum count seen.

This works correctly but is inefficient because we recount characters for overlapping windows.

```cpp
class Solution {
public:
    int maxVowels(string s, int k) {
        unordered_set<char> vowels = {'a', 'e', 'i', 'o', 'u'};
        int res = 0;

        for (int i = 0; i <= s.size() - k; i++) {
            int cnt = 0;
            for (int j = i; j < i + k; j++) {
                if (vowels.count(s[j])) {
                    cnt++;
                }
            }
            res = max(res, cnt);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$ extra space.

## 2. Prefix Count

We can precompute a prefix sum array where `prefix[i]` stores the number of vowels in `s[0..i-1]`. Then, the vowel count in any window `s[i-k..i-1]` is simply `prefix[i] - prefix[i-k]`.

This allows us to answer each window query in O(1) time after O(n) preprocessing.

```cpp
class Solution {
public:
    int maxVowels(string s, int k) {
        unordered_set<char> vowels = {'a', 'e', 'i', 'o', 'u'};
        vector<int> prefix(s.size() + 1, 0);

        for (int i = 0; i < s.size(); i++) {
            prefix[i + 1] = prefix[i] + (vowels.count(s[i]) ? 1 : 0);
        }

        int res = 0;
        for (int i = k; i <= s.size(); i++) {
            res = max(res, prefix[i] - prefix[i - k]);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Sliding Window

Instead of storing prefix sums, we can maintain a running count of vowels in the current window. As we slide the window right:

- Add `1` if the new character entering the window is a vowel.
- Subtract `1` if the character leaving the window is a vowel.

This gives us O(n) time with O(1) extra space.

```cpp
class Solution {
public:
    int maxVowels(string s, int k) {
        unordered_set<char> vowels = {'a', 'e', 'i', 'o', 'u'};

        int l = 0, cnt = 0, res = 0;
        for (int r = 0; r < s.length(); r++) {
            cnt += (vowels.count(s[r]) ? 1 : 0);
            if (r - l + 1 > k) {
                cnt -= (vowels.count(s[l++]) ? 1 : 0);
            }
            res = max(res, cnt);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## 4. Sliding Window (Bit Mask)

Checking if a character is a vowel using a set or string comparison can be optimized using a bitmask. We assign each letter a bit position (a=0, b=1, ..., z=25). The vowels form a constant bitmask. Checking if a character is a vowel becomes a single bitwise operation.

This is a micro-optimization but can improve cache performance and avoid hash lookups.

```cpp
class Solution {
public:
    int maxVowels(string s, int k) {
        int mask = (1 << ('a' - 'a')) | (1 << ('e' - 'a')) |
                   (1 << ('i' - 'a')) | (1 << ('o' - 'a')) |
                   (1 << ('u' - 'a'));

        int l = 0, cnt = 0, res = 0;
        for (int r = 0; r < s.size(); r++) {
            cnt += (mask >> (s[r] - 'a')) & 1;
            if (r - l + 1 > k) {
                cnt -= (mask >> (s[l] - 'a')) & 1;
                l++;
            }
            res = max(res, cnt);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## Standalone solution file (`cpp/1456-maximum-number-of-vowels-in-a-substring-of-given-length.cpp` in the NeetCode repo)

```cpp
/*
  Given a string s and an integer k, return the maximum number of vowel letters in any substring of s with length k.
  Vowel letters in English are 'a', 'e', 'i', 'o', and 'u'.

  Ex.
  Input: s = "abciiidef", k = 3
  Output: 3
  Explanation: The substring "iii" contains 3 vowel letters.

  Approach : Sliding Window

  Time  : O(N)
  Space : O(1)
*/


class Solution {
public:
    bool isVowel(char ch) {
        if(ch == 'a' || ch == 'e' || ch == 'i' || ch == 'o' || ch == 'u') 
            return true;
        return false;
    }
    int maxVowels(string s, int k) {
        int ptr1 = 0, ptr2 = 0, count = 0, maxi = INT_MIN;
        while(ptr2 < s.size()) {
            if(ptr2 - ptr1 == k) {
                maxi = max(count, maxi);
                if(maxi == k)
                    return count;
                if(isVowel(s[ptr1++]))
                    count--;
                if(isVowel(s[ptr2++]))
                    count++;

            } else {
                if(isVowel(s[ptr2]))
                    count++;
                ptr2++;
            }
        }
        maxi = max(count, maxi);
        return maxi;
    }
};
```
