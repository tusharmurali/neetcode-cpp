# 604. Design Compressed String Iterator

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/design-compressed-string-iterator/>  
- **NeetCode:** <https://neetcode.io/problems/design-compressed-string-iterator>  

[← Back to index](../INDEX.md)

## 1. Uncompressing the String (Time Limit Exceeded)

The most straightforward approach is to fully decompress the string during initialization. We parse each character-count pair and append the character that many times to a result array. Then iteration simply walks through this precomputed array. This is easy to implement but can use excessive memory and time when counts are very large.

```cpp
class StringIterator {
public:
    string res;
    int ptr;
    
    StringIterator(string compressedString) {
        res = "";
        ptr = 0;
        
        int i = 0;
        while (i < compressedString.length()) {
            char ch = compressedString[i++];
            int num = 0;
            while (i < compressedString.length() && isdigit(compressedString[i])) {
                num = num * 10 + compressedString[i] - '0';
                i++;
            }
            
            for (int j = 0; j < num; j++)
                res += ch;
        }
    }
    
    char next() {
        if (!hasNext())
            return ' ';
        
        return res[ptr++];
    }
    
    bool hasNext() {
        return ptr != res.length();
    }
};
```

**Complexity**

- We precompute the elements of the uncompressed string. Thus, the space required in this case is $O(m)$, where $m$ refers to the length of the uncompressed string.

- The time required for precomputation is $O(m)$ since we need to generate the uncompressed string of length $m$.

- Once the precomputation has been done, the time required for performing `next()` and `hasNext()` is $O(1)$ for both.

- This approach can be easily extended to include `previous()`, `last()` and `find()` operations. All these operations require the use of an index only and thus, take $O(1)$ time. Operations like `hasPrevious()` can also be easily included.

- Since once the precomputation has been done, `next()` requires $O(1)$ time, this approach is useful if `next()` operation needs to be performed a large number of times. However, if `hasNext()` is performed most of the times, this approach isn't much advantageous since precomputation needs to be done anyhow.

- A potential problem with this approach could arise if the length of the uncompressed string is very large. In such a case, the size of the complete uncompressed string could become so large that it can't fit in the memory limits, leading to memory overflow.

>  Where $m$ is the length of the **uncompressed** string.

## 2. Pre-Computation

Instead of fully decompressing, we can store the compressed representation more efficiently by separating characters and their counts into parallel arrays. During iteration, we track which character group we're in and how many of that character remain. When a count reaches zero, we move to the next group. This uses space proportional to the compressed string rather than the decompressed length.

```cpp
class StringIterator {
public:
    int ptr = 0;
    vector<char> chars;
    vector<int> nums;
    
    StringIterator(string compressedString) {
        for (int i = 0; i < compressedString.length(); i++) {
            if (isalpha(compressedString[i])) {
                chars.push_back(compressedString[i]);
                int num = 0;
                i++;
                while (i < compressedString.length() && isdigit(compressedString[i])) {
                    num = num * 10 + (compressedString[i] - '0');
                    i++;
                }
                nums.push_back(num);
                i--;
            }
        }
    }
    
    char next() {
        if (!hasNext())
            return ' ';
        
        nums[ptr]--;
        char res = chars[ptr];
        
        if (nums[ptr] == 0)
            ptr++;
        
        return res;
    }
    
    bool hasNext() {
        return ptr != chars.size();
    }
};
```

**Complexity**

- The space required for storing the results of the precomputation is $O(n)$, where $n$ refers to the length of the compressed string. The $nums$ and $chars$ array contain a total of $n$ elements.

- The precomputation step requires $O(n)$ time. Thus, if `hasNext()` operation is performed most of the times, this precomputation turns out to be non-advantageous.

- Once the precomputation has been done, `hasNext()` and `next()` require $O(1)$ time.

- This approach can be extended to include the `previous()` and `hasPrevious()` operations, but that would require making some simple modifications to the current implementation.

>  Where $n$ is the length of the **compressed** string.

## 3. Demand-Computation

The most space-efficient approach avoids any preprocessing. We store the original compressed string and parse it lazily as we iterate. We keep track of the current character and how many times it should still be returned. When that count reaches zero, we parse the next character-count pair from the string on demand.

```cpp
class StringIterator {
public:
    string res;
    int ptr = 0, num = 0;
    char ch = ' ';
    
    StringIterator(string compressedString) {
        res = compressedString;
    }
    
    char next() {
        if (!hasNext())
            return ' ';

        if (num == 0) {
            ch = res[ptr++];
            while (ptr < res.length() && isdigit(res[ptr])) {
                num = num * 10 + (res[ptr++] - '0');
            }
        }
        
        num--;
        return ch;
    }
    
    bool hasNext() {
        return ptr != res.length() || num != 0;
    }
};
```

**Complexity**

- Since no precomputation is done, constant space is required in this case.

- The time required to perform `next()` operation is $O(1)$.

- The time required for `hasNext()` operation is $O(1)$.

- Since no precomputations are done, and `hasNext()` requires only $O(1)$ time, this solution is advantageous if `hasNext()` operation is performed most of the times.

- This approach can be extended to include `previous()` and `hasPrevious()` operations, but this will require the use of some additional variables.
