from dataclasses import dataclass
from datetime import datetime
from email import message
from email.errors import MessageError
import json
from database import *
import copy
import re


attr = {
    "region": {"1": "America", "2": "Europe", "3": "Asia"},
    "ladder": {"1": "Ladder", "2": "Non-Ladder"},
    "hc": {"1": "Hardcode", "2": "Softcore"},
    "progress": {
        "1": "1. Terror gazes upon Sanctuary.",
        "2": "2. Terror approaches Sanctuary.",
        "3": "3. Terror begins to form within Sanctuary.",
        "4": "4. Terror spreads across Sanctuary.",
        "5": "5. Terror is about to be unleashed upon Sanctuary.",
        "6": "6. Diablo has invaded Sanctuary.",
    },
}


class User:
    def __init__(self, chat_id) -> None:
        self.chat_id = chat_id
        self.region = "1|2|3"
        self.hc = "2"
        self.ladder = "1"
        self.progress = "4|5|6"
        self.existing = False

    # def sync_from_db(self):
    #     user = self.database.get_user(self.chat_id)

    def print_json(self):
        item = copy.deepcopy(self.__dict__)
        item = json.dumps(item, ensure_ascii=False, sort_keys=True, indent=4)
        print(item)
        return item

    def subscription_str(self):
        region = ", ".join(map_attr(self.region, "region"))
        hc = ", ".join(map_attr(self.hc, "hc"))
        ladder = ", ".join(map_attr(self.ladder, "ladder"))
        progress = self.progress.replace("|", ", ")

        warning = ""

        if len(region) <= 0:
            region = "none, /add NA/EU/ASIA to add one"
            warning = "!!!! none status will stop app sending you message"

        if len(hc) <= 0:
            hc = "none, /add hardcore/softcare to add one"
            warning = "none status will stop app sending you message"

        if len(ladder) <= 0:
            ladder = "none, /add ladder/non-ladder to add one"
            warning = "!!!! none status will stop app sending you message"

        if len(progress) <= 0:
            progress = "none, /add progress 1/2/3/4/5/6 to add one"
            warning = "none status will stop app sending you message"

        message = f"""Region: {region}\nCoreness: {hc}\nLadder: {ladder}\nProgress: {progress} \n\n{warning}"""
        print(message)
        return message


def map_attr(items, attr_name):
    items = items.split("|")
    try:
        items.remove("")
    except:
        pass
    return [attr[attr_name][item] for item in items]


def append_db_string(original, new):
    array = original.split("|")
    try:
        array.remove("")
    except:
        pass

    if new not in array:
        array.append(new)
    array.sort()

    return "|".join(array)


def remove_db_string(original, new):
    array = original.split("|")
    try:
        array.remove("")
    except:
        pass

    if new in array:
        array.remove(new)
    array.sort()

    return "|".join(array)


