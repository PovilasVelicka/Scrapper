import json


class AppSettings:
    def __init__(self, settings_path: str):
        self.__settings_path = settings_path
        self.settings = self._load(settings_path)


    def save(self):
        with open(self.__settings_path, 'w', encoding='utf-8') as f:
            obj = json.dumps(self.settings, indent=4, ensure_ascii=False)
            f.write(obj)


    @staticmethod
    def _load(filepath: str) -> dict:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Settings file '{filepath}' not found. Using defaults.")
            return {}
        except json.JSONDecodeError:
            print(f"Invalid JSON format in '{filepath}'. Using defaults.")
            return {}


    @property
    def log_level(self) -> str:
        return self.settings.get('Logging', {}).get('LogLevel', 'INFO').upper()


    @property
    def logs_dir(self) -> str:
        return self.settings.get('Logging', {}).get('LogsDir', 'Logs')

    @property
    def scrape_url(self) -> str:
        return self.settings.get('Scrapping', {}).get('Url', '')


    @property
    def scrape_interval(self) -> int:
        return self.settings.get('Scrapping', {}).get('Interval', 0)


    @property
    def db_path(self) -> str:
        path = self.settings.get('DataBase', {}).get('FilePath', '')
        if path:
            return path
        raise KeyError("Json path not provided in settings. Please check appsettings.json file")

