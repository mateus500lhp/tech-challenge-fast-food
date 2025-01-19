def is_cpf_valid(cpf: str) -> bool:
    """
    Valida se um CPF é válido (removendo caracteres não numéricos,
    checando length e dígitos verificadores).
    """
    # Remove caracteres não numéricos
    digits = "".join(c for c in cpf if c.isdigit())

    if len(digits) != 11:
        return False

    if digits == digits[0] * 11:
        return False

    # Cálculo do primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += int(digits[i]) * (10 - i)
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto

    # Cálculo do segundo dígito verificador
    soma = 0
    for i in range(10):
        soma += int(digits[i]) * (11 - i)
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto

    return (int(digits[9]) == digito1) and (int(digits[10]) == digito2)