from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# 获取学生JSON文件路径
def get_file(student_id):
    return os.path.join(DATA_DIR, f"{student_id}.json")

# 加载学习进度：拆分当前路径、全历史掌握度
# 加载学习进度：拆分当前路径、全历史掌握度
def load_progress(student_id):
    file_path = get_file(student_id)
    # 文件不存在=全新用户，空白初始化
    if not os.path.exists(file_path):
        init_data = {
            "current_topics": [],    # 本次待学习知识点（启动默认空）
            "history_mastery": {}    # 所有历史知识点的掌握度（永久保存）
        }
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(init_data, f, ensure_ascii=False, indent=2)
        return init_data
    # 文件存在读取，自动兼容升级旧结构
    with open(file_path, "r", encoding="utf-8") as f:
        progress = json.load(f)
    # 兼容老版本无history_mastery的情况
    if "history_mastery" not in progress:
        progress["history_mastery"] = progress.get("topic_mastery", {})
        if "topic_mastery" in progress:
            del progress["topic_mastery"]
        save_progress(student_id, progress)
    return progress

# 保存进度
def save_progress(student_id, data):
    file_path = get_file(student_id)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 接口1：更新本次学习路径（只覆盖current_topics，不改动history_mastery历史）
@app.route('/api/update_topics', methods=['POST'])
def update_topics():
    req_data = request.get_json()
    student_id = req_data.get("student_id", "student001")
    new_topics = req_data.get("topics", [])
    
    progress = load_progress(student_id)
    progress["current_topics"] = new_topics
    # 新知识点自动写入历史记录，初始掌握度0
    for topic in new_topics:
        if topic not in progress["history_mastery"]:
            progress["history_mastery"][topic] = 0
    save_progress(student_id, progress)
    return jsonify({"status": "ok"})

# 接口2：更新单个知识点掌握度（同步更新历史记录）
@app.route('/api/update', methods=['POST'])
def update_mastery():
    req_data = request.get_json()
    student_id = req_data.get("student_id", "student001")
    topic_name = req_data.get("node_name")
    mastery_score = req_data.get("mastery", 0)

    progress = load_progress(student_id)
    # 历史记录永久更新分数
    progress["history_mastery"][topic_name] = mastery_score
    save_progress(student_id, progress)
    return jsonify({"status": "ok"})

# 接口3：前端地图只展示【当前待学路径】的知识点
@app.route('/api/get_status')
def get_current_status():
    student_id = request.args.get("student_id", "student001")
    progress = load_progress(student_id)
    # 只返回current_topics里的知识点+对应历史分数
    res_map = {t: progress["history_mastery"][t] for t in progress["current_topics"]}
    return jsonify(res_map)

# 接口4：重新规划薄弱点（仅筛选掌握度<50分知识点）
@app.route('/api/replan', methods=['POST'])
def replan_weak():
    req_data = request.get_json() or {}
    student_id = req_data.get("student001")
    progress = load_progress(student_id)

    # 只筛选分数严格小于50的薄弱知识点
    all_history = progress["history_mastery"]
    weak_list = [k for k, v in all_history.items() if v < 50]
    # 分数从小到大排序，最弱的排在最前面优先学
    weak_list.sort(key=lambda x: all_history[x])

    progress["current_topics"] = weak_list
    save_progress(student_id, progress)

    print("\n" + "="*50)
    print("薄弱点重新规划完成（仅掌握度＜50分知识点）")
    print(f"新学习路径：{weak_list}")
    print("="*50)
    return jsonify({
        "status": "success",
        "message": "仅掌握度低于50分知识点已重新规划",
        "weak_topics": weak_list
    })
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)