import streamlit as st
import requests
import json
from xinference.client import Client

# 嵌入模型API函数
def get_embedding(query):
    try:
        # 替换为你的嵌入模型API的URL
        embedding_api_url = Client("http://10.100.4.120:9997")
        model = embedding_api_url.get_model("embed")
        res = model.create_embedding(query)
        
        if 'data' in res and res['data'][0].get('embedding'):
            return res['data'][0]['embedding']
        else:
            st.error("无法获取嵌入向量")
            return None
    except Exception as e:
        st.error(f"获取嵌入向量时出错：{e}")
        return None

# Qdrant搜索函数
def vector_search(query_vector):
    try:
        qdrant_url = "http://10.1.20.150:6333"  # Replace with your Qdrant server address and port
        collection_name = "Vector_index_1a52614d_99eb_46b7_a6c9_070310c2ba76_Node"  # Replace with your Qdrant collection name

        response = requests.post(
            f"{qdrant_url}/collections/{collection_name}/points/search",
            headers={"Content-Type": "application/json"},
            data=json.dumps({
                "vector": query_vector,
                "top": 10,  # Return top 10 most similar results
                "with_payload": {
                        "include": ["page_content"]
                }
            })
        )
        if response.status_code == 200:
            response_data = response.json()
            # Extracting page_content from each search result
            page_contents = [item['payload']['page_content'] for item in response_data['result']]
            return page_contents
        else:
            st.error("Search request failed")
            return None
    except Exception as e:
        st.error(f"Error executing search: {e}")
        return None
    
def rerank(query, search_results):
    try:
        rerank_api_url = "http://10.100.4.120:9997"
        client = Client(rerank_api_url)
        model = client.get_model("rerank")

        reranked_response = model.rerank(search_results, query)

        # Extracting documents from the response
        if reranked_response and "results" in reranked_response and reranked_response["results"]:
            reranked_documents = [item["document"] for item in reranked_response["results"]]
            return reranked_documents
        else:
            st.info("No results found after re-ranking.")
            return []

    except Exception as e:
        st.error(f"Error during re-ranking: {e}")
        return search_results  # Return the original results if re-ranking fails

    try:
        rerank_api_url = "http://10.100.4.120:9997"
        client = Client(rerank_api_url)
        model = client.get_model("rerank")

        # Convert search results to the expected format for the rerank model
        formatted_search_results = [{"text": item} for item in search_results]

        reranked_response = model.rerank(search_results, query)

        # Debugging: Print the rerank response
        print("Rerank response:", reranked_response)

        # Check and parse the response
        if reranked_response and "results" in reranked_response:
            # Safely extracting 'text' and 'score' from each item in results
            reranked_documents = [{"text": item.get("text"), "score": item.get("score")} 
                                  for item in reranked_response["results"] if "text" in item]
            return reranked_documents
        else:
            raise ValueError("Re-rank response is empty or has an unexpected format")

    except ValueError as ve:
        st.error(f"Validation error during re-ranking: {ve}")
        return search_results  # Return original results if validation fails
    except Exception as e:
        st.error(f"Error during re-ranking: {e}")
        return search_results  # Return the original results if re-ranking fails

    try:
        rerank_api_url = "http://10.100.4.120:9997"
        client = Client(rerank_api_url)
        model = client.get_model("rerank")

        # Convert search results to the expected format for the rerank model
        formatted_search_results = [{"text": item} for item in search_results]

        reranked_response = model.rerank(search_results, query)

        # Check and parse the response
        if reranked_response and "results" in reranked_response:
            # Extracting the reranked documents and scores
            reranked_documents = [{"text": item["text"], "score": item["score"]} 
                                  for item in reranked_response["results"]]
            return reranked_documents
        else:
            raise ValueError("Re-rank response is empty or has an unexpected format")

    except ValueError as ve:
        st.error(f"Validation error during re-ranking: {ve}")
        return search_results  # Return original results if validation fails
    except Exception as e:
        st.error(f"Error during re-ranking: {e}")
        return search_results  # Return the original results if re-ranking fails

# Streamlit应用
def main():
    st.title("文本向量化搜索")

    # 输入框
    query = st.text_input("输入你的搜索词")

    if st.button("搜索"):

        query_vector = get_embedding(query)
        # 获取嵌入向量
        if query_vector is not None:
            # Vector search
            search_results = vector_search(query_vector)

            if search_results:
                # Re-ranking
                reranked_results = rerank(query, search_results)

                # Display results
                st.write(reranked_results)

if __name__ == "__main__":
    main()
