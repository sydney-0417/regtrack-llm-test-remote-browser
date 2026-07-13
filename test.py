from browser_use import Agent, ChatOllama
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
import asyncio

server_ip = "10.34.167.129"
MODEL_API_BASE_URL = f"http://{server_ip}:11434/v1"

# load_dotenv()
async def main():
    from browser_use import Browser

    remote_base_url = f"http://{server_ip}:11434/v1"
    session = Browser(
        headless=False,
        window_size={'width': 1000, 'height': 700},
        # cdp_url="http://127.0.0.1:9222", # dev-only. Goal is to run browser in a docker container
        wait_for_network_idle_page_load_time=5,
        minimum_wait_page_load_time=1,
    )


    task = pythontask = """
        Browse like a real person, not a bot. Scroll before clicking, take imperfect paths, don't need to be efficient.
        1. open a browser and navigate to https://www.cbc.ca. 
        2. When a cookie/consent banner or paywall appears, first investigate the banner if it allows you to customize what to consent and reject. 
        3-1. Once you make sure it's customizable, select the option that consents to the least by clicking reject options for optional cookies / selecting accept option for mandatory cookies. 
        3-2. After that, make sure you apply your decision and close the banner.
        4. when successfully browsed 3 different pages that's not either landing page/consent banner, stop and save the har file named 'har_file.har' with summary of actions/steps performed on browser, then quit.
        5. if any tasks failed, return the reason of failure
    """

    llm_remote = ChatOllama(
        base_url = remote_base_url,
        model=MODEL_API_BASE_URL,
    )
    agent = Agent(task=task, llm=llm_remote, browser_session=session)
    result = await agent.run()
    print(result)
  

if __name__ == "__main__":
    asyncio.run(main())


