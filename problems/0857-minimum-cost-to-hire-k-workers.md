# 857. Minimum Cost to Hire K Workers

- **Difficulty:** Hard  
- **Pattern:** Heap / Priority Queue  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/minimum-cost-to-hire-k-workers/>  
- **NeetCode:** <https://neetcode.io/problems/minimum-cost-to-hire-k-workers>  
- **Video:** <https://www.youtube.com/watch?v=f879mUH6vJk>  

[← Back to index](../INDEX.md)

## 1. Greedy + Max-Heap

Every worker has a minimum wage expectation. If we pay workers proportionally to their quality, the worker with the highest wage-to-quality ratio sets the "rate" for the group. Total cost equals `rate * total_quality`. To minimize cost with a fixed rate, we want workers with the smallest quality values. We sort workers by their rate, then use a max-heap to maintain the k workers with lowest quality seen so far.

```cpp
class Solution {
public:
    double mincostToHireWorkers(vector<int>& quality, vector<int>& wage, int k) {
        int n = quality.size();
        vector<pair<double, int>> workers(n);
        for (int i = 0; i < n; i++) {
            workers[i] = { (double)wage[i] / quality[i], quality[i] };
        }

        sort(workers.begin(), workers.end());
        priority_queue<int> maxHeap;
        double totalQuality = 0, res = DBL_MAX;

        for (auto& worker : workers) {
            double ratio = worker.first;
            int q = worker.second;
            maxHeap.push(q);
            totalQuality += q;

            if (maxHeap.size() > k) {
                totalQuality -= maxHeap.top();
                maxHeap.pop();
            }

            if (maxHeap.size() == k) {
                res = min(res, totalQuality * ratio);
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * (\log n + \log k))$
- Space complexity: $O(n)$

> Where $n$ is the number of workers, and $k$ is the number of workers to be hired.
