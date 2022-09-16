# Examples of String Formatting Syntax


# String Length
s = "Mathematics"
formatted = f"{s:$^{30}}" #fill 30 characters with s and then $ signs
print(formatted)

s = "wizardry"
formatted = f"{s: ^{20}}" #pad the beginning of string with spaces to fill 2
print(formatted)


# Decimal Formatting
n = 0.2343536654364236
s2 = f"{n:.2f}" #2 decimal places
print(s2)
