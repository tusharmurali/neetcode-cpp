# 973. K Closest Points to Origin

- **Difficulty:** Medium  
- **Pattern:** Heap / Priority Queue  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/k-closest-points-to-origin/>  
- **NeetCode:** <https://neetcode.io/problems/k-closest-points-to-origin>  
- **Video:** <https://www.youtube.com/watch?v=rI2EBUEMfTk>  

[← Back to index](../INDEX.md)

## 1. Sorting

To find the **k closest points to the origin `(0, 0)`**, we compare points by their distance from the origin.
Since the actual distance uses a square root, and **square root preserves ordering**, we can instead compare using **squared distance**:

\[
d^2 = x^2 + y^2
\]

This avoids unnecessary computation and is sufficient for sorting.

If we sort all points by this squared distance, then the **first `k` points** in sorted order must be the `k` closest ones.

```cpp
class Solution {
public:
    vector<vector<int>> kClosest(vector<vector<int>>& points, int k) {
        sort(points.begin(), points.end(), [](const auto& a, const auto& b) {
            return (a[0] * a[0] + a[1] * a[1]) < (b[0] * b[0] + b[1] * b[1]);
        });
        return vector<vector<int>>(points.begin(), points.begin() + k);
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 2. Min-Heap

A min-heap always gives you the **smallest element first**.
If we insert every point into a min-heap, using its squared distance from the origin as the priority, then:

- The closest point will be at the top.
- The next closest will be removed next, and so on.

So if we remove from the heap **`k` times**, we get exactly the **`k` closest points**.

This works because the heap always keeps the smallest distances at the front.

```cpp
class Solution {
public:
    vector<vector<int>> kClosest(vector<vector<int>>& points, int K) {
        auto comp = [](const vector<int>& a, const vector<int>& b) {
            return a[0]*a[0] + a[1]*a[1] > b[0]*b[0] + b[1]*b[1];
        };

        priority_queue<vector<int>, vector<vector<int>>, decltype(comp)> minHeap(comp);

        for (const auto& point : points) {
            minHeap.push({point[0], point[1]});
        }

        vector<vector<int>> result;
        for (int i = 0; i < K; ++i) {
            result.push_back(minHeap.top());
            minHeap.pop();
        }
        return result;
    }
};
```

**Complexity**

- Time complexity: $O(n + k * \log n)$ when building the heap with `heapify`, or $O(n * \log n + k * \log n)$ when inserting each point with a heap push.
- Space complexity: $O(n)$

> Where $n$ is the length of the array $points$.

## 3. Max Heap

We want the **`k` closest points**, not all points sorted.

Use a **max-heap of size `k`**:

- The heap always keeps the **`k` closest points found so far**.
- The point with the **largest distance** among these `k` sits at the top.
- When a new point is **closer than the farthest in the heap**, we remove the farthest and insert the new one.

This way, the heap never grows beyond size `k`, and it always contains the `k` best candidates.

```cpp
class Solution {
public:
    vector<vector<int>> kClosest(vector<vector<int>>& points, int k) {
        priority_queue<pair<int, pair<int, int>>> maxHeap;
        for (auto& point : points) {
            int dist = point[0] * point[0] + point[1] * point[1];
            maxHeap.push({dist, {point[0], point[1]}});
            if (maxHeap.size() > k) {
                maxHeap.pop();
            }
        }

        vector<vector<int>> res;
        while (!maxHeap.empty()) {
            res.push_back({maxHeap.top().second.first,
                           maxHeap.top().second.second});
            maxHeap.pop();
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * \log k)$
- Space complexity: $O(k)$

> Where $n$ is the length of the array $points$.

## 4. Quick Select

We want the **`k` closest points**, but we do NOT need them sorted.

This is a perfect use-case for **QuickSelect**, the same idea used in QuickSort's partition step:

- Pick a **pivot point**.
- Partition all points into:
    - points **closer** than the pivot
    - points **farther** than the pivot
- After partitioning, the pivot ends at its **correct position** in the final sorted order.
- If the pivot ends up at index `p`:
    - If `p == k`, then the left side already contains the `k` closest points.
    - If `p < k`, search the **right half**.
    - If `p > k`, search the **left half**.

This avoids fully sorting the array and runs in **average O(N)** time.

```cpp
class Solution {
public:
    vector<vector<int>> kClosest(vector<vector<int>>& points, int k) {
        int L = 0, R = points.size() - 1;
        int pivot = points.size();

        while (pivot != k) {
            pivot = partition(points, L, R);
            if (pivot < k) {
                L = pivot + 1;
            } else {
                R = pivot - 1;
            }
        }
        return vector<std::vector<int>>(points.begin(), points.begin() + k);
    }

private:
    int partition(vector<vector<int>>& points, int l, int r) {
        int pivotIdx = r;
        int pivotDist = euclidean(points[pivotIdx]);
        int i = l;
        for (int j = l; j < r; j++) {
            if (euclidean(points[j]) <= pivotDist) {
                swap(points[i], points[j]);
                i++;
            }
        }
        swap(points[i], points[r]);
        return i;
    }

    int euclidean(vector<int>& point) {
        return point[0] * point[0] + point[1] * point[1];
    }
};
```

**Complexity**

- Time complexity: $O(n)$ in average case, $O(n ^ 2)$ in worst case.
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0973-k-closest-points-to-origin.cpp` in the NeetCode repo)

```cpp
/*
    Given array of points & an int k, return k closest points to (0, 0)
    Ex. points = [[1,3],[-2,2]], k = 1 -> [[-2,2]]

    Quickselect, partition until pivot = k, left side all < k

    Time: O(k log n)
    Space: O(n)
*/

// class Solution {
// public:
//     vector<vector<int>> kClosest(vector<vector<int>>& points, int k) {
//         priority_queue<pair<double, vector<int>>> pq;
//         for (int i = 0; i < points.size(); i++) {
//             double distance = sqrt(pow(points[i][0], 2) + pow(points[i][1], 2));
//             pq.push({distance, points[i]});
//             if (pq.size() > k) {
//                 pq.pop();
//             }
//         }
        
//         vector<vector<int>> result;
//         while(!pq.empty()) {
//             result.push_back(pq.top().second);
//             pq.pop();
//         }
        
//         return result;
//     }
// };
/*
class Solution {
public:
    vector<vector<int>> kClosest(vector<vector<int>>& points, int k) {
        int low = 0;
        int high = points.size() - 1;
        int pivotIndex = points.size();
        
        while (pivotIndex != k) {
            pivotIndex = partition(points, low, high);
            if (pivotIndex < k) {
                low = pivotIndex;
            } else {
                high = pivotIndex - 1;
            }
        }
        
        return vector<vector<int>>(points.begin(), points.begin() + k);
    }
private:
    int partition(vector<vector<int>>& points, int low, int high) {
        vector<int> pivot = points[low + (high - low) / 2];
        int pivotDistance = getDistance(pivot);
        
        while (low < high) {
            if (getDistance(points[low]) >= pivotDistance) {
                swap(points[low], points[high]);
                high--;
            } else {
                low++;
            }
        }
        
        if (getDistance(points[low]) < pivotDistance) {
            low++;
        }
        return low;
    }
    
    int getDistance(vector<int>& point) {
        return pow(point[0], 2) + pow(point[1], 2);
    }
};
*/

/*
// O(n logn) solution using sorting
class Solution {
public:
    vector<vector<int>> kClosest(vector<vector<int>>& points, int k) {
        vector<vector<int>> res(k);
        sort(points.begin(), points.end(), [](vector<int>& p1, vector<int>& p2){
            int dist_p1 = pow(p1[0],2) + pow(p1[1],2);
            int dist_p2 = pow(p2[0],2) + pow(p2[1],2);
            return dist_p1 < dist_p2;
        });
        copy(points.begin(), points.begin() + k, res.begin());
        return res;
    }
};
*/

// O(k logn) solution
class Solution {
public:
    vector<vector<int>> kClosest(vector<vector<int>>& points, int k) {
        vector<vector<int>> triples;
        for (auto& p : points)
            triples.push_back({p[0] * p[0] + p[1] * p[1], p[0], p[1]});
        // Min heap of vectors (triples). This constructor takes O(n) time (n = len(v))
        priority_queue<vector<int>, vector<vector<int>>, greater<vector<int>>> pq(triples.begin(), triples.end());
        vector<vector<int>> res;
        while (k--){
            vector<int> el = pq.top();
            pq.pop();
            res.push_back({el[1], el[2]});
        }
        return res;
    }
};
```
