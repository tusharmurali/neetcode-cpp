# 912. Sort an Array

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/sort-an-array/>  
- **NeetCode:** <https://neetcode.io/problems/sort-an-array>  
- **Video:** <https://www.youtube.com/watch?v=MsYZSinhuFo>  

[← Back to index](../INDEX.md)

## 1. Quick Sort

Quick sort works by selecting a `pivot` element and partitioning the array so that elements smaller than the `pivot` go to its left and larger elements go to its right. This implementation uses median-of-three pivot selection (comparing `left`, `middle`, and `right` elements) to avoid worst-case performance on already sorted arrays. After partitioning, we recursively sort the two halves.

```cpp
class Solution {
public:
int partition(vector<int>& nums, int left, int right) {
        int mid = (left + right) >> 1;
        swap(nums[mid], nums[left + 1]);

        if (nums[left] > nums[right])
            swap(nums[left], nums[right]);
        if (nums[left + 1] > nums[right])
            swap(nums[left + 1], nums[right]);
        if (nums[left] > nums[left + 1])
            swap(nums[left], nums[left + 1]);

        int pivot = nums[left + 1];
        int i = left + 1;
        int j = right;

        while (true) {
            while (nums[++i] < pivot);
            while (nums[--j] > pivot);
            if (i > j) break;
            swap(nums[i], nums[j]);
        }

        nums[left + 1] = nums[j];
        nums[j] = pivot;
        return j;
    }

    void quickSort(vector<int>& nums, int left, int right) {
        if (right <= left + 1) {
            if (right == left + 1 && nums[right] < nums[left])
                swap(nums[left], nums[right]);
            return;
        }

        int j = partition(nums, left, right);
        quickSort(nums, left, j - 1);
        quickSort(nums, j + 1, right);
    }

    vector<int> sortArray(vector<int>& nums) {
        quickSort(nums, 0, nums.size() - 1);
        return nums;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$ in average case, $O(n ^ 2)$ in worst case.
- Space complexity: $O(\log n)$ for recursive stack.

## 2. Merge Sort

Merge sort divides the array into two halves, recursively sorts each half, and then merges the sorted halves. The merge step combines two sorted arrays into one by repeatedly picking the smaller element from the front of each array. This divide-and-conquer approach guarantees O(n log n) time regardless of input order.

```cpp
class Solution {
public:
    vector<int> sortArray(vector<int>& nums) {
        mergeSort(nums, 0, nums.size() - 1);
        return nums;
    }

private:
    void mergeSort(vector<int>& arr, int l, int r) {
        if (l >= r) return;
        int m = (l + r) / 2;
        mergeSort(arr, l, m);
        mergeSort(arr, m + 1, r);
        merge(arr, l, m, r);
    }

