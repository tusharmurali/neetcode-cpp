# 347. Top K Frequent Elements

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/top-k-frequent-elements/>  
- **NeetCode:** <https://neetcode.io/problems/top-k-elements-in-list>  
- **Video:** <https://www.youtube.com/watch?v=YPTqKIgVk-k>  

[← Back to index](../INDEX.md)

## 1. Sorting

To find the `k` most frequent elements, we first need to know how often each number appears.
Once we count the frequencies, we can sort the unique numbers based on how many times they occur.
After sorting, the numbers with the highest frequencies will naturally appear at the end of the list.
By taking the last `k` entries, we get the `k` most frequent elements.

This approach is easy to reason about:
**count the frequencies → sort by frequency → take the top `k`.**

```cpp
class Solution {
public:
    vector<int> topKFrequent(vector<int>& nums, int k) {
        unordered_map<int, int> count;
        for (int num : nums) {
            count[num]++;
        }

        vector<pair<int, int>> arr;
        for (const auto& p : count) {
            arr.push_back({p.second, p.first});
        }
        sort(arr.rbegin(), arr.rend());

        vector<int> res;
        for (int i = 0; i < k; ++i) {
            res.push_back(arr[i].second);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 2. Min-Heap

After counting how often each number appears, we want to efficiently keep track of only the `k` most frequent elements.
A **min-heap** is perfect for this because it always keeps the smallest element at the top.
By pushing `(frequency, value)` pairs into the heap and removing the smallest whenever the heap grows beyond size `k`, we ensure that the heap always contains the top `k` most frequent elements.
In the end, the heap holds exactly the `k` values with the highest frequencies.

```cpp
class Solution {
public:
    vector<int> topKFrequent(vector<int>& nums, int k) {
        unordered_map<int, int> count;
        for (int num : nums) {
            count[num]++;
        }

        priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> heap;
        for (auto& entry : count) {
            heap.push({entry.second, entry.first});
            if (heap.size() > k) {
                heap.pop();
            }
        }

        vector<int> res;
        for (int i = 0; i < k; i++) {
            res.push_back(heap.top().second);
            heap.pop();
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log k)$
- Space complexity: $O(n + k)$

> Where $n$ is the length of the array and $k$ is the number of top frequent elements.

## 3. Bucket Sort

Each number in the array appears a certain number of times, and the maximum possible frequency is the length of the array.
We can use this idea by creating a list where the index represents a frequency, and at each index we store all numbers that appear exactly that many times.

For example:

- All numbers that appear `1` time go into group `freq[1]`.
- All numbers that appear `2` times go into group `freq[2]`.
- And so on.

After we build these groups, we look from the highest possible frequency down to the lowest and collect numbers from these groups until we have `k` of them.
This way, we directly jump to the most frequent numbers without sorting all the elements by frequency.

```cpp
class Solution {
public:
    vector<int> topKFrequent(vector<int>& nums, int k) {
        unordered_map<int, int> count;
        vector<vector<int>> freq(nums.size() + 1);

        for (int n : nums) {
            count[n] = 1 + count[n];
        }
        for (const auto& entry : count) {
            freq[entry.second].push_back(entry.first);
        }

        vector<int> res;
        for (int i = freq.size() - 1; i > 0; --i) {
            for (int n : freq[i]) {
                res.push_back(n);
                if (res.size() == k) {
                    return res;
                }
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/0347-top-k-frequent-elements.cpp` in the NeetCode repo)

```cpp
/*
    Given an integer array nums & an integer k, return the k most frequent elements
    Ex. nums = [1,1,1,2,2,3] k = 2 -> [1,2], nums = [1] k = 1 -> [1]
    
    Heap -> optimize w/ freq map & bucket sort (no freq can be > n), get results from end
*/

// Time: O(n log k)
// Space: O(n + k)

// class Solution {
// public:
//     vector<int> topKFrequent(vector<int>& nums, int k) {
//         unordered_map<int, int> m;
//         for (int i = 0; i < nums.size(); i++) {
//             m[nums[i]]++;
//         }
//         priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;
//         for (auto it = m.begin(); it != m.end(); it++) {
//             pq.push({it->second, it->first});
//             if (pq.size() > k) {
//                 pq.pop();
//             }
//         }
//         vector<int> result;
//         while (!pq.empty()) {
//             result.push_back(pq.top().second);
//             pq.pop();
//         }
//         return result;
//     }
// };

// Time: O(n)
// Space: O(n)

class Solution {
public:
    vector<int> topKFrequent(vector<int>& nums, int k) {
        int n = nums.size();
        
        unordered_map<int, int> m;
        for (int i = 0; i < n; i++) {
            m[nums[i]]++;
        }
        
        vector<vector<int>> buckets(n + 1);
        for (auto it = m.begin(); it != m.end(); it++) {
            buckets[it->second].push_back(it->first);
        }
        
        vector<int> result;
        
        for (int i = n; i >= 0; i--) {
            if (result.size() >= k) {
                break;
            }
            if (!buckets[i].empty()) {
                result.insert(result.end(), buckets[i].begin(), buckets[i].end());
            }
        }
        
        return result;
    }
};
```
