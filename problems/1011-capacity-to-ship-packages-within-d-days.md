# 1011. Capacity to Ship Packages Within D Days

- **Difficulty:** Medium  
- **Pattern:** Binary Search  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/>  
- **NeetCode:** <https://neetcode.io/problems/capacity-to-ship-packages-within-d-days>  
- **Video:** <https://www.youtube.com/watch?v=ER_oLmdc-nw>  
- **Video approach:** 2. Binary Search  

[← Back to index](../INDEX.md)

## 1. Linear Search

The minimum possible ship capacity must be at least as large as the heaviest package (otherwise that package could never be shipped). Starting from this minimum value, we can try each capacity one by one, simulating the shipping process to see if all packages can be delivered within the given number of days. The first capacity that works is our answer.

```cpp
class Solution {
public:
    int shipWithinDays(vector<int>& weights, int days) {
        int res = *max_element(weights.begin(), weights.end());
        while (true) {
            int ships = 1, cap = res;
            for (int w : weights) {
                if (cap - w < 0) {
                    ships++;
                    cap = res;
                }
                cap -= w;
            }
            if (ships <= days) {
                return res;
            }
            res++;
        }
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 2. Binary Search ▶ video

Instead of checking every capacity linearly, we can use binary search because the problem has a monotonic property: if a capacity works, any larger capacity will also work. The search space ranges from the maximum package weight (minimum valid capacity) to the sum of all weights (shipping everything in one day). For each mid-point capacity, we check if it allows shipping within the day limit and adjust our search accordingly.

```cpp
class Solution {
public:
    int shipWithinDays(vector<int>& weights, int days) {
        int l = *max_element(weights.begin(), weights.end());
        int r = accumulate(weights.begin(), weights.end(), 0);
        int res = r;

        while (l <= r) {
            int cap = (l + r) / 2;
            if (canShip(weights, days, cap)) {
                res = min(res, cap);
                r = cap - 1;
            } else {
                l = cap + 1;
            }
        }
        return res;
    }

private:
    bool canShip(const vector<int>& weights, int days, int cap) {
        int ships = 1, currCap = cap;
        for (int w : weights) {
            if (currCap - w < 0) {
                ships++;
                if (ships > days) {
                    return false;
                }
                currCap = cap;
            }
            currCap -= w;
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/1011-capacity-to-ship-packages-within-d-days.cpp` in the NeetCode repo)

```cpp
/*
    Shipping capacity at the least needs to be
    as much as the highest weight on the conveyor
    belt and at the maximum can be total of all 
    the weights on the conveyor belt. 

    
    Time Complexity -> O(nlogn)
    Space Complexity -> O(1)
*/
class Solution {
public:
    int shipWithinDays(vector<int>& weights, int days) {

        int high = 0;
        int low = 0;
        
        for (int i = 0; i < weights.size(); i++) {
            high += weights[i];
            low = max(low, weights[i]);
        }
        
        int answer = high;
        
        while (low <= high) {
            int mid = low + (high - low) / 2;

            if (canShipWithinDays(weights, days, mid)) {
                high = mid - 1;
                answer = min(answer, mid);
            } else low = mid + 1;
            
        }

        return answer;
    }

private:
    bool canShipWithinDays(vector<int>&weights, int days, int max) {
        int sum = 0;
        
        for (int i = 0; i < weights.size() - 1; i++) {
            sum += weights[i];
            
            if (sum + weights[i + 1] > max) {
                sum = 0;
                days--;
            }
        }

        return days > 0;
    }
};
```
