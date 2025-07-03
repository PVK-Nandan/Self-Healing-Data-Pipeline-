from typing import Dict
from detector import DataDetector
from repair_engine import RepairEngine

class SelfHealingPipeline:
    def __init__(self):
        self.detector = DataDetector()
        self.repair_engine = RepairEngine()
    
    def process(self, data: Dict) -> Dict:
        print(f"\nProcessing data: {data}")
        
        # Step 1: Detect issues
        issues = self.detector.detect_issues(data)
        if not issues:
            print("✅ Data is valid")
            return data
            
        print("❌ Issues found:")
        for issue in issues:
            print(f"- {issue['message']}")
        
        # Step 2: Generate fixes
        fixes = self.repair_engine.generate_fixes(data, issues)
        if not fixes:
            print("⚠️ No fixes could be generated")
            return data
            
        print("\n🔧 Suggested fixes:")
        for field, fix in fixes.items():
            print(f"- {field}: {data.get(field)} → {fix}")
        
        # Step 3: Apply fixes
        repaired_data = {**data, **fixes}
        
        # Step 4: Verify fixes
        remaining_issues = self.detector.detect_issues(repaired_data)
        if remaining_issues:
            print("\n❌ Some issues remain after repair:")
            for issue in remaining_issues:
                print(f"- {issue['message']}")
        else:
            print("\n✅ All issues resolved!")
        
        return repaired_data