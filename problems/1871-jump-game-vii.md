# 1871. Jump Game VII

- **Difficulty:** Medium  
- **Pattern:** Greedy  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/jump-game-vii/>  
- **NeetCode:** <https://neetcode.io/problems/jump-game-vii>  
- **Video:** <https://www.youtube.com/watch?v=v1HpZUnQ4Yo>  

[← Back to index](../INDEX.md)

## 1. Brute Force (Memoization)

From each position, we can jump to any position within the range `[i + minJump, i + maxJump]` if that position contains `'0'`. We use recursion with memoization to explore all valid jumps. Starting from index `0`, we try every reachable position and recursively check if we can reach the end. Memoization prevents recalculating the same positions.

```cpp
class Solution {
public:
    int n;
    vector<int> dp;

    bool canReach(string s, int minJump, int maxJump) {
        this->n = s.size();
        dp.resize(n, -1);
        dp[n - 1] = 1;

        if (s[n - 1] == '1') {
            return false;
        }

        return dfs(0, s, minJump, maxJump);
    }

private:
    bool dfs(int i, string& s, int& minJump, int& maxJump) {
        if (dp[i] != -1) {
            return dp[i];
        }

        dp[i] = 0;
        for (int j = i + minJump; j <= min(n - 1, i + maxJump); ++j) {
            if (s[j] == '0' && dfs(j, s, minJump, maxJump)) {
                dp[i] = 1;
                break;
            }
        }
        return dp[i];
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(n)$

> Where $n$ is the length of the string $s$ and $m$ is the given range of the jump $(maxJump - minJump + 1)$.

## 2. Breadth First Search

BFS naturally explores positions level by level, where each level represents positions reachable in one jump. The key optimization is tracking the farthest index we've already processed. When processing position `i`, we only need to check new positions starting from `max(i + minJump, farthest + 1)` to avoid revisiting positions already added to the queue.

```cpp
class Solution {
public:
    bool canReach(string s, int minJump, int maxJump) {
        queue<int> q;
        q.push(0);
        int farthest = 0;
        int n = s.size();

        while (!q.empty()) {
            int i = q.front();
            q.pop();
            int start = max(i + minJump, farthest + 1);

            for (int j = start; j < min(i + maxJump + 1, n); ++j) {
                if (s[j] == '0') {
                    q.push(j);
                    if (j == n - 1) {
                        return true;
                    }
                }
            }
            farthest = i + maxJump;
        }

        return false;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Dynamic Programming (Sliding Window)

Position `i` is reachable if any position in `[i - maxJump, i - minJump]` is reachable (and `s[i] == '0'`). Instead of checking all positions in this range for each `i`, we maintain a running count of reachable positions within the window. As we move forward, we add newly entering positions to the count and remove positions that exit the window.

```cpp
class Solution {
public:
    bool canReach(string s, int minJump, int maxJump) {
        int n = s.size();
        if (s[n - 1] == '1') {
            return false;
        }

        vector<bool> dp(n, false);
        dp[0] = true;
        int cnt = 0;

        for (int i = 1; i < n; i++) {
            if (i >= minJump && dp[i - minJump]) {
                cnt++;
            }
            if (i > maxJump && dp[i - maxJump - 1]) {
                cnt--;
            }
            if (cnt > 0 && s[i] == '0') {
                dp[i] = true;
            }
        }

        return dp[n - 1];
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Dynamic Programming (Two Pointers)

Instead of tracking a count, we use a pointer `j` to remember the farthest position we've marked as reachable so far. From each reachable position `i`, we can mark all positions in `[i + minJump, i + maxJump]` as reachable. The pointer `j` ensures we never mark the same position twice, achieving linear time.

```cpp
class Solution {
public:
    bool canReach(string s, int minJump, int maxJump) {
        int n = s.size();
        if (s[n - 1] == '1') {
            return false;
        }

        vector<bool> dp(n, false);
        dp[0] = true;
        int j = 0;

        for (int i = 0; i < n; i++) {
            if (!dp[i]) {
                continue;
            }
            j = max(j, i + minJump);
            while (j < min(i + maxJump + 1, n)) {
                if (s[j] == '0') {
                    dp[j] = true;
                }
                j++;
            }
        }

        return dp[n - 1];
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$
