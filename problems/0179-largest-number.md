# 179. Largest Number

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/largest-number/>  
- **NeetCode:** <https://neetcode.io/problems/largest-number>  
- **Video:** <https://www.youtube.com/watch?v=WDx6Y4i4xJ8>  

[← Back to index](../INDEX.md)

## 1. Brute Force

To form the largest number, we need to decide the order of numbers such that when concatenated, they produce the maximum value. The key insight is that comparing two numbers `a` and `b` requires checking which concatenation is larger: `a + b` or `b + a`. For example, given `9` and `34`, we compare `"934"` vs `"349"` and pick the order that gives the larger result.

The brute force approach repeatedly finds the "best" number to place next by comparing all remaining numbers using this concatenation rule, then appends it to the result.

```cpp
class Solution {
public:
    string largestNumber(vector<int>& nums) {
        vector<string> arr;
        for (int num : nums) {
            arr.push_back(to_string(num));
        }

        string res;
        while (!arr.empty()) {
            int maxi = 0;
            for (int i = 1; i < arr.size(); i++) {
                if (arr[i] + arr[maxi] > arr[maxi] + arr[i]) {
                    maxi = i;
                }
            }
            res += arr[maxi];
            arr.erase(arr.begin() + maxi);
        }

        return res[0] == '0' ? "0" : res;
    }
};
```

**Complexity**

- Time complexity: $O(n * N)$
- Space complexity: $O(N)$

> Where $n$ is the size of the array $nums$ and $N$ is the total number of digits in the array $nums$.

## 2. Sorting

Instead of repeatedly scanning for the best number, we can use sorting with a custom comparator. The comparator determines the order by checking if `a + b > b + a`. By sorting the entire array once using this rule, numbers naturally arrange themselves so that their concatenation yields the largest possible value.

This approach is more efficient because sorting is faster than repeatedly finding and removing the maximum element.

```cpp
class Solution {
public:
    string largestNumber(vector<int>& nums) {
        vector<string> arr;
        for (int num : nums) {
            arr.push_back(to_string(num));
        }

        sort(arr.begin(), arr.end(), [](string& a, string& b) {
            return a + b > b + a;
        });

        string res;
        for (string& num : arr) {
            res += num;
        }

        return res[0] == '0' ? "0" : res;
    }
};
```

**Complexity**

- Time complexity: $O(N \log N)$
- Space complexity: $O(N)$

> Where $N$ is the total number of digits in the array $nums$.

## Standalone solution file (`cpp/0179-largest-number.cpp` in the NeetCode repo)

```cpp
class Solution {
public:

    // to check which should come first
    // see that by adding in which way gives bigger number
    static bool mysort(string a, string b){
        return a+b > b+a;
    }
    string largestNumber(vector<int>& nums) {
        string s = "";
        vector<string> all_numbers;
        
        // convert every number to string
        for(int it: nums){
            all_numbers.push_back(to_string(it));
        }

        // sort accoring to custom sort function
        sort(all_numbers.begin(),all_numbers.end(),mysort);
        if(all_numbers[0]=="0"){
            return "0";
        }
        
        for(string a: all_numbers){
            s += a;
        }
        return s;
    }
};
```
