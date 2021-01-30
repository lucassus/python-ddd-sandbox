def camelize(str: str) -> str:
    return "".join(
        [
            char.upper() if str[i - 1] == "_" else char
            for i, char in enumerate(str)
            if char != "_"
        ]
    )
