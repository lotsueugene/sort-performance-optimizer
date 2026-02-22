"""
Sorting Assignment Starter Code
Implement five sorting algorithms and benchmark their performance.
"""

import json
import time
import random
import tracemalloc


# ============================================================================
# PART 1: SORTING IMPLEMENTATIONS
# ============================================================================

def bubble_sort(arr):

    arr_copy = arr.copy()
    for i in range(len(arr_copy)):
       
        swapped = False

        for j in range(0,len(arr_copy)-i-1):

            if arr_copy[j] > arr_copy[j+ 1]:

                temp = arr_copy[j]
                arr_copy[j] = arr_copy[j + 1]
                arr_copy[j+1]=temp

                swapped = True
            
        if not swapped:
            break

    return arr_copy


def selection_sort(arr):

    arr_copy = arr.copy()
    for step in range(len(arr_copy)):
        min = step

        for i in range(step + 1, len(arr_copy)):
            if  arr_copy[i] <  arr_copy[min]:
                min = i
        
        ( arr_copy[step],  arr_copy[min]) = ( arr_copy[min],  arr_copy[step])
    return arr_copy


def insertion_sort(arr):
    arr_copy = arr.copy()
    for step in range(1, len(arr_copy)):
        key = arr_copy[step]
        j = step - 1

        while j >= 0 and key < arr_copy[j]:
            arr_copy[j+ 1] = arr_copy[j]
            j = j -1

        arr_copy[j + 1] = key
    
    return arr_copy

        

def merge_sort(arr):
    arr_copy = arr.copy()

    # Base case
    if len(arr_copy) <= 1:
        return arr_copy

    r = len(arr_copy) // 2
    L = arr_copy[:r]
    M = arr_copy[r:]

 
    L = merge_sort(L)
    M = merge_sort(M)

    i = j = k = 0

    # Merge
    while i < len(L) and j < len(M):
        if L[i] < M[j]:
            arr_copy[k] = L[i]
            i += 1
        else:
            arr_copy[k] = M[j]
            j += 1
        k += 1

    # Remaining elements
    while i < len(L):
        arr_copy[k] = L[i]
        i += 1
        k += 1

    while j < len(M):
        arr_copy[k] = M[j]
        j += 1
        k += 1

    return arr_copy

# ============================================================================
# PART 2: STABILITY DEMONSTRATION
# ============================================================================

def demonstrate_stability():
    """
    Demonstrate which sorting algorithms are stable by sorting products by price.
    
    Creates a list of product dictionaries with prices and original order.
    Sorts by price and checks if products with same price maintain original order.
    
    Returns:
        dict: Results showing which algorithms preserved order for equal elements
    """
    # Sample products with duplicate prices
    products = [
        {"name": "Widget A", "price": 1999, "original_position": 0},
        {"name": "Gadget B", "price": 999, "original_position": 1},
        {"name": "Widget C", "price": 1999, "original_position": 2},
        {"name": "Tool D", "price": 999, "original_position": 3},
        {"name": "Widget E", "price": 1999, "original_position": 4},
    ]
    
    # TODO: Sort products by price using each algorithm
    # Hint: You'll need to modify your sorting functions to work with dictionaries
    # Hint: Or extract prices, sort them, and check if stable algorithms maintain original order
    # Hint: For stable sort: items with price 999 should stay in order (B before D)
    # Hint: For stable sort: items with price 1999 should stay in order (A before C before E)
    
    results = {
        "bubble_sort": "Not tested",
        "selection_sort": "Not tested", 
        "insertion_sort": "Not tested",
        "merge_sort": "Not tested"
    }
    
    # TODO: Test each algorithm and update results dictionary with "Stable" or "Unstable"
    
    return results


# ============================================================================
# PART 3: PERFORMANCE BENCHMARKING
# ============================================================================

def load_dataset(filename):
    """Load a dataset from JSON file."""
    with open(f"datasets/{filename}", "r") as f:
        return json.load(f)


