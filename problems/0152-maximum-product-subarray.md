# 152. Maximum Product Subarray

- **Difficulty:** Medium  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/maximum-product-subarray/>  
- **NeetCode:** <https://neetcode.io/problems/maximum-product-subarray>  
- **Video:** <https://www.youtube.com/watch?v=lXVy6YWFcRM>  
- **Video approach:** 3. Kadane's Algorithm  

[← Back to index](../INDEX.md)

## 1. Brute Force

A **subarray product** can change drastically because of:

- **Negative numbers** → can flip max to min and vice-versa
- **Zero** → resets the product

In brute force, we:

- Fix a starting index
- Keep multiplying elements to the right
- Track the maximum product seen

This works because every possible contiguous subarray is explicitly evaluated.

```cpp
class Solution {
public:
    int maxProduct(vector<int>& nums) {
        int res = nums[0];

        for (int i = 0; i < nums.size(); i++) {
            int cur = nums[i];
            res = max(res, cur);
            for (int j = i + 1; j < nums.size(); j++) {
                cur *= nums[j];
                res = max(res, cur);
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 2. Sliding Window

The maximum-product subarray problem is tricky because:

- A **negative** number flips the sign (a very small negative can become a very large positive after another negative).
- A **zero** breaks any product (anything crossing a zero becomes 0).

So we can treat the array as **separate segments split by zeros**.  
Inside one zero-free segment:

- If the count of negative numbers is **even**, the product of the whole segment is positive → usually the best.
- If the count is **odd**, we must **drop either the prefix up to the first negative** or **the suffix after the last negative** to make the remaining product have an even number of negatives.

This “sliding window” idea maintains a window that contains an allowed number of negatives (even), shrinking from the left when we exceed that.

```cpp
class Solution {
public:
    int maxProduct(vector<int>& nums) {
        vector<vector<int>> A;
        vector<int> cur;
        int res = INT_MIN;
        for (auto& num : nums) {
            res = max(res, num);
            if (num == 0) {
                if (!cur.empty()) A.push_back(cur);
                cur.clear();
            } else cur.push_back(num);
        }
        if (!cur.empty()) {
            A.push_back(cur);
        }

        for (auto& sub : A) {
            int negs = 0;
            for (auto& i : sub) {
                if (i < 0) negs++;
            }

            int prod = 1;
            int need = (negs % 2 == 0) ? negs : (negs - 1);
            negs = 0;
            for (int i = 0, j = 0; i < sub.size(); i++) {
                prod *= sub[i];
                if (sub[i] < 0) {
                    negs++;
                    while (negs > need) {
                        prod /= sub[j];
                        if (sub[j] < 0) negs--;
                        j++;
                    }
                }
                if (j <= i) res = max(res, prod);
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Kadane's Algorithm ▶ video

This is the **Kadane-style solution adapted for products**.

In the classic maximum-sum subarray, we only track one value (current max sum).  
For products, that’s **not enough** because:

- A **negative × negative = positive**
- A very small (negative) product can suddenly become the **maximum** after multiplying by another negative.

So at every index, we must track **two values**:

- `curMax`: maximum product ending at this index.
- `curMin`: minimum product ending at this index.

Why `curMin` matters:

- If the current number is negative, multiplying it with `curMin` might produce a new maximum.

Zeros are naturally handled because choosing `num` alone can reset the product.

```cpp
class Solution {
public:
    int maxProduct(vector<int>& nums) {
        int res = nums[0];
        int curMin = 1, curMax = 1;

        for (int num : nums) {
            int tmp = curMax * num;
            curMax = max(max(num * curMax, num * curMin), num);
            curMin = min(min(tmp, num * curMin), num);
            res = max(res, curMax);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 4. Prefix & Suffix

The key idea is that the **maximum product subarray must appear as either**:

- a **prefix product** of some segment, or
- a **suffix product** of some segment.

Why this works:

- Negative numbers flip signs. If a subarray has an **even number of negatives**, the full product is positive.
- If it has an **odd number of negatives**, removing either:
    - the prefix up to the first negative, or
    - the suffix after the last negative  
      will give the maximum product.
- Zeros break subarrays completely, so products must restart after a zero.

By scanning:

- once from **left to right** (prefix)
- once from **right to left** (suffix)

we implicitly consider all valid subarrays without explicitly tracking negatives.

The `(prefix or 1)` trick resets the product after encountering `0`.

```cpp
class Solution {
public:
    int maxProduct(vector<int>& nums) {
        int n = nums.size(), res = nums[0];
        int prefix = 0, suffix = 0;

        for (int i = 0; i < n; i++) {
            prefix = nums[i] * (prefix == 0 ? 1 : prefix);
            suffix = nums[n - 1 - i] * (suffix == 0 ? 1 : suffix);
            res = max(res, max(prefix, suffix));
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0152-maximum-product-subarray.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    int maxProduct(vector<int>& nums) {
        int res = nums[0];
        int curMin = 1, curMax = 1;
        
        for(int i = 0; i < nums.size(); i++)
        {
            int n = nums[i];
                
            int tmp = curMax * n;
            curMax = max(max(n * curMax, n * curMin), n);
            curMin = min(min(tmp, n * curMin), n);
            res = max(res, curMax);
        }
        
        return res;
    }
};
```
