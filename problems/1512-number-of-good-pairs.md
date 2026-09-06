# 1512. Number of Good Pairs

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/number-of-good-pairs/>  
- **NeetCode:** <https://neetcode.io/problems/number-of-good-pairs>  
- **Video:** <https://www.youtube.com/watch?v=BqhDFUo1rjs>  

[← Back to index](../INDEX.md)

## 1. Brute Force

A good pair is defined as a pair `(i, j)` where `i < j` and `nums[i] == nums[j]`. The simplest approach is to check every possible pair of indices and count those that satisfy both conditions.

```cpp
class Solution {
public:
    int numIdenticalPairs(vector<int>& nums) {
        int res = 0;
        for (int i = 0; i < nums.size(); i++) {
            for (int j = i + 1; j < nums.size(); j++) {
                if (nums[i] == nums[j]) {
                    res++;
                }
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 2. Hash Map (Math)

If a value appears `c` times, the number of good pairs using that value equals the number of ways to choose 2 indices from `c` positions, which is `c * (c - 1) / 2`. We can count frequencies first, then sum up the pairs for each value.

```cpp
class Solution {
public:
    int numIdenticalPairs(vector<int>& nums) {
        unordered_map<int, int> count;
        int res = 0;
        for (int num : nums) {
            count[num]++;
        }
        for (auto& [num, c] : count) {
            res += c * (c - 1) / 2;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Hash Map

Instead of counting all frequencies first and then computing pairs, we can count pairs on the fly. As we traverse the array, each new occurrence of a value can form a good pair with every previous occurrence of that same value. We track the count of each value seen so far and add it to the `res` before updating the count.

```cpp
class Solution {
public:
    int numIdenticalPairs(vector<int>& nums) {
        unordered_map<int, int> count;
        int res = 0;
        for (int num : nums) {
            res += count[num];
            count[num]++;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/1512-number-of-good-pairs.cpp` in the NeetCode repo)

```cpp
class Solution { 
        unordered_map<int, int> Memo = {};    
        int numIdenticalPairs(vector<int> & nums){            
            unordered_map<int, int> Memo;            
            int i, k;            
            int NGood;            
            NGood = 0;            
            Memo = {};            
            for(int & i : nums){                
                if(Memo.find(i) == Memo.end()){                    
                    Memo.insert(make_pair(i, 1));                
                }
                else{                    
                    NGood = NGood + Memo[i];                    
                    Memo[i]++;                    
                }                
            }            
            return NGood;            
        }    
};
```
