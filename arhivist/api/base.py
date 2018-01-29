from .template import AbsBookApi


class BaseThumbnailApi(object):

    def download(self, link, download_dir):
        pass

    def get_id(self):
        pass

    def make_scale_url(self):
        pass

    def save(self):
        pass


class BaseBookApi(AbsBookApi):

    def download_thumbnail(self, link, download_dir):
        t_id = self.get_id_thumbnail(link)

        t_resp = self.get_thumbnail(t_url)
        t_name = f"{t_id}.png"
        full_path = os.path.join(self.download_dir, t_name)
        self.save_thumbnail(t_resp, full_path)
        resp['thumbnail'] = t_name

        some_logic = None
        return thumb_id
