# Create rules
rule1 = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
rule2 = "((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)"

# Parse the rules into ASTs
ast1 = parse_rule(rule1)
ast2 = parse_rule(rule2)

# Combine rules
combined_ast = combine_rules([rule1, rule2])

# Test evaluation
user_data1 = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}
user_data2 = {"age": 22, "department": "Marketing", "salary": 45000, "experience": 4}

print(f"Evaluation for user_data1: {evaluate_rule(combined_ast, user_data1)}")  # Should be True
print(f"Evaluation for user_data2: {evaluate_rule(combined_ast, user_data2)}")  # Should be False
