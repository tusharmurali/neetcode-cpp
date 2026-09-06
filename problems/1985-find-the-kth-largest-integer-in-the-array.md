# 1985. Find The Kth Largest Integer In The Array

- **Difficulty:** Medium  
- **Pattern:** Heap / Priority Queue  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/find-the-kth-largest-integer-in-the-array/>  
- **NeetCode:** <https://neetcode.io/problems/find-the-kth-largest-integer-in-the-array>  
- **Video:** <https://www.youtube.com/watch?v=lRCaNiqO3xI>  

[← Back to index](../INDEX.md)

## 1. Sorting

Since numbers are represented as strings and can be very large (up to 100 digits), we cannot convert them to integers directly. Instead, we compare strings by length first, then lexicographically. A longer string represents a larger number, and for equal lengths, lexicographic order matches numeric order. After sorting in descending order, the `k`th element is our answer.

```cpp
class Solution {
public:
    string kthLargestNumber(vector<string>& nums, int k) {
        sort(nums.begin(), nums.end(), [](const string& a, const string& b) {
            return a.size() == b.size() ? a > b : a.size() > b.size();
        });
        return nums[k - 1];
    }
};
```

**Complexity**

- Time complexity: $O(m * n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

> Where $n$ is the number of strings and $m$ is the average length of a string.

## 2. Max-Heap

A max-heap keeps the largest element at the top. By inserting all elements into a max-heap and extracting the maximum `k` times, the `k`th extraction gives us the `k`th largest element. The custom comparator ensures proper ordering for string-represented numbers.

```cpp
class Solution {
public:
    string kthLargestNumber(vector<string>& nums, int k) {
        auto cmp = [](const string& a, const string& b) {
            return a.size() == b.size() ? a < b : a.size() < b.size();
        };

        priority_queue<string, vector<string>, decltype(cmp)> maxHeap(cmp);

        for (const string& num : nums) {
            maxHeap.push(num);
        }

        while (--k > 0) {
            maxHeap.pop();
        }

        return maxHeap.top();
    }
};
```

**Complexity**

- Time complexity: $O(m * (n + k) * \log n)$
- Space complexity: $O(n)$

> Where $n$ is the number of strings and $m$ is the average length of a string.

## 3. Min-Heap

Instead of storing all elements and extracting `k` times, we can maintain a min-heap of size `k`. The smallest element in this heap is always at the top. As we process elements, if the heap size exceeds `k`, we remove the smallest. After processing all elements, the heap contains the `k` largest elements, and the top (minimum of these `k`) is the `k`th largest overall.

```cpp
class Solution {
public:
    string kthLargestNumber(vector<string>& nums, int k) {
        auto cmp = [](const string& a, const string& b) {
            return a.size() == b.size() ? a > b : a.size() > b.size();
        };

        priority_queue<string, vector<string>, decltype(cmp)> minHeap(cmp);

        for (const string& num : nums) {
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

- Time complexity: $O(m * n * \log k)$
- Space complexity: $O(k)$

> Where $n$ is the number of strings and $m$ is the average length of a string.

## 4. Quick Select

Quick Select is a selection algorithm based on the partitioning step of QuickSort. Instead of fully sorting the array, we only partition around a pivot and recurse into the side that contains our target index. On average, this finds the `k`th element in linear time. The algorithm uses median-of-three pivot selection to improve performance and avoid worst-case scenarios.

```cpp
class Solution {
public:
    string kthLargestNumber(vector<string>& nums, int k) {
        return quickSelect(nums, k - 1);
    }

private:
    bool greater(const string& x, const string& y) {
        if (x.size() != y.size()) {
            return x.size() > y.size();
        }
        return x > y;
    }

    bool less(const string& x, const string& y) {
        if (x.size() != y.size()) {
            return x.size() < y.size();
        }
        return x < y;
    }

    int partition(vector<string>& nums, int left, int right) {
        int mid = (left + right) >> 1;
        swap(nums[mid], nums[left + 1]);

        if (less(nums[left], nums[right])) {
            swap(nums[left], nums[right]);
        }
        if (less(nums[left + 1], nums[right])) {
            swap(nums[left + 1], nums[right]);
        }
        if (less(nums[left], nums[left + 1])) {
            swap(nums[left], nums[left + 1]);
        }

        string pivot = nums[left + 1];
        int i = left + 1, j = right;

        while (true) {
            while (greater(nums[++i], pivot));
            while (less(nums[--j], pivot));
            if (i > j) break;
            swap(nums[i], nums[j]);
        }

        swap(nums[left + 1], nums[j]);
        return j;
    }

    string quickSelect(vector<string>& nums, int k) {
        int left = 0, right = nums.size() - 1;

        while (true) {
            if (right <= left + 1) {
                if (right == left + 1 && greater(nums[right], nums[left])) {
                    swap(nums[left], nums[right]);
                }
                return nums[k];
            }

            int j = partition(nums, left, right);
            if (j >= k) {
                right = j - 1;
            }
            if (j <= k) {
                left = j + 1;
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$ in average case, $O(m * n ^ 2)$ in worst case.
- Space complexity: $O(1)$

## Standalone solution file (`cpp/1985-find-the-kth-largest-integer-in-the-array.cpp` in the NeetCode repo)

```cpp
class Solution {
private:
    static bool st(string &a,string &b){
        if(a.size()==b.size()) return a<b;
        return a.size()<b.size();
    }
    
    
public:
    string kthLargestNumber(vector<string>& nums, int k) {
        sort(nums.begin(),nums.end(),st);
        return nums[nums.size()-k];
        
    }
};
```