def load_test_cases():
    """Load test cases for validation."""
    with open("datasets/test_cases.json", "r") as f:
        return json.load(f)


def test_sorting_correctness():
    """Test that sorting functions work correctly on small test cases."""
    print("="*70)
    print("TESTING SORTING CORRECTNESS")
    print("="*70 + "\n")
    
    test_cases = load_test_cases()
    
    test_names = ["small_random", "small_sorted", "small_reverse", "small_duplicates"]
    algorithms = {
        "Bubble Sort": bubble_sort,
        "Selection Sort": selection_sort,
        "Insertion Sort": insertion_sort,
        "Merge Sort": merge_sort
    }
    
    for test_name in test_names:
        print(f"Test: {test_name}")
        print(f"  Input:    {test_cases[test_name]}")
        print(f"  Expected: {test_cases['expected_sorted'][test_name]}")
        print()
        
        for algo_name, algo_func in algorithms.items():
            try:
                result = algo_func(test_cases[test_name].copy())
                expected = test_cases['expected_sorted'][test_name]
                status = "✓ PASS" if result == expected else "✗ FAIL"
                print(f"    {algo_name:20s}: {result} {status}")
            except Exception as e:
                print(f"    {algo_name:20s}: ERROR - {str(e)}")
        
        print()


def benchmark_algorithm(sort_func, data):
    """
    Benchmark a sorting algorithm on given data.
    
    Args:
        sort_func: The sorting function to test
        data: The dataset to sort (will be copied so original isn't modified)
    
    Returns:
        tuple: (execution_time_ms, peak_memory_kb)
    """
    # Copy data so we don't modify original
    data_copy = data.copy()
    
    # Start memory tracking
    tracemalloc.start()
    
    # Measure execution time
    start_time = time.perf_counter()
    sort_func(data_copy)
    end_time = time.perf_counter()
    
    # Get peak memory usage
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    execution_time_ms = (end_time - start_time) * 1000
    peak_memory_kb = peak / 1024
    
    return execution_time_ms, peak_memory_kb


def benchmark_all_datasets():
    """Benchmark all sorting algorithms on all datasets."""
    print("\n" + "="*70)
    print("BENCHMARKING SORTING ALGORITHMS")
    print("="*70 + "\n")
    
    datasets = {
        "orders.json": ("Order Processing Queue", 50000, 5000),
        "products.json": ("Product Catalog", 100000, 5000),
        "inventory.json": ("Inventory Reconciliation", 25000, 5000),
        "activity_log.json": ("Customer Activity Log", 75000, 5000)
    }
    
    algorithms = {
        "Bubble Sort": bubble_sort,
        "Selection Sort": selection_sort,
        "Insertion Sort": insertion_sort,
        "Merge Sort": merge_sort
    }
    
    for filename, (description, full_size, sample_size) in datasets.items():
        print(f"Dataset: {description} ({sample_size:,} element sample)")
        print("-" * 70)
        
        data = load_dataset(filename)
        # Use first sample_size elements for fair comparison
        data_sample = data[:sample_size]
        
        for algo_name, algo_func in algorithms.items():
            try:
                exec_time, memory = benchmark_algorithm(algo_func, data_sample)
                print(f"  {algo_name:20s}: {exec_time:8.2f} ms | {memory:8.2f} KB")
            except Exception as e:
                print(f"  {algo_name:20s}: ERROR - {str(e)}")
        
        print()


def analyze_stability():
    """Test and display which algorithms are stable."""
    print("="*70)
    print("STABILITY ANALYSIS")
    print("="*70 + "\n")
    
    print("Testing which algorithms preserve order of equal elements...\n")
    
    results = demonstrate_stability()
    
    for algo_name, stability in results.items():
        print(f"  {algo_name:20s}: {stability}")
    
    print()


if __name__ == "__main__":
    test_sorting_correctness()
    benchmark_all_datasets()
    analyze_stability()
