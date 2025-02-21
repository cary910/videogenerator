from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.utilities import WikipediaAPIWrapper
import os

def generate_script(subject,video_length,creativity,api_key,base_url):
    title_template = ChatPromptTemplate.from_messages([
        ("human","请你根据｛subject｝这个主题写一个标题，要求尽量吸引人")
    ])
    script_template = ChatPromptTemplate.from_messages([
        ("human",'''你是一个经验丰富的多视频博主，请根据下面的标题和要求，写一份短视频文案，
        视频的标题是{title},视频的长度是｛duration｝,请根据视频的主题，撰写
        一份短视频文案，文案要求包含【开头、中间、结尾】三个部分，三个部分分开写，要求
        开头吸引人，中间提供干货，结尾给人意外。 
        可以使用维基百科来搜索主题的相关内容，并将相关的内容编入文案，无关的则不要编入文案
        ---{wikipedia}---''')
    ])

    model = ChatOpenAI(openai_api_key=api_key,
                       temperature=creativity,
                       base_url=base_url)
    title_chain = title_template|model
    title = title_chain.invoke({"subject": subject}).content

    search = WikipediaAPIWrapper(lang="zh")
    search_result = search.run(subject)

    script_chain = script_template|model
    script = script_chain.invoke({
        "title": title,
        "duration": video_length,
        "wikipedia": search_result
    }).content
    return search_result,title, script

# print(generate_script("混元大模型",1,0.7,os.getenv("DASHSCOPE_API_KEY"),"https://api.aigc369.com/v1"))