class UserController:
    def __init__(self, chat_id) -> None:
        self.database = DcloneDB()
        self.user = User(chat_id)

        self.user.existing = self.database.is_existing_user(chat_id)

        if self.user.existing:
            self.sync_from_db()

    def sync_from_db(self):
        user = self.database.get_user(self.user.chat_id)
        self.user.region = user["sub_regions"]
        self.user.hc = user["sub_hc"]
        self.user.ladder = user["sub_ladder"]
        self.user.progress = user["sub_progress"]

    def subscribe_default(self):
        self.database.put_user(self.user)

    def user_json(self):
        return self.user.print_json()

    def unsub_user(self):
        self.database.delete_user(self.user.chat_id)

    def update_user(self, message):
        ret_message = ["Not Valid"]
        message = message.lower()
        if "/add" in message:
            print("add stuff")
            if " na" in message or " us" in message or "america" in message:
                self.user.region = append_db_string(self.user.region, "1")
                ret_message += [f"subscribed to America Region"]

            if " eu" in message or "europe" in message:
                self.user.region = append_db_string(self.user.region, "2")
                ret_message += [f"subscribed to Europe Region"]

            if "asia" in message:
                self.user.region = append_db_string(self.user.region, "3")
                ret_message += [f"subscribed to Asia Region"]

            if "hardcore" in message:
                self.user.hc = append_db_string(self.user.hc, "1")
                ret_message += [f"subscribed to hardcore"]

            if "softcore" in message:
                self.user.hc = append_db_string(self.user.hc, "2")
                ret_message += [f"subscribed to softcore"]

            if " ladder" in message:
                self.user.ladder = append_db_string(self.user.ladder, "1")
                ret_message += [f"subscribed to ladder"]
            if "non-ladder" in message:
                self.user.ladder = append_db_string(self.user.ladder, "2")
                ret_message += [f"subscribed to non-ladder"]

            if "progress" in message:
                nums = re.sub("[^0-9]", "", str(message))
                for num in nums:
                    self.user.progress = append_db_string(self.user.progress, num)
                    ret_message += [f"subscribed to progress {num}"]

        if "/remove" in message:
            print("remove stuff")

            if " na" in message or " us" in message or "america" in message:
                self.user.region = remove_db_string(self.user.region, "1")
                ret_message += [f"unsubscribed from America Region"]

            if " eu" in message or "europe" in message:
                self.user.region = remove_db_string(self.user.region, "2")
                ret_message += [f"unsubscribed from Europe Region"]

            if "asia" in message:
                self.user.region = remove_db_string(self.user.region, "3")
                ret_message += [f"unsubscribed from Asia Region"]

            if "hardcore" in message:
                self.user.hc = remove_db_string(self.user.hc, "1")
                ret_message += [f"unsubscribed from hardcore"]

            if "softcore" in message:
                self.user.hc = remove_db_string(self.user.hc, "2")
                ret_message += [f"unsubscribed from softcore"]

            if " ladder" in message:
                self.user.ladder = remove_db_string(self.user.ladder, "1")
                ret_message += [f"unsubscribed from ladder"]

            if "non-ladder" in message:
                self.user.ladder = remove_db_string(self.user.ladder, "2")
                ret_message += [f"unsubscribed from non-ladder"]

            if "progress" in message:
                nums = re.sub("[^0-9]", "", str(message))
                for num in nums:
                    self.user.progress = remove_db_string(self.user.progress, num)
                    ret_message += [f"unsubscribed from progress {num}"]

        if len(ret_message) > 1:
            ret_message = "\n".join(ret_message[1:])
        else:
            ret_message = "\n".join(ret_message)

        self.user_json()
        self.database.update_user(self.user)
        return ret_message

    def related_status(self, all=False):
        user = self.user
        if not all:
            regions = user.region.split("|")
            hc = user.hc.split("|")
            ladder = user.ladder.split("|")
        else:
            regions = attr["region"].keys()
            hc = attr["hc"].keys()
            ladder = attr["ladder"].keys()

        message = []
        for climb in ladder:
            for core in hc:
                for region in regions:
                    result = self.database.find_status(region, core, climb)
                    if result:
                        region_str = attr["region"][str(result["region"])]
                        hc_str = attr["hc"][str(result["hc"])]
                        ladder_str = attr["ladder"][str(result["ladder"])]
                        message.append(
                            f"""{result['progress']}/6 {region_str} / {hc_str} / {ladder_str} """
                        )
        message = "\n".join(message)
        return message


class Status:
    def __init__(self, record) -> None:
        self.region = record["region"]
        self.hc = record["hc"]
        self.ladder = record["ladder"]
        self.progress = record["progress"]
        self.time = record["timestamped"]

        self.region_str = attr["region"][self.region]
        self.hc_str = attr["hc"][self.hc]
        self.ladder_str = attr["ladder"][self.ladder]
        self.progress_str = attr["progress"][self.progress]

        # print(datetime.fromtimestamp(int(record["timestamped"])))

    def print_json(self):
        item = copy.deepcopy(self.__dict__)
        item = json.dumps(item, ensure_ascii=False, sort_keys=True, indent=4)
        print(item)
        return item


class StatusController:
    def __init__(self, record) -> None:
        self.database = DcloneDB()
        self.status = Status(record)

        self.status.existing = self.database.is_existing_status(self.status)

        if not self.status.existing:
            print("new status", record)
            self.record_status()
        else:
            pass

    def record_status(self):
        self.database.put_status(self.status)

    def status_not_exist(self):
        return self.status.existing == False

    def user_json(self):
        return self.status.print_json()

    def get_users_subbed(self):
        return self.database.get_subscribed_users(self.status)


if __name__ == "__main__":
    user = UserController("")
    user.related_status()
