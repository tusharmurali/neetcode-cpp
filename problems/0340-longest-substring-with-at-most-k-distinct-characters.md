# 340. Longest Substring with At Most K Distinct Characters

- **Difficulty:** Medium  
- **Pattern:** Sliding Window  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/>  
- **NeetCode:** <https://neetcode.io/problems/longest-substring-with-at-most-k-distinct-characters>  

[← Back to index](../INDEX.md)

## 1. Binary Search + Fixed Size Sliding Window

The answer has a monotonic property: if we can find a valid substring of length `L`, then there must also exist valid substrings of all lengths less than `L`. This makes binary search applicable. We binary search on the answer length and for each candidate length, use a fixed-size sliding window to check if any window of that size has at most `k` distinct characters.

```cpp
class Solution {
public:
    int lengthOfLongestSubstringKDistinct(string s, int k) {
        int n = s.length();
        if (k >= n) {
            return n;
        }

        int left = k, right = n;
        while (left < right) {
            int mid = (left + right + 1) / 2;

            if (isValid(s, mid, k)) {
                left = mid;
            } else {
                right = mid - 1;
            }
        }

        return left;
    }

private:
    bool isValid(string s, int size, int k) {
        int n = s.length();
        unordered_map<char, int> counter;

        for (int i = 0; i < size; i++) {
            char c = s[i];
            counter[c]++;
        }

        if (counter.size() <= k) {
            return true;
        }

        for (int i = size; i < n; i++) {
            char c1 = s[i];
            counter[c1]++;
            char c2 = s[i - size];
            counter[c2]--;
            if (counter[c2] == 0) {
                counter.erase(c2);
            }
            if (counter.size() <= k) {
                return true;
            }
        }

        return false;
    }
};
```

**Complexity**

- Time complexity: $O(n \cdot \log n)$
- Space complexity: $O(n)$

> Where $n$ is the length of the input string `s` and $k$ is the maximum number of distinct characters.

## 2. Sliding Window

A variable-size sliding window is the natural fit for this problem. We expand the window by moving the right pointer and adding characters. When we exceed `k` distinct characters, we shrink the window from the left until we're back to at most `k` distinct characters. The maximum window size seen during this process is our answer.

```cpp
class Solution {
public:
    int lengthOfLongestSubstringKDistinct(string s, int k) {
        int n = s.length();
        int maxSize = 0;
        unordered_map<char, int> counter;

        int left = 0;
        for (int right = 0; right < n; right++) {
            counter[s[right]]++;

            while (counter.size() > k) {
                counter[s[left]]--;
                if (counter[s[left]] == 0) {
                    counter.erase(s[left]);
                }
                left++;
            }

            maxSize = max(maxSize, right - left + 1);
        }

        return maxSize;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(k)$

> Where $n$ is the length of the input string `s` and $k$ is the maximum number of distinct characters.

## 3. Sliding Window II

An optimization on the standard sliding window: instead of shrinking the window with a while loop, we only shrink by one step when invalid. This keeps the window size from ever decreasing by more than one, which means we only need to track when the window grows. The final answer is the maximum window size achieved, which equals `n - left` at the end.

```cpp
class Solution {
public:
    int lengthOfLongestSubstringKDistinct(string s, int k) {
        int n = s.length();
        int maxSize = 0;
        unordered_map<char, int> counter;

        for (int right = 0; right < n; right++) {
            counter[s[right]]++;

            if (counter.size() <= k) {
                maxSize++;
            } else {
                counter[s[right - maxSize]]--;
                if (counter[s[right - maxSize]] == 0) {
                    counter.erase(s[right - maxSize]);
                }
            }
        }
        return maxSize;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

> Where $n$ is the length of the input string `s` and $k$ is the maximum number of distinct characters.
