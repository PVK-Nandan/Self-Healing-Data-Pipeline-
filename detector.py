import re
from typing import Dict, List
from validation_rules import VALIDATION_RULES

class DataDetector:
    def __init__(self, rules=None):
        self.rules = rules or VALIDATION_RULES

    def detect_issues(self, data: Dict) -> List[Dict]:
        issues = []
        
        for rule in self.rules:
            field = rule["field"]
            value = data.get(field)
            
            # Check required fields
            if rule.get("required") and value is None:
                issues.append({
                    "field": field,
                    "error": "missing_required_field",
                    "message": f"Missing required field: {field}"
                })
                continue
                
            # Skip validation if field is optional and not provided
            if value is None:
                continue
                
            # Type validation
            if rule["type"] == "number":
                if not str(value).isdigit():
                    issues.append({
                        "field": field,
                        "error": "invalid_number_format",
                        "message": f"Invalid number format for {field}"
                    })
                    continue
                    
                value = int(value)
                
                # Range validation
                if "min" in rule and value < rule["min"]:
                    issues.append({
                        "field": field,
                        "error": "value_below_minimum",
                        "message": f"{field} value {value} is below minimum {rule['min']}"
                    })
                    
                if "max" in rule and value > rule["max"]:
                    issues.append({
                        "field": field,
                        "error": "value_above_maximum",
                        "message": f"{field} value {value} is above maximum {rule['max']}"
                    })
                    
            elif rule["type"] == "string":
                if not isinstance(value, str):
                    issues.append({
                        "field": field,
                        "error": "invalid_string_format",
                        "message": f"Invalid string format for {field}"
                    })
                    continue
                    
                # Pattern validation
                if "pattern" in rule and not re.match(rule["pattern"], value):
                    issues.append({
                        "field": field,
                        "error": "pattern_mismatch",
                        "message": f"Invalid format for {field}"
                    })
        
        return issues