from mpos.apps import Activity
import mpos.ui
import lvgl as lv

DARKPINK = lv.color_hex(0xEC048C)
CURSOR_COLOR = lv.color_hex(0x00FF00)  # Green cursor
CURSOR_DRAWING_COLOR = lv.color_hex(0xFF0000)  # Red cursor when drawing

class QuasiDoodle(Activity):

    hor_res = 0
    ver_res = 0

    # Widgets:
    canvas = None

    # Cursor state
    cursor_x = 0
    cursor_y = 0
    is_drawing = False
    cursor_step = 5  # How many pixels to move per key press
    cursor_backup = {}  # Store pixels under cursor to restore them later

    def onCreate(self):
        screen = lv.obj()
        self.canvas = lv.canvas(screen)
        disp = lv.display_get_default()
        self.hor_res = disp.get_horizontal_resolution()
        self.ver_res = disp.get_vertical_resolution()
        self.canvas.set_size(self.hor_res, self.ver_res)
        self.canvas.set_style_bg_color(lv.color_white(), 0)
        buffer = bytearray(self.hor_res * self.ver_res * 4)
        self.canvas.set_buffer(buffer, self.hor_res, self.ver_res, lv.COLOR_FORMAT.RGB888)
        self.canvas.fill_bg(lv.color_white(), lv.OPA.COVER)

        # Initialize cursor at center
        self.cursor_x = self.hor_res // 2
        self.cursor_y = self.ver_res // 2

        # Make canvas focusable and add to focus group
        self.canvas.add_flag(lv.obj.FLAG.CLICKABLE)
        focusgroup = lv.group_get_default()
        if focusgroup:
            focusgroup.add_obj(self.canvas)

        # Add key event handler
        self.canvas.add_event_cb(self.key_cb, lv.EVENT.KEY, None)

        # Draw initial cursor
        self.draw_cursor()

        self.setContentView(screen)

    def key_cb(self, event):
        key = event.get_key()

        # If we're in drawing mode and about to move, draw paint at current position first
        if self.is_drawing and key in [lv.KEY.UP, lv.KEY.DOWN, lv.KEY.LEFT, lv.KEY.RIGHT]:
            self.draw_paint()

        # Clear old cursor
        self.clear_cursor()

        # Handle arrow keys
        if key == lv.KEY.UP:
            self.cursor_y = max(0, self.cursor_y - self.cursor_step)
        elif key == lv.KEY.DOWN:
            self.cursor_y = min(self.ver_res - 1, self.cursor_y + self.cursor_step)
        elif key == lv.KEY.LEFT:
            self.cursor_x = max(0, self.cursor_x - self.cursor_step)
        elif key == lv.KEY.RIGHT:
            self.cursor_x = min(self.hor_res - 1, self.cursor_x + self.cursor_step)
        elif key == lv.KEY.ENTER:
            # Toggle drawing mode
            self.is_drawing = not self.is_drawing
            print(f"Drawing mode: {'ON' if self.is_drawing else 'OFF'}")

        # Draw new cursor
        self.draw_cursor()

    def draw_cursor(self):
        """Draw the cursor at current position, saving what's underneath"""
        radius = 4
        cursor_color = CURSOR_DRAWING_COLOR if self.is_drawing else CURSOR_COLOR
        square = radius * radius
        self.cursor_backup = {}

        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if dx * dx + dy * dy <= square:
                    newx, newy = self.cursor_x + dx, self.cursor_y + dy
                    if 0 <= newx < self.hor_res and 0 <= newy < self.ver_res:
                        # Save the pixel color before drawing cursor (as RGB values)
                        pixel = self.canvas.get_px(newx, newy)
                        self.cursor_backup[(newx, newy)] = (pixel.red, pixel.green, pixel.blue)
                        # Draw cursor
                        self.canvas.set_px(newx, newy, cursor_color, lv.OPA.COVER)

    def clear_cursor(self):
        """Clear the cursor at current position by restoring saved pixels"""
        for (x, y), (r, g, b) in self.cursor_backup.items():
            if 0 <= x < self.hor_res and 0 <= y < self.ver_res:
                # Reconstruct color from RGB values
                restored_color = lv.color_hex((r << 16) | (g << 8) | b)
                self.canvas.set_px(x, y, restored_color, lv.OPA.COVER)
        self.cursor_backup = {}

    def draw_paint(self):
        """Draw paint at current cursor position"""
        radius = 7
        square = radius * radius

        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if dx * dx + dy * dy <= square:
                    newx, newy = self.cursor_x + dx, self.cursor_y + dy
                    if 0 <= newx < self.hor_res and 0 <= newy < self.ver_res:
                        self.canvas.set_px(newx, newy, DARKPINK, lv.OPA.COVER)
