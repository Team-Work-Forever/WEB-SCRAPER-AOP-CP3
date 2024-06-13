class UrlResult():
    url: str

    def __init__(self, url: str):
        self.url = ''
        self.handle(url)

    def handle(self, url: str):
        if url:
            self.url = url.strip()
        else:
            raise Exception("Sem url!")
        
    def __str__(self) -> str:
        return f"Url: {self.url}\n"