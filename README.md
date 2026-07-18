# Pen plotter
## A simple pen plotter using an esp32, stepper motors, a servo and timing belts
### Demo videos
- [Demo 1 - Hilbert curves](https://www.youtube.com/watch?v=iywQXDerfF4)  
- [Demo 2 - Cat](https://www.youtube.com/shorts/F5tRbeLazfQ)  
- [Demo 3 - Triangles](https://www.youtube.com/shorts/Yr_N4DkdwpU)  
- [Demo 4 - Another Cat](https://www.youtube.com/shorts/lvt_kN0ZHD0)  

### Capabilities
#### It can convert images into lines, where the amount of lines shows the darkness of the pixels. Also, it can use canny edge detection to convert images into paths, and from there into drawings
<img width="2944" height="2944" alt="cat" src="https://github.com/user-attachments/assets/695f1675-c3b9-4812-8ed7-74dfc011bc83" />  
<img width="424" height="405" alt="{EF9DE653-6C88-40CC-B70B-28055ED8D5D0}" src="https://github.com/user-attachments/assets/1fdd371d-64c7-4bc8-8b82-8d609a61aae8" />


#### It can also draw hilbert curves and sierpinski triangles
<img width="1044" height="800" alt="{B3DB4044-183A-462D-B0FC-778355AC7D37}" src="https://github.com/user-attachments/assets/ba4afe40-388b-43df-954d-12a8b27feb54" />  
<img width="526" height="761" alt="{AF7F2D5E-4E53-49CD-B731-9960951EA636}" src="https://github.com/user-attachments/assets/fb1e3ad1-e5be-47b3-b9bd-43c51e050423" />

#### Other features
- Auto Homing: Can return to (0, 0) automatically
- E-Stop Button: Stop suddenly when things go wrong
- Adjustable Pen Holder: Support for pens of all shapes and sizes
- Easy Assembly (Well... It's not that easy, but easier than the last version)
- Precise movement


### Design
The plotter uses a cartesian gantry system. Originally I was going to use a bed slinger system, like the Bambu Lab A1 Mini, however I decided to redesign it to corexy. After I realised how hard corexy would be to implement, I modified it to use the gantry.  
<img width="914" height="576" alt="{F74FA99E-C383-4A17-BCB6-C585A155FD70}" src="https://github.com/user-attachments/assets/8553e9d4-c45f-4ca0-9b8e-1baf8fac443a" />

There's 3 stepper motors, driven by 2 A4988 drivers. 2 of the motors are wired in series on the drivers, which makes sense since they're both on the y axis.

**Electronics**
- I used an ESP32, which is useful because it runs python, runs wifi, and is also far more capable than an arduino. I'm not using the wifi at the moment but might do later.
- The stepper drivers are A4988. I used generic breakout boards and soldered together a custom board with them that integrates the 2 of them with merged power, enable and gnd pins.
- The steppers are generic nema 17 motors, using 1/16 step
- The servo is a cheap SG90

### Print settings
- .28mm layer height, ~20-30% gyroid infill
- Auto supports
- Almost anything would work to be honest as long as it prints

### BOM
- 8mmx300mm steel linear rod (4x)
- M3 Nuts/Bolts
- NEMA 17 Stepper motors (3x)
- GT2 Timing belts (~3m)
- GT2 Spring belt tensioners (4-8x)
- GT2 Idlers (3x)
- GT2 Drive Pulleys (3x)
- Any random button/microswitch (3x)
- _Some_ M5 bolts (although 3d printed replacements would do)
- Wood screws/hot glue (anything to attach to baseboard)

### Build advice
If you want to print this yourself, I wouldn't recommend it. While it is in a working state, there are a lot of issues with the build that either make it a pain to build or just not work at all. If you do insist on building it yourself, find some random piece of wood or plastic to use as the baseboard. In a future version I'll improve the mounting holes and also make a semi-ridgid frame to help align it.

#### Instructions
1. Attach motors to parts using M3 screws.
2. Put the pen lift arm on the carriage
3. Assemble all the parts as shown without the timing belts. Take care not to bend the steel rods
4. Add the timing belts. Try to make them as tight as possible
5. If needed, add belt tensioning springs.
6. Wire the 2 Y axis motors in series
7. Either create or buy some dual stepper driver board (note that the 3 are treated as 2 motors because 2 of them are in series)
8. Press fit the servo into place, and (depending on print precision) add screws to hold in place if needed


### Credits
- Sierpinski triangle algorithm modified from https://runestone.academy/ns/books/published/pythonds/Recursion/pythondsSierpinskiTriangle.html
- Hilbert curve algorithm modified from https://www.compuphase.com/hilbert.htm
- Parts of edge detection algorithm modified from https://learnopencv.com/edge-detection-using-opencv/

### AI Usage
AI was used in doing research on components and design ideas, as well as for troubleshooting, and for advice about algorithms to use. It was also used for doing research on micropython and debugging code
