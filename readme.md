# 个人情绪概念分析工具

## 概述

此工具用于分析和可视化个人情绪概念数据。它可以从Markdown或JSON文件中加载数据，然后用户可以对每种情绪的频次和影响程度进行评分。最后，它会生成一个情绪分布图，并将结果保存为JSON文件和PNG图像。

## 功能
- 加载和创建情绪报告。
- 从Markdown或JSON文件中读取情绪数据。
- 允许用户为每种情绪的频次和影响程度进行评分。
- 生成情绪分布图。
- 保存情绪报告和图表。

![情绪分布图_awyugan.png](https://static.aiwriter.net/2utuxsJh4CXi46hzmc3uZ3/wWiUWkSCcoAVaeC3eA4Qs5/dBUnwnVA9wmQsLzvGrFQxW)

## 如何使用
1. 将脚本保存到本地。
2. 安装依赖(可在conda中安装)`pip install -r requirements.txt`
3. 在终端运行脚本，传入Markdown或JSON文件作为命令行参数。
   ```bash
   python ET01test01.py {name}.md
   ```
   或者
   ```bash
   python ET01test01.py {name}.json
   ```
4. 根据提示，为情绪的频次和影响程度输入评分。
5. 查看生成的情绪分布图和保存的报告。

## 文件结构
- `ET01Test01`: 保存JSON报告和情绪分布图的默认文件夹。
- `ET01test01.py`: 主脚本文件，包含情绪分析的所有功能。

## 注意事项
- 确保Python环境已安装所需的库。
- 脚本使用中文，确保系统支持中文显示。
- 本工具需要访问和写入文件权限。

## 支持的文件格式

- Markdown (.md)
- JSON (.json)

## 示例

假设有一个Markdown文件`example.md`，内容如下（可直接复制excel表格中的内容到example.md）：
```
此时此刻我的情绪感受是什么？	快乐	悲伤
过去18个月，我反复出现的情绪体验是什么？	焦虑
```
运行命令：
```bash
python 情绪分析脚本.py example.md
```
按照提示输入情绪的频次和影响程度评分，然后查看生成的情绪分布图和JSON报告。


## 版本历史
- v1.0 - 初始完成md、json转报告

## 待解决问题

- [ ] 无法处理报告重复问题，如生成重复报告，请删除`ET01Test01`文件夹中的相关文件