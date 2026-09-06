# 3572. Maximize Y-Sum by Picking a Triplet of Distinct X-Values

- **Difficulty:** Medium  
- **Pattern:** Greedy  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/maximize-ysum-by-picking-a-triplet-of-distinct-xvalues/>  
- **NeetCode:** <https://neetcode.io/problems/maximize-ysum-by-picking-a-triplet-of-distinct-xvalues>  

[← Back to index](../INDEX.md)

## 1. Hash Map

We need to pick three indices with distinct x-values and maximize the sum of their corresponding y-values. For each unique x-value, we only care about the maximum y-value associated with it, since choosing a smaller y-value for the same x would never be optimal.

After collecting the best y-value for each distinct x, we simply need the three largest values. If there are fewer than three distinct x-values, the answer is `-1`.

```cpp
class Solution {
public:
    int maxSumDistinctTriplet(vector<int>& x, vector<int>& y) {
        unordered_map<int,int> mp;
        for (int i = 0; i < x.size(); i++) {
            int key = x[i], val = y[i];
            mp[key] = max(mp[key], val);
        }
        if (mp.size() < 3) return -1;
        vector<int> vals;
        vals.reserve(mp.size());
        for (auto &p : mp) vals.push_back(p.second);
        sort(vals.begin(), vals.end());
        int n = vals.size();
        return vals[n-1] + vals[n-2] + vals[n-3];
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 2. Hash Map + Min-Heap

Instead of sorting all values to find the top `3`, we can use a min-heap of size `3`. As we iterate through the distinct y-values, we maintain only the three largest seen so far. This avoids the overhead of sorting the entire collection.

Whenever the heap exceeds size `3`, we remove the smallest element. After processing all values, the heap contains exactly the three largest y-values (if at least `3` exist).

```cpp
class Solution {
public:
    int maxSumDistinctTriplet(vector<int>& x, vector<int>& y) {
        unordered_map<int,int> mp;
        for (int i = 0; i < x.size(); i++) {
            mp[x[i]] = max(mp[x[i]], y[i]);
        }
        priority_queue<int, vector<int>, greater<int>> pq;
        for (auto &p : mp) {
            pq.push(p.second);
            if (pq.size() > 3) {
                pq.pop();
            }
        }

        if (pq.size() < 3) return -1;
        int sum = 0;
        while (!pq.empty()) {
            sum += pq.top();
            pq.pop();
        }
        return sum;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Greedy

We can track the top `3` candidates in constant space by maintaining a sorted list of the best `3` (x, y) pairs seen so far. For each new element, we either update an existing entry (if the x-value matches) or insert it if the y-value is large enough to make the top `3`.

The key insight is that we only ever need to compare against at most `3` entries. When an x-value already exists in our top `3`, we update its y-value if the new one is larger and re-sort. Otherwise, we check if the new y-value can replace the smallest of our current top `3`.

```cpp
class Solution {
public:
    int maxSumDistinctTriplet(vector<int>& x, vector<int>& y) {
        vector<pair<int,int>> best(3, {INT_MIN, INT_MIN});
        for (int i = 0; i < x.size(); i++) {
            int xi = x[i], yi = y[i];
            bool updated = false;
            for (int j = 0; j < 3; j++) {
                if (best[j].first == xi) {
                    if (yi > best[j].second) {
                        best[j].second = yi;
                        sort(best.begin(), best.end(),
                             [](auto &a, auto &b){ return a.second > b.second; });
                    }
                    updated = true;
                    break;
                }
            }
            if (updated) continue;
            if (yi > best[0].second) {
                best.insert(best.begin(), {xi, yi});
                best.pop_back();
            } else if (yi > best[1].second) {
                best.insert(best.begin()+1, {xi, yi});
                best.pop_back();
            } else if (yi > best[2].second) {
                best[2] = {xi, yi};
            }
        }
        if (best[2].second == INT_MIN) return -1;
        return best[0].second + best[1].second + best[2].second;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$
