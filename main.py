import streamlit as st
from utils import generate_script

st.title("视频脚本生成器")

with st.sidebar:
    api_key = st.text_input("请输入deep seek API密钥", type="password")
    st.markdown("[获取deep seek API密钥](https://platform.deepseek.com/api_keys)")

subject = st.text_input("💡请输入视频的主题")
video_length = st.number_input("⏱️请输入视频的大致时长（单位：秒）",min_value=1,value=10, step=5)
creativity = st.slider("✨请输入视频脚本的创造力（数字越小越保守，数字越大越奔放）",min_value=0.0,max_value=1.5,value=0.7,step=0.1)

submit = st.button("生成脚本")

if submit and not api_key:
    st.info("请输入您的deep seek密钥。")
    st.stop()

if submit and not subject:
    st.info("请输入您的视频主题。")
    st.stop()

if submit and not video_length>=10:
    st.info("视频时长需要大于或等于10秒。")
    st.stop()

if submit:
    with st.spinner("AI正在思考中..."):
        try:
            title,script = generate_script(subject,video_length,creativity,api_key)
        except Exception as e:
            if "invalid api key" in str(e).lower() or "authentication" in str(e).lower():
                st.error("生成失败：API 密钥错误，请检查密钥是否正确！")
            elif "timeout" in str(e).lower():
                st.error("生成失败：网络超时，请稍后重试！")
            elif"rate limit" in str(e).lower():
                st.error("生成失败：API 调用频率超限，请稍后再试！")
            else:
                st.error(f"生成失败：{str(e)}")
            st.stop()  # 终止后续执行

    # 生成成功后替换原有展示逻辑
    st.success("视频脚本已生成！")

    # 标题展示 + 复制按钮
    st.subheader("🔥标题：")
    st.write(title)

    st.subheader("📝 视频脚本：")
    st.write(script)