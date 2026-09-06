# 1100. Find K-Length Substrings With No Repeated Characters

- **Difficulty:** Medium  
- **Pattern:** Sliding Window  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/find-k-length-substrings-with-no-repeated-characters/>  
- **NeetCode:** <https://neetcode.io/problems/find-k-length-substrings-with-no-repeated-characters>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The most direct approach is to examine every substring of length `k` and check if it contains all unique characters. For each starting position, we scan `k` characters and track their frequencies. If any character appears more than once, we stop early and move to the next substring.

```cpp
class Solution {
public:
    int numKLenSubstrNoRepeats(string s, int k) {
        if (k > 26) return 0;

        int answer = 0;
        int n = s.size();

        for (int i = 0; i <= n - k; i++) {
            // Initializing an empty frequency array
            int freq[26] = {0};
            bool isUnique = true;

            for (int j = i; j < i + k; j++) {
                // Incrementing the frequency of current character
                freq[s[j] - 'a']++;

                // If a repeated character is found, we stop the loop
                if (freq[s[j] - 'a'] > 1) {
                    isUnique = false;
                    break;
                }
            }

            // If the substring does not have any repeated characters,
            // we increment the answer
            if (isUnique) {
                answer++;
            }
        }

        return answer;
    }
};
```

**Complexity**

- Time complexity: $O(n \cdot \min(m, k))$
- Space complexity: $O(m)$

> Where $n$ is the length of `s`, $k$ is the given substring length, and $m$ is the number of unique characters allowed in the string. In this case, $m=26$.

## 2. Sliding Window

Instead of recomputing character frequencies for each substring from scratch, we can maintain a sliding window. As we move the window, we add the new character on the right and remove the character that falls off on the left. When a duplicate is detected, we shrink the window from the left until all characters are unique again.

```cpp
class Solution {
public:
    int numKLenSubstrNoRepeats(string s, int k) {
        // We can reuse the condition from the first approach
        // as for k > 26, there can be no substrings with only unique characters
        if (k > 26) return 0;

        int answer = 0;
        int n = s.size();

        // Initializing the left and right pointers
        int left = 0, right = 0;
        // Initializing an empty frequency array
        int freq[26] = {0};

        while (right < n) {
            // Add the current character in the frequency array
            freq[s[right] - 'a']++;

            // If the current character appears more than once in the frequency
            // array keep contracting the window and removing characters from
            // the frequency array till the frequency of the current character
            // becomes 1.
            while (freq[s[right] - 'a'] > 1) {
                freq[s[left] - 'a']--;
                left++;
            }

            // Check if the length of the current unique substring is equal to k
            if (right - left + 1 == k) {
                answer++;

                // Contract the window and remove the leftmost character from
                // the frequency array
                freq[s[left] - 'a']--;
                left++;
            }

            // Expand the window
            right++;
        }

        return answer;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(m)$

> Where $n$ is the length of `s` and $m$ is the number of unique characters allowed in the string. In this case, $m=26$.
