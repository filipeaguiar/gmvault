import yaml
def dump_yaml_indented(data, indent=2):
    if not data:
        return "[]" if isinstance(data, list) else "{}"
    yaml_str = yaml.dump(data, default_flow_style=False, sort_keys=False, allow_unicode=True)
    prefix = " " * indent
    return "\n" + "\n".join(prefix + line for line in yaml_str.splitlines())

data = {"acrobatics": {"bonus": 3}}
res = f"  skills: {dump_yaml_indented(data, 4).lstrip(chr(10) + ' ')}"
print(res)

res2 = f"  skills:{dump_yaml_indented(data, 4)}"
print("---")
print(res2)