    void merge(vector<int>& arr, int l, int m, int r) {
        vector<int> temp;
        int i = l, j = m + 1;

        while (i <= m && j <= r) {
            if (arr[i] <= arr[j]) {
                temp.push_back(arr[i++]);
            } else {
                temp.push_back(arr[j++]);
            }
        }

        while (i <= m) temp.push_back(arr[i++]);
        while (j <= r) temp.push_back(arr[j++]);

        for (int i = l; i <= r; i++) {
            arr[i] = temp[i - l];
        }
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 3. Heap Sort

Heap sort uses a binary heap data structure to sort elements. First, we build a max-heap from the array, which places the largest element at the root. Then we repeatedly extract the maximum (swap it to the end) and restore the heap property. This process naturally sorts the array from smallest to largest.

```cpp
class Solution {
public:
    vector<int> sortArray(vector<int>& nums) {
        heapSort(nums);
        return nums;
    }
private:
    void heapify(vector<int>& arr, int n, int i) {
        int l = (i << 1) + 1;
        int r = (i << 1) + 2;
        int largestNode = i;

        if (l < n && arr[l] > arr[largestNode]) {
            largestNode = l;
        }

        if (r < n && arr[r] > arr[largestNode]) {
            largestNode = r;
        }

        if (largestNode != i) {
            swap(arr[i], arr[largestNode]);
            heapify(arr, n, largestNode);
        }
    }

    void heapSort(vector<int>& arr) {
        int n = arr.size();
        for (int i = n / 2 - 1; i >= 0; i--) {
            heapify(arr, n, i);
        }

        for (int i = n - 1; i > 0; i--) {
            swap(arr[0], arr[i]);
            heapify(arr, i, 0);
        }
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(\log n)$ for recursive stack.

## 4. Counting Sort

Counting sort works by counting the frequency of each distinct value, then reconstructing the sorted array by outputting each value the appropriate number of times. This is efficient when the range of values (max - min) is not significantly larger than the number of elements. It avoids comparisons entirely.

```cpp
class Solution {
private:
    void countingSort(vector<int> &arr) {
        unordered_map<int, int> count;
        int minVal = *min_element(arr.begin(), arr.end());
        int maxVal = *max_element(arr.begin(), arr.end());

        for (auto& val : arr) {
            count[val]++;
        }

        int index = 0;
        for (int val = minVal; val <= maxVal; ++val) {
            while (count[val] > 0) {
                arr[index] = val;
                index += 1;
                count[val] -= 1;
            }
        }
    }

public:
    vector<int> sortArray(vector<int>& nums) {
        countingSort(nums);
        return nums;
    }
};
```

**Complexity**

- Time complexity: $O(n + k)$
- Space complexity: $O(n)$

> Where $n$ is the size of the array $nums$ and $k$ is the range between the minimum and maximum values in the array.

## 5. Radix Sort

Radix sort processes integers digit by digit, from least significant to most significant. For each digit position, we use counting sort as a stable subroutine. Since counting sort is stable, the relative order from previous digit sorts is preserved. To handle negative numbers, we separate them, sort their absolute values in reverse, and concatenate.

```cpp
class Solution {
public:
    vector<int> sortArray(vector<int>& nums) {
        vector<int> negatives, positives;

        for (int num : nums) {
            if (num < 0) {
                negatives.push_back(-num);
            } else {
                positives.push_back(num);
            }
        }

        if (!negatives.empty()) {
            radixSort(negatives);
            reverse(negatives.begin(), negatives.end());
            for (int& num : negatives) {
                num = -num;
            }
        }

        if (!positives.empty()) {
            radixSort(positives);
        }

        int index = 0;
        for (int& num : negatives) {
            nums[index++] = num;
        }
        for (int& num : positives) {
            nums[index++] = num;
        }
        return nums;
    }

private:
    void countSort(vector<int>& arr, int n, int d) {
        vector<int> count(10, 0);
        for (int num : arr) {
            count[(num / d) % 10]++;
        }
        for (int i = 1; i < 10; i++) {
            count[i] += count[i - 1];
        }

        vector<int> res(n);
        for (int i = n - 1; i >= 0; i--) {
            int idx = (arr[i] / d) % 10;
            res[count[idx] - 1] = arr[i];
            count[idx]--;
        }

        for (int i = 0; i < n; i++) {
            arr[i] = res[i];
        }
    }

    void radixSort(vector<int>& arr) {
        int n = arr.size();
        int maxElement = *max_element(arr.begin(), arr.end());
        int d = 1;

        while (maxElement / d > 0) {
            countSort(arr, n, d);
            d *= 10;
        }
    }
};
```

**Complexity**

- Time complexity: $O(d * n)$
- Space complexity: $O(n)$

> Where $n$ is the size of the array $nums$ and $d$ is the number of digits in the maximum element of the array.

## 6. Shell Sort

Shell sort is a generalization of insertion sort that allows exchanges of elements far apart. It starts by sorting elements at a large gap, then progressively reduces the gap. This allows elements to move quickly toward their final positions. When the gap becomes 1, it performs a standard insertion sort on an already nearly-sorted array.

```cpp
class Solution {
private:
    void shellSort(vector<int>& nums, int n) {
        for (int gap = n / 2; gap >= 1; gap /= 2) {
            for (int i = gap; i < n; i++) {
                int tmp = nums[i];
                int j = i - gap;
                while (j >= 0 && nums[j] > tmp) {
                    nums[j + gap] = nums[j];
                    j -= gap;
                }
                nums[j + gap] = tmp;
            }
        }
    }

public:
    vector<int> sortArray(vector<int>& nums) {
        if (nums.size() == 1) return nums;
        shellSort(nums, nums.size());
        return nums;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$ in average case, $O(n ^ 2)$ in worst case.
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0912-sort-an-array.cpp` in the NeetCode repo)

```cpp
/*
    Given an array of integers nums, sort the array in ascending order and return it.
    Ex. nums = [5,2,3,1] -> [1,2,3,5]

    Use Merge sort to sort the array.

    Time - O(nlogn)
    Space - O(n)
*/

class Solution {
  private:
    void merge(vector<int> &nums, int low, int mid, int high) {
        if(low >= high) 
            return;
        
        int l = low, r = mid + 1, k = 0, size = high - low + 1;
        vector<int> sorted(size, 0);
        
        while (l <= mid and r <= high){
            if(nums[l] < nums[r])
                sorted[k++] = nums[l++];
            else
                sorted[k++] = nums[r++];
        }

        while(l <= mid) 
            sorted[k++] = nums[l++];
        while(r <= high) 
            sorted[k++] = nums[r++];
        
        for(k = 0; k < size; k++)
            nums[k + low] = sorted[k];
    }

    void mergeSort(vector<int>& nums, int low, int high){
        if(low >= high) 
            return;
	    
        int mid = low + (high - low) / 2;
	    
        mergeSort(nums, low, mid);
	    mergeSort(nums, mid + 1, high);
	    merge(nums, low, mid, high);
    }

public:
    vector<int> sortArray(vector<int>& nums) {
        mergeSort(nums, 0, nums.size()-1);
        return nums;
    }
};
```
