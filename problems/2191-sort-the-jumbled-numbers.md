# 2191. Sort the Jumbled Numbers

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/sort-the-jumbled-numbers/>  
- **NeetCode:** <https://neetcode.io/problems/sort-the-jumbled-numbers>  
- **Video:** <https://www.youtube.com/watch?v=rmkF2mxPoZM>  

[← Back to index](../INDEX.md)

## 1. Convert To Strings + Sorting

We need to sort numbers based on their "mapped" values, where each digit is replaced according to a mapping array. By converting each number to a string, we can easily iterate through its digits and build the mapped value. We store each mapped value along with the original index to preserve relative ordering for equal mapped values, then sort by the mapped values.

```cpp
class Solution {
public:
    vector<int> sortJumbled(vector<int>& mapping, vector<int>& nums) {
        vector<pair<int, int>> pairs;

        for (int i = 0; i < nums.size(); ++i) {
            string numStr = to_string(nums[i]);
            int mapped_n = 0;
            for (char c : numStr) {
                mapped_n = mapped_n * 10 + mapping[c - '0'];
            }
            pairs.push_back({mapped_n, i});
        }

        sort(pairs.begin(), pairs.end());

        vector<int> res;
        for (auto& p : pairs) {
            res.push_back(nums[p.second]);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 2. Iterate On Numbers + Sorting

Instead of converting numbers to strings, we can extract digits directly using arithmetic operations. We repeatedly take the last digit using modulo, map it, and accumulate the mapped value by multiplying by the appropriate power of 10. This avoids the overhead of string conversion while achieving the same result.

```cpp
class Solution {
public:
    vector<int> sortJumbled(vector<int>& mapping, vector<int>& nums) {
        vector<pair<int, int>> pairs;

        for (int i = 0; i < nums.size(); i++) {
            int mapped_n = 0, base = 1;
            int num = nums[i];

            if (num == 0) {
                mapped_n = mapping[0];
            } else {
                while (num > 0) {
                    int digit = num % 10;
                    num /= 10;
                    mapped_n += base * mapping[digit];
                    base *= 10;
                }
            }

            pairs.push_back({mapped_n, i});
        }

        sort(pairs.begin(), pairs.end());

        vector<int> res;
        for (auto& p : pairs) {
            res.push_back(nums[p.second]);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$
