import streamlit as st
import google.generativeai as genai

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="SWOT Analysis AI", page_icon="📊", layout="wide")
st.title("📊 AI SWOT Analysis Web App")
st.markdown("เปลี่ยนข้อมูลดิบ แผนธุรกิจ หรือปัญหาการทำงาน ให้เป็นกรอบการวิเคราะห์ SWOT ภายในพริบตา")

# 2. แถบด้านข้างสำหรับใส่ API Key (เพื่อความปลอดภัย)
with st.sidebar:
    st.header("⚙️ การตั้งค่าระบบ")
    api_key = st.text_input("ใส่ Google Gemini API Key:", type="password")
    st.markdown("*(รับ API Key ฟรีได้ที่ [Google AI Studio](https://aistudio.google.com/app/apikey))*")

# 3. กล่องรับข้อมูลจากผู้ใช้งาน
user_input = st.text_area(
    "กรอกข้อมูลที่คุณต้องการวิเคราะห์ (เช่น แผนก, ธุรกิจ, หรือสถานการณ์):", 
    height=200,
    placeholder="ตัวอย่าง: ทีมจัดส่งมีรถ 21 คัน ส่งของ 300 ออเดอร์ต่อวัน ส่งตรงเวลา 95% แต่มีปัญหาพนักงานขับรถลาออกบ่อย และราคาน้ำมันกำลังปรับตัวสูงขึ้น..."
)

# 4. ปุ่มกดเพื่อวิเคราะห์
if st.button("🚀 เริ่มวิเคราะห์ SWOT"):
    if not api_key:
        st.warning("⚠️ กรุณาใส่ API Key ที่แถบด้านซ้ายก่อนครับ")
    elif not user_input:
        st.warning("⚠️ กรุณากรอกข้อมูลที่ต้องการวิเคราะห์ก่อนครับ")
    else:
        try:
            # เชื่อมต่อกับสมองของ Gemini
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-pro')
            
            # System Prompt ที่ฝังบทบาทนักวิเคราะห์และผู้เชี่ยวชาญซัพพลายเชน
            system_prompt = """
            คุณคือนักวิเคราะห์กลยุทธ์ธุรกิจและผู้เชี่ยวชาญด้านซัพพลายเชน 
            จงวิเคราะห์ข้อมูลที่ให้มาและสกัดเป็นกรอบ SWOT Analysis 
            โดยจัดรูปแบบให้สวยงาม อ่านง่าย แยกเป็น 4 หมวดหมู่ชัดเจน:
            - 💪 Strengths (จุดแข็ง)
            - ⚠️ Weaknesses (จุดอ่อน)
            - 🌟 Opportunities (โอกาส)
            - 🔥 Threats (อุปสรรค)
            ใช้ Bullet points อธิบายให้กระชับและตรงประเด็น หากเป็นเรื่องการจัดส่งหรือซัพพลายเชนให้เน้นย้ำเป็นพิเศษ
            """
            
            with st.spinner("AI กำลังวิเคราะห์ข้อมูลให้คุณ..."):
                # ส่งข้อมูลไปให้ AI ประมวลผล
                response = model.generate_content(system_prompt + "\n\nข้อมูลที่ต้องวิเคราะห์:\n" + user_input)
                
                # 5. แสดงผลลัพธ์
                st.success("✅ วิเคราะห์เสร็จสิ้น!")
                st.markdown("---")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"❌ เกิดข้อผิดพลาดในการเชื่อมต่อ: {e}")
