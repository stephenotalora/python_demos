__author__ = 'jotalora'
# url: http://www.codeskulptor.org/#user38_4NmbShwS2w_6.py
# template for "Stopwatch: The Game"
import simplegui

# define global variables
timer = 0
tenthSec = 0
tList = [0] * 4
x = 0 # number of successful stops
y = 0 # number of total stops
hasStopped = False

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    global tList
    temp = t # local value so that left most value can be calculated
    # pop digits every tenth of a second or half
    if t > 599 and t < 999: t %= 100  # check to see if t is valid tenth of a second if so pop left most value
    else: t %= 600 # other reset
    #decompose t
    for index in range(3, 0, -1):
        tList[index] = t%10
        t/=10
    tList[0] = temp / 600 # increment seconds until left most int overflows i.e. > 10 mins. good luck waiting that long lol
    #build str and return
    return (str(tList[0]) if tList[0] > 9 else '0' + str(tList[0])) + ':' + str(tList[1]) + str(tList[2]) + '.' + str(tList[3])

# define event handlers for buttons; "Start", "Stop", "Reset"
def start_timer():
    global timer, hasStopped
    if hasStopped: hasStopped = False
    if not timer: timer = simplegui.create_timer(100, interval_handler)
    timer.start()

def stop_handler():
    global x, y, hasStopped
    if not hasStopped:
        if not tList[3]:
            x+=1
        hasStopped = True
        y += 1
    timer.stop()

def reset_handler():
    global tenthSec, x, y, hasStopped
    tenthSec = 0
    x = 0
    y = 0
    hasStopped = False
    timer.stop()

# define event handler for timer with 0.1 sec interval
def interval_handler():
    global tenthSec
    tenthSec += 1

# define draw handler
def draw_handler(canvas):
    canvas.draw_text(format(tenthSec), [100,125], 40, 'White')
    canvas.draw_text(str(x) + '/' + str(y), [260, 25] if y < 10 else [240, 25], 30, 'Red' if hasStopped else 'Green')

# create frame
frame = simplegui.create_frame('Stopwatch: The Game', 300, 250)
frame.add_button('Start', start_timer, 100)
frame.add_button('Stop', stop_handler, 100)
frame.add_button('Reset', reset_handler, 100)

# register event handlers
frame.set_draw_handler(draw_handler)

# start frame
frame.start()

# Please remember to review the grading rubric

