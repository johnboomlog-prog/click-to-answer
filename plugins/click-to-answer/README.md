# Click to Answer · 点选回答

Version 0.2.0 — persistent native-choice preferences for Codex.

本插件为 Codex 管理长期点选偏好。Skill 用于设置和实测，常驻行为由独立的持久指令提供。安装本身不会改全局设置。

## 用法

安装后，在新任务中选择 Click to Answer，说“为当前项目开启常驻点选回答”“全局开启点选回答”“检查点选回答状态”或“关闭全局点选回答”。Python 3.11+，无第三方依赖。

也可以在本插件目录运行：

```sh
python scripts/preferences.py enable --scope global --dry-run
python scripts/preferences.py enable --scope global
python scripts/preferences.py doctor --scope global
python scripts/preferences.py disable --scope global
```

项目范围使用 `--scope project --project "项目完整路径"`。全局范围尊重 CODEX_HOME，可通过 --codex-home 指定其他配置目录。设置之后需要新任务读取。

## 保护已有规则

优先选择非空 AGENTS.override.md，否则选择 AGENTS.md。只管理自己的标记块，保留其他内容。重复开启不会重复写入；改变文件前在旁边的 `.click-to-answer-backups/` 留存备份。备份可能包含私有规则，请勿公开。

关闭会清理两个候选文件中的标记块，保留其余内容和备份。项目关闭不关闭全局偏好。升级后再次 enable 才更新既有规则。**先关闭各作用域，再卸载插件**；仅卸载插件不能撤销已存储的指令。

## 能力边界

有兼容原生工具时优先显示 YES/NO 或编号选项，保留自由输入。客户端决定按钮或单选控件外观及是否需要提交。无允许使用的工具时回退文字。不修改客户端，不保证每个回答遵守，不代替操作批准。

doctor 只检查配置，不声称看到了 UI 或实际鼠标点击。实测应保持问题待回答，收到真实答复后再继续。当前公开市场尚未提交，上架准备见 SUBMISSION.md。LICENSE 为 MIT。
