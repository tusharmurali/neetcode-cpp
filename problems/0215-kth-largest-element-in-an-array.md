# 215. Kth Largest Element In An Array

- **Difficulty:** Medium  
- **Pattern:** Heap / Priority Queue  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/kth-largest-element-in-an-array/>  
- **NeetCode:** <https://neetcode.io/problems/kth-largest-element-in-an-array>  
- **Video:** <https://www.youtube.com/watch?v=XEmy13g1Qxc>  

[← Back to index](../INDEX.md)

## 1. Sorting

If you sort the entire array, all elements will be arranged from smallest to largest.  
Once sorted:

- The **largest element** is at the last position.
- The **2nd largest** is one position before that.
- The **k-th largest** is simply at index `n - k`.

So the problem becomes:  
→ _Sort the array and pick the element that is k steps from the end._

This is simple but not the most efficient, because sorting takes `O(n log n)`.

```cpp
class Solution {
public:
    int findKthLargest(vector<int>& nums, int k) {
        sort(nums.begin(), nums.end());
        return nums[nums.size() - k];
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 2. Min-Heap

Instead of sorting the whole array, we only need to keep track of the **k largest elements** seen so far.

A **min-heap** is perfect for this:

- A min-heap always keeps the _smallest_ element at the top.
- If we maintain a heap of size `k`, then:
    - the heap will always contain the `k` largest elements seen so far.
    - the root of the heap (the smallest among these `k`) will be the **k-th largest** element.

Process:

- Add elements into the heap.
- If the heap grows larger than `k`, remove the smallest element.
- At the end, the root of the heap is exactly the k-th largest element.

This avoids sorting the entire array and keeps memory small.

```cpp
class Solution {
public:
    int findKthLargest(vector<int>& nums, int k) {
        priority_queue<int, vector<int>, greater<int>> minHeap;
        for (int num : nums) {
            minHeap.push(num);
            if (minHeap.size() > k) {
                minHeap.pop();
            }
        }
        return minHeap.top();
    }
};
```

**Complexity**

- Time complexity: $O(n \log k)$
- Space complexity: $O(k)$

> Where $n$ is the length of the array $nums$.

## 3. Quick Select

Quick Select is a selection algorithm that works like QuickSort but only explores the side of the array that contains the answer.

Key idea:

- Pick a pivot.
- Rearrange elements so that:
    - all numbers **smaller than or equal to** the pivot go to the left,
    - all numbers **greater** go to the right.
- After partitioning, the pivot ends up in its correct sorted position.
- Instead of sorting the whole array, we check:
    - If the pivot’s final position is the index we want → answer found.
    - Otherwise, recurse only into the side where the target index lies.

Because we eliminate half the array each time, this approach is much faster on average than full sorting.

For the k-th largest:

- Convert it to the corresponding index in sorted order:
    - index = n − k
- Then use Quick Select to find the value that would appear at that index.

```cpp
class Solution {
public:
    int findKthLargest(vector<int>& nums, int k) {
        k = nums.size() - k;
        return quickSelect(nums, 0, nums.size() - 1, k);
    }

    int quickSelect(vector<int>& nums, int left, int right, int k) {
        int pivot = nums[right];
        int p = left;

        for (int i = left; i < right; ++i) {
            if (nums[i] <= pivot) {
                swap(nums[p], nums[i]);
                p++;
            }
        }
        swap(nums[p], nums[right]);

        if (p > k) {
            return quickSelect(nums, left, p - 1, k);
        } else if (p < k) {
            return quickSelect(nums, p + 1, right, k);
        } else {
            return nums[p];
        }
    }
};
```

**Complexity**

- Time complexity: $O(n)$ in average case, $O(n ^ 2)$ in worst case.
- Space complexity: $O(n)$

## 4. Quick Select (Optimal)

Quick Select finds the k-th largest (or smallest) element without sorting the whole array.

This **optimal version** improves the classic Quick Select by:

- choosing a pivot more intelligently (using a 3-element median-like technique),
- reducing worst-case behavior,
- partitioning the array efficiently so that large elements move left and small elements move right.

The key idea is still the same:

- After partitioning, the pivot ends up exactly where it belongs in sorted order.
- If the pivot’s final index is the one we need, we’re done.
- Otherwise, we only search the half of the array where the answer lies.

This drastically reduces unnecessary work and leads to **O(n)** average time.

```cpp
class Solution {
public:
    int partition(vector<int>& nums, int left, int right) {
        int mid = (left + right) >> 1;
        swap(nums[mid], nums[left + 1]);

        if (nums[left] < nums[right])
            swap(nums[left], nums[right]);
        if (nums[left + 1] < nums[right])
            swap(nums[left + 1], nums[right]);
        if (nums[left] < nums[left + 1])
            swap(nums[left], nums[left + 1]);

        int pivot = nums[left + 1];
        int i = left + 1;
        int j = right;

        while (true) {
            while (nums[++i] > pivot);
            while (nums[--j] < pivot);
            if (i > j) break;
            swap(nums[i], nums[j]);
        }

        nums[left + 1] = nums[j];
        nums[j] = pivot;
        return j;
    }

