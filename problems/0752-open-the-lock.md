# 752. Open The Lock

- **Difficulty:** Medium  
- **Pattern:** Graphs  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/open-the-lock/>  
- **NeetCode:** <https://neetcode.io/problems/open-the-lock>  
- **Video:** <https://www.youtube.com/watch?v=Pzg3bCDY87w>  

[← Back to index](../INDEX.md)

## 1. Breadth First Search - I

Think of each lock combination as a node in a graph, where two nodes are connected if you can reach one from the other by turning a single wheel one step. Starting from "0000", we want to find the shortest path to the target while avoiding deadends.

BFS is the natural choice here because it explores all states at distance `1` before distance `2`, and so on. This guarantees that when we first reach the target, we've found the minimum number of moves. We treat deadends as blocked nodes and use a visited set to avoid revisiting the same combination.

```cpp
class Solution {
public:
    int openLock(vector<string>& deadends, string target) {
        unordered_set<string> visit(deadends.begin(), deadends.end());
        if (visit.count("0000")) return -1;

        queue<pair<string, int>> q;
        q.push({"0000", 0});
        visit.insert("0000");

        while (!q.empty()) {
            auto [lock, turns] = q.front();
            q.pop();

            if (lock == target) return turns;
            for (string child : children(lock)) {
                if (!visit.count(child)) {
                    visit.insert(child);
                    q.push({child, turns + 1});
                }
            }
        }
        return -1;
    }

private:
    vector<string> children(string lock) {
        vector<string> res;
        for (int i = 0; i < 4; ++i) {
            string next = lock;
            next[i] = (next[i] - '0' + 1) % 10 + '0';
            res.push_back(next);

            next = lock;
            next[i] = (next[i] - '0' - 1 + 10) % 10 + '0';
            res.push_back(next);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(d ^ n + m)$
- Space complexity: $O(d ^ n)$

> Where $d$ is the number of digits $(0 - 9)$, $n$ is the number of wheels $(4)$, and $m$ is the number of deadends.

## 2. Breadth First Search - II

This is a cleaner implementation of the same BFS approach. Instead of generating all children at once through a helper function, we iterate through each of the `4` wheels and try both directions (`+1` and `-1`) inline. The core idea remains the same: explore level by level to find the shortest path.

By processing all nodes at the current level before incrementing the step counter, we ensure the first time we reach the target corresponds to the minimum number of moves.

```cpp
class Solution {
public:
    int openLock(vector<string>& deadends, string target) {
        if (target == "0000") return 0;

        unordered_set<string> visit(deadends.begin(), deadends.end());
        if (visit.count("0000")) return -1;

        queue<string> q;
        q.push("0000");
        visit.insert("0000");
        int steps = 0;

        while (!q.empty()) {
            steps++;
            for (int i = q.size(); i > 0; i--) {
                string lock = q.front(); q.pop();
                for (int j = 0; j < 4; j++) {
                    for (int move : {1, -1}) {
                        string nextLock = lock;
                        nextLock[j] = (nextLock[j] - '0' + move + 10) % 10 + '0';
                        if (visit.count(nextLock)) continue;
                        if (nextLock == target) return steps;
                        q.push(nextLock);
                        visit.insert(nextLock);
                    }
                }
            }
        }
        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(d ^ n + m)$
- Space complexity: $O(d ^ n)$

> Where $d$ is the number of digits $(0 - 9)$, $n$ is the number of wheels $(4)$, and $m$ is the number of deadends.

## 3. Bidirectional Breadth First Search

Standard BFS explores outward from the start, which can lead to exploring many states before reaching a distant target. Bidirectional BFS improves this by searching from both ends simultaneously: one frontier starts at "0000" and another at the target. When they meet, we've found the shortest path.

The key optimization is to always expand the smaller frontier. This balances the search and reduces the total number of states explored, especially when the search space branches heavily in one direction.

```cpp
class Solution {
public:
    int openLock(vector<string>& deadends, string target) {
        if (target == "0000") return 0;

        unordered_set<string> visit(deadends.begin(), deadends.end());
        if (visit.count("0000")) return -1;

        unordered_set<string> begin = {"0000"}, end = {target};
        int steps = 0;

        while (!begin.empty() && !end.empty()) {
            if (begin.size() > end.size()) swap(begin, end);
            steps++;
            unordered_set<string> temp;

            for (const string& lock : begin) {
                for (int i = 0; i < 4; ++i) {
                    for (int j : {-1, 1}) {
                        string nextLock = lock;
                        nextLock[i] = (nextLock[i] - '0' + j + 10) % 10 + '0';

                        if (end.count(nextLock)) return steps;
                        if (visit.count(nextLock)) continue;

                        visit.insert(nextLock);
                        temp.insert(nextLock);
                    }
                }
            }
            begin = temp;
        }
        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(d ^ n + m)$
- Space complexity: $O(d ^ n)$

> Where $d$ is the number of digits $(0 - 9)$, $n$ is the number of wheels $(4)$, and $m$ is the number of deadends.
