# 605. Can Place Flowers

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/can-place-flowers/>  
- **NeetCode:** <https://neetcode.io/problems/can-place-flowers>  
- **Video:** <https://www.youtube.com/watch?v=ZGxqqjljpUI>  
- **Video approach:** 2. Iteration - II (auto-matched)  

[← Back to index](../INDEX.md)

## 1. Iteration - I

A flower can be planted at position `i` only if positions `i-1`, `i`, and `i+1` are all empty. To handle edge cases at the boundaries, we pad the flowerbed with zeros at both ends. This way, we can apply the same rule uniformly across all positions without special boundary checks.

```cpp
class Solution {
public:
    bool canPlaceFlowers(vector<int>& flowerbed, int n) {
        vector<int> f(flowerbed.size() + 2, 0);
        for (int i = 0; i < flowerbed.size(); i++) {
            f[i + 1] = flowerbed[i];
        }

        for (int i = 1; i < f.size() - 1; i++) {
            if (f[i - 1] == 0 && f[i] == 0 && f[i + 1] == 0) {
                f[i] = 1;
                n--;
            }
        }
        return n <= 0;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Iteration - II ▶ video

Instead of checking each position individually, we can count consecutive empty plots between flowers. For a sequence of `k` empty plots between two flowers, we can plant `(k-1)/2` flowers. At the beginning and end of the flowerbed, the formula differs slightly since there is no blocking flower on one side: we can plant `k/2` flowers at the edges.

```cpp
class Solution {
public:
    bool canPlaceFlowers(vector<int>& flowerbed, int n) {
        int empty = flowerbed[0] == 0 ? 1 : 0;

        for (int f : flowerbed) {
            if (f == 1) {
                n -= (empty - 1) / 2;
                empty = 0;
            } else {
                empty++;
            }
        }

        n -= empty / 2;
        return n <= 0;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0605-can-place-flowers.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    bool canPlaceFlowers(vector<int>& flowerbed, int n) {
        // pre-check, if n is 0 ... return true
        if(n == 0){
            return true;
        }
        
        // add a zero to the front and end of FB
        flowerbed.insert (flowerbed.begin(),0);
        flowerbed.push_back(0);

        // iterate through vector (1, vector -1) (for)
        //  if prev, curr, and next are 0
        //      plant flower (1)
        //      decrement n
        for(int i = 1; i < flowerbed.size() - 1; i++){
            if (flowerbed[i - 1] == 0 && flowerbed[i] == 0 && flowerbed[i+1] == 0){
                flowerbed[i] = 1;
                n--;
            }
            if (n == 0){
                return true;
            }

        }

        // return false as else
        return false;

    }
};
```
