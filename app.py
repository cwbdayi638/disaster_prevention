import gradio as gr
import folium
from folium.plugins import MarkerCluster
import json
import os
from datetime import datetime

# 灾害数据文件路径
DATA_FILE = "disaster_data.json"

# 初始示例数据
SAMPLE_DATA = [
    {
        "id": 1,
        "location": "XX县XX路50号",
        "lat": 24.948199,
        "lng": 121.225912,
        "description": "山路边坡出现裂痕，有土石滑落风险",
        "level": "中",
        "reported_at": "2025-03-10 00:00",
        "status": "待处理"
    },
    {
        "id": 2,
        "location": "OO市OO山道",
        "lat": 25.032061,
        "lng": 121.565428,
        "description": "暴雨后斜坡不稳定，建议警戒",
        "level": "高",
        "reported_at": "2025-03-09 23:30",
        "status": "警戒中"
    }
]

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        # 首次运行创建示例数据
        save_data(SAMPLE_DATA)
        return SAMPLE_DATA

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def create_map(data):
    # 创建地图中心点（以第一个灾害点为中心）
    if data:
        center_lat = sum(d["lat"] for d in data) / len(data)
        center_lng = sum(d["lng"] for d in data) / len(data)
    else:
        center_lat, center_lng = 24.948199, 121.225912  # 默认：台北
    
    m = folium.Map(location=[center_lat, center_lng], zoom_start=12)
    
    # 使用 MarkerCluster 聚合标记
    marker_cluster = MarkerCluster().add_to(m)
    
    # 根据风险等级设置颜色
    level_colors = {
        "高": "red",
        "中": "orange",
        "低": "green"
    }
    
    for item in data:
        color = level_colors.get(item["level"], "blue")
        popup_html = f"""
        <b>地点：</b> {item['location']}<br>
        <b>描述：</b> {item['description']}<br>
        <b>风险等级：</b> {item['level']}<br>
        <b>通报时间：</b> {item['reported_at']}<br>
        <b>状态：</b> {item['status']}
        """
        
        folium.Marker(
            location=[item["lat"], item["lng"]],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{item['location']} - {item['level']}风险",
            icon=folium.Icon(color=color, icon="warning", prefix="fa")
        ).add_to(marker_cluster)
    
    # 保存地图为 HTML 字符串
    return m._repr_html_()

def get_report_list(data):
    """生成通报列表用于显示"""
    if not data:
        return "暂无通报资料"
    
    lines = []
    for i, item in enumerate(data, 1):
        lines.append(f"{i}. [{item['level']}] {item['location']} - {item['description'][:30]}... ({item['reported_at']})")
    return "\n".join(lines)

def submit_report(location, description, lat, lng, level):
    """提交新通报"""
    if not location or not description:
        return "❌ 请填写地点和描述", gr.update(), gr.update()
    
    try:
        lat = float(lat) if lat else 24.948199
        lng = float(lng) if lng else 121.225912
    except:
        lat, lng = 24.948199, 121.225912
    
    data = load_data()
    new_id = max([d["id"] for d in data], default=0) + 1
    new_item = {
        "id": new_id,
        "location": location,
        "lat": lat,
        "lng": lng,
        "description": description,
        "level": level,
        "reported_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "status": "待处理"
    }
    data.append(new_item)
    save_data(data)
    
    return "✅ 通报已成功提交！", create_map(data), get_report_list(data)

# 初始加载数据
initial_data = load_data()

# 创建界面
with gr.Blocks(title="土石流防災即時資訊地圖") as demo:
    gr.Markdown("# ⚠️ 土石流防災即時資訊系統")
    gr.Markdown("整合 AI 防災助理，24小時自動監測與通報")
    
    with gr.Row():
        with gr.Column(scale=3):
            # 地图显示
            map_html = gr.HTML(value=create_map(initial_data))
            
        with gr.Column(scale=1):
            gr.Markdown("## 📋 通報列表")
            report_list = gr.Textbox(
                value=get_report_list(initial_data),
                label="",
                lines=20,
                interactive=False
            )
    
    with gr.Row():
        gr.Markdown("---")
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("## 📝 提交新通報")
            with gr.Row():
                location_input = gr.Textbox(label="地點", placeholder="例如：XX县XX路XX号附近")
                level_input = gr.Dropdown(
                    choices=["低", "中", "高"],
                    value="中",
                    label="风险等级"
                )
            description_input = gr.Textbox(
                label="详细描述",
                placeholder="请描述具体情况（如山墙裂痕、土石滑动等）",
                lines=3
            )
            with gr.Row():
                lat_input = gr.Textbox(label="纬度", placeholder="可选，默认台北")
                lng_input = gr.Textbox(label="经度", placeholder="可选，默认台北")
            submit_btn = gr.Button("📤 送出通報", variant="primary")
            result_msg = gr.Textbox(label="提交结果", interactive=False)
    
    # 事件绑定
    submit_btn.click(
        fn=submit_report,
        inputs=[location_input, description_input, lat_input, lng_input, level_input],
        outputs=[result_msg, map_html, report_list]
    )

# 启动
if __name__ == "__main__":
    demo.launch()
