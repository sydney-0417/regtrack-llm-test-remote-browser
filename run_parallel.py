import asyncio
from browser_use import Agent, ChatOllama
from browser_use.browser.session import BrowserSession

PORTS = [9222, 9223, 9224] #issue: creating only three + hard coded ports

async def run_task(port: int, task: str):
    session = BrowserSession(
        cdp_url=f"http://127.0.0.1:{port}",
        wait_for_network_idle_page_load_tim                                                                                       e=5,
        minimum_wait_page_load_time=1,
    )
    llm = ChatOllama(model="qwen3.5:9b") #issue: model is hardcoded

    agent = Agent(
        task=task,
        llm=llm,
        browser_session=session,
    )

    try:
        return await agent.run()
    finally:
        await session.close()

async def main():

    # issue: prompt should be passed as a file
    tasks = [
        "Go to https://ycombinator.com and find the first headline",
        "Go to https://wikipedia.org and search for computer science",
        "Go to https://cbc.com and check the page title",
    ]

    coroutines = []
    for port, task in zip(PORTS, tasks):
        coroutines.append(run_task(port, task))

    # Run all tasks concurrently
    results = await asyncio.gather(*coroutines, return_exceptions=True)

    # Print results cleanly
    for port, result in zip(PORTS, results):
        if isinstance(result, Exception):
            print(f"[port {port}] FAILED: {result}")
        else:
            print(f"[port {port}] {result}")

if __name__ == "__main__":
    asyncio.run(main())


