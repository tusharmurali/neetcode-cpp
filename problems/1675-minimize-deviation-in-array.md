# 1675. Minimize Deviation in Array

- **Difficulty:** Hard  
- **Pattern:** Heap / Priority Queue  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/minimize-deviation-in-array/>  
- **NeetCode:** <https://neetcode.io/problems/minimize-deviation-in-array>  
- **Video:** <https://www.youtube.com/watch?v=boHNFptxo2A>  

[← Back to index](../INDEX.md)

## 1. Sorting + Sliding Window

Each element in the array can only take certain values: odd numbers can become themselves or double themselves, while even numbers can be halved repeatedly until they become odd. The key insight is that we can precompute all possible values each element can take, then find the smallest range that contains at least one value from each original element.

This transforms the problem into finding the smallest window in a sorted list of values where each original array element is represented at least once. We use a sliding window approach on the sorted list of all possible values, tracking which original elements are covered.

```cpp
class Solution {
public:
    int minimumDeviation(vector<int>& nums) {
        int n = nums.size();
        vector<pair<int, int>> arr;

        for (int i = 0; i < n; i++) {
            int num = nums[i];
            if (num % 2 == 1) {
                arr.emplace_back(num, i);
                arr.emplace_back(num * 2, i);
            } else {
                while (num % 2 == 0) {
                    arr.emplace_back(num, i);
                    num /= 2;
                }
                arr.emplace_back(num, i);
            }
        }

        sort(arr.begin(), arr.end());
        int res = INT_MAX;

        vector<int> seen(n, 0);
        int count = 0, i = 0;

        for (int j = 0; j < arr.size(); j++) {
            seen[arr[j].second]++;
            if (seen[arr[j].second] == 1) {
                count++;
                while (count == n) {
                    res = min(res, arr[j].first - arr[i].first);
                    seen[arr[i].second]--;
                    if (seen[arr[i].second] == 0) {
                        count--;
                    }
                    i++;
                }
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O((n \log m) * \log (n \log m))$
- Space complexity: $O(n \log m)$

> Where $n$ is the size of the array $nums$ and $m$ is the maximum element in $nums$.

## 2. Min-Heap

Instead of generating all possible values upfront, we can work incrementally. First, reduce every number to its minimum possible value (divide even numbers until they become odd). Then, we repeatedly try to increase the smallest element by doubling it (if possible), since increasing smaller values is the only way to reduce the deviation.

The min-heap lets us efficiently access the smallest current value. We track the maximum value in the heap separately. Each iteration, we pop the minimum, update our best deviation, and if that minimum can still be doubled, we push the doubled value back.

```cpp
class Solution {
public:
    int minimumDeviation(vector<int>& nums) {
        priority_queue<pair<int, int>, vector<pair<int, int>>, greater<>> minHeap;
        int heapMax = 0;

        for (int num : nums) {
            int tmp = num;
            while (num % 2 == 0) {
                num /= 2;
            }
            minHeap.push({num, max(tmp, 2 * num)});
            heapMax = max(heapMax, num);
        }

        int res = INT_MAX;

        while (minHeap.size() == nums.size()) {
            auto [n, nMax] = minHeap.top();
            minHeap.pop();
            res = min(res, heapMax - n);

            if (n < nMax) {
                minHeap.push({n * 2, nMax});
                heapMax = max(heapMax, n * 2);
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n *\log n * \log m)$
- Space complexity: $O(n)$

> Where $n$ is the size of the array $nums$ and $m$ is the maximum element in $nums$.

## 3. Max-Heap

We can approach this from the opposite direction: start with all numbers at their maximum possible value, then repeatedly decrease the largest element. Odd numbers are first doubled to reach their maximum. Even numbers stay as they are initially.

Using a max-heap, we always have quick access to the current largest value. We track the minimum value separately. Each iteration, we halve the maximum (if even) and update our best deviation. The process stops when the maximum is odd, since odd numbers cannot be reduced.

```cpp
class Solution {
public:
    int minimumDeviation(vector<int>& nums) {
        priority_queue<int> maxHeap;
        int minVal = INT_MAX;

        for (int num : nums) {
            if (num % 2 == 1) num *= 2;
            maxHeap.push(num);
            minVal = min(minVal, num);
        }

        int res = INT_MAX;

        while (!maxHeap.empty()) {
            int maxVal = maxHeap.top();
            maxHeap.pop();
            res = min(res, maxVal - minVal);

            if (maxVal % 2 == 1) break;

            int nextVal = maxVal / 2;
            maxHeap.push(nextVal);
            minVal = min(minVal, nextVal);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n *\log n * \log m)$
- Space complexity: $O(n)$

> Where $n$ is the size of the array $nums$ and $m$ is the maximum element in $nums$.

## Standalone solution file (`cpp/1675-minimize-deviation-in-array.cpp` in the NeetCode repo)

```cpp
/*
  You are given an array nums of n positive integers.

  You can perform two types of operations on any element of the array any number of times:

    If the element is even, divide it by 2.
        For example, if the array is [1,2,3,4], then you can do this operation on the last element, and the array will be [1,2,3,2].
    If the element is odd, multiply it by 2.
        For example, if the array is [1,2,3,4], then you can do this operation on the first element, and the array will be [2,2,3,4].

  The deviation of the array is the maximum difference between any two elements in the array.

Return the minimum deviation the array can have after performing some number of operations.
  Ex. Input: nums = [1,2,3,4]
      Output: 1
      Explanation: You can transform the array to [1,2,3,2], then to [2,2,3,2], then the deviation will be 3 - 2 = 1.

  Time  : O(N);
  Space : O(N);
*/

class Solution {
public:
    int minimumDeviation(vector<int>& nums) {
        priority_queue <int> pq;
        int minimum = INT_MAX;
        for(auto i : nums) {
            if(i & 1)
                i *= 2;
            minimum = min(minimum, i);
            pq.push(i);
        }
        int res = INT_MAX;
        while(pq.top() % 2 == 0) {
            int val = pq.top();
            res = min(res, val - minimum);
            minimum = min(val/2, minimum);
            pq.pop();
            pq.push(val/2);
        }
        return min(res, pq.top() - minimum);
    }
};
```
