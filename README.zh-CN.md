# Click to Answer · 点选回答

**少打字，多点选。让 Codex 的追问更轻松。**

[English](README.md) · [兼容性与实测](docs/compatibility.md) · [发布说明](docs/publishing.md)

开启一次后，后续新任务默认优先用原生 YES/NO 和带编号的选项提问。不需要每次选择 Skill。开放式问题仍可自由输入。

这是持久偏好管理工具，不修改客户端：客户端必须提供允许使用的选择工具，无法保证所有环境或每次回答都出现按钮。

## 三步开始

下载源码包并解压，或克隆仓库。需要 **Python 3.11+**，无第三方依赖。在仓库目录打开终端：

```sh
python plugins/click-to-answer/scripts/preferences.py enable --scope global --dry-run
python plugins/click-to-answer/scripts/preferences.py enable --scope global
python plugins/click-to-answer/scripts/preferences.py doctor --scope global
```

然后新建 Codex 任务，试着让它询问是否使用中文，或让你选择一种导出格式。Windows 也可以用 `py -3` 代替 `python`。

只对当前项目启用：

```sh
python plugins/click-to-answer/scripts/preferences.py enable --scope project --project .
```

## 插件安装

从 GitHub 插件市场安装：

```sh
codex plugin marketplace add https://github.com/johnboomlog-prog/click-to-answer.git
codex plugin add click-to-answer@click-to-answer
```

在新任务中选择 **Click to Answer · 点选回答**，说“为当前项目开启常驻点选回答”或“全局开启点选回答”。也可以要求检查、关闭或实测。插件的 Skill 只是设置入口，常驻指令独立生效；安装本身不会自动改全局设置。

## 查看与关闭

```sh
python plugins/click-to-answer/scripts/preferences.py status --scope global
python plugins/click-to-answer/scripts/preferences.py disable --scope global
```

项目级关闭使用 `disable --scope project --project .`。如果全局也开启了，关闭项目设置不会关闭全局设置。**先关闭各作用域的设置，再卸载插件。** 单独卸载插件不会撤销已经写入的持久偏好。

## 为什么不是只复制一段提示词

- 可选项目或全局范围；遵循 `CODEX_HOME`，可指定 `--codex-home`。
- 识别非空 `AGENTS.override.md` 的优先级。
- 重复开启不重复写入，关闭只移除自己的标记块。
- 保留其他规则、UTF-8 BOM 与换行；修改前备份，原子替换文件。
- 拒绝损坏标记、重复块、未知编码和符号链接指令文件。
- 自检明确区分“配置存在”与“当前会话实际加载、控件成功呈现”。

备份位于指令文件旁的 `.click-to-answer-backups/`，可能包含私有指令，不要上传。关闭会保留备份，可能保留空的指令文件。更深层项目规则、上下文限制及不同配置目录仍可能影响行为。

工具没有后台服务、账户、遥测或 API Key。原生界面可能需要“选中＋提交”，不承诺单击立即发送。缺少可用选择工具时会回退文字。

## 当前状态

0.2.0 已实现持久设置和文件安全测试，本机 Codex CLI 冷启动也读到了项目规则。Windows 桌面端十种主动测试场景均显示选项并返回对应答案，包括四选一、长标签和混合语言；其中两次面板收起，点击“回答问题”可恢复。此结果不能证明任何自然问题的自动触发率或跨客户端稳定性。见[逐项测试记录](docs/choice-ui-test-2026-09-16.md)。没有将静态示意图当成实测录屏。

GitHub 源码包与插件包可由同一仓库构建。官方公开市场尚未提交，见[发布清单](docs/publishing.md)。

```sh
python -m unittest discover -s tests -v
python scripts/build_release.py
```

MIT 开源。如果它减少了你的重复输入，欢迎 Star；也欢迎提交客户端版本及可复现的问题。
