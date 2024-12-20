def threeSum(nums):
    nums.sort()  # Sort the array in ascending order
    result = []
    
    for i in range(len(nums)-2):
        if i > 0 and nums[i] == nums[i-1]:
            continue  # Skip duplicates
        
        left = i + 1
        right = len(nums) - 1
        
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            
            if total < 0:
                left += 1
            elif total > 0:
                right -= 1
            else:
                result.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left] == nums[left+1]:
                    left += 1  # Skip duplicates
                while left < right and nums[right] == nums[right-1]:
                    right -= 1  # Skip duplicates
                left += 1
                right -= 1
    
    return result

# Test the function
nums = [-1, 0, 1, 2, -1, -4]
print(threeSum(nums))