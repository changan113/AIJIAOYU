import json
import requests
from llm_utils import call_ollama

# 生成学习路径，同步给后端current_topics
def plan_learning_path(goal, mastered_list=[]):
    prompt = f"""
学习目标：{goal}
跳过已完全掌握知识点：{', '.join(mastered_list)}
严格输出5个循序渐进知识点，只返回纯JSON格式：
{{"steps":["知识点1","知识点2","知识点3","知识点4","知识点5"]}}
"""
    res_text = call_ollama(prompt)
    try:
        if '{' in res_text and '}' in res_text:
            res_text = res_text[res_text.index('{'):res_text.rindex('}')+1]
        return json.loads(res_text)
    except Exception as e:
        print(f"路径生成解析失败：{e}")
        return {"steps": []}

# 针对知识点出题
def generate_question(topic, sub_topic=None):
    sub = sub_topic if sub_topic else topic
    prompt = f"""
针对核心知识点「{topic}」，子考点「{sub}」出单选题
硬性要求：
1. 只输出JSON，无多余文字
2. question只写题干，不带选项
3. options固定4项：A./B./C./D.开头
4. answer只填单个大写字母
示例模板：
{{
"question":"题干内容",
"options":["A.选项1","B.选项2","C.选项3","D.选项4"],
"answer":"A"
}}
"""
    # 最多重试2次出题
    for _ in range(2):
        res = call_ollama(prompt)
        if not res:
            continue
        try:
            json_str = res[res.index('{'):res.rindex('}')+1]
            q_data = json.loads(json_str)
            if len(q_data["options"]) == 4 and all(opt.startswith(("A.","B.","C.","D.")) for opt in q_data["options"]):
                return q_data
        except Exception as err:
            print(f"出题失败重试：{err}")
    print("❌ 本题出题失败，跳过")
    return None

# 答案对错判断
def judge_answer(correct_ans, user_ans):
    return user_ans.strip().upper() == correct_ans.strip().upper()

# 错误讲解
def explain_error(question, correct, user):
    prompt = f"题目：{question}，正确答案{correct}，用户答{user}，一句话通俗解释错误原因"
    return call_ollama(prompt) or "AI讲解服务暂时不可用"

# 同步本次学习路径到后端current_topics
def sync_current_topics(topic_list):
    try:
        requests.post(
            "http://127.0.0.1:5000/api/update_topics",
            json={"student_id": "student001", "topics": topic_list},
            timeout=5
        )
    except Exception as e:
        print(f"同步学习路径失败：{e}")

# 同步知识点掌握度到history_mastery历史库
def sync_topic_score(topic, score):
    try:
        requests.post(
            "http://127.0.0.1:5000/api/update",
            json={"student_id": "student001", "node_name": topic, "mastery": score},
            timeout=5
        )
    except Exception as e:
        print(f"同步掌握分数失败：{e}")

# 单个知识点学习流程
def learn_single_topic(topic_name):
    print(f"\n===== 开始学习知识点：{topic_name} =====")
    correct_count = 0
    max_question = 4
    current_score = 0

    for q_idx in range(max_question):
        if current_score >= 100:
            print(f"✅ {topic_name}已满分掌握，提前结束学习")
            break
        print(f"\n【第{q_idx+1}/{max_question}题】")
        question_info = generate_question(topic_name)
        if not question_info:
            continue
        
        print(f"题目：{question_info['question']}")
        for opt in question_info["options"]:
            print(opt)
        
        user_input = input("请输入答案(A/B/C/D)：")
        if judge_answer(question_info["answer"], user_input):
            print("回答正确！掌握度+25%")
            correct_count += 1
            current_score = correct_count * 25
            sync_topic_score(topic_name, current_score)
        else:
            print(f"回答错误，标准答案：{question_info['answer']}")
            print("错误解析：", explain_error(question_info["question"], question_info["answer"], user_input))
            # 错题重答机会
            retry_choose = input("是否重新作答一次？(y/n)：")
            if retry_choose.lower() == "y":
                retry_ans = input("重新输入答案：")
                if judge_answer(question_info["answer"], retry_ans):
                    print("这次答对了，但不提升掌握度")
                else:
                    print("依旧答错，本题结束")
            sync_topic_score(topic_name, current_score)
        
        # 中途重规划入口
        print("\n1.继续答题  2.立刻重新规划薄弱点")
        select = input("请选择操作：")
        if select == "2":
            return None, current_score
    return topic_name, current_score

# 整体学习启动入口
def start_learning_flow(learning_goal):
    # 先拉取后端所有已满分知识点
    try:
        history_data = requests.get("http://127.0.0.1:5000/api/get_all_history", timeout=5).json()
        fully_mastered = [k for k, v in history_data.items() if v >= 100]
    except Exception:
        fully_mastered = []
    
    # AI生成新学习路径
    path_result = plan_learning_path(learning_goal, fully_mastered)
    step_list = path_result.get("steps", [])
    if not step_list:
        print("❌ 学习路径生成失败，请重试")
        return
    
    # 把新路径同步给后端current_topics（地图展示）
    sync_current_topics(step_list)
    print("\n=== 本次规划学习路径 ===")
    for idx, step in enumerate(step_list, 1):
        print(f"{idx}. {step}")
    
    learn_record = {}
    # 逐个学习知识点
    for topic in step_list:
        finish_topic, final_score = learn_single_topic(topic)
        # 用户中途选择重规划，终止本轮学习
        if finish_topic is None:
            requests.post(
                "http://127.0.0.1:5000/api/replan",
                json={"student_id": "student001"},
                timeout=5
            )
            print("已自动重新规划薄弱知识点，本轮学习终止")
            return
        learn_record[finish_topic] = final_score

if __name__ == "__main__":
    print("========== 智能知识孪生学习系统 ==========")
    while True:
        target_goal = input("\n请输入你的整体学习目标：")
        start_learning_flow(target_goal)
        # 学习结束后操作菜单
        print("\n===== 操作菜单 =====")
        print("1. 重新设定目标开始新一轮学习")
        print("2. 退出程序")
        opt = input("输入选择(1/2)：")
        if opt == "2":
            print("程序退出，历史学习数据已保存")
            break