    int quickSelect(vector<int>& nums, int k) {
        int left = 0;
        int right = nums.size() - 1;

        while (true) {
            if (right <= left + 1) {
                if (right == left + 1 && nums[right] > nums[left])
                    swap(nums[left], nums[right]);
                return nums[k];
            }

            int j = partition(nums, left, right);

            if (j >= k) right = j - 1;
            if (j <= k) left = j + 1;
        }
    }

    int findKthLargest(vector<int>& nums, int k) {
        return quickSelect(nums, k - 1);
    }
};
```

**Complexity**

- Time complexity: $O(n)$ in average case, $O(n ^ 2)$ in worst case.
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0215-kth-largest-element-in-an-array.cpp` in the NeetCode repo)

```cpp
/*
    Given array and int k, return kth largest element in array
    Ex. nums = [3,2,1,5,6,4], k = 2 -> 5

    Quickselect, partition until pivot = k, left side all > k

    Time: O(n) -> optimized from O(n log k) min heap solution
    Space: O(1)
*/

// class Solution {
// public:
//     int findKthLargest(vector<int>& nums, int k) {
//         priority_queue<int, vector<int>, greater<int>> pq;
//         for (int i = 0; i < nums.size(); i++) {
//             pq.push(nums[i]);
//             if (pq.size() > k) {
//                 pq.pop();
//             }
//         }
//         return pq.top();
//     }
// };

/*
class Solution {
public:
    int findKthLargest(vector<int>& nums, int k) {
        int low = 0;
        int high = nums.size() - 1;
        int pivotIndex = nums.size();
        
        while (pivotIndex != k - 1) {
            pivotIndex = partition(nums, low, high);
            if (pivotIndex < k - 1) {
                low = pivotIndex + 1;
            } else {
                high = pivotIndex - 1;
            }
        }
        
        return nums[k - 1];
    }
private:
    int partition(vector<int>& nums, int low, int high) {
        int pivot = nums[low];
        
        int i = low + 1;
        int j = high;
        
        while (i <= j) {
            if (nums[i] < pivot && pivot < nums[j]) {
                swap(nums[i], nums[j]);
                i++;
                j--;
            }
            if (nums[i] >= pivot) {
                i++;
            }
            if (pivot >= nums[j]) {
                j--;
            }
        }
        
        swap(nums[low], nums[j]);
        return j;
    }
};
*/

// Video's QuickSelect implementation
// class Solution {
// public:
//     int findKthLargest(vector<int>& nums, int k) {
//         int index = nums.size() - k;
//         return quickSelect(nums, index, 0, nums.size() - 1);
//     }
// private:
//     int quickSelect(vector<int>& nums, int k, int l, int r){
//         int pivot = nums[r];
//         int p_pos = l;
//         for (int i = l; i < r; ++i){
//             if (nums[i] <= pivot){
//                 swap(nums[i], nums[p_pos]);
//                 ++p_pos;
//             }
//         }
//         swap(nums[p_pos], nums[r]);
//         if (k < p_pos)
//             return quickSelect(nums, k, l, p_pos - 1);
//         if (k > p_pos)
//             return quickSelect(nums, k, p_pos + 1, r);
//         return nums[p_pos];
//     }
// };

// Solution that can pass current tests
class Solution {
public:
    int findKthLargest(vector<int>& nums, int k) {
        int pivot = nums[rand() % nums.size()];
        vector<int> left, mid, right;
        for (auto num: nums) {
            if (num > pivot) left.push_back(num);
            else if (num == pivot) mid.push_back(num);
            else right.push_back(num);
        }
        if (k <= left.size()) return findKthLargest(left, k);
        else if (k <= left.size() + mid.size()) return mid[0];
        else return findKthLargest(right, k - left.size() - mid.size());
    }
};
```
