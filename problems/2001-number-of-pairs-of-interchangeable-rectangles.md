# 2001. Number of Pairs of Interchangeable Rectangles

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/number-of-pairs-of-interchangeable-rectangles/>  
- **NeetCode:** <https://neetcode.io/problems/number-of-pairs-of-interchangeable-rectangles>  
- **Video:** <https://www.youtube.com/watch?v=lEQ8ZlLOuyQ>  
- **Video approach:** 2. Hash Map (Two Pass) (auto-matched)  

[← Back to index](../INDEX.md)

## 1. Brute Force

Two rectangles are interchangeable if they have the same aspect ratio (width divided by height). The simplest approach is to compare every pair of rectangles and check if their ratios match. For each pair where the ratios are equal, we count it as an interchangeable pair.

```cpp
class Solution {
public:
    long long interchangeableRectangles(vector<vector<int>>& rectangles) {
        long long res = 0;
        for (int i = 1; i < rectangles.size(); i++) {
            for (int j = 0; j < i; j++) {
                if ((double) rectangles[i][0] / rectangles[i][1] == (double) rectangles[j][0] / rectangles[j][1]) {
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

## 2. Hash Map (Two Pass) ▶ video

Instead of comparing every pair, we can group rectangles by their aspect ratio. Rectangles with the same ratio form a group, and any two rectangles in the same group are interchangeable. If a group has `c` rectangles, the number of pairs is `c * (c-1) / 2` (choosing 2 from `c`). We use a hash map to count how many rectangles share each ratio.

```cpp
class Solution {
public:
    long long interchangeableRectangles(vector<vector<int>>& rectangles) {
        unordered_map<double, int> count;
        for (const auto& rect : rectangles) {
            double ratio = (double) rect[0] / rect[1];
            count[ratio]++;
        }

        long long res = 0;
        for (const auto& [key, c] : count) {
            if (c > 1) {
                res += (c * 1LL * (c - 1)) / 2;
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Hash Map (One Pass)

We can optimize the two-pass approach into a single pass. As we process each rectangle, we check how many rectangles with the same ratio we have seen before. Each previously seen rectangle with the same ratio forms a new interchangeable pair with the current rectangle. This way, we count pairs incrementally as we go.

```cpp
class Solution {
public:
    long long interchangeableRectangles(vector<vector<int>>& rectangles) {
        unordered_map<double, int> count;
        long long res = 0;
        for (const auto& rect : rectangles) {
            double ratio = (double) rect[0] / rect[1];
            res += count[ratio];
            count[ratio]++;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Greatest Common Divisor

Using floating-point division for ratios can lead to precision issues with very large numbers. A more robust approach is to reduce each ratio to its simplest form using the greatest common divisor (`GCD`). Two rectangles have the same ratio if and only if their reduced forms are identical. We can pack the reduced width and height into a single integer key for efficient hashing.

```cpp
class Solution {
public:
    long long hash(int a, int b) {
        long long mask = a;
        mask |= ((long long)b << 31);
        return mask;
    }

    long long interchangeableRectangles(vector<vector<int>>& rectangles) {
        long long res = 0;
        unordered_map<long long, int> count;
        for (const auto& rect : rectangles) {
            int gcd = __gcd(rect[0], rect[1]);
            long long key = hash(rect[0] / gcd, rect[1] / gcd);
            res += count[key];
            count[key]++;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/2001-number-of-pairs-of-interchangeable-rectangles.cpp` in the NeetCode repo)

```cpp
/*
    Approach: 
    Keep the track of the ratios in a hash map
    
    Time complexity : O(n)
    Space complexity: O(n)

    n is number of rectangles
*/

class Solution {
public:
    long long interchangeableRectangles(vector<vector<int>>& rectangles) {
        
        map<long double,int> hash;
        long double ratio;

        long long answer=0;

        for(int i=0;i<rectangles.size();i++){
            ratio = (long double)(rectangles[i][0])/
                    (long double)(rectangles[i][1]);
            
            if(hash.find(ratio)!=hash.end()){
                hash[ratio]++;
            }
            else{
                hash[ratio] = 1;
            }
        }

        for(auto it:hash){
            answer+= (long long)(it.second)*(long long)(it.second-1)/2;
        }

        return answer;
    }
};
```
