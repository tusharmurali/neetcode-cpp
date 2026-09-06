# 875. Koko Eating Bananas

- **Difficulty:** Medium  
- **Pattern:** Binary Search  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/koko-eating-bananas/>  
- **NeetCode:** <https://neetcode.io/problems/eating-bananas>  
- **Video:** <https://www.youtube.com/watch?v=U2SozAs9RzA>  
- **Video approach:** 2. Binary Search  

[← Back to index](../INDEX.md)

## 1. Brute Force

We try every possible eating speed starting from `1`.
For each speed, we simulate how many hours it would take to finish all piles.
The first speed that finishes within `h` hours is the answer.

```cpp
class Solution {
public:
    int minEatingSpeed(vector<int>& piles, int h) {
        int speed = 1;
        while (true) {
            long long totalTime = 0;
            for (int pile : piles) {
                totalTime += (pile + speed - 1) / speed;
            }

            if (totalTime <= h) {
                return speed;
            }
            speed++;
        }
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(1)$

> Where $n$ is the length of the input array $piles$ and $m$ is the maximum number of bananas in a pile.

## 2. Binary Search ▶ video

Instead of checking every speed one by one, we notice that the total time needed **decreases** as the eating speed increases.
This means the answer lies in a **sorted search space** from `1` to `max(piles)`.

Because the search space is ordered, we can use **binary search** to efficiently find the smallest speed that allows finishing the piles within `h` hours.

```cpp
class Solution {
public:
    int minEatingSpeed(vector<int>& piles, int h) {
        int l = 1;
        int r = *max_element(piles.begin(), piles.end());
        int res = r;

        while (l <= r) {
            int k = (l + r) / 2;

            long long totalTime = 0;
            for (int p : piles) {
                totalTime += ceil(static_cast<double>(p) / k);
            }
            if (totalTime <= h) {
                res = k;
                r = k - 1;
            } else {
                l = k + 1;
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * \log m)$
- Space complexity: $O(1)$

> Where $n$ is the length of the input array $piles$ and $m$ is the maximum number of bananas in a pile.

## Standalone solution file (`cpp/0875-koko-eating-bananas.cpp` in the NeetCode repo)

```cpp
/*
    Given array of banana piles, guards are gone for h hours
    Return min int k such that can eat all banans within h
    Ex. piles = [3,6,7,11] h = 8 -> 4 (1@3, 2@6, 2@7, 3@11)

    Binary search, for each k count hours needed, store min

    Time: O(n x log m) -> n = # of piles, m = max # in a pile
    Space: O(1)
*/

class Solution {
public:
    int minEatingSpeed(vector<int>& piles, int h) {
        int n = piles.size();
        
        int low = 1;
        int high = 0;
        for (int i = 0; i < n; i++) {
            high = max(high, piles[i]);
        }
        
        int result = high;
        
        while (low <= high) {
            int k = low + (high - low) / 2;
            long int hours = 0;
            for (int i = 0; i < n; i++) {
                hours += ceil((double) piles[i] / k);
            }
            if (hours <= h) {
                result = min(result, k);
                high = k - 1;
            } else {
                low = k + 1;
            }
        }
        
        return result;
    }
};
```
