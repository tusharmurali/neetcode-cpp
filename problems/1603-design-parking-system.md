# 1603. Design Parking System

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/design-parking-system/>  
- **NeetCode:** <https://neetcode.io/problems/design-parking-system>  
- **Video:** <https://www.youtube.com/watch?v=d5zCHesOrSk>  

[← Back to index](../INDEX.md)

## 1. Array - I

A parking lot has a fixed number of spaces for each car size (big, medium, small). We can represent the available slots using an array of three integers. Since car types are numbered `1`, `2`, and `3`, we map them to array indices `0`, `1`, and `2` by subtracting `1`. When a car arrives, we check if there is room for its type. If so, we decrement the count and allow parking; otherwise, we reject it.

```cpp
class ParkingSystem {
    int spaces[3];

public:
    ParkingSystem(int big, int medium, int small) {
        spaces[0] = big;
        spaces[1] = medium;
        spaces[2] = small;
    }

    bool addCar(int carType) {
        if (spaces[carType - 1] > 0) {
            spaces[carType - 1]--;
            return true;
        }
        return false;
    }
};
```

**Complexity**

- Time complexity:
    - $O(1)$ time for initialization.
    - $O(1)$ time for each $addCar()$ function call.
- Space complexity: $O(1)$

## 2. Array - II

This is a more concise version of the array approach. Instead of checking before decrementing, we decrement first and then check if the result is non-negative. The logic works because if there were no available slots, the count becomes negative, which we use to indicate failure. This allows the check and update to happen in a single expression.

```cpp
class ParkingSystem {
    int spaces[3];

public:
    ParkingSystem(int big, int medium, int small) {
        spaces[0] = big, spaces[1] = medium, spaces[2] = small;
    }

    bool addCar(int carType) {
        return spaces[carType - 1]-- > 0;
    }
};
```

**Complexity**

- Time complexity:
    - $O(1)$ time for initialization.
    - $O(1)$ time for each $addCar()$ function call.
- Space complexity: $O(1)$

## Standalone solution file (`cpp/1603-design-parking-system.cpp` in the NeetCode repo)

```cpp
class ParkingSystem {
public:
    ParkingSystem(int big, int medium, int small) : mCarSpotsLeft{big, medium, small} {}
    
    bool addCar(int carType) {
        if (mCarSpotsLeft[carType - 1] > 0) {
            mCarSpotsLeft[carType - 1]--;
            return true;
        } else {
            return false;
        }
    }

private:
    array<int, 3> mCarSpotsLeft;
};
```
