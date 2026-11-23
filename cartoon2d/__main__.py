from cartoon2d import *

def main():
    NewScene("sunset", width_px=480)
    DrawMountain("#5c4a7a", 30, 18, 1.4)
    DrawMountain("#6d5a8c", 75, 18, 1.1)
    sun = DrawSun("gold", 80, 42); Move(sun, (80, 30), 0, 50)
    DrawHouse("tomato", 15, 12)
    car = DrawCar("royalblue", -12, 3, shadow=True)
    Drive(car, (112, 3), 0, 50)
    Say("cartoon2d", 50, 52, 4, 45, color="white")
    Save("cartoon2d_demo.gif", show=False)
    print("wrote cartoon2d_demo.gif")

if __name__ == "__main__":
    main()
