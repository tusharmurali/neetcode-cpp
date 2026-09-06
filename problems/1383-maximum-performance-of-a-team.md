# 1383. Maximum Performance of a Team

- **Difficulty:** Hard  
- **Pattern:** Heap / Priority Queue  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/maximum-performance-of-a-team/>  
- **NeetCode:** <https://neetcode.io/problems/maximum-performance-of-a-team>  
- **Video:** <https://www.youtube.com/watch?v=Y7UTvogADH0>  

[← Back to index](../INDEX.md)

## 1. Brute Force (Recursion)

The simplest approach is to try all possible subsets of engineers with size at most `k`. For each subset, we compute the sum of speeds and multiply by the minimum efficiency in that subset. We track the maximum performance across all valid subsets.

This works because performance is defined as (sum of speeds) \* (minimum efficiency), so we need to consider every combination to find the optimal team.

```cpp
class Solution {
private:
    static constexpr int MOD = 1000000007;
    vector<int> speed, efficiency;
    int n;
    long long res;

public:
    int maxPerformance(int n, vector<int>& speed, vector<int>& efficiency, int k) {
        this->n = n;
        this->speed = speed;
        this->efficiency = efficiency;
        res = 0;

        dfs(0, k, INT_MAX, 0);
        return int(res % MOD);
    }

private:
    void dfs(int i, int k, int minEff, long long speedSum) {
        res = max(res, speedSum * minEff);
        if (i == n || k == 0) return;

        dfs(i + 1, k, minEff, speedSum);
        dfs(i + 1, k - 1, min(minEff, efficiency[i]), speedSum + speed[i]);
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ n)$
- Space complexity: $O(n)$ for recursion stack.

## 2. Sorting + Min-Heap

The key insight is that the minimum efficiency in a team acts as a bottleneck. If we fix which engineer has the minimum efficiency, we want to maximize the sum of speeds among the remaining selected engineers.

By sorting engineers in descending order of efficiency, as we iterate through them, each new engineer we consider has the smallest efficiency so far. At that point, we want to pick the engineers with the highest speeds (up to `k` total) from those we have seen. A min-heap helps us efficiently maintain the top `k` speeds.

```cpp
class Solution {
public:
    int maxPerformance(int n, vector<int>& speed, vector<int>& efficiency, int k) {
        constexpr int MOD = 1'000'000'007;
        vector<pair<int, int>> engineers;

        for (int i = 0; i < n; i++) {
            engineers.emplace_back(efficiency[i], speed[i]);
        }

        sort(engineers.rbegin(), engineers.rend());

        priority_queue<int, vector<int>, greater<int>> minHeap;
        long long speedSum = 0, res = 0;

        for (const auto& [eff, spd] : engineers) {
            if (minHeap.size() == k) {
                speedSum -= minHeap.top();
                minHeap.pop();
            }
            speedSum += spd;
            minHeap.push(spd);
            res = max(res, speedSum * eff);
        }

        return res % MOD;
    }
};
```

**Complexity**

- Time complexity: $O(n * (\log n + \log k))$
- Space complexity: $O(n + k)$

> Where $n$ is the number of engineers and $k$ is the maximum number of engineers that can be selected.
