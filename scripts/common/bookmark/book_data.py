class Bookmark:
    def __init__(self, title, url, add_date, tags=None, icon=None, modified_date=None):
        self.title = title
        self.url = url
        self.add_date = add_date
        self.tags = tags if tags else []
        self.icon = icon
        self.modified_date = modified_date

    def add_tag(self, tag):
        self.tags.append(tag)

    def __repr__(self):
        return f"Title: {self.title}, URL: {self.url}, Added Date: {self.add_date}, Tags: {self.tags}"
