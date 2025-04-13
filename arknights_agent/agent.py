# このスクリプトは、GoogleのADKを使用して、アークナイツのキャラクターに関する質問に答えるエージェントを作成します。
# MCPサーバーを使用して、キャラクターの情報を取得します。
# 元のソースコードは https://google.github.io/adk-docs/tools/mcp-tools/ を参考にしています。
import asyncio
import os
from dotenv import load_dotenv
from google.genai import types
from google.adk.agents.llm_agent import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import (
    InMemoryArtifactService,
)
from google.adk.tools.mcp_tool.mcp_toolset import (
    MCPToolset,
    StdioServerParameters,
    AsyncExitStack,
)


async def get_tools_async():
    """Playwright MCPサーバからツールを取得する関数"""
    print("Playwright MCP serverを起動中...")
    tools, exit_stack = await MCPToolset.from_server(
        # https://github.com/microsoft/playwright-mcp
        connection_params=StdioServerParameters(
            command="npx",
            args=[
                "-y",
                "@playwright/mcp@latest",
                "--headless",
            ],
        )
    )
    print("Playwright MCP serverが起動しました。")
    return tools, exit_stack


async def get_agent_async() -> tuple[LlmAgent, AsyncExitStack[bool | None]]:
    """Agentを作成する関数"""
    tools, exit_stack = await get_tools_async()
    print(f"{len(tools)} 個のtoolsが見つかりました。")
    root_agent = LlmAgent(
        model="gemini-2.0-flash",  # Adjust model name if needed based on availability
        name="arknights_assistant",
        instruction="""あなたはアークナイツのキャラクターについて聞かれたら答えるエージェントです。
      ユーザからキャラクターについて尋ねられたらまず、以下のページを確認して当該キャラクターが存在することを確認します。
      - https://arknights.wikiru.jp/?キャラクター一覧
      キャラクターが存在する場合はそのページに遷移し、聞かれている内容について簡潔にまとめて教えて下さい。
      もし存在しなければ、そのようなキャラクターは存在しないと返してください。
      例)
      Q. イネスのLv90時点の攻撃力を教えて下さい
      A. 589です。さらに信頼度補正で + 50されます。
      """,
        tools=tools,  # Provide the MCP tools to the ADK agent
    )
    return root_agent, exit_stack


async def async_main():
    """メイン関数"""
    session_service = InMemorySessionService()
    artifacts_service = InMemoryArtifactService()

    session = session_service.create_session(
        state={}, app_name="arknights_character_search_app", user_id="user_fs"
    )
    # ユーザからの質問を取得
    print("質問を入力してください:")
    query = input().strip()
    # query = "ロゴスのスキル3のダメージ量を計算してください"
    content = types.Content(role="user", parts=[types.Part(text=query)])

    root_agent, exit_stack = await get_agent_async()

    runner = Runner(
        app_name="arknights_character_search_app",
        agent=root_agent,
        artifact_service=artifacts_service,
        session_service=session_service,
    )

    print("Running agent...")
    events_async = runner.run_async(
        session_id=session.id, user_id=session.user_id, new_message=content
    )

    async for event in events_async:
        print(f"Event received: {event}")

    # Crucial Cleanup: Ensure the MCP server process connection is closed.
    print("Closing MCP server connection...")
    await exit_stack.aclose()
    print("Cleanup complete.")


if __name__ == "__main__":
    path = os.path.abspath(__file__)
    dirname = os.path.dirname(path)
    dotenv_path = os.path.join(dirname, ".env")
    load_dotenv(dotenv_path)
    try:
        asyncio.run(async_main())
    except Exception as e:
        print(f"An error occurred: {e}")
