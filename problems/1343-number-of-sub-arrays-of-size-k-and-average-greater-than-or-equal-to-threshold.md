# 1343. Number of Sub Arrays of Size K and Avg Greater than or Equal to Threshold

- **Difficulty:** Medium  
- **Pattern:** Sliding Window  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/number-of-sub-arrays-of-size-k-and-average-greater-than-or-equal-to-threshold/>  
- **NeetCode:** <https://neetcode.io/problems/number-of-sub-arrays-of-size-k-and-average-greater-than-or-equal-to-threshold>  
- **Video:** <https://www.youtube.com/watch?v=D8B4tKxMTnY>  
- **Video approach:** 3. Sliding Window - I (auto-matched)  

[← Back to index](../INDEX.md)

## 1. Brute Force

For each valid starting position of a subarray of size `k`, we compute the sum of all elements in that window and check if the average meets the threshold. This approach recalculates the sum from scratch for every window.

```cpp
class Solution {
public:
    int numOfSubarrays(vector<int>& arr, int k, int threshold) {
        int res = 0, l = 0;

        for (int r = k - 1; r < arr.size(); r++) {
            int sum = 0;
            for (int i = l; i <= r; i++) {
                sum += arr[i];
            }
            if (sum / k >= threshold) {
                res++;
            }
            l++;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * k)$
- Space complexity: $O(1)$

> Where $n$ is the size of the array $arr$ and $k$ is the size of the sub-array.

## 2. Prefix Sum

Instead of recalculating sums from scratch, we precompute prefix sums. The sum of any subarray from index `l` to `r` becomes a simple subtraction: `prefix[r+1] - prefix[l]`. This trades memory for faster subarray sum queries.

```cpp
class Solution {
public:
    int numOfSubarrays(vector<int>& arr, int k, int threshold) {
        vector<int> prefixSum(arr.size() + 1);
        for (int i = 0; i < arr.size(); i++) {
            prefixSum[i + 1] += prefixSum[i] + arr[i];
        }

        int res = 0, l = 0;
        for (int r = k - 1; r < arr.size(); r++) {
            int sum = prefixSum[r + 1] - prefixSum[l];
            if (sum / k >= threshold) {
                res++;
            }
            l++;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

> Where $n$ is the size of the array $arr$ and $k$ is the size of the sub-array.

## 3. Sliding Window - I ▶ video

We maintain a running sum of the current window. When the window slides, we add the new element entering from the right and remove the element leaving from the left. This gives constant-time updates per window instead of recalculating from scratch.

```cpp
class Solution {
public:
    int numOfSubarrays(vector<int>& arr, int k, int threshold) {
        int res = 0, curSum = 0;

        for (int i = 0; i < k - 1; i++) {
            curSum += arr[i];
        }

        for (int L = 0; L <= arr.size() - k; L++) {
            curSum += arr[L + k - 1];
            if ((curSum / k) >= threshold) {
                res++;
            }
            curSum -= arr[L];
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

> Where $n$ is the size of the array $arr$ and $k$ is the size of the sub-array.

## 4. Sliding Window - II

A small optimization: instead of dividing the sum by `k` for each comparison, we multiply the threshold by `k` once upfront. This converts the average check into a simple sum comparison, avoiding repeated division.

```cpp
class Solution {
public:
    int numOfSubarrays(vector<int>& arr, int k, int threshold) {
        threshold *= k;
        int res = 0, curSum = 0;

        for (int R = 0; R < arr.size(); R++) {
            curSum += arr[R];
            if (R >= k - 1) {
                if (curSum >= threshold) {
                    res++;
                }
                curSum -= arr[R - k + 1];
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

> Where $n$ is the size of the array $arr$ and $k$ is the size of the sub-array.

## Standalone solution file (`cpp/1343-number-of-sub-arrays-of-size-k-and-average-greater-than-or-equal-to-threshold.cpp` in the NeetCode repo)

```cpp
/*
Using Sliding window.
First we calculate sum of first k elements in vector then we check if the average is greater than or equal to the threshold.
If the condition is met then we append the res variable.
Then we maintain the k size window and traverse over the vector and check for the condition.

Since we are traversing only once
T.C -> O(N)
S.c -> O(1)
*/
class Solution {
public:
    int numOfSubarrays(vector<int>& arr, int k, int threshold) {
        int sum = 0;
        int n = arr.size();
        for(int i=0;i<k;i++){
            sum += arr[i];
        }
        int left = 0;
        int right = k;
        int res = 0;
        if(sum/k >= threshold) res++;
        while(right < n){
            sum -= arr[left++];
            sum += arr[right++];
            if(sum/k >= threshold) res++;
        }
        return res;
    }
};
```
