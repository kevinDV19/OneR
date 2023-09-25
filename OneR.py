def fit(x_train, y_train):
    frequency_table = compute_frequency_table(x_train, y_train)
    rules, error_rates = compute_rules(frequency_table)
    attribute_min_error = find_attribute_with_min_error_rate(error_rates)
    rule = {attribute_min_error: rules[attribute_min_error]}
    return rule


def evaluate(rule, x_test, y_test):
    print("Evaluando conjunto de prueba ...")
    hits = 0
    attribute = list(rule.keys())[0]
    num_rows = x_test[attribute].shape[0]

    for i in range(num_rows):
        value = x_test[attribute].iloc[i].strip()
        expected_class = y_test.iloc[i]
        estimated_class = rule[attribute][value].strip()

        hits += 1 if expected_class == estimated_class else 0

        print('Instancia {}:'.format(i))
        print('Atributo: {}'.format(attribute))
        print('Valor: {}'.format(value))
        print('Clase Esperada: {}'.format(expected_class))
        print('Clase Estimada: {}'.format(estimated_class))
        print('¿Acierto?: {}\n'.format(expected_class == estimated_class))

    print("Done.")
    return hits


def compute_frequency_table(x_train, y_train):
    print("Calculando Tabla De Frecuencias ... ")

    frequency_tables = {}
    domain_classes = y_train.unique()

    for column_name in x_train.columns:
        frequency_table = {}
        value_class_tuples = zip(x_train[column_name], y_train)

        for value, expected_class in value_class_tuples:
            value = value.strip() if type(value) is str else value

            if value not in frequency_table.keys():
                frequency_table[value] = {}
                for class_name in domain_classes:
                    frequency_table[value][class_name] = 1  # Initialization with laplace correction

            frequency_table[value][expected_class] += 1

        frequency_tables[column_name] = frequency_table

    print("Done.")
    print("\n Tablas De Frecuencias:")
    for attribute, frequency_table in frequency_tables.items():
        print("Atributo:", attribute)
        print(frequency_table)

    return frequency_tables


def compute_rules(frequency_tables):
    print("Encontrando regla con tasa de error mínima ... ")
    rules = {}
    total_error_rate = {}
    
    for attribute, frequency_table in frequency_tables.items():
        total_error_numerator = 0
        total_error_denominator = 0
        rule = {}
        
        for value, class_counts in frequency_table.items():
            max_class = max(class_counts, key=class_counts.get)
            rule[value] = max_class
            
            total_error_numerator += sum(class_counts.values()) - class_counts[max_class]
            total_error_denominator += sum(class_counts.values())
        
        rules[attribute] = rule
        total_error_rate[attribute] = (total_error_numerator / total_error_denominator) * 100  # Convert to percentage

    print('Done.')
    print("\nReglas:")
    for attribute, rule in rules.items():
        print("Atributo:", attribute)
        print(rule)
    print("\nTasas de Error Total::")
    for attribute, error_rate in total_error_rate.items():
        print("Atributo:", attribute)
        print("{:.2f}%".format(error_rate))

    return rules, total_error_rate


def find_attribute_with_min_error_rate(error_rates):
    return min(error_rates, key=error_rates.get)


def print_rule(rule):
    attribute = list(rule.keys())[0].strip()
    print()
    print('Regla Final Obtenida:')
    print('{:^20}|{:^20}|{:^20}'.format('Atributo', 'Valor', 'Clase Estimada'))
    for attribute in rule:
        for value in rule[attribute]:
            print('{:^20}|{:^20}|{:^20}'.format(attribute, value, rule[attribute][value]))
    print()

# Ejemplo de uso:
# rule = fit(x_train, y_train)
# evaluate(rule, x_test, y_test)
