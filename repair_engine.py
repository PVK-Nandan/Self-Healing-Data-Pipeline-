from typing import Dict, List, Union
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
            
            rule = next((r for r in self.rules if r["field"] == field), None)
            if not rule:
                continue
                
            # Convert current_value to proper type for comparison
            try:
                if rule["type"] == "number" and current_value is not None:
                    current_value = int(current_value)
            except (ValueError, TypeError):
                continue
                
            for strategy in rule.get("fix_strategies", []):
                if self._should_apply_strategy(strategy, error_type, current_value, rule):
                    fixed_value = self._apply_strategy(strategy, current_value)
                    if fixed_value is not None:
                        fixes[field] = fixed_value
                    break
        
        return fixes
    
    def _should_apply_strategy(self, strategy: Dict, error_type: str, 
                             value: Union[str, int, None], rule: Dict) -> bool:
        try:
            if "match" in strategy:
                return error_type == strategy["match"]
            elif "condition" in strategy:
                if strategy["condition"] == "value < min":
                    return value is not None and value < rule["min"]
                elif strategy["condition"] == "value > max":
                    return value is not None and value > rule["max"]
            return False
        except (TypeError, KeyError):
            return False
    
    def _apply_strategy(self, strategy: Dict, value: Union[str, int, None]) -> Union[str, int, None]:
        try:
            action = strategy["action"]
            
            if action == "insert":
                position = strategy.get("position", -1)
                char = strategy.get("value", "@")
                if value is None:
                    return char
                if position == -1:
                    return f"{value}{char}"
                else:
                    return f"{value[:position]}{char}{value[position:]}"
                    
            elif action == "append":
                return f"{value}{strategy['value']}" if value is not None else strategy['value']
                
            elif action == "set":
                return strategy["value"]
                
            return value
        except (KeyError, TypeError):
            return None