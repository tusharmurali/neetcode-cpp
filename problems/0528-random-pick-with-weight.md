# 528. Random Pick with Weight

- **Difficulty:** Medium  
- **Pattern:** Binary Search  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/random-pick-with-weight/>  
- **NeetCode:** <https://neetcode.io/problems/random-pick-with-weight>  

[← Back to index](../INDEX.md)

## 1. Prefix Sum + Linear Search

To pick an index with probability proportional to its weight, imagine laying all weights on a number line. A weight of `3` takes up `3` units, a weight of `1` takes up `1` unit, and so on. We pick a random point on this line, then find which weight's segment contains that point. The larger the weight, the more likely its segment gets hit.

```cpp
class Solution {
public:
    vector<int> w;
    int total = 0;

    Solution(vector<int>& w) {
        this->w = w;
        for (int weight : w) {
            total += weight;
        }
    }

    int pickIndex() {
        double target = total * ((double) rand() / RAND_MAX);
        int curSum = 0;
        for (int i = 0; i < w.size(); i++) {
            curSum += w[i];
            if (curSum > target) {
                return i;
            }
        }
        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n)$ for initializing and $O(n)$ for each $pickIndex()$ function call.
- Space complexity: $O(n)$

## 2. Prefix Sum + Binary Search

The linear search can be optimized using binary search. By precomputing a prefix sum array, each index `i` represents the cumulative weight up to that point. When we generate a random target, we binary search for the smallest index whose prefix sum exceeds the target. This maps directly to the weight segment containing our random point.

```cpp
class Solution {
public:
    vector<int> prefix;

    Solution(vector<int>& w) {
        prefix.push_back(0);
        for (int wgt : w) {
            prefix.push_back(prefix.back() + wgt);
        }
    }

    int pickIndex() {
        double target = prefix.back() * ((double) rand() / RAND_MAX);
        int l = 1, r = prefix.size();
        while (l < r) {
            int mid = (l + r) >> 1;
            if (prefix[mid] <= target) {
                l = mid + 1;
            } else {
                r = mid;
            }
        }
        return l - 1;
    }
};
```

**Complexity**

- Time complexity: $O(n)$ for initializing and $O(\log n)$ for each $pickIndex()$ function call.
- Space complexity: $O(n)$
