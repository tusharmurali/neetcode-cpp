# 2551. Put Marbles in Bags

- **Difficulty:** Hard  
- **Pattern:** Greedy  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/put-marbles-in-bags/>  
- **NeetCode:** <https://neetcode.io/problems/put-marbles-in-bags>  
- **Video:** <https://www.youtube.com/watch?v=lB_gLotpnuY>  

[← Back to index](../INDEX.md)

## 1. Dynamic Programming (Top-Down)

We need to partition marbles into k bags and find the difference between maximum and minimum possible scores. Each bag's cost is the sum of its first and last marble weights. Using memoization, we can explore all possible partition points. At each position, we decide whether to make a cut (starting a new bag) or continue the current bag, tracking both max and min scores simultaneously.

```cpp
class Solution {
public:
    unordered_map<string, pair<long long, long long>> cache;

    long long putMarbles(vector<int>& weights, int k) {
        int n = weights.size();
        auto ans = dfs(0, k - 1, weights, n);
        return ans.first - ans.second;
    }

    pair<long long, long long> dfs(int i, int k, vector<int>& weights, int n) {
        string key = to_string(i) + "," + to_string(k);
        if (cache.count(key)) return cache[key];
        if (k == 0) return {0LL, 0LL};
        if (i == n - 1 || n - i - 1 < k) {
            return {-1000000000000000LL, 1000000000000000LL};
        }

        pair<long long, long long> res = {0LL, 1000000000000000LL};

        auto cur = dfs(i + 1, k - 1, weights, n);
        res.first = max(res.first, (long long)weights[i] + weights[i + 1] + cur.first);
        res.second = min(res.second, (long long)weights[i] + weights[i + 1] + cur.second);

        cur = dfs(i + 1, k, weights, n);
        res.first = max(res.first, cur.first);
        res.second = min(res.second, cur.second);

        return cache[key] = res;
    }
};
```

**Complexity**

- Time complexity: $O(n * k)$
- Space complexity: $O(n * k)$

> Where $n$ is the number of marbles, and $k$ is the number of bags.

## 2. Greedy + Sorting

The key observation is that the first and last marbles always contribute to the total score regardless of how we partition. What matters is where we place the k-1 dividers. Each divider at position i adds `weights[i] + weights[i+1]` to the score. To maximize the score, pick the k-1 largest such sums. To minimize, pick the k-1 smallest. The difference between these gives our answer.

```cpp
class Solution {
public:
    long long putMarbles(vector<int>& weights, int k) {
        if (k == 1) return 0LL;

        int n = weights.size();
        vector<int> splits;

        for (int i = 0; i < n - 1; ++i) {
            splits.push_back(weights[i] + weights[i + 1]);
        }

        sort(splits.begin(), splits.end());
        int i = k - 1;
        long long minScore = 0, maxScore = 0;

        for (int j = 0; j < i; ++j) minScore += splits[j];
        for (int j = splits.size() - i; j < splits.size(); ++j) {
            maxScore += splits[j];
        }

        return maxScore - minScore;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

> Where $n$ is the number of marbles, and $k$ is the number of bags.

## 3. Heap

Instead of sorting all adjacent pair sums, we can use two heaps to efficiently track just the k-1 largest and k-1 smallest values. A min-heap keeps the k-1 largest sums (evicting smaller ones), while a max-heap keeps the k-1 smallest sums (evicting larger ones). This is more efficient when k is small relative to n.

```cpp
class Solution {
public:
    long long putMarbles(vector<int>& weights, int k) {
        if (k == 1) return 0LL;

        priority_queue<int, vector<int>, greater<int>> minHeap;
        priority_queue<int> maxHeap;

        for (int i = 0; i < weights.size() - 1; ++i) {
            int split = weights[i] + weights[i + 1];

            if ((int)minHeap.size() < k - 1) minHeap.push(split);
            else if (split > minHeap.top()) {
                minHeap.pop();
                minHeap.push(split);
            }

            if ((int)maxHeap.size() < k - 1) maxHeap.push(split);
            else if (split < maxHeap.top()) {
                maxHeap.pop();
                maxHeap.push(split);
            }
        }

        long long maxScore = 0, minScore = 0;
        while (!minHeap.empty()) {
            maxScore += minHeap.top();
            minHeap.pop();
        }
        while (!maxHeap.empty()) {
            minScore += maxHeap.top();
            maxHeap.pop();
        }

        return maxScore - minScore;
    }
};
```

**Complexity**

- Time complexity: $O(n \log k)$
- Space complexity: $O(k)$

> Where $n$ is the number of marbles, and $k$ is the number of bags.
