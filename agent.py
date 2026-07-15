import asyncio
from browser_use import Agent, Browser, ChatOllama

llm = ChatOllama(
    model="qwen3.6:35b-a3b",
    host="http://localhost:11434",  # via SSH tunnel → Machine A
)

browser = Browser(
    headless=False,  # visible on the monitor
    record_har_path="./trace.har",
    record_har_content="embed",
    record_har_mode="full",
)

agent = Agent(
    task="""
        Browse like a real person, not a bot. Scroll before clicking, take imperfect paths, don't need to be efficient.
        1. open a browser and navigate to force.com 
        2. When a cookie/consent banner or paywall appears, first investigate the banner if it allows you to customize what to consent and reject. 
        3-1. Once you make sure it's customizable, select the option that consents to the least by clicking reject options for optional cookies / selecting accept option for mandatory cookies. 
        3-2. After that, make sure you apply your decision and close the banner.
        4. when successfully browsed 1 different page that's not either landing page/consent banner, stop and save the har file named 'har_file.har' with summary of actions/steps performed on browser, then leave the browser open.
        5. if any tasks failed, return the reason of failure
    """,
    llm=llm,
    browser=browser,
)

last_cookies = []

async def capture_cookies(agent):
    # agent.run() force-closes the browser right after the last step
    # (judge eval + teardown), so grab cookies live on every step instead
    # of after run() returns.
    global last_cookies
    try:
        last_cookies = await browser.cookies()
    except Exception as e:
        print(f"cookie capture failed mid-run: {e}")

async def main():
    await agent.run(on_step_end=capture_cookies)

    print(f"\n--- final cookie snapshot ({len(last_cookies)} cookies) ---")
    for c in last_cookies:
        print(f"{c['name']} ({c['domain']}): {c['value']}")

asyncio.run(main())