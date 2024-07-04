import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import sys
import re
from matplotlib.font_manager import FontManager
from adjustText import adjust_text

FOLDER_NAME = "ET01Test01"
QUESTIONS = [
    "此时此刻我的情绪感受是什么？",
    "过去18个月，我反复出现的情绪体验是什么？",
    "在我0-12岁，反复出现的情绪体验是什么？",
    "在我12-24岁，反复出现的情绪体验是什么？",
    "我有什么常见的口头禅？",
    "我在近期和家人、亲朋好友的微信对话，呈现出了哪些情绪概念？",
    "我近期发的朋友圈、对外写的文章中，反映了哪些情绪感受和体验？",
    "家人、朋友、同事和我交流的时候，认为我经常出现的情绪是什么？"
]

def check_and_set_font():
    font_options = ["SimHei", "Microsoft YaHei", "Arial Unicode MS"]
    available_fonts = {f.name: f.fname for f in FontManager().ttflist}
    for font in font_options:
        if font in available_fonts:
            plt.rcParams['font.sans-serif'] = [font]
            plt.rcParams['axes.unicode_minus'] = False
            return
    print("未找到支持中文的字体，请下载 SimHei 字体:")
    print("https://github.com/StellarCN/scp_zh/blob/master/fonts/SimHei.ttf")
    sys.exit()

def load_or_create_report(name):
    file_path = os.path.join(FOLDER_NAME, f"{name}.json")
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        if not os.path.exists(FOLDER_NAME):
            os.makedirs(FOLDER_NAME)
        return {question: [] for question in QUESTIONS}

def save_report(name, report):
    file_path = os.path.join(FOLDER_NAME, f"{name}.json")
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=4, ensure_ascii=False)

def get_valid_input(prompt, valid_range=None):
    while True:
        user_input = input(prompt)
        if user_input.lower() == 't':
            return None
        if valid_range:
            try:
                value = int(user_input)
                if value in valid_range:
                    return value
                else:
                    print(f"请输入有效值 {valid_range} 或 'T' 跳过。")
            except ValueError:
                print(f"请输入有效整数 {valid_range} 或 'T' 跳过。")
        else:
            return user_input

def plot_emotions(report, name):
    check_and_set_font()
    emotion_data = []
    for question, emotions in report.items():
        for emotion in emotions:
            if emotion["频次"] is not None and emotion["影响程度"] is not None:
                emotion_data.append([emotion["情绪概念"], int(emotion["频次"]), int(emotion["影响程度"])])

    df = pd.DataFrame(emotion_data, columns=['情绪概念', '频次', '影响程度'])
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(df['频次'], df['影响程度'], s=df['频次'].astype(float) * 50, alpha=0.5)
    texts = []
    for i, row in df.iterrows():
        texts.append(plt.text(row['频次'], row['影响程度'], row['情绪概念'], ha='center'))
    adjust_text(texts, arrowprops=dict(arrowstyle='->', color='red'))
    plt.xlabel('频次')
    plt.ylabel('影响程度')
    plt.title('情绪分布图')
    plt.savefig(os.path.join(FOLDER_NAME, f'情绪分布图_{name}.png'))
    plt.show()

def load_md_file(file_path):
    report = {question: [] for question in QUESTIONS}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                parts = line.split('\t')
                if parts[0] in QUESTIONS:
                    question = parts[0]
                    emotions = parts[1:]
                    for emotion in emotions:
                        report[question].append({"情绪概念": emotion, "频次": None, "影响程度": None})
    except FileNotFoundError:
        print(f"文件未找到: {file_path}")
    except Exception as e:
        print(f"读取文件时出错: {e}")
    return report

def main():
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        name = os.path.splitext(os.path.basename(file_path))[0]
        report = load_or_create_report(name)

        if file_path.endswith('.md'):
            new_report = load_md_file(file_path)
            for question in QUESTIONS:
                if question in new_report:
                    report[question].extend(new_report[question])
        elif file_path.endswith('.json'):
            with open(file_path, 'r') as f:
                new_report = json.load(f)
            for question in QUESTIONS:
                if question in new_report:
                    report[question].extend(new_report[question])

        for question in QUESTIONS:
            for emotion in report[question]:
                if emotion["频次"] is None:
                    emotion["频次"] = get_valid_input(f"请用1-5评分表达'{emotion['情绪概念']}'的频次（1=很少，5=经常）：", range(1, 6))
                if emotion["影响程度"] is None:
                    emotion["影响程度"] = get_valid_input(f"请用1-5评分表达'{emotion['情绪概念']}'的影响程度（1=轻微，5=严重）：", range(1, 6))

        save_report(name, report)
        plot_emotions(report, name)
        print(f"报告已保存至 {os.path.join(FOLDER_NAME, name)}.json")

if __name__ == "__main__":
    main()