# 649. Dota2 Senate

- **Difficulty:** Medium  
- **Pattern:** Greedy  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/dota2-senate/>  
- **NeetCode:** <https://neetcode.io/problems/dota2-senate>  
- **Video:** <https://www.youtube.com/watch?v=zZA5KskfMuQ>  

[← Back to index](../INDEX.md)

## 1. Brute Force

We can simulate the voting process directly. Each senator, when it's their turn, will ban the next opposing senator in the circular order. We keep iterating through the remaining senators until only one party remains. This approach mirrors the problem's rules exactly but requires repeatedly scanning the list to find and remove opponents.

```cpp
class Solution {
public:
    string predictPartyVictory(string senate) {
        vector<char> s(senate.begin(), senate.end());

        while (true) {
            int i = 0;
            while (i < s.size()) {
                if (find(s.begin(), s.end(), 'R') == s.end()) {
                    return "Dire";
                }
                if (find(s.begin(), s.end(), 'D') == s.end()) {
                    return "Radiant";
                }
                if (s[i] == 'R') {
                    int j = (i + 1) % s.size();
                    while (s[j] == 'R') {
                        j = (j + 1) % s.size();
                    }
                    s.erase(s.begin() + j);
                    if (j < i) {
                        i--;
                    }
                } else {
                    int j = (i + 1) % s.size();
                    while (s[j] == 'D') {
                        j = (j + 1) % s.size();
                    }
                    s.erase(s.begin() + j);
                    if (j < i) {
                        i--;
                    }
                }
                i++;
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 2. Greedy (Two Queues)

The key insight is that a senator should always ban the nearest opposing senator who would otherwise act before them. We use two queues to track the positions of Radiant and Dire senators. When comparing the front of both queues, the senator with the smaller index acts first and bans the other. The surviving senator then re-enters at the end of the queue with an updated index (adding `n` to represent the next round).

```cpp
class Solution {
public:
    string predictPartyVictory(string senate) {
        queue<int> R, D;
        int n = senate.size();

        for (int i = 0; i < n; i++) {
            if (senate[i] == 'R') {
                R.push(i);
            } else {
                D.push(i);
            }
        }

        while (!R.empty() && !D.empty()) {
            int rTurn = R.front(); R.pop();
            int dTurn = D.front(); D.pop();

            if (rTurn < dTurn) {
                R.push(rTurn + n);
            } else {
                D.push(dTurn + n);
            }
        }

        return R.empty() ? "Dire" : "Radiant";
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Greedy

We can track pending bans using a single counter. When we encounter a Radiant senator (`R`), they either get banned by a waiting Dire (if `cnt < 0`) or they ban a future Dire senator. Similarly, Dire senators either get banned or ban future Radiant senators. The twist is that when a senator is banned, their surviving opponent is appended to the end to act again in future rounds.

```cpp
class Solution {
public:
    string predictPartyVictory(string senate) {
        int cnt = 0, i = 0;

        while (i < senate.size()) {
            char c = senate[i];
            if (c == 'R') {
                if (cnt < 0) {
                    senate.push_back('D');
                }
                cnt++;
            } else {
                if (cnt > 0) {
                    senate.push_back('R');
                }
                cnt--;
            }
            i++;
        }

        return cnt > 0 ? "Radiant" : "Dire";
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$
