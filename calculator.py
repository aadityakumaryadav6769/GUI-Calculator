import tkinter 
import math

# --- App Configuration & Layout Layout ---
button_values = [
    ["AC", "+/-", "%", "÷"], 
    ["7", "8", "9", "×"], 
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "√", "="]
]

right_symbols = ["÷", "×", "-", "+", "="]
top_symbols = ["AC", "+/-", "%"]

row_count = len(button_values)
column_count = len(button_values[0])

# Modern Dark-Themed Color Palette
color_bg = "#1E1E24"          # Deep charcoal main background
color_display = "#2A2A32"     # Slightly lighter background for the screen
color_light_gray = "#3E3E4A"  # Top functional buttons (AC, +/-, %)
color_dark_gray = "#2D2D37"   # Numeric/digit buttons
color_accent = "#4D7CFF"      # Modern slate blue accent for operations
color_white = "#FFFFFF"       # White text for readability
color_text_muted = "#A0A0AA"  # Muted silver text for the top row

# Hover Palette Mapping
hover_colors = {
    color_light_gray: "#4E4E5A",
    color_dark_gray: "#3D3D47",
    color_accent: "#3B66DF"
}

# --- Window Setup ---
window = tkinter.Tk()
window.title("Calculator")
window.resizable(False, False)
window.config(bg=color_bg)

# Master layout container with breathing room padding
frame = tkinter.Frame(window, bg=color_bg, padx=12, pady=12)
frame.pack()

# Modern, flat text display
label = tkinter.Label(
    frame, text="0", font=("Segoe UI", 42, "bold"), 
    background=color_display, foreground=color_white, 
    anchor="e", width=11, padx=15, pady=20, bd=0, relief="flat"
)
label.grid(row=0, column=0, columnspan=column_count, sticky="we", pady=(0, 12))

# --- Hover Effects Callbacks ---
def on_enter(e, base_color):
    e.widget.config(background=hover_colors.get(base_color, base_color))

def on_leave(e, base_color):
    e.widget.config(background=base_color)

# --- Generate Dynamic Grid ---
for row in range(row_count):
    for column in range(column_count):
        value = button_values[row][column]
        
        # Completely flat UI design via flat relief and zero borders
        button = tkinter.Button(
            frame, text=value, font=("Segoe UI", 20, "bold"),
            width=4, height=2, bd=0, relief="flat", activebackground=color_bg,
            command=lambda value=value: button_clicked(value)
        )
        
        # Color mapping application
        if value in top_symbols:
            bg_col = color_light_gray
            button.config(foreground=color_text_muted, background=bg_col)
        elif value in right_symbols:
            bg_col = color_accent
            button.config(foreground=color_white, background=bg_col)
        else:
            bg_col = color_dark_gray
            button.config(foreground=color_white, background=bg_col)
        
        # Attach hover system listeners
        button.bind("<Enter>", lambda e, bg=bg_col: on_enter(e, bg))
        button.bind("<Leave>", lambda e, bg=bg_col: on_leave(e, bg))
        
        # Clean spacing layout grid
        button.grid(row=row+1, column=column, padx=3, pady=3)

# --- Calculator Logic Engine ---
A = "0"
operator = None
B = None
reset_screen = False  # Tells the screen logic to clear on the next digit keystroke

def clear_all():
    global A, B, operator, reset_screen
    A = "0"
    operator = None
    B = None
    reset_screen = False

def remove_zero_decimal(num):
    if num % 1 == 0:
        num = int(num)
    return str(num)

def button_clicked(value):
    global right_symbols, top_symbols, label, A, B, operator, reset_screen

    # Block further execution if the screen is currently holding an explicit error code
    if "Error" in label["text"] or label["text"] == "Invalid Input":
        if value != "AC":
            return  # Lock interface until explicit AC reset
        
    if value in right_symbols:
        if value == "=":
            if A is not None and operator is not None:
                B = label["text"]
                try:
                    numA = float(A)
                    numB = float(B)

                    # Core operations map
                    if operator == "+":
                        label["text"] = remove_zero_decimal(numA + numB)
                    elif operator == "-":
                        label["text"] = remove_zero_decimal(numA - numB)
                    elif operator == "×":
                        label["text"] = remove_zero_decimal(numA * numB)
                    elif operator == "÷":
                        # Division-by-zero protection guardrail
                        if numB == 0:
                            label["text"] = "Error: Div by 0"
                        else:
                            label["text"] = remove_zero_decimal(numA / numB)
                except ValueError:
                    label["text"] = "Error"
                
                clear_all()
                reset_screen = True

        elif value in "+-×÷":
            if operator is None:
                A = label["text"]
            operator = value
            reset_screen = True

    elif value in top_symbols:
        if value == "AC":
            clear_all()
            label["text"] = "0"

        elif value == "+/-":
            try:
                result = float(label["text"]) * -1
                label["text"] = remove_zero_decimal(result)
            except ValueError:
                pass

        elif value == "%":
            try:
                result = float(label["text"]) / 100
                label["text"] = remove_zero_decimal(result)
            except ValueError:
                pass
            
    elif value == "√":
        try:
            current_val = float(label["text"])
            # Invalid square root protection
            if current_val < 0:
                label["text"] = "Invalid Input"
            else:
                label["text"] = remove_zero_decimal(math.sqrt(current_val))
            reset_screen = True
        except ValueError:
            label["text"] = "Error"
        
    else:  # Numeric Entry and Decimals
        if reset_screen:
            if value == ".":
                label["text"] = "0."
            else:
                label["text"] = value
            reset_screen = False
            return

        if value == ".":
            if value not in label["text"]:
                label["text"] += value
        elif value in "0123456789":
            if label["text"] == "0":
                label["text"] = value
            else:
                label["text"] += value

# --- Window Centering Calculation ---
window.update()  # Force internal rendering to grab accurate dimensions
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width / 2) - (window_width / 2))
window_y = int((screen_height / 2) - (window_height / 2))

# Position geometry application
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")
window.mainloop()

