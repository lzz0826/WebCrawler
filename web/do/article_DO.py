class Article_DO:
    def __init__(self, id, source, article_id, title, tags, content, images, source_url, download_url, folder_path,
                 status, memo, update_time, create_time):
        self.id = id
        self.source = source
        self.article_id = article_id
        self.title = title
        self.content = content
        self.tags = tags
        self.images = images
        self.source_url = source_url
        self.download_url = download_url
        self.folder_path = folder_path
        self.status = status
        self.memo = memo
        self.update_time = update_time
        self.create_time = create_time