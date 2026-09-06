# 1921. Eliminate Maximum Number of Monsters

- **Difficulty:** Medium  
- **Pattern:** Greedy  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/eliminate-maximum-number-of-monsters/>  
- **NeetCode:** <https://neetcode.io/problems/eliminate-maximum-number-of-monsters>  
- **Video:** <https://www.youtube.com/watch?v=6QQRayzOTD4>  

[← Back to index](../INDEX.md)

## 1. Sorting

The weapon needs 1 minute to recharge after each shot. To maximize eliminations, we should prioritize monsters that will reach the city soonest. For each monster, we calculate the time it takes to arrive (`distance / speed`, rounded up). Sorting these arrival times lets us greedily eliminate monsters in order of urgency. If at any minute the earliest uneliminated monster has already arrived, the game ends.

```cpp
class Solution {
public:
    int eliminateMaximum(vector<int>& dist, vector<int>& speed) {
        int n = dist.size();
        vector<int> minReach(n);

        for (int i = 0; i < n; i++) {
            minReach[i] = ceil((double)dist[i] / speed[i]);
        }

        sort(minReach.begin(), minReach.end());

        int res = 0;
        for (int minute = 0; minute < n; minute++) {
            if (minute >= minReach[minute]) {
                return res;
            }
            res++;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 2. Sorting (Overwriting Input Array)

This is the same approach as above, but we save space by reusing the input `dist` array to store arrival times instead of creating a new array. The logic remains identical: compute arrival times, sort, and check if we can eliminate each monster before it arrives.

```cpp
class Solution {
public:
    int eliminateMaximum(vector<int>& dist, vector<int>& speed) {
        int n = dist.size();
        for (int i = 0; i < n; i++) {
            dist[i] = ceil((double)dist[i] / speed[i]);
        }

        sort(dist.begin(), dist.end());
        for (int minute = 0; minute < n; minute++) {
            if (minute >= dist[minute]) {
                return minute;
            }
        }

        return n;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 3. Min-Heap

Instead of sorting all arrival times upfront, we can use a min-heap to extract the minimum arrival time on demand. This still achieves the same goal of processing monsters in order of how soon they reach the city. We pop from the heap one at a time and check if the monster arrives before the current minute.

```cpp
class Solution {
public:
    int eliminateMaximum(vector<int>& dist, vector<int>& speed) {
        priority_queue<double, vector<double>, greater<double>> minHeap;
        for (int i = 0; i < dist.size(); i++) {
            minHeap.push((double)dist[i] / speed[i]);
        }

        int res = 0;
        while (!minHeap.empty()) {
            if (res >= minHeap.top()) {
                return res;
            }
            minHeap.pop();
            res++;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/1921-eliminate-maximum-number-of-monsters.cpp` in the NeetCode repo)

```cpp
/*
  You are playing a video game where you are defending your city from a group of n monsters. 
  You are given a 0-indexed integer array dist of size n, where dist[i] is the initial distance in kilometers of the ith monster from the city.
  The monsters walk toward the city at a constant speed. The speed of each monster is given to you in an integer array speed of size n, 
  where speed[i] is the speed of the ith monster in kilometers per minute.
  You have a weapon that, once fully charged, can eliminate a single monster. 
  However, the weapon takes one minute to charge.The weapon is fully charged at the very start.
  You lose when any monster reaches your city. If a monster reaches the city at the exact moment the weapon is fully charged, 
  it counts as a loss, and the game ends before you can use your weapon.
  
  Return the maximum number of monsters that you can eliminate before you lose, or n if you can eliminate all the monsters before they reach the city. 

  Ex. Input: dist = [1,3,4], speed = [1,1,1]
      Output: 3
      Explanation:
      In the beginning, the distances of the monsters are [1,3,4]. You eliminate the first monster.
      After a minute, the distances of the monsters are [X,2,3]. You eliminate the second monster.
      After a minute, the distances of the monsters are [X,X,2]. You eliminate the thrid monster.
      All 3 monsters can be eliminated.

  Time  : O(N)
  Space : O(N)
*/

class Solution {
public:
    int eliminateMaximum(vector<int>& dist, vector<int>& speed) {
        vector<float> v;
         
        for(int i = 0 ; i < dist.size() ; i++)
            v.push_back((float) dist[i] / speed[i]);
            
        sort(v.begin(), v.end());
        int count = 0;
        int time = 0, i = 0;
        while(i < v.size()) {
            if(time >= v[i])
                return count;
            ++count;
            time += 1;
            ++i;
        }
        return count;
    }
};
```
