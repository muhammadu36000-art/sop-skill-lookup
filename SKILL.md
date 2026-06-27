---
name: "SOP·技能速查工具"
summary: "自动扫描 WorkBuddy 技能和 SOP 文件，生成可分享的 HTML 速查手册"
trigger: ["更新手册", "生成手册", "扫描技能", "scan sop", "update manual", "手册同步"]
description: "首次运行引导配置路径，之后自动扫描全部技能和 SOP，生成/更新 HTML 速查手册。支持技能手册和 SOP 手册两个 Tab。"
read_when:
  - 用户说「更新手册」「生成手册」「扫描技能」「scan sop」「update manual」
---

# SOP·技能速查工具

自动扫描你安装的所有 WorkBuddy 技能和 SOP 工作流文件，生成一个完整的 HTML 速查手册（含 SOP 手册 + 技能手册两个 Tab），可直接用浏览器打开查看。

---

## 执行流程

### 第一步：检查配置文件

读取配置文件：`~/.workbuddy/skills/SOP·技能速查工具/config.json`

- **文件存在** → 直接跳到「第三步：扫描并生成」
- **文件不存在** → 执行「第二步：首次运行引导」

---

### 第二步：首次运行引导

**先输出一段简洁介绍（让用户知道这个技能是干嘛的、怎么用）：**

> **🧭 SOP·技能速查工具**
> 
> 这个技能会自动扫描你安装的所有 WorkBuddy 技能和 SOP 工作流文件，生成一份完整的 **HTML 速查手册**。
> 
> **生成的手动有什么？**
> - 📋 **SOP 手册** Tab：你所有的 SOP 工作流，点击可展开查看每一步做什么、有什么规则
> - 🛠 **技能手册** Tab：你安装的所有技能，按分类展示，支持搜索和筛选
> 
> **怎么用？**
> 以后只要说「**更新手册**」或「**生成手册**」，我就会自动重新扫描并更新这份手册。
> 
> ---
> 
> 首次使用需要配置一件事：**手册想保存在哪？**
> （例如：`D:\My Documents\工作手册.html`）
> 
> 技能和 SOP 的扫描路径我会自动获取，不需要你告诉我国。

**不要问用户任何目录路径。** 以下内容全部自动获取：

| 项目 | 获取方式 |
|---|---|
| 用户级技能目录 | 固定路径：`~/.workbuddy/skills/`（直接扫描这个目录） |
| 项目级技能 | 见下方「扫描逻辑」|
| SOP 文件 | 见下方「扫描逻辑」|

用户回复路径后，创建配置文件：

用户回复路径后，创建配置文件：

```json
{
  "manual_path": "用户指定的完整路径",
  "created_at": "YYYY-MM-DD",
  "version": "1.0"
}
```

保存到 `~/.workbuddy/skills/SOP·技能速查工具/config.json`

然后继续执行第三步。

---

### 第三步：扫描并生成

#### 3.1 扫描技能

**用户级技能（固定路径）：**
`~/.workbuddy/skills/` 下每个子目录 = 一个技能

对每个技能目录，读取 `SKILL.md` 的前 20 行，提取：
- `name`（技能名称）
- `description`（如有，从 SKILL.md 的 metadata 或第一行标题提取）
- 触发词（从 SKILL.md 内容中查找「触发词」「trigger」「说XX」等关键词后的内容）

**项目级技能（自动查找工作区）：**

