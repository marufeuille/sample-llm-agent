# 実験用 LLM エージェント置き場

## arknghts_agent

使い方

`arknights_agent/.env` に以下を書いてください。

```
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=YOUR_API_KEY_HERE
```

その後以下のように実行します。

```
$ echo "ロゴスのS3の特化によるダメージの伸びを教えて下さい" | uv run python arknights_agent/agent.py
質問を入力してください:
Playwright MCP serverを起動中...
Playwright MCP serverが起動しました。
20 個のtoolsが見つかりました。
Running agent...
...
Event received: content=Content(parts=[Part(video_metadata=None, thought=None, code_execution_result=None, executable_code=None, file_data=None, function_call=None, function_response=None, inline_data=None, text='ロゴスのスキル3「差延視界」の特化によるダメージの伸びは以下の通りです。\n\nスキルランク | 効果\n------- | --------\n1 | 攻撃力+100%、敵3体を同時攻撃\n2 | 攻撃力+120%、敵3体を同時攻撃\n3 | 攻撃力+140%、敵3体を同時攻撃\n4 | 攻撃力+160%、敵3体を同時攻撃\n5 | 攻撃力+180%、敵3体を同時攻撃\n6 | 攻撃力+200%、敵3体を同時攻撃\n7 | 攻撃力+220%、敵3体を同時攻撃\n特化I | 攻撃力+240%、敵4体を同時攻撃\n特化II | 攻撃力+260%、敵4体を同時攻撃\n特化III | 攻撃力+300%、敵4体を同時攻撃\n\n特化IIIにすることで、スキルランク7と比較して攻撃力が+80%増加し、同時攻撃できる敵の数が1体増加します。')], role='model') grounding_metadata=None partial=None turn_complete=None error_code=None error_message=None interrupted=None invocation_id='e-651c153a-af39-4e73-9166-eaa0ca564e4b' author='arknights_assistant' actions=EventActions(skip_summarization=None, state_delta={}, artifact_delta={}, transfer_to_agent=None, escalate=None, requested_auth_configs={}) long_running_tool_ids=None branch=None id='sOH10Jl1' timestamp=1744532804.866164
Closing MCP server connection...
Cleanup complete.
```
