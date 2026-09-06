# 380. Insert Delete Get Random O(1)

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/insert-delete-getrandom-o1/>  
- **NeetCode:** <https://neetcode.io/problems/insert-delete-getrandom-o1>  
- **Video:** <https://www.youtube.com/watch?v=j4KwhBziOpg>  

[← Back to index](../INDEX.md)

## 1. Hash Map

A hash map provides O(1) average time for insert and delete operations, making it a natural choice for the first two requirements. However, hash maps don't support random access by index.
For `getRandom()`, we need to pick a random element, but iterating to a random position takes O(n) time. We convert the keys to a list and pick a random index.
This approach sacrifices `getRandom()` performance to keep the implementation simple.

```cpp
class RandomizedSet {
private:
    unordered_map<int, int> numMap;
    int size;

public:
    RandomizedSet() : size(0) {}

    bool insert(int val) {
        if (numMap.count(val)) return false;
        numMap[val] = 1;
        size++;
        return true;
    }

    bool remove(int val) {
        if (!numMap.count(val)) return false;
        numMap.erase(val);
        size--;
        return true;
    }

    int getRandom() {
        int idx = rand() % size;
        auto it = numMap.begin();
        advance(it, idx);
        return it->first;
    }
};
```

**Complexity**

- Time complexity: $O(n)$ for $getRandom()$, $O(1)$ for other function calls.
- Space complexity: $O(n)$

## 2. Hash Map + List

To achieve O(1) for all operations including `getRandom()`, we combine a hash map with a dynamic array. The array stores the actual values and allows random access, while the hash map stores each value's index in the array for fast lookups.
The tricky part is deletion: removing from the middle of an array is O(n). We solve this by swapping the element to delete with the last element, then removing from the end in O(1) time.
This swap-and-pop technique is a common pattern for O(1) deletion from unordered collections.

```cpp
class RandomizedSet {
private:
    unordered_map<int, int> numMap;
    vector<int> nums;

public:
    RandomizedSet() {}

    bool insert(int val) {
        if (numMap.count(val)) return false;
        numMap[val] = nums.size();
        nums.push_back(val);
        return true;
    }

    bool remove(int val) {
        if (!numMap.count(val)) return false;
        int idx = numMap[val];
        int last = nums.back();
        nums[idx] = last;
        numMap[last] = idx;
        nums.pop_back();
        numMap.erase(val);
        return true;
    }

    int getRandom() {
        return nums[rand() % nums.size()];
    }
};
```

**Complexity**

- Time complexity: $O(1)$ for each function call.
- Space complexity: $O(n)$

## Standalone solution file (`cpp/0380-insert-delete-getrandom-o1.cpp` in the NeetCode repo)

```cpp
class RandomizedSet {
public:

    unordered_map<int,int> indices;
    vector<int> values;
    RandomizedSet() {
    }
    
    bool insert(int val) {

        if(indices.find(val)==indices.end()){
            values.push_back(val);
            // store the index of that value
            indices[val] = values.size() -1;
            return true;
        }
        return false;
    }
    
    bool remove(int val) {

       if(indices.find(val)==indices.end()){
           return false;
       }

        // find index of the value
        int idx = indices[val];
        // get the last value in the vector
        // and change its index to curr val's index
        indices[values[values.size()-1]] = idx;

        // replace curr vals index with last 
        // last value
        values[idx] = values[values.size()-1];

        // so now the curr val is removed from the
        // vector replaced by last value and so 
        // we could just remove last value 
        values.pop_back();

        // also erase it from the hash map
        indices.erase(val);
        return true;
    }
    
    int getRandom() {
        return values[rand()%values.size()];
    }
};

/**
 * Your RandomizedSet object will be instantiated and called as such:
 * RandomizedSet* obj = new RandomizedSet();
 * bool param_1 = obj->insert(val);
 * bool param_2 = obj->remove(val);
 * int param_3 = obj->getRandom();
 */
```
