# 159. Longest Substring with At Most Two Distinct Characters

- **Difficulty:** Medium  
- **Pattern:** Sliding Window  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/longest-substring-with-at-most-two-distinct-characters/>  
- **NeetCode:** <https://neetcode.io/problems/longest-substring-with-at-most-two-distinct-characters>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The most direct approach is to examine every possible substring and check if it contains at most two distinct characters. For each starting position, we extend the substring character by character, tracking the distinct characters seen. Once we see a third distinct character, we stop and record the maximum valid length found.

```cpp
class Solution {
public:
    int lengthOfLongestSubstringTwoDistinct(string s) {
        int res = 0, n = s.size();

        for (int i = 0; i < n; i++) {
            unordered_set<char> seen;
            int curLen = 0;
            for (int j = i; j < n; j++) {
                seen.insert(s[j]);
                if (seen.size() > 2) {
                    break;
                }
                curLen++;
            }
            res = max(res, curLen);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$ since we have at most $52$ different characters.

## 2. Sliding Window

We maintain a window that always contains at most two distinct characters. As we expand the window to the right, we track character frequencies in a hash map. When adding a new character causes us to have more than two distinct characters, we shrink the window from the left until we're back to two or fewer distinct characters.

```cpp
class Solution {
public:
    int lengthOfLongestSubstringTwoDistinct(string s) {
        int res = 0, n = s.size();
        unordered_map<char, int> seen;
        int j = 0;

        for (int i = 0; i < n; i++) {
            seen[s[i]]++;

            while (seen.size() > 2) {
                char c = s[j];
                seen[c]--;
                if (seen[c] == 0) {
                    seen.erase(c);
                }
                j++;
            }
            res = max(res, i - j + 1);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ since we have at most $52$ different characters.

## 3. Sliding Window (Optimal)

We can further optimize by observing that we only care about the maximum window size. Instead of tracking the actual maximum during iteration, we maintain a window that never shrinks by more than one element at a time. When we have too many distinct characters, we shift the entire window right by one. The final window size represents the longest valid substring.

```cpp
class Solution {
public:
    int lengthOfLongestSubstringTwoDistinct(string s) {
        int n = s.size();
        unordered_map<char, int> count;
        int j = 0, i = 0;
        for (i = 0; i < n; i++) {
            count[s[i]]++;
            if (count.size() > 2) {
                count[s[j]]--;
                if (count[s[j]] == 0) count.erase(s[j]);
                j++;
            }
        }
        return i - j;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ since we have at most $52$ different characters.
