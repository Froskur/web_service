# Хелперы для разных штук

def model_full_convert_to_dict(m):
    result = m.dict()
    for key, value in result.items():
        if hasattr(value, "dict"):
            m[key] = model_full_convert_to_dict(value)

    return result

