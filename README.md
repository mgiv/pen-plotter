# Pen plotter
## A simple pen plotter using an esp32, stepper motors, a servo and some sewing thread.
### Why?
My handwriting has always been quite bad, and because of that I want to be able to get a robot to write for me. Instead of using a regular solution like typing into word, I want to have a robot draw writing onto paper.
### Design
**X Axis**
- The X axis uses a stepper motor with a spool on it. The spool is split into 2 different halves, one of which pulls in, and the other pushes. This ensures that the carriage in the centre moves.  
- This is somewhat similar in design to a capstan drive, the main difference being that the thread is fixed instead of allowing to move freely. This means that it won't go round and round forever, but in this case that isn't a problem.  
- At the end is a spool, this one with 2 ball bearings to keep it moving smoothly. There are adjustable screws to allow for tensioning the drive
- The carriage is set on 2 steel rods, which are fixed at the enns, and holds the servo motor for tilting the pen up and down  
- The pen uses a hinge system, with it swinging towards the paper due to gravity. When the servo is activated, it pushes the swing arm up, and swings the pen off the paper.  
- This can have problems when the paper isn't flat or secured down properly, so in the future when I make the Y axis I will make sure the paper is clamped down properly

**Electronics**
- I used an ESP32, which is useful because it runs python, runs wifi, and is also far more capable than an arduino. I'm not using the wifi at the moment but might do later.
- The stepper drivers are A4988. I used generic breakout boards and soldered together a custom board with them that integrates the 2 of them with merged power, enable and gnd pins.
- The steppers are generic nema 17 motors, using 1/16 step
- The servo is a cheap SG90
- At some point, I'll add a screen to show print times, similar to the display on a 3d printer.
