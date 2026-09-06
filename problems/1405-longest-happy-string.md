# 1405. Longest Happy String

- **Difficulty:** Medium  
- **Pattern:** Heap / Priority Queue  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/longest-happy-string/>  
- **NeetCode:** <https://neetcode.io/problems/longest-happy-string>  
- **Video:** <https://www.youtube.com/watch?v=8u-H6O_XQKE>  

[← Back to index](../INDEX.md)

## 1. Greedy

A "happy" string has no three consecutive identical characters. To maximize length, we should greedily use the most abundant character whenever possible. However, if we just used the same character twice in a row, we must switch to a different one to avoid three in a row. By always picking the character with the highest remaining count (that we're allowed to use), we maximize our chances of using all characters.

```cpp
class Solution {
public:
    string longestDiverseString(int a, int b, int c) {
        vector<int> count = {a, b, c};
        string res;

        int repeated = -1;
        while (true) {
            int maxChar = getMax(count, repeated);
            if (maxChar == -1) {
                break;
            }
            res += (char)(maxChar + 'a');
            count[maxChar]--;

            if (res.size() > 1 && res.back() == res[res.size() - 2]) {
                repeated = maxChar;
            } else {
                repeated = -1;
            }
        }

        return res;
    }

private:
    int getMax(const vector<int>& count, int repeated) {
        int idx = -1, maxCnt = 0;
        for (int i = 0; i < 3; i++) {
            if (i == repeated || count[i] == 0) {
                continue;
            }
            if (maxCnt < count[i]) {
                maxCnt = count[i];
                idx = i;
            }
        }
        return idx;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity:
    - $O(1)$ extra space.
    - $O(n)$ space for the output string.

## 2. Greedy (Max-Heap)

Using a max-heap streamlines finding the character with the highest count. We pop the top character and try to use it. If doing so would create three in a row, we instead use the second-highest character (if available), then push the first one back. This ensures we always make progress while respecting the constraint.

```cpp
class Solution {
public:
    string longestDiverseString(int a, int b, int c) {
        string res;
        priority_queue<pair<int, char>> maxHeap;
        if (a > 0) maxHeap.push({a, 'a'});
        if (b > 0) maxHeap.push({b, 'b'});
        if (c > 0) maxHeap.push({c, 'c'});

        while (!maxHeap.empty()) {
            auto [count, ch] = maxHeap.top();
            maxHeap.pop();

            if (res.size() > 1 && res[res.size() - 1] == ch && res[res.size() - 2] == ch) {
                if (maxHeap.empty()) break;
                auto [count2, ch2] = maxHeap.top();
                maxHeap.pop();
                res += ch2;
                if (--count2 > 0) maxHeap.push({count2, ch2});
                maxHeap.push({count, ch});
            } else {
                res += ch;
                if (--count > 0) maxHeap.push({count, ch});
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity:
    - $O(1)$ extra space.
    - $O(n)$ space for the output string.

## 3. Greedy (Recursion)

We can express the greedy logic recursively. At each step, we sort the characters by count (keeping the largest first) and decide how many of the most frequent character to use. If the most frequent character still dominates after using two of it, we insert one of the second character to break it up. Then we recurse on the reduced counts.

```cpp
class Solution {
public:
    string longestDiverseString(int a, int b, int c) {
        vector<char> res = rec(a, b, c, 'a', 'b', 'c');
        return string(res.begin(), res.end());
    }

private:
    vector<char> rec(int max1, int max2, int max3, char char1, char char2, char char3) {
        if (max1 < max2) {
            return rec(max2, max1, max3, char2, char1, char3);
        }
        if (max2 < max3) {
            return rec(max1, max3, max2, char1, char3, char2);
        }
        if (max2 == 0) {
            vector<char> result(min(2, max1), char1);
            return result;
        }

        int use1 = min(2, max1);
        int use2 = (max1 - use1 >= max2) ? 1 : 0;

        vector<char> res(use1, char1);
        res.insert(res.end(), use2, char2);

        vector<char> rest = rec(max1 - use1, max2 - use2, max3, char1, char2, char3);
        res.insert(res.end(), rest.begin(), rest.end());

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity:
    - $O(n)$ for recursion stack.
    - $O(n)$ space for the output string.
