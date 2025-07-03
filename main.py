import json
from pipeline import SelfHealingPipeline

def load_test_data(file_path="test_data.json"):
    with open(file_path) as f:
        return json.load(f)

def main():
    pipeline = SelfHealingPipeline()
    test_cases = load_test_data()
    
    for i, test_data in enumerate(test_cases, 1):
        print(f"\n=== Test Case {i} ===")
        result = pipeline.process(test_data)
        print("Final result:", result)

if __name__ == "__main__":
    main()