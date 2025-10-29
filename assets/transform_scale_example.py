from mpos.apps import Activity
import lvgl as lv

class Draw2(Activity):
    """
    Opacity and Transformations Example
    Based on lv_example_style_15
    """

    def onCreate(self):
        print("=== Draw2.onCreate START ===")
        screen = lv.obj()

        # Normal button
        btn = lv.button(screen)
        btn.set_size(100, 40)
        btn.align(lv.ALIGN.CENTER, 0, -70)

        label = lv.label(btn)
        label.set_text("Normal")
        label.center()

        # Set opacity
        # The button and the label is rendered to a layer first and that layer is blended
        btn = lv.button(screen)
        btn.set_size(100, 40)
        btn.set_style_opa(lv.OPA._50, 0)
        btn.align(lv.ALIGN.CENTER, 0, 0)

        label = lv.label(btn)
        label.set_text("Opa:50%")
        label.center()

        # Set transformations
        # The button and the label is rendered to a layer first and that layer is transformed
        btn = lv.button(screen)
        btn.set_size(100, 40)
        btn.set_style_transform_rotation(150, 0)  # 15 deg
        btn.set_style_transform_scale(256 + 64, 0)  # 1.25x
        btn.set_style_transform_pivot_x(50, 0)
        btn.set_style_transform_pivot_y(20, 0)
        btn.set_style_opa(lv.OPA._50, 0)
        btn.align(lv.ALIGN.CENTER, 0, 70)

        label = lv.label(btn)
        label.set_text("Transf.")
        label.center()

        self.setContentView(screen)
        print("=== Draw2.onCreate COMPLETE ===")
