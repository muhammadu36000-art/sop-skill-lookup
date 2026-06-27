#!/usr/bin/env python3
"""
SOP·技能速查工具 — HTML 手册生成脚本
用法：python generate.py <template.html> <output.html> <data.json>

data.json 格式：
{
  "sops": [ {id, area, areaLabel, areaClass, title, desc, keywords, chips, link, steps}, ... ],
  "skills": [ {name, cat, type, desc, use, triggers}, ... ]
}
"""

import sys, json, os, re

def escape_js_str(s):
    if s is None:
        return ""
    s = s.replace("\\", "\\\\")
    s = s.replace('"', '\\"')
    s = s.replace("\n", "\\n")
    s = s.replace("\r", "\\r")
    s = s.replace("\t", "\\t")
    return s

def val_to_js(v, indent=0):
    pad = " " * indent
    if isinstance(v, str):
        return f'"{escape_js_str(v)}"'
    elif isinstance(v, bool):
        return "true" if v else "false"
    elif isinstance(v, (int, float)):
        return str(v)
    elif isinstance(v, list):
        items = [val_to_js(x, indent + 2) for x in v]
        inner = ",\n".join(items)
        return f"[\n{pad}  {inner}\n{pad}]"
    elif isinstance(v, dict):
        lines = []
        for k, v2 in v.items():
            val = val_to_js(v2, indent + 2)
            lines.append(f"{pad}  {k}:{val}")
        inner = ",\n".join(lines)
        return f"{{\n{inner}\n{pad}}}"
    else:
        return '""'

def build_js_array(name, data):
    lines = [f"const {name} = ["]
    for item in data:
        lines.append("  {")
        for k, v in item.items():
            val = val_to_js(v, 2)
            lines.append(f"    {k}:{val},")
        lines.append("  },")
    lines.append("];")
    return "\n".join(lines)

def main():
    if len(sys.argv) < 4:
        print("Usage: python generate.py <template.html> <output.html> <data.json>")
        sys.exit(1)

    template_path = sys.argv[1]
    output_path = sys.argv[2]
    data_path = sys.argv[3]

    with open(template_path, "r", encoding="utf-8") as f:
        content = f.read()

    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    sops = data.get("sops", [])
    skills = data.get("skills", [])

    print(f"Data: SOP={len(sops)}, skills={len(skills)}")

    # 替换 SOP 占位行
    sops_js = build_js_array("sops", sops)
    placeholder_sops = 'const sops = [];  // __SOPS_DATA__'
    if placeholder_sops in content:
        content = content.replace(placeholder_sops, sops_js)
        print("OK: SOP data injected")
    else:
        # fallback: 直接找 const sops = [];
        content = re.sub(r'const sops = \[\];?', sops_js, content)
        print("OK: SOP data injected (fallback)")

    # 替换技能占位行
    skills_js = build_js_array("skills", skills)
    placeholder_skills = 'const skills = [];  // __SKILLS_DATA__'
    if placeholder_skills in content:
        content = content.replace(placeholder_skills, skills_js)
        print("OK: skills data injected")
    else:
        content = re.sub(r'const skills = \[\];?', skills_js, content)
        print("OK: skills data injected (fallback)")

    # 写入输出
    out_dir = os.path.dirname(output_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Done: manual generated -> {output_path}")

if __name__ == "__main__":
    main()
