# 1899. Merge Triplets to Form Target Triplet

- **Difficulty:** Medium  
- **Pattern:** Greedy  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/merge-triplets-to-form-target-triplet/>  
- **NeetCode:** <https://neetcode.io/problems/merge-triplets-to-form-target>  
- **Video:** <https://www.youtube.com/watch?v=kShkQLQZ9K4>  
- **Video approach:** 1. Greedy  

[← Back to index](../INDEX.md)

## 1. Greedy ▶ video

We are given several triplets and a target triplet.
We can merge triplets by taking the **maximum value at each index**, and we want to know if it is possible to obtain the target exactly.

A key observation is:

- any triplet that has a value **greater than the target at any index** can never be used, because merging only increases values
- so such triplets should be ignored

For the remaining valid triplets:

- if a triplet matches the target at a certain index, it can help us reach that target value at that position

If we can find triplets that collectively cover **all three indices** of the target, then merging them will produce the target.

```cpp
class Solution {
public:
    bool mergeTriplets(vector<vector<int>>& triplets, vector<int>& target) {
        unordered_set<int> good;

        for (const auto& t : triplets) {
            if (t[0] > target[0] || t[1] > target[1] || t[2] > target[2]) {
                continue;
            }
            for (int i = 0; i < t.size(); i++) {
                if (t[i] == target[i]) {
                    good.insert(i);
                }
            }
        }
        return good.size() == 3;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 2. Greedy (Optimal)

We are given several triplets and a target triplet.
When we merge triplets, we take the **maximum value at each index**, so values can only **increase**, never decrease.

This leads to an important rule:

- Any triplet that has a value **greater than the target at any index** cannot be used to form the target.

Instead of collecting indices in a set, we can think more directly:

- To reach `target[0]`, we need **at least one triplet** where:
    - the first value equals `target[0]`
    - the other two values do not exceed the target
- Similarly for `target[1]` and `target[2]`

If we can independently satisfy all three positions using valid triplets, then merging those triplets will exactly form the target.

```cpp
class Solution {
public:
    bool mergeTriplets(vector<vector<int>>& triplets, vector<int>& target) {
        bool x = false, y = false, z = false;
        for (const auto& t : triplets) {
            x |= (t[0] == target[0] && t[1] <= target[1] && t[2] <= target[2]);
            y |= (t[0] <= target[0] && t[1] == target[1] && t[2] <= target[2]);
            z |= (t[0] <= target[0] && t[1] <= target[1] && t[2] == target[2]);
            if (x && y && z) return true;
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/1899-merge-triplets-to-form-target-triplet.cpp` in the NeetCode repo)

```cpp
/*
    Update: [max(ai,aj), max(bi,bj), max(ci,cj)], return if possible to obtain target
    Ex. triplets = [[2,5,3],[1,8,4],[1,7,5]] target = [2,7,5] -> true, update 1st/3rd

    Skip all "bad" triplets (can never become target), if match add to "good" set

    Time: O(n)
    Space: O(1)
*/

class Solution {
public:
    bool mergeTriplets(vector<vector<int>>& triplets, vector<int>& target) {
        unordered_set<int> s;
        
        for (int i = 0; i < triplets.size(); i++) {
            if (triplets[i][0] > target[0] || triplets[i][1] > target[1] || triplets[i][2] > target[2]) {
                continue;
            }
            
            for (int j = 0; j < 3; j++) {
                if (triplets[i][j] == target[j]) {
                    s.insert(j);
                }
            }
        }
        
        return s.size() == 3;
    }
};
```