工作区查找逻辑：
1. 读取 `~/.workbuddy/memory/MEMORY.md` 查找工作区路径
2. 同时扫描以下常见位置：
   - `D:\WR WORK SPACE\`（朝梧的配置，其他用户可能不同）
   - 让用户的工作区目录（可以从 WorkBuddy 配置中查找，或直接 ask：你有多个工作区吗？告诉我就行）
3. 对每个找到的工作区，扫描 `{workspace}/.workbuddy/skills/` 目录

**每个技能的数据格式（写入 HTML 的 `skills` 数组）：**

```javascript
{
  name: "技能显示名称",
  cat: "分类名",        // 见下方「分类列表」
  type: "user",          // user=用户级 / project=项目级 / plugin=MCP插件 / bunded=系统内置
  desc: "一句话功能描述",
  use: "如何调用（可选）",
  triggers: ["触发词1", "触发词2"]
}
```

**分类列表（保持这个顺序）：**
AI资讯与情报 / 内容创作·写作 / AI视频生成 / 视频剪辑与处理 / 图像生成与设计 / PPT与演示 / 社交媒体运营 / 搜索工具 / AI角色与专家 / 音频处理 / 内容校准系统 / 办公与云服务 / 多模态分析 / 工具与系统 / 工作流/SOP / 文档处理 / 项目工具 / 金融数据

#### 3.2 扫描 SOP

**扫描逻辑：**
1. 扫描所有工作区的根目录和子目录，查找含以下关键词的 `.md` 文件：
   - `SOP`、`sop`、`流程`、`工作流`、`执行手册`、`操作手册`
2. 读取每个命中文件的前 50 行，判断是否是真正的 SOP（含步骤/流程描述）
3. 提取：SOP 名称、所属工作区、简介、步骤列表

**每个 SOP 的数据格式（写入 HTML 的 `sops` 数组）：**

```javascript
{
  id: "唯一ID（英文+数字，如 ai-sop）",
  area: "工作区英文标识",   // ai / travel / story / ppt / global / research
  areaLabel: "工作区中文名",
  areaClass: "tag-ai",       // 对应 CSS 类
  title: "SOP 显示标题",
  desc: "一句话描述",
  keywords: "关键词1 关键词2 ...",
  chips: ["标签1", "标签2"],
  link: "file:///完整路径（URL编码）",
  steps: [
    {
      num: "Step 0",
      name: "步骤名称",
      task: "这一步做什么",
      rules: [
        {type: "hard", text: "硬规内容"},
        {type: "soft", text: "软规内容"},
        {type: "tip", text: "提示内容"}
      ],
      tools: ["工具名"],
      path: "输出路径"
    }
  ]
}
```

**工作区颜色映射：**
| area | areaClass | 颜色 |
|---|---|---|
| ai | tag-ai | 蓝色 #2563eb |
| travel | tag-travel | 绿色 #16a34a |
| story | tag-story | 橙色 #d97706 |
| ppt | tag-ppt | 紫色 #7c3aed |
| global | tag-global | 红色 #e11d48 |
| research | tag-research | 青色 #0d9488 |

#### 3.3 生成 HTML 手册

**读取模板：** `~/.workbuddy/skills/SOP·技能速查工具/template.html`
**生成脚本：** `~/.workbuddy/skills/SOP·技能速查工具/generate.py`（技能包自带，无需临时创建）

**执行流程：**

1. 将扫描到的 `sops` 和 `skills` 数据写入临时 JSON 文件（如 `C:\Users\h\AppData\Local\Temp\sop_skill_data.json`）
   - JSON 格式：`{"sops": [...], "skills": [...]}`
2. 运行生成脚本：
   ```
   python generate.py <template.html> <output.html> <data.json>
   ```
   - `template.html`：技能目录下的 `template.html`
   - `output.html`：`config.json` 里配置的 `manual_path`
   - `data.json`：上一步写入的临时 JSON 文件
3. 脚本运行完毕后，删除临时 JSON 文件

#### 3.4 输出结果

生成完成后，输出：

```
🧭 工作手册已生成 / 更新

📋 SOP 手册：N 个
  （列出新发现的 SOP）

🛠 技能手册：N 个
  （列出新发现的技能）

手册路径：{config.manual_path}
```

---

## 注意事项

1. **路径处理**：SOP 的 `link` 字段必须是 `file:///` 格式 + URL 编码的完整路径（Windows 路径如 `D:\foo\bar.md` → `file:///D:/foo/bar.md`）
2. **分类归属**：扫描技能时，从 SKILL.md 的 metadata `summary` 或内容推断分类，无法确定时归为「工具与系统」
3. **SOP 步骤详情**：如果 SOP 文件没有明确分步，将整个文件内容作为「步骤一」放入
4. **去重**：生成前检查 `sops` 和 `skills` 数组，确保没有重复名称
5. **template.html 的读取**：从技能自己的安装目录读取，路径为 `~/.workbuddy/skills/SOP·技能速查工具/template.html`

---

## 配置文件格式

`~/.workbuddy/skills/SOP·技能速查工具/config.json`

```json
{
  "manual_path": "D:/xxx/工作手册.html",
  "created_at": "2026-06-27",
  "version": "1.0",
  "workspace_roots": ["D:/WR WORK SPACE"],
  "note": "workspace_roots 由 AI 自动填写，用户无需关心"
}
```

---

## 触发词

| 触发词 | 效果 |
|---|---|
| `更新手册` / `手册同步` | 扫描并生成/更新手册 |
| `生成手册` | 强制重新生成（不管是否已存在）|
| `扫描技能` | 只扫描并列出技能（不生成文件）|
| `scan sop` / `update manual` | 英文触发词 |

---

## 更新记录

- v1.0（2026-06-27）：初始版本，支持自动扫描技能和 SOP，生成双 Tab HTML 手册
