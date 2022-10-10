from time import sleep
import qbittorrentapi
import time
import hashlib
import bencoding


class Client:
    def __init__(self, host, port, username, password):
        self.c = qbittorrentapi.Client(host, port, username, password)
        try:
            self.c.auth_log_in()
        except qbittorrentapi.LoginFailed as e:
            print(e)

    def add_torrent(self, file, paused, timeout):
        res = self.c.torrents_add(torrent_files=file, category="byr", is_paused=True)
        if res == "Fails.":
            return None
        time.sleep(3)

        data = bencoding.bdecode(file)
        info = data[b'info']
        info_hash = hashlib.sha1(bencoding.bencode(info)).hexdigest()

        res = torrent_info()
        res.id = info_hash
        return res

    def remove_torrent(self, ids, delete_data, timeout):
        self.c.torrents_delete(torrent_hashes=ids)

    def start_torrent(self, ids, timeout):
        self.c.torrents_resume(torrent_hashes=ids)

    def get_torrent(self, id):
        res = self.c.torrents_info(torrent_hashes=id, category="byr")

        dat = torrent_info()
        dat.total_size = res[0]["size"]  # 不知道能运行不
        dat.name = res[0]["name"]
        dat.id = res[0]["hash"]
        return dat

    def get_torrents(self, timeout):
        res = self.c.torrents_info(category="byr")

        dat=[]
        for elem in res:
            temp = torrent_info()
            temp.date_added=elem["added_on"]
            if elem["state"] is "checkingUP" or elem["state"] is "checkingDL":
                temp.status.checking=True
            else:
                temp.status.checking=False
            if elem["state"] is "downloading":
                temp.status.downloading=True
            else:
                temp.status.downloading=False
            if elem["state"] is "uploading":
                temp.status.downloading=True
            else:
                temp.status.downloading=False
            temp.rateUpload=elem["upspeed"]
            temp.id=elem["hash"]
            temp.total_size=elem["total_size"]
            dat.append(temp)

        return dat

    def free_space(self, path, timeout):
        res = self.c.sync_maindata()
        return res["server_state"]["free_space_on_disk"]  # 不知道能运行不


class status:
    checking=0
    downloading=0

class torrent_info:
    total_size = 0
    name = 0
    id = 0
    info_hash = 0
    date_added = 0
    status=status()
