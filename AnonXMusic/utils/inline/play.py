import math
from pyrogram import enums, types

class Inline:
    def __init__(self):
        self.ikm = types.InlineKeyboardMarkup
        self.ikb = types.InlineKeyboardButton

        self.styles = {
            "default": enums.ButtonStyle.DEFAULT,
            "primary": enums.ButtonStyle.PRIMARY,
            "success": enums.ButtonStyle.SUCCESS,
            "danger": enums.ButtonStyle.DANGER,
        }

    def _button(self, text: str, category: str = "default", **kwargs):
        return self.ikb(
            text=text,
            style=self.styles.get(category, enums.ButtonStyle.DEFAULT),
            **kwargs,
        )

    # MAIN CONTROL HUB
    def track_markup(self, _, chat_id: int, status: str = None, timer_row: list = None, remove: bool = False):
        keyboard = []

        # Abstract Graphic Progress Button sabse upar rahega
        if timer_row:
            keyboard.append(timer_row)
        elif status:
            keyboard.append([self._button(text=status, category="default", callback_data="noop")])

        # MAIN CONTROLS ROW (Sleek Compact Layout - No text on buttons)
        if not remove:
            keyboard.append(
                [
                    self._button(
                        text="▶️",
                        category="success",
                        callback_data=f"ADMIN Resume|{chat_id}",
                    ),
                    self._button(
                        text="⏮️",
                        category="primary",
                        callback_data=f"ADMIN Replay|{chat_id}",
                    ),
                    self._button(
                        text="⏸️",
                        category="primary",
                        callback_data=f"ADMIN Pause|{chat_id}",
                    ),
                    self._button(
                        text="⏭️",
                        category="primary",
                        callback_data=f"ADMIN Skip|{chat_id}",
                    ),
                    self._button(
                        text="⏹️",
                        category="danger",
                        callback_data=f"ADMIN Stop|{chat_id}",
                    ),
                ]
            )

        # FIX: Wrapped in self.ikm() so Pyrogram can read it as a proper markup
        return keyboard 

    # INTERACTIVE MATHEMATICAL GRAPHIC LOOP
    def stream_markup_timer(self, _, chat_id: int, played: str, duration: str):
        # Normal digits ko mathematical bold script fonts mein convert karne ke liye helper
        def to_script_font(time_str):
            font_map = {'0': '𝟬', '1': '𝟭', '2': '𝟮', '3': '𝟯', '4': '𝟰', '5': '𝟱', '6': '𝟲', '7': '𝟳', '8': '𝟴', '9': '𝟵', ':': ':'}
            return "".join(font_map.get(c, c) for c in time_str)

        try:
            p_min, p_sec = map(int, played.split(":"))
            d_min, d_sec = map(int, duration.split(":"))

            played_seconds = (p_min * 60) + p_sec
            total_seconds = (d_min * 60) + d_sec

            percentage = (played_seconds / total_seconds) * 100 if total_seconds > 0 else 0
        except:
            percentage = 0

        # FIX: Corrected Indentation here (8 spaces instead of 7)
        textile_track = ["", "II", "_", "S", "I", "M", "P", "L", "E", "_II"]
        total_steps = len(textile_track)

        active_pos = math.floor((percentage / 100) * total_steps)
        if active_pos >= total_steps:
            active_pos = total_steps - 1

        bar_text = ""
        for i in range(total_steps):
            if i < active_pos:
                # Solid matrix flow blocks (Snake tail/body)
                bar_text += "►" 
            elif i == active_pos:
                # Moving prism node (Active snake head)
                bar_text += "𝋃"
            else:
                # Wave vectors path yet to cover
                bar_text += textile_track[i]

        # Script styled counters build karna
        played_font = to_script_font(played)
        duration_font = to_script_font(duration)

        # Pure graphic layout frame
        full_graphic_bar = f"𝄃 {played_font} ❖ {bar_text} ❖ {duration_font} 𝄃"

        # Action based background color (End phase par automatic Red/Danger ho jayega)
        button_color = "danger" if percentage >= 85 else "success"
        timer_row = [self._button(text=full_graphic_bar, category=button_color, callback_data="noop")]

        return self.track_markup(_, chat_id, timer_row=timer_row)

    # ALL RECOVERY BACKUPS TO PREVENT SYSTEM CRASH
    def playlist_markup(self, _, chat_id: int): return self.track_markup(_, chat_id)
    def livestream_markup(self, _, chat_id: int): return self.track_markup(_, chat_id)
    def slider_markup(self, _, chat_id: int): return self.track_markup(_, chat_id)
    def queue_markup(self, chat_id: int, text: str, playing: bool = False):
        action = "pause" if playing else "resume"
        return self.ikm([[self._button(text=text, category="success" if playing else "danger", callback_data=f"ADMIN {action.capitalize()}|{chat_id}")]])
    def play_queued(self, chat_id: int, item_id: str, text: str):
        return self.ikm([[self._button(text=text, category="success", callback_data=f"ADMIN Resume|{chat_id}")]])
    def yt_key(self, link: str):
        return self.ikm([[self._button(text="📋 Copy Link", category="primary", copy_text=link), self._button(text="🎬 YouTube", category="danger", url=link)]])

buttons = Inline()

# MAPPING ALL VARIABLES FOR FULL PLUGIN COMPATIBILITY
controls = buttons.track_markup
track_markup = buttons.track_markup
stream_markup = buttons.track_markup
stream_markup_timer = buttons.stream_markup_timer
playlist_markup = buttons.playlist_markup
livestream_markup = buttons.livestream_markup
slider_markup = buttons.slider_markup
queue_markup = buttons.queue_markup
play_queued = buttons.play_queued
yt_key = buttons.yt_key