# 1642. Furthest Building You Can Reach

- **Difficulty:** Medium  
- **Pattern:** Heap / Priority Queue  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/furthest-building-you-can-reach/>  
- **NeetCode:** <https://neetcode.io/problems/furthest-building-you-can-reach>  
- **Video:** <https://www.youtube.com/watch?v=zyTeznvXCtg>  

[← Back to index](../INDEX.md)

## 1. Brute Force (Greedy)

The key observation is that ladders are most valuable for the largest height differences, since a ladder covers any gap regardless of size while bricks are consumed proportionally. For each position we reach, we can check if it's achievable by sorting all the height jumps encountered so far and using ladders for the largest ones while using bricks for the rest.

```cpp
class Solution {
public:
    int furthestBuilding(vector<int>& heights, int bricks, int ladders) {
        int n = heights.size();

        for (int i = 1; i < n; i++) {
            if (ladders >= i) {
                continue;
            }

            vector<int> diffs;
            for (int j = 0; j < i; j++) {
                if (heights[j + 1] > heights[j]) {
                    diffs.push_back(heights[j + 1] - heights[j]);
                }
            }

            sort(diffs.begin(), diffs.end());
            long long brickSum = 0;
            for (int j = 0; j < int(diffs.size()) - ladders; j++) {
                brickSum += diffs[j];
            }

            if (brickSum > bricks) {
                return i - 1;
            }
        }

        return n - 1;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 \log n)$
- Space complexity: $O(n)$

## 2. Binary Search On Buildings

Instead of checking each building sequentially, we can use binary search to find the furthest reachable building. The key insight is that reachability is monotonic: if we can reach building `i`, we can also reach all buildings before it. This lets us binary search on the answer.

```cpp
class Solution {
public:
    int furthestBuilding(vector<int>& heights, int bricks, int ladders) {
        int l = ladders - 1, r = heights.size() - 1;

        while (l <= r) {
            int mid = (l + r) / 2;
            if (canReach(heights, mid, bricks, ladders)) {
                l = mid + 1;
            } else {
                r = mid - 1;
            }
        }

        return l - 1;
    }

private:
    bool canReach(vector<int>& heights, int mid, int bricks, int ladders) {
        vector<int> diffs;

        for (int i = 0; i < mid; i++) {
            if (heights[i + 1] > heights[i]) {
                diffs.push_back(heights[i + 1] - heights[i]);
            }
        }

        sort(diffs.begin(), diffs.end());
        long long brickSum = 0;

        for (int j = 0; j < int(diffs.size()) - ladders; j++) {
            brickSum += diffs[j];
            if (brickSum > bricks) {
                return false;
            }
        }

        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n \log ^ 2 n)$
- Space complexity: $O(n)$

## 3. Binary Search On Buildings (Optimal)

We can optimize the previous approach by pre-sorting all height differences once instead of sorting repeatedly for each binary search check. By storing differences with their indices and sorting them in descending order, we can efficiently determine for any target building which jumps to cover with ladders (the largest ones) and which to cover with bricks.

```cpp
class Solution {
public:
    int furthestBuilding(vector<int>& heights, int bricks, int ladders) {
        vector<pair<int, int>> diffs;
        for (int i = 1; i < heights.size(); i++) {
            if (heights[i] > heights[i - 1]) {
                diffs.emplace_back(heights[i] - heights[i - 1], i);
            }
        }

        sort(diffs.rbegin(), diffs.rend()); // Sort in descending order

        int l = 1, r = heights.size() - 1;
        while (l <= r) {
            int mid = (l + r) >> 1;
            if (canReach(diffs, mid, bricks, ladders)) {
                l = mid + 1;
            } else {
                r = mid - 1;
            }
        }

        return l - 1;
    }

private:
    bool canReach(vector<pair<int, int>>& diffs, int index, int bricks, int ladders) {
        int useLadders = 0;
        long long useBricks = 0;
        for (auto& diff : diffs) {
            int jump = diff.first, i = diff.second;

            if (i > index) continue;

            if (useLadders < ladders) {
                useLadders++;
            } else {
                useBricks += jump;
                if (useBricks > bricks) {
                    return false;
                }
            }
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 4. Max-Heap

We can make greedy decisions as we traverse by initially using bricks for each jump, then retroactively swapping to a ladder when bricks run out. A max-heap tracks all brick usages so far, allowing us to efficiently swap the largest brick usage with a ladder when needed. This ensures ladders always cover the biggest gaps.

```cpp
class Solution {
public:
    int furthestBuilding(vector<int>& heights, int bricks, int ladders) {
        priority_queue<int> maxHeap;

        for (int i = 0; i < heights.size() - 1; i++) {
            int diff = heights[i + 1] - heights[i];
            if (diff <= 0) continue;

            bricks -= diff;
            maxHeap.push(diff);

            if (bricks < 0) {
                if (ladders == 0) return i;
                ladders--;
                bricks += maxHeap.top();
                maxHeap.pop();
            }
        }

        return heights.size() - 1;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 5. Min-Heap

Instead of tracking brick usages, we can track ladder usages in a min-heap. We greedily assign ladders to each jump, but once we've used more than the allowed number of ladders, we convert the smallest ladder usage back to bricks. This way, ladders always end up covering the largest jumps.

```cpp
class Solution {
public:
    int furthestBuilding(vector<int>& heights, int bricks, int ladders) {
        priority_queue<int, vector<int>, greater<int>> minHeap;

        for (int i = 0; i < int(heights.size()) - 1; i++) {
            int diff = heights[i + 1] - heights[i];
            if (diff <= 0) continue;

            minHeap.push(diff);
            if (minHeap.size() > ladders) {
                bricks -= minHeap.top(); minHeap.pop();
                if (bricks < 0) return i;
            }
        }

        return int(heights.size()) - 1;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$
