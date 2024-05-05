
import package as p
from importlib import reload
from logging.handlers import  TimedRotatingFileHandler 

if __name__ == "__main__":
    # securely grab the app name and the logger streamhandler
    name = p.SETTINGS_GLOBAL.get("metadata", {}).get("name", "app")
    streamhandler = p.LOGGER.parent.handlers[ [index for index, obj in enumerate(p.LOGGER.parent.handlers) if isinstance(obj, TimedRotatingFileHandler)][0]]
    streamhandler.doRollover()
    
    # start the application loop
    p.LOGGER.info(f"Starting {name}, hello world!")
    while True:
        try:
            apiEngine = p.ApiEngine()
            apiEngine.run()
        except KeyboardInterrupt:
            p.LOGGER.warning(f"Recieved KeyboardInterrupt, stopping gracefully...")
            apiEngine.stop()
            break
        except Exception as e:
            p.LOGGER.error(f"An error occured:\n{e}\nRestarting {name}")
            reload(p)
        
    # say a final goodbye
    p.LOGGER.info(f"Stopping {name}, goodbye!")