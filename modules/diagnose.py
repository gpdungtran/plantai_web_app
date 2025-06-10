# diagnose.py - hiện thông tin bệnh
import json
import streamlit as st

import streamlit as st
import json

def load_disease_info():
    # Nếu bạn đã lưu cái JSON đó thành file disease_info.json,
    # thì có thể mở file; nếu không, bạn có thể paste thẳng dict vào đây.
    # Ví dụ với dict trực tiếp:
    return {
      "coffee_leaf_rust": {
        "name": "Rỉ sắt lá cà phê",
        "description": "Do nấm Hemileia vastatrix gây ra. Xuất hiện các đốm vàng cam trên mặt dưới của lá, khiến lá bị rụng sớm và giảm năng suất.",
        "solution": "Phun thuốc Mancozeb hoặc Copper Hydroxide định kỳ. Cắt tỉa và tiêu hủy lá bệnh, giữ cho vườn thông thoáng."
      },
      "durian_algal_leaf": {
        "name": "Bệnh lá tảo ở sầu riêng",
        "description": "Xuất hiện các đốm màu nâu đỏ hoặc cam trên lá do tảo Cephaleuros virescens gây ra.",
        "solution": "Cắt tỉa lá bệnh và phun thuốc chứa đồng (Copper-based fungicide)."
      },
      "durian_allocaridara_attack": {
        "name": "Sầu riêng bị côn trùng Allocardia gây hại",
        "description": "Côn trùng Allocaridara phá hoại mô lá non và làm xoăn mép lá.",
        "solution": "Sử dụng thuốc trừ sâu sinh học hoặc hóa học có chọn lọc. Theo dõi thường xuyên."
      },
      "durian_leaf_blight": {
        "name": "Bệnh cháy lá sầu riêng",
        "description": "Lá bị cháy mép, khô từng phần hoặc toàn bộ, thường do nấm hoặc điều kiện môi trường bất lợi.",
        "solution": "Tưới nước hợp lý, cải thiện thông thoáng. Phun thuốc kháng nấm nếu cần."
      },
      "durian_phomopsis_leaf_spot": {
        "name": "Đốm lá Phomopsis trên sầu riêng",
        "description": "Gây ra bởi nấm Phomopsis spp., tạo đốm tròn đen trên lá, có thể làm rụng lá.",
        "solution": "Loại bỏ lá bệnh, dùng thuốc trừ nấm chứa carbendazim hoặc mancozeb."
      },
      "lemon_deficiency_leaf": {
        "name": "Lá chanh bị thiếu dinh dưỡng",
        "description": "Lá vàng nhạt, gân xanh do thiếu nitơ, sắt hoặc magie.",
        "solution": "Bón phân đầy đủ và cân đối. Sử dụng phân bón lá chứa vi lượng."
      },
      "lemon_leaf_anthracnose": {
        "name": "Bệnh thán thư trên lá chanh",
        "description": "Do nấm Colletotrichum spp. gây ra. Lá có đốm nâu, lõm nhẹ và lan rộng.",
        "solution": "Tỉa bỏ cành lá bệnh, phun thuốc gốc đồng hoặc azoxystrobin."
      },
      "lemon_spider_mite_leaf": {
        "name": "Lá chanh bị nhện đỏ tấn công",
        "description": "Nhện đỏ gây hại hút nhựa làm lá vàng, khô và rụng.",
        "solution": "Phun nước áp lực để rửa nhện. Sử dụng thuốc trừ nhện sinh học hoặc abamectin."
      },
      "coffee_leaf_red_spider_mite": {
        "name": "Lá cà phê bị nhện đỏ",
        "description": "Nhện đỏ gây hại mặt dưới lá, tạo đốm vàng, làm giảm quang hợp và năng suất.",
        "solution": "Tưới nước giữ ẩm, phun thuốc trừ nhện đúng thời điểm như abamectin."
      }
    }

def show_disease_info(predicted_class: str):
    """
    Hiển thị thông tin bệnh dựa trên class trả về từ API.
    predicted_class: chuỗi do API trả, ví dụ "lemon spider mite leaf"
    """
    info = load_disease_info()

    # Chuẩn hoá: chuyển dấu cách thành gạch dưới, và xuống thường
    key = predicted_class.strip().replace(" ", "_").lower()

    if key in info:
        data = info[key]
        name     = data.get("name",        "Chưa có tên bệnh")
        desc     = data.get("description", "Chưa có mô tả.")
        solution = data.get("solution",    "Chưa có giải pháp.")

        st.subheader(f"🔎 Tên bệnh: {name}")
        st.write("**📝 Mô tả:**", desc)
        st.write("**💡 Giải pháp:**", solution)
    else:
        st.warning(
            f"Không tìm thấy thông tin cho lớp **{predicted_class}** (key='{key}').\n"
            "Hãy kiểm tra lại tên class hoặc data JSON."
        )

