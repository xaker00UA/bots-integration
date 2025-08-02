import yaml
import os
from src.models.model import RestUser
from datetime import datetime, timedelta


class Responses:
    def __init__(self, path: str):
        with open(path, encoding="utf-8") as f:
            self._data = yaml.safe_load(f)

    def get(self, *keys, default=None) -> str:
        ref = self._data
        for key in keys:
            if key in ref:
                ref = ref[key]
            else:
                return default
        return ref


class SafeFormatDict(dict):
    def __missing__(self, key):
        return f"-"  # или верни дефолтное значение, например `"-"`


class GenerateStatsMessage:
    def __init__(self):
        self.response = Responses(
            os.path.join(os.getcwd(), "src", "locales", "telegram", "messages.yaml")
        )

    def relative_time(self, seconds: int) -> str:

        if seconds < 60:
            return "менее минуты назад"
        elif seconds < 3600:
            return f"{seconds // 60} мин. назад"
        elif seconds < 86400:
            return f"{seconds // 3600} ч. назад"
        else:
            return f"{seconds // 86400} дн. назад"

    def render_tanks(self, tanks: list[dict]) -> str:
        if not tanks:
            return "❌ Нет данных о танках."

        lines = ["\n🛡️ <b>Танки:</b>\n"]

        for tank in tanks:
            all_stats = tank.get("all", {})
            lines.append(
                f"<b>{tank.get('name')}</b> (уровень: {tank.get('level')})\n"
                f" Бои: {all_stats.get('battles', 0)}, \n"
                f"Победы: {all_stats.get('winrate', 0)}%, \n"
                f"Урон: {all_stats.get('damage', 0)}\n"
                f"Точность: {all_stats.get('accuracy', 0)}%, \n"
                f"Выжываемость: {all_stats.get('survival', 0)}%, \n"
            )
        return "\n".join(lines)

    def flatten(self, d: dict, parent_key: str = "", sep: str = "_"):
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self.flatten(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    def render_rating(self, rating: dict) -> str:
        if not rating:
            return "❌ Нет данных о рейтинге."
        string = f"""-----------------------------------------------
        \n🛡️ <b>Рейтинг:</b>\n
        Бои: {rating.get('battles', 0)}, \n"
        f"Победы: {rating.get('winrate', 0)}%, \n"
        f"Урон: {rating.get('damage', 0)},\n"
        f"Точность: {rating.get('accuracy', 0)}%, \n"
        f"Выжываемость: {rating.get('survival', 0)}%, \n"
        """
        return string

    def send_message(self, user: RestUser | str) -> str:
        if isinstance(user, str):
            return user
        if not user.general.session.all and not user.general.session.rating:
            return self.response.get("get_session", "no_battle")
        user = user.model_dump()
        user["time"] = self.relative_time(user["time"])
        tanks_md = self.render_tanks(user.get("tanks", {}).get("session", []))
        data = self.flatten(user)
        data["tanks"] = tanks_md
        data["rating"] = self.render_rating(
            user.get("general", {}).get("session", {}).get("rating")
        )
        template = self.response.get("get_session", "success")
        text = template.format_map(SafeFormatDict(data))
        return text


message_res = Responses(
    os.path.join(os.getcwd(), "src", "locales", "telegram", "messages.yaml")
)
