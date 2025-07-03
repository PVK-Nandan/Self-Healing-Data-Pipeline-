from typing import Dict, List
from validation_rules import VALIDATION_RULES

class RepairEngine:
    def __init__(self):
        self.rules = VALIDATION_RULES

    def generate_fixes(self, data: Dict, issues: List[Dict]) -> Dict:
        fixes = {}
        
        for issue in issues:
            field = issue["field"]
            error_type = issue["error"]
            current_value = data.get(field)
            
            # Find matching rule
            rule = next((r for r in self.rules if r["field"] == field), None)
            if not rule:
                continue
                
            # Apply fix strategies
            for strategy in rule.get("fix_strategies", []):
                if self._should_apply_strategy(strategy, error_type, current_value, rule):
                    fixes[field] = self._apply_strategy(strategy, current_value)
                    break
        
        return fixes
    
    def _should_apply_strategy(self, strategy, error_type, value, rule):
        if "match" in strategy:
            return error_type == strategy["match"]
        elif "condition" in strategy:
            if strategy["condition"] == "value < min":
                return value < rule["min"]
            elif strategy["condition"] == "value > max":
                return value > rule["max"]
        return False
    
    def _apply_strategy(self, strategy, value):
        action = strategy["action"]
        
        if action == "insert":
            position = strategy.get("position", -1)
            char = strategy.get("value", "@")
            if position == -1:
                return f"{value}{char}"
            else:
                return f"{value[:position]}{char}{value[position:]}"
                
        elif action == "append":
            return f"{value}{strategy['value']}"
            
        elif action == "set":
            return strategy["value"]
            
        return value