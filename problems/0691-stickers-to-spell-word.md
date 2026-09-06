# 691. Stickers to Spell Word

- **Difficulty:** Hard  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/stickers-to-spell-word/>  
- **NeetCode:** <https://neetcode.io/problems/stickers-to-spell-word>  
- **Video:** <https://www.youtube.com/watch?v=hsomLb6mUdI>  

[← Back to index](../INDEX.md)

## 1. Dynamic Programming (Top-Down) - I

We need to find the minimum number of stickers to spell the target string, where each sticker can be used multiple times. This is a classic memoization problem where we track which characters from the target still need to be covered. At each step, we pick a sticker that can help (contains the first remaining character) and recursively solve for the remaining characters.

```cpp
class Solution {
    vector<unordered_map<char, int>> stickCount;
    unordered_map<string, int> dp;

public:
    int minStickers(vector<string>& stickers, string target) {
        stickCount.clear();
        dp.clear();

        for (const string& s : stickers) {
            unordered_map<char, int> countMap;
            for (char c : s) {
                countMap[c]++;
            }
            stickCount.push_back(countMap);
        }

        int res = dfs(target, unordered_map<char, int>());
        return res == INT_MAX ? -1 : res;
    }

private:
    int dfs(const string& t, unordered_map<char, int> stick) {
        if (t.empty()) return 0;
        if (dp.count(t)) return dp[t];

        int res = stick.empty() ? 0 : 1;
        string remainT;

        for (char c : t) {
            if (stick.count(c) && stick[c] > 0) {
                stick[c]--;
            } else {
                remainT += c;
            }
        }

        if (!remainT.empty()) {
            int used = INT_MAX;
            for (const auto& s : stickCount) {
                if (!s.count(remainT[0])) continue;
                int curr = dfs(remainT, unordered_map<char, int>(s));
                if (curr != INT_MAX) {
                    used = min(used, curr);
                }
            }
            dp[remainT] = used;
            if (used != INT_MAX && res != INT_MAX) {
                res += used;
            } else {
                res = INT_MAX;
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * k *2 ^ n)$
- Space complexity: $O(m * k + 2 ^ n)$

> Where $n$ is the length of the target string, $m$ is the number of stickers and $k$ is the average length of each sticker.

## 2. Dynamic Programming (Top-Down) - II

This approach improves on the previous one by sorting the target string. When we sort the target, strings with the same character composition map to the same state, reducing the number of unique states. Instead of tracking the exact order of remaining characters, we only care about which characters and how many of each are needed.

```cpp
class Solution {
private:
    unordered_map<string, int> dp;
    vector<unordered_map<char, int>> stickCount;

public:
    int minStickers(vector<string>& stickers, string target) {
        dp[""] = 0;
        for (const string& s : stickers) {
            unordered_map<char, int> counter;
            for (char c : s) {
                counter[c]++;
            }
            stickCount.push_back(counter);
        }

        sort(target.begin(), target.end());
        int ans = dfs(target);
        return ans == INT_MAX ? -1 : ans;
    }

    int dfs(const string& t) {
        if (dp.find(t) != dp.end()) {
            return dp[t];
        }

        unordered_map<char, int> tarMp;
        for (char c : t) {
            tarMp[c]++;
        }

        int res = INT_MAX;
        for (auto& s : stickCount) {
            if (s.find(t[0]) == s.end()) {
                continue;
            }

            string remainT;
            for (const auto& [c, count] : tarMp) {
                int need = count - (s.count(c) ? s.at(c) : 0);
                remainT.append(max(0, need), c);
            }

            sort(remainT.begin(), remainT.end());
            int cur = dfs(remainT);
            if (cur == INT_MAX) cur--;
            res = min(res, 1 + cur);
        }

        dp[t] = res;
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * k *2 ^ n)$
- Space complexity: $O(m * k + 2 ^ n)$

> Where $n$ is the length of the target string, $m$ is the number of stickers and $k$ is the average length of each sticker.

## 3. Dynamic Programming (Bottom-Up)

We can represent the state as a bitmask where each bit indicates whether a character in the target has been covered. Starting from state `0` (no characters covered), we iterate through all states and for each sticker, compute which new state we can reach. This bottom-up approach systematically explores all possible ways to build the target.

```cpp
class Solution {
public:
    int minStickers(vector<string>& stickers, string target) {
        int n = target.length();
        int N = 1 << n;
        vector<int> dp(N, -1);
        dp[0] = 0;

        for (int t = 0; t < N; t++) {
            if (dp[t] == -1) continue;
            for (string& s : stickers) {
                int nextT = t;
                for (char c : s) {
                    for (int i = 0; i < n; i++) {
                        if (target[i] == c && ((nextT >> i) & 1) == 0) {
                            nextT |= 1 << i;
                            break;
                        }
                    }
                }
                if (dp[nextT] == -1 || dp[nextT] > dp[t] + 1) {
                    dp[nextT] = dp[t] + 1;
                }
            }
        }

        return dp[N - 1];
    }
};
```

**Complexity**

- Time complexity: $O(n * m * k *2 ^ n)$
- Space complexity: $O(2 ^ n)$

> Where $n$ is the length of the target string, $m$ is the number of stickers and $k$ is the average length of each sticker.
