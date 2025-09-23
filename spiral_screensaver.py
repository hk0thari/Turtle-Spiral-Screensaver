import turtle
import time
import sys
import tkinter as tk
from tkinter import messagebox, ttk
import json
import os


class SpiralScreensaver:
    def __init__(self):
        self.running = True
        self.screen = None
        self.turtle_obj = None
        self.config = self.load_config()

    def load_config(self):
        """Load configuration from file or use defaults"""
        default_config = {
            "background_color": "black",
            "pen_color": "white",
            "speed": 0.03,
            "max_length": 400,
            "step_size": 1,
            "angle_step_size": 0.25,
            "start_length": 5
        }

        try:
            config_path = os.path.join(os.path.expanduser("~"), "spiral_screensaver_config.json")
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    saved_config = json.load(f)
                    default_config.update(saved_config)
        except:
            pass

        return default_config

    def save_config(self, config):
        """Save configuration to file"""
        try:
            config_path = os.path.join(os.path.expanduser("~"), "spiral_screensaver_config.json")
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
        except:
            pass

    def setup_screen(self):
        """Set up the turtle screen for screensaver display"""
        self.screen = turtle.Screen()
        self.screen._RUNNING = True
        self.screen.bgcolor("black")
        self.screen.setup(width=1.0, height=1.0, startx=0, starty=0)
        self.screen.title("Spiral Screensaver")
        self.screen.tracer(0)

        # Bind exit events
        self.screen.onkey(self.exit_screensaver, "Escape")
        self.screen.onkey(self.exit_screensaver, "space")
        self.screen.onclick(self.exit_screensaver)
        self.screen.listen()

        # Try to make it full-screen
        try:
            root = self.screen.getcanvas().winfo_toplevel()
            root.attributes('-fullscreen', True)
            root.attributes('-topmost', True)
            root.configure(cursor="none")  # Hide cursor
        except:
            pass

        return self.screen

    def exit_screensaver(self, *args):
        """Exit the screensaver"""
        self.running = False
        if self.screen:
            try:
                self.screen.bye()
            except:
                pass

    def draw_spiral_pattern(self):
        """Main screensaver animation loop"""
        try:
            self.running = True
            self.setup_screen()

            # Create turtle
            self.turtle_obj = turtle.Turtle()
            self.turtle_obj.speed(0)
            self.turtle_obj.hideturtle()
            self.turtle_obj.penup()
            self.turtle_obj.setpos(0, -150)
            self.turtle_obj.pendown()

            step = self.config["step_size"]
            # Determines how many frames are going to be drawn in total
            # number of frames = (360/angle_step) + 1
            angle_step = self.config["angle_step_size"]
            self.turtle_obj.pencolor(self.config["pen_color"])

            while self.running:
                # + 1 as starting frame is repeated
                for angle in range(int(360 / angle_step + 1)):
                    if not self.running:
                        break

                    self.turtle_obj.clear()

                    # Reset position and settings
                    self.turtle_obj.penup()
                    self.turtle_obj.home()
                    self.turtle_obj.pendown()
                    self.turtle_obj.left(90)

                    length = self.config["start_length"]

                    # Draw the spiral
                    while length < self.config["max_length"] * step and self.running:
                        self.turtle_obj.forward(length)
                        self.turtle_obj.right(angle / 4)
                        length += step

                    if self.running:
                        self.screen.update()
                        # Slow down animation as it approaches 180 degrees, then speed up again
                        # Doing this because the animation otherwise seems to speed up as the angle is close to 180
                        # because the shape changes a lot more
                        time.sleep(self.config["speed"] * (3 - 2 * abs(angle * angle_step - 180) / 360))

        except turtle.Terminator as e:
            pass
        except:
            pass
        finally:
            pass
            # self.exit_screensaver()


