import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, OpenAITextEmbedding
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureTextEmbedding
from semantic_kernel.connectors.memory.chroma import ChromaMemoryStore
import os 
import shutil
import pandas as pd
import numpy as np

async def make_kernel():
    kernel = sk.Kernel()

    endpoint = "https://thirdray-openai-demo-instance-us-east.openai.azure.com"
    api_key = "917bf6ea50214df7a19a1bf1572aab3d"
    deployment = 'gpt-4'

    kernel.add_text_completion_service("azureopenaicompletion", AzureChatCompletion(deployment, endpoint, api_key))
    kernel.add_text_embedding_generation_service("ada", AzureTextEmbedding("text-embedding-ada-002", endpoint, api_key))

    print("Kernel is ready")

    return kernel


async def make_kernel_with_memory(memory_name, collection_name, csv_name):
    kernel = sk.Kernel()

    endpoint = "https://thirdray-openai-demo-instance-us-east.openai.azure.com"
    api_key = "917bf6ea50214df7a19a1bf1572aab3d"
    deployment = 'gpt-4'

    kernel.add_text_completion_service("azureopenaicompletion", AzureChatCompletion(deployment, endpoint, api_key))
    kernel.add_text_embedding_generation_service("ada", AzureTextEmbedding("text-embedding-ada-002", endpoint, api_key))

    print("Kernel is ready")

    kernel.register_memory_store(memory_store=ChromaMemoryStore(persist_directory=memory_name))
    # print("Made two new services attached to the kernel and made a Chroma memory store that's persistent.")

    ### ONLY DELETE THE DIRECTORY IF YOU WANT TO CLEAR THE MEMORY
    ### OTHERWISE, SET delete_dir = True

    delete_dir = False

    if (delete_dir):
        dir_path = memory_name
        shutil.rmtree(dir_path)
        kernel.register_memory_store(memory_store=ChromaMemoryStore(persist_directory=dir_path))
        print("⚠️ Memory cleared and reset")

    df = pd.read_csv(csv_name)

    df_string = df.to_string(index=False)
    df_list = df_string.split('\n')

    memoryCollectionName = collection_name
    for i in range(len(df_list)):
        await kernel.memory.save_information_async(memoryCollectionName, id=f"df_list-{i}", text=f"{df_list[i]}")

    return kernel
    