import streamlit as st
from utils_P1_复现03_副本 import generate_script

st.title("视频脚本生成器")

with st.sidebar:
    dashscope_api_key = st.text_input("请输入DASHSCOPE API 密钥：",type="password") #第一个是提示内容
    st.markdown("[获取DASHSCOPE API密钥](https://account.aliyun.com/)")


#让用户提供主题，第一个参数是给用户的提示
subject = st.text_input("请输入视频的主题")
#让用户提供视频的大致时长,应该是数字，第一个参数仍然是给用户的提示，数值变化也为0.1
video_length = st.number_input("请输入视频的大致时长（单位：分钟）",min_value=0.1 ,step=0.1)
#slier组件可以拖动,数字类型得统一
creativity = st.slider("请输入视频脚本的创造力（数字越小说明更严谨，数字越大说明更多样）",
          min_value=0.1,max_value=1.0,value=0.2, step=0.1)
#添加按钮，返回的是布尔值，因此可以用条件函数来判断
submit = st.button("生成脚本")
if submit and not dashscope_api_key:
    st.info("请输入您的OpenAI密钥")
    st.stop()
    #streamlit的stop的用法是执行到这里，后面的代码都不会被执行了
if submit and not subject:
    st.info("请输入您的视频主题")
    st.stop()
if submit and not video_length >=0.1:
    st.info("视频长度需要大于或等于0.1")
    st.stop()
if submit:
    with st.spinner(("您的视频正在生成中，请稍候...")):
        search_result, title, script  =generate_script(subject, video_length, creativity, dashscope_api_key)
        #上面的缩进表示当缩进内容未显示，则spinner起作用
    st.success("视频脚本已生成！")
    st.subheader("标题")
    st.write(title)

    st.subheader("视频脚本")
    st.write(script)

    with st.expander("维基百科搜索结果"):
        st.info(search_result)