def show_config_dialog():
    """Show configuration dialog"""
    screensaver = SpiralScreensaver()
    config = screensaver.config.copy()

    root = tk.Tk()
    root.title("Spiral Screensaver Configuration")
    root.geometry("500x600")
    root.resizable(False, False)

    # Color options
    colors = ["black", "white", "red", "green", "blue", "purple", "orange", "yellow", "pink", "cyan"]

    # Background Color
    tk.Label(root, text="Background Color:", font=("Arial", 10, "bold")).pack(pady=5)
    bg_var = tk.StringVar(value=config["background_color"])
    bg_combo = ttk.Combobox(root, textvariable=bg_var, values=colors, state="readonly")
    bg_combo.pack(pady=5)

    # Pen Color
    tk.Label(root, text="Pen Color:", font=("Arial", 10, "bold")).pack(pady=5)
    pen_var = tk.StringVar(value=config["pen_color"])
    pen_combo = ttk.Combobox(root, textvariable=pen_var, values=colors, state="readonly")
    pen_combo.pack(pady=5)

    # Speed
    tk.Label(root, text="Animation Speed:", font=("Arial", 10, "bold")).pack(pady=5)
    speed_var = tk.DoubleVar(value=config["speed"])
    speed_frame = tk.Frame(root)
    speed_frame.pack(pady=5)
    tk.Label(speed_frame, text="Fast").pack(side=tk.LEFT)
    speed_scale = tk.Scale(speed_frame, from_=0.01, to=0.1, resolution=0.01,
                           orient=tk.HORIZONTAL, variable=speed_var, length=200)
    speed_scale.pack(side=tk.LEFT, padx=10)
    tk.Label(speed_frame, text="Slow").pack(side=tk.RIGHT)

    # Max Length
    tk.Label(root, text="Spiral Size:", font=("Arial", 10, "bold")).pack(pady=5)
    length_var = tk.IntVar(value=config["max_length"])
    length_frame = tk.Frame(root)
    length_frame.pack(pady=5)
    tk.Label(length_frame, text="Small").pack(side=tk.LEFT)
    length_scale = tk.Scale(length_frame, from_=100, to=500, orient=tk.HORIZONTAL,
                            variable=length_var, length=200)
    length_scale.pack(side=tk.LEFT, padx=10)
    tk.Label(length_frame, text="Large").pack(side=tk.RIGHT)

    # Step Size
    tk.Label(root, text="Line Density:", font=("Arial", 10, "bold")).pack(pady=5)
    step_var = tk.IntVar(value=config["step_size"])
    step_frame = tk.Frame(root)
    step_frame.pack(pady=5)
    tk.Label(step_frame, text="Dense").pack(side=tk.LEFT)
    step_scale = tk.Scale(step_frame, from_=1, to=5, orient=tk.HORIZONTAL,
                          variable=step_var, length=200)
    step_scale.pack(side=tk.LEFT, padx=10)
    tk.Label(step_frame, text="Sparse").pack(side=tk.RIGHT)

    # Angle Step Size
    tk.Label(root, text="Angle Step Size:", font=("Arial", 10, "bold")).pack(pady=5)
    angle_step_var = tk.DoubleVar(value=config["angle_step_size"])
    angle_step_frame = tk.Frame(root)
    angle_step_frame.pack(pady=5)
    tk.Label(angle_step_frame, text="Small").pack(side=tk.LEFT)
    angle_step_scale = tk.Scale(angle_step_frame, from_=0.1, to=1, resolution=0.01, orient=tk.HORIZONTAL,
                                variable=angle_step_var, length=200)
    angle_step_scale.pack(side=tk.LEFT, padx=10)
    tk.Label(angle_step_frame, text="Large").pack(side=tk.RIGHT)

    # Preview button
    def preview_settings():
        # Update config with current values
        temp_config = {
            "background_color": bg_var.get(),
            "pen_color": pen_var.get(),
            "speed": speed_var.get(),
            "max_length": length_var.get(),
            "step_size": step_var.get(),
            "angle_step_size": angle_step_var.get(),
            "start_length": config["start_length"]
        }

        # Save temp config and run preview
        screensaver.config = temp_config
        root.withdraw()
        try:
            screensaver.draw_spiral_pattern()
        except:
            pass
        root.deiconify()

    tk.Button(root, text="Preview", command=preview_settings,
              bg="lightblue", font=("Arial", 10)).pack(pady=10)

    # Save and Cancel buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=20)

    def save_settings():
        new_config = {
            "background_color": bg_var.get(),
            "pen_color": pen_var.get(),
            "speed": speed_var.get(),
            "max_length": length_var.get(),
            "step_size": step_var.get(),
            "angle_step_size": angle_step_var.get(),
            "start_length": config["start_length"]
        }
        screensaver.save_config(new_config)
        messagebox.showinfo("Settings Saved", "Your screensaver settings have been saved!")
        root.destroy()

    def cancel_settings():
        root.destroy()

    tk.Button(button_frame, text="Save", command=save_settings,
              bg="lightgreen", font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Cancel", command=cancel_settings,
              bg="lightcoral", font=("Arial", 10)).pack(side=tk.LEFT, padx=10)

    # Instructions
    instructions = tk.Text(root, height=4, width=45, font=("Arial", 8))
    instructions.pack(pady=10)
    instructions.insert("1.0", "Instructions:\n"
                               "• Choose your preferred colors and settings\n"
                               "• Click 'Preview' to test your settings\n"
                               "• Click 'Save' to apply changes\n"
                               "• Press Escape during preview to return here")
    instructions.config(state=tk.DISABLED)

    root.mainloop()


def main():
    """Main entry point"""
    # Check command line arguments for Windows screensaver integration
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg.startswith('/s'):  # Start screensaver
            screensaver = SpiralScreensaver()
            screensaver.draw_spiral_pattern()
        elif arg.startswith('/c'):  # Configure screensaver
            show_config_dialog()
        elif arg.startswith('/p'):  # Preview mode
            # For preview mode, normally you'd draw in a small window,
            # but I'm just gonna draw it in full screen mode for convenience
            screensaver = SpiralScreensaver()
            screensaver.draw_spiral_pattern()
    else:
        # Default behavior - run screensaver
        screensaver = SpiralScreensaver()
        screensaver.draw_spiral_pattern()

    sys.exit()


if __name__ == "__main__":
    main()
