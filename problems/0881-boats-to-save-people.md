# 881. Boats to Save People

- **Difficulty:** Medium  
- **Pattern:** Two Pointers  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/boats-to-save-people/>  
- **NeetCode:** <https://neetcode.io/problems/boats-to-save-people>  
- **Video:** <https://www.youtube.com/watch?v=XbaxWuHIWUs>  
- **Video approach:** 1. Sorting + Two Pointers  

[← Back to index](../INDEX.md)

## 1. Sorting + Two Pointers ▶ video

Since each boat can carry at most two people and has a weight limit, we want to pair the heaviest person with the lightest person when possible. By sorting the weights, we can use two pointers: one at the heaviest person and one at the lightest. If they can share a boat, we move both pointers; otherwise, the heaviest person takes a boat alone.

```cpp
class Solution {
public:
    int numRescueBoats(vector<int>& people, int limit) {
        sort(people.begin(), people.end());
        int res = 0, l = 0, r = people.size() - 1;
        while (l <= r) {
            int remain = limit - people[r--];
            res++;
            if (l <= r && remain >= people[l]) {
                l++;
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 2. Counting Sort

When the range of weights is limited, counting sort can be faster than comparison-based sorting. We count the frequency of each weight, then reconstruct the sorted array. After sorting, we apply the same two-pointer greedy strategy as before.

```cpp
class Solution {
public:
    int numRescueBoats(vector<int>& people, int limit) {
        int m = *max_element(people.begin(), people.end());
        vector<int> count(m + 1, 0);
        for (int p : people) {
            count[p]++;
        }

        int idx = 0, i = 1;
        while (idx < people.size()) {
            while (count[i] == 0) {
                i++;
            }
            people[idx++] = i;
            count[i]--;
        }

        int res = 0, l = 0, r = people.size() - 1;
        while (l <= r) {
            int remain = limit - people[r--];
            res++;
            if (l <= r && remain >= people[l]) {
                l++;
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(m)$

> Where $n$ is the size of the input array and $m$ is the maximum value in the array.

## Standalone solution file (`cpp/0881-boats-to-save-people.cpp` in the NeetCode repo)

```cpp
/*
    Given an array of people's weight, people[i] is the weight of the ith person, 
    and there is an infinite number of boats where each boat can carry a maximum weight of limit. 
    Each boat carries at most two people at the same time, provided the sum of the weight of those people is at most limit.
    Return minimum number of boats to carry every given person.

    sort, while there is people to carry 
    carry the heaviest and lightest person provided their weight doesn't exceed limit.
    otherwise, carry the heaviest person only

    Time: O(n)
    Space: O(1)
*/

class Solution {
public:
    int numRescueBoats(vector<int>& people, int limit) {
        sort(people.begin(), people.end());
        
        int boatRequired = 0;
        int lightestPerson = 0;
        int heaviestPerson = people.size()-1;

        //WHILE THERE IS SOMEONE TO CARRY
        while (lightestPerson <= heaviestPerson){
            if(people[lightestPerson] + people[heaviestPerson] <= limit){
                --heaviestPerson;
                ++lightestPerson;
            }
            else{
                --heaviestPerson;
            }
            ++boatRequired;
        }

        return boatRequired;
    }
};
```
