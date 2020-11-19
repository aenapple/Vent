import ctypes
import matplotlib.pyplot as plt
import pprint
import matplotlib.gridspec as gridspec
import os.path

def set_horizontal_marker(ax, y, color='b'):
    ax.plot(ax.get_xlim(), [y]*2,'--', color=color)

class Struct2StringMixin():
    def __str__(self):
        s = []
        for r in self._fields_:
            n = r[0]
            t = r[1]
            s.append( str(n) + " = " + str(self.__getattribute__(n)))
        return '{%s}' % ',\n'.join(s)
    
    def __repr__(self):
        return self.__str__()

"""
typedef struct
{
    uint8_t input_open:1,
            input_blocked:1,
            exit_open:1,
            exit_blocked:1,
            drum_enter_open:1,
            drum_enter_blocked:1,
            drum_home_open:1,
            drum_home_blocked:1;
} tEventLogModuleState;
"""
class tEventLogModuleState(Struct2StringMixin, ctypes.Structure):
    _pack_ = 1
    _fields_ = [
    ('input_open', ctypes.c_uint8, 1),
    ('input_blocked', ctypes.c_uint8, 1),
    ('exit_open', ctypes.c_uint8, 1),
    ('exit_blocked', ctypes.c_uint8, 1),
    ('drum_enter_open', ctypes.c_uint8, 1),
    ('drum_enter_blocked', ctypes.c_uint8, 1),
    ('drum_home_open', ctypes.c_uint8, 1),
    ('drum_home_blocked', ctypes.c_uint8, 1),
    ]
"""
typedef struct
{
    uint16_t input1_open:1,
             input1_blocked:1,
             input2_open:1,
             input2_blocked:1,
             exit_open:1,
             exit_blocked:1,
             laser_open:1,
             laser_blocked:1,
             laser_blocked_double:1,
             //TSHeadMovingSM HeadMovingSM fields
             //TSHeadPlatform HeadPlatform fields
             scan_open:1,
             scan_blocked:1;
            // added from 12/11/2018 !!!
             uint8_t laser_value;
} tEventLogHeadState;
"""
class tEventLogHeadState(Struct2StringMixin, ctypes.Structure):
    _pack_ = 1
    _fields_ = [
    ('input1_open', ctypes.c_uint16, 1),
    ('input1_blocked', ctypes.c_uint16, 1),
    ('input2_open', ctypes.c_uint16, 1),
    ('input2_blocked', ctypes.c_uint16, 1),
    ('exit_open', ctypes.c_uint16, 1),
    ('exit_blocked', ctypes.c_uint16, 1),
    ('laser_open', ctypes.c_uint16, 1),
    ('laser_blocked', ctypes.c_uint16, 1),
    ('laser_blocked_double', ctypes.c_uint16, 1),
    ('scan_open', ctypes.c_uint16, 1),
    ('scan_blocked', ctypes.c_uint16, 1),
    ('latch_blocked', ctypes.c_uint16, 1),
    ('platform_blocked', ctypes.c_uint16, 1),
    ('front_lid_blocked', ctypes.c_uint16, 1),
    #('_dummy', ctypes.c_uint16, 2),
    ('laser_value', ctypes.c_uint8),
    ('laser_specle_value', ctypes.c_uint8),
    ]
"""
typedef struct
{
    uint8_t box_open:1,
            box_blocked:1,
            cycle_open:1,
            cycle_blocked:1;
} tEventLogFrameState;
"""
class tEventLogFrameState(Struct2StringMixin, ctypes.Structure):
    _pack_ = 1
    _fields_ = [
    ('box_open', ctypes.c_uint8, 1),
    ('box_blocked', ctypes.c_uint8, 1),
    ('cycle_open', ctypes.c_uint8, 1),
    ('cycle_blocked', ctypes.c_uint8, 1),
    ]
"""
typedef struct
{
    int8_t pwm; // in percent plus sign selects direction
    uint16_t steps;
} tEventLogMotorState;
"""
class tEventLogMotorState(Struct2StringMixin, ctypes.Structure):
    _pack_ = 1
    _fields_ = [
    ('pwm', ctypes.c_int8),
    ('steps', ctypes.c_uint16),
    ]
"""
typedef struct
{
    int8_t pwm;
} tEventLogSolenoidState;
"""
class tEventLogSolenoidState(Struct2StringMixin, ctypes.Structure):
    _pack_ = 1
    _fields_ = [
    ('pwm', ctypes.c_uint8),
    ]
    
"""
typedef struct
{
    int8_t pwm;
} tEventLogSimpleMotorState;
"""
class tEventLogSimpleMotState(Struct2StringMixin, ctypes.Structure):
    _pack_ = 1
    _fields_ = [
    ('pwm', ctypes.c_int8),
    ]
    
"""
typedef struct
{
    tEventLogHeadState head;
    tEventLogFrameState frame;
    tEventLogModuleState mod[3];
    tEventLogSimpleMotState mot_feeder;
    tEventLogSimpleMotState mot_stacker;
    uint8_t _reserved_free;
    tEventLogMotorState mot_separator;
    tEventLogMotorState mot_transport;
    tEventLogSolenoidState sol_head;
    tEventLogMotorState mot_mod_drum[3];
    tEventLogMotorState mot_mod_transport[3];
} tEventLogState;
"""

class tEventLogState(Struct2StringMixin, ctypes.Structure):
    _pack_ = 1
    _fields_ = [
    ('head', tEventLogHeadState),
    ('frame', tEventLogFrameState),
    ('mod', tEventLogModuleState*3),
    ('mot_feeder', tEventLogSimpleMotState),
    ('mot_stacker', tEventLogSimpleMotState),
    ('__reserved', ctypes.c_uint8),
    ('mot_separator', tEventLogMotorState),
    ('mot_transport', tEventLogMotorState),
    ('sol_head', tEventLogSolenoidState),
    ('mot_mod_drum', tEventLogMotorState*3),
    ('mot_mod_transport', tEventLogMotorState*3),
    ]
    def pprint(self):
        print '--head--'
        print self.head
        print '--frame--'
        print self.frame
        for i, m in enumerate(self.mod):
            print '--mod%i--'%i
            print m
        print '--motor feeder--'
        print self.mot_feeder
        print '--motor separator--'
        print self.mot_separator
        print '--motor transport--'
        print self.mot_transport
        print '--solenoid head--'
        print self.sol_head
        for i, m in enumerate(self.mot_mod_drum):
            print '--mod%i motor drum--'%i
            print m
        for i, m in enumerate(self.mot_mod_transport):
            print '--mod%i motor transport--'%i
            print m


if __name__ == '__main__':
    with open('r:\EventLog.bin', 'rb') as f:
    data = f.read()
    print(len(data)%ctypes.sizeof(tEventLogState))
    #data = data[len(data)%ctypes.sizeof(tEventLogState):]
    #with open('cut.bin', 'wb') as f:
    #    f.write(data)
    n = len(data)/ctypes.sizeof(tEventLogState)
    print(n, "records", ",%s seconds"%(n*0.005))
    log = (tEventLogState*n).from_buffer_copy(data)
    max_log_length = 500000
    if n > max_log_length:
        print("reducing log length to %i last records" % max_log_length)
        log = log[-max_log_length:]
    #print "last state", log[-1]
#    log[-1].pprint()
    input1_blocked = [s.head.input1_blocked for s in log]
    input1_open = [s.head.input1_open for s in log]
    input2_blocked = [s.head.input2_blocked for s in log]
    exit_blocked = [s.head.exit_blocked for s in log]
    exit_open = [s.head.exit_open for s in log]
    scan_blocked = [s.head.scan_blocked for s in log]
    scan_open = [s.head.scan_open for s in log]
    latch_blocked = [s.head.latch_blocked for s in log]
    platform_blocked = [s.head.platform_blocked for s in log]
    front_lid_blocked = [s.head.front_lid_blocked for s in log]
    #adc_scan_trig = [s.head.adc_scan_trig for s in log]
    tm_pwm = [s.mot_transport.pwm for s in log]
    feed_pwm = [s.mot_feeder.pwm for s in log]
    sep_pwm = [s.mot_separator.pwm for s in log]
    stacker_pwm = [s.mot_stacker.pwm for s in log]
    solenoid_pwm = [s.sol_head.pwm for s in log]
    tm_steps = [s.mot_transport.steps for s in log]
    separator_steps = [s.mot_separator.steps for s in log]
    laser_open = [s.head.laser_open for s in log]
    laser_blocked = [s.head.laser_blocked for s in log]
    laser_blocked_double = [s.head.laser_blocked_double for s in log]
    laser_value = [s.head.laser_value for s in log]
    laser_specle_value = [s.head.laser_specle_value for s in log]
    #laser_pwm = [s.head.laser_pwm for s in log]
    mod0_exit_blocked = [s.mod[0].exit_blocked for s in log]
    mod1_exit_blocked = [s.mod[1].exit_blocked for s in log]
    mod0_input_open = [s.mod[0].input_open for s in log]
    mod1_input_open = [s.mod[1].input_open for s in log]
    mod0_drum_blocked = [s.mod[0].drum_enter_blocked for s in log]
    mod1_drum_blocked = [s.mod[1].drum_enter_blocked for s in log]
    mod0_input_blocked = [s.mod[0].input_blocked for s in log]
    mod1_input_blocked = [s.mod[1].input_blocked for s in log]
    mod0_motor_transport_pwm = [s.mot_mod_transport[0].pwm for s in log]
    mod1_motor_transport_pwm = [s.mot_mod_transport[1].pwm for s in log]
    mod0_motor_drum_pwm = [s.mot_mod_drum[0].pwm for s in log]
    mod1_motor_drum_pwm = [s.mot_mod_drum[1].pwm for s in log]
    
    
    cycle_blocked = [s.frame.cycle_blocked for s in log]
    box_blocked = [s.frame.box_blocked for s in log]
    
    """
    plt.figure()
    plt.grid()
    plt.plot(input1_blocked, label="input1_blocked")
    plt.plot(input2_blocked, label="input2_blocked")
    plt.plot(input1_open, label="input1_open")
    plt.legend()
    
    plt.figure()
    plt.grid()
    plt.plot(exit_open, label="exit_open")
    plt.plot(exit_blocked, label="exit_blocked")
    plt.legend()
    
    plt.figure()
    plt.grid()
    plt.plot(scan_blocked, label="scan_blocked")
    plt.plot(scan_open, label="scan_open")
    plt.legend()
    
    plt.figure()
    plt.grid()
    plt.plot(laser_open, label="laser_open")
    plt.plot(laser_blocked, label="laser_blocked")
    plt.plot(laser_blocked_double, label="laser_blocked_double")
    plt.legend()
     
    plt.figure()
    plt.grid()
    plt.plot(tm_pwm, label="tm_pwm")
    plt.plot(feed_pwm, label="feed_pwm")
    plt.plot(mod1_motor_transport_pwm, label="mod1 tm pwm")
    plt.plot(mod0_motor_transport_pwm, label="mod0 tm pwm")
    plt.legend()
    
    plt.figure()
    plt.grid()
    plt.plot(tm_steps, label="tm_steps")
    plt.legend()

    plt.figure()
    plt.grid()
    plt.plot(exit_blocked, label="exit_blocked")
    plt.plot(mod0_exit_blocked, label="mod0_exit_blocked")
    plt.plot(mod1_exit_blocked, label="mod1_exit_blocked") 
    plt.plot(tm_pwm, label="tm_pwm")
    plt.plot(feed_pwm, label="feed_pwm")
    plt.plot(mod1_motor_transport_pwm, label="mod1 tm pwm")
    plt.plot(mod0_motor_transport_pwm, label="mod0 tm pwm")    
    plt.legend()

    plt.figure()
    plt.grid()
    ax1 = plt.gca()
    ax1.plot(adc_scan_trig, label="adc_scan_trig", color='b')
    ax2 = plt.twinx()
    ax2.plot(scan_blocked, label="scan_blocked", color='g')
    ax2.plot(exit_blocked, label="exit_blocked", color='r')
    ax1.legend(loc=1)
    ax2.legend(loc=4)"""
    plt.figure()
    gs = gridspec.GridSpec(nrows=7, ncols=1,
                           width_ratios=[1],
                           height_ratios=[3,1,3,1,1,1,1]
                           )
    
    plt.grid()
    ax1 = plt.subplot(gs[0])
    ax1.plot(tm_steps, label="tm_steps", color='b')
    ax1.plot(separator_steps, label="separator_steps", color='b', linestyle=':')
    
    #ax1.plot(adc_scan_trig, label="adc_scan_trig", color='m')
    ax2 = plt.twinx()
    ax2.plot(exit_blocked, label="exit_blocked", color='r')
    #ax2.plot(exit_open, label="exit_open", color='r')
    ax2.plot(scan_blocked, label="scan_blocked", color='g')
    #ax2.plot(input1_blocked, label="input1_blocked", color='y')
    ax2.plot(latch_blocked, label="latch_blocked", color='y')
    #plt.plot(laser_open, label="laser_open")
    plt.grid()
    ax3 = plt.subplot(gs[1], sharex=ax1)
    ax3.plot(input1_blocked, label="input1_blocked", color='b', linestyle=':', linewidth=3)
    ax3.plot(input2_blocked, label="input2_blocked", color='b', linestyle='--')
    plt.grid()
    ax4 = plt.subplot(gs[2], sharex=ax1)
    ax4.plot(tm_pwm, label="tm_pwm")
    ax4.plot(feed_pwm, label="feed_pwm")
    ax4.plot(sep_pwm, label="sep_pwm")
    ax4.plot(mod1_motor_transport_pwm, label="mod1 tm pwm")
    ax4.plot(mod0_motor_transport_pwm, label="mod0 tm pwm")  
    ax4.plot(stacker_pwm, label="stacker_pwm") 
    ax4.plot(solenoid_pwm, label="solenoid_pwm") 
    plt.grid()
    ax5 = plt.subplot(gs[3], sharex=ax1)
    ax5.plot(mod0_input_blocked, label='mod0_input_blocked')
    ax5.plot(mod0_drum_blocked, label='mod0_drum_blocked')
    ax5.plot(mod0_exit_blocked, label='mod0_exit_blocked')
    ax6 = plt.subplot(gs[4], sharex=ax1)  
    ax6.plot(mod1_input_blocked, label='mod1_input_blocked')
    ax6.plot(mod1_exit_blocked, label='mod1_exit_blocked')
    ax6.plot(mod1_drum_blocked, label='mod1_drum_blocked')
    plt.grid()
    ax7 = plt.subplot(gs[5], sharex=ax1)  
    ax7.plot(cycle_blocked, label='cycle_blocked')
    ax7.plot(box_blocked, label='box_blocked')
    ax7.plot(front_lid_blocked, label="front_lid_blocked")
    plt.grid()
    ax8 = plt.subplot(gs[6], sharex=ax1)
    ax8.plot(laser_blocked, label="laser_blocked", color='r', linestyle=':', linewidth=2)
    ax8.plot(laser_open, label="laser_open", color='g', linestyle=':')
    ax8.plot(laser_blocked_double, label="laser_blocked_double", color='m', linestyle=':')
    plt.grid()
    ax9 = plt.twinx()
    ax9.plot(laser_value, label="laser_value")
    #ax9.plot(laser_pwm, label="laser_pwm")
    ax1.legend(loc=1)
    ax2.legend(loc=4)
    ax3.legend(loc=1)
    ax4.legend(loc=4)
    ax5.legend(loc=1)
    ax6.legend(loc=1)
    ax7.legend(loc=1)
    ax8.legend(loc=1)
    ax9.legend(loc=4)
    plt.grid()

    points = []
    plt1_axes = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9]
    def onclick(event):
        print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
              ('double' if event.dblclick else 'single', event.button,
               event.x, event.y, event.xdata, event.ydata))
        if event.button == 3:#right click
            for ax in plt1_axes:
                ax.axvline(x=event.xdata, linestyle='--', color='black')
            points.append(event.xdata)
            print points
            print map(lambda a: (a[1]-a[0])*5, zip(points[::2], points[1::2]))


    cid = plt.gcf().canvas.mpl_connect('button_press_event', onclick)
    
    
    plt.figure()
    ax1 = plt.gca()
    ax1.plot(laser_blocked, label="laser_blocked", color='r', linestyle=':', linewidth=2)
    ax1.plot(laser_open, label="laser_open", color='g', linestyle=':')
    ax1.plot(laser_blocked_double, label="laser_blocked_double", color='m', linewidth=4, linestyle=':')
    plt.grid()
    ax2 = plt.twinx()
    ax2.plot(laser_value, label="laser_value")
    ax2.plot(laser_specle_value, label="laser_specle_value")
    ax1.legend(loc=1)
    ax2.legend(loc=4)
    #ax9.plot(laser_pwm, label="laser_pwm")

    #plt.figure()
    #plt.plot(latch_blocked, label="latch_blocked")
    #plt.plot(platform_blocked, label="platform_blocked")
    #plt.plot(front_lid_blocked, label="front_lid_blocked")
    #plt.grid()
    #plt.legend()
    """
    def fn_split_by_tm_steps(log, start=-1):
        split_by_tm_steps = []
        for i in xrange(1, len(log)):
            if log[i].mot_transport.steps < log[i-1].mot_transport.steps or i == len(log)-1:
                if (start >= 0):
                    split_by_tm_steps.append(log[start:i])
                start = i
        return split_by_tm_steps
    split_by_tm_steps = fn_split_by_tm_steps(log)
    plt.figure()
    gs = gridspec.GridSpec(nrows=4, ncols=1,
                           width_ratios=[1],
                           height_ratios=[1,1,1,1]
                           )
    ax1 = plt.subplot(gs[0])
    ax2 = plt.twinx()
    ax3 = plt.subplot(gs[1], sharex=ax1)
    ax4 = plt.subplot(gs[2], sharex=ax1)
    ax5 = plt.subplot(gs[3], sharex=ax1)
    try:
        for l in (split_by_tm_steps[2], split_by_tm_steps[3], split_by_tm_steps[4]):
        #for l in (split_by_tm_steps[4], split_by_tm_steps[5], split_by_tm_steps[11]):
        #for l in split_by_tm_steps:
            tm_steps = [s.mot_transport.steps for s in l]
            tm_speed = [(l[i].mot_transport.steps - l[i-1].mot_transport.steps)/0.1 if i>0 else 0 for i in xrange(len(l))]
            exit_blocked = [s.head.exit_blocked for s in l]
            scan_blocked = [s.head.scan_blocked for s in l]
            mod0_exit_blocked = [s.mod[0].exit_blocked for s in l]
            mod1_exit_blocked = [s.mod[1].exit_blocked for s in l]
            laser_open = [s.head.laser_open for s in l]
            laser_blocked = [s.head.laser_blocked for s in l]
            laser_blocked_double = [s.head.laser_blocked_double for s in l]
            b, = ax1.plot(tm_steps, label="tm_steps", color='b')
            #y, = ax1.plot(tm_speed, label="tm_speed", color='y')
            r, = ax2.plot(exit_blocked, label="exit_blocked", color='r')
            g, = ax2.plot(scan_blocked, label="scan_blocked", color='g')
            #plt.plot(mod0_exit_blocked, label="mod0_exit_blocked")
            #plt.plot(mod1_exit_blocked, label="mod1_exit_blocked") 
            #plt.plot(laser_open, label="laser_open", color='b', linestyle=':', linewidth=3)
            #plt.plot(laser_blocked, label="laser_blocked")
            #plt.plot(laser_blocked_double, label="laser_blocked_double", color='b', linestyle=':', linewidth=3)
            
            tm_pwm = [s.mot_transport.pwm for s in l]
            feed_pwm = [s.mot_feeder.pwm for s in l]
            sep_pwm = [s.mot_separator.pwm for s in l]
            stacker_pwm = [s.mot_stacker.pwm for s in l]
            solenoid_pwm = [s.sol_head.pwm for s in l]
            mod0_motor_transport_pwm = [s.mot_mod_transport[0].pwm for s in l]
            mod1_motor_transport_pwm = [s.mot_mod_transport[1].pwm for s in l]
            mod0_motor_drum_pwm = [s.mot_mod_drum[0].pwm for s in l]
            mod1_motor_drum_pwm = [s.mot_mod_drum[1].pwm for s in l]

            ax3.plot(tm_pwm, label="tm_pwm")
            ax3.plot(feed_pwm, label="feed_pwm")
            ax3.plot(sep_pwm, label="sep_pwm")
            ax5.plot(mod1_motor_transport_pwm, label="mod1 tm pwm")
            ax4.plot(mod0_motor_transport_pwm, label="mod0 tm pwm")  
            ax3.plot(stacker_pwm, label="stacker_pwm") 
            ax3.plot(solenoid_pwm, label="solenoid_pwm")
            ax5.plot(mod1_motor_drum_pwm, label="mod1 drum pwm")
            ax4.plot(mod0_motor_drum_pwm, label="mod0 drum pwm")         
        ax1.legend([b], ('tm_steps', ), loc=1)
        ax2.legend([r, g], ('exit_blocked', 'scan_blocked'), loc=4)
        ax3.legend(loc=1)
        ax4.legend(loc=1)
        ax5.legend(loc=1)
        plt.grid()
    except:
        pass
    
    start = -1
    split_by_exit_blocked = []
    for i in xrange(1, len(log)):
        if log[i].head.exit_blocked > log[i-1].head.exit_blocked:
            start = i
        if log[i].head.exit_blocked < log[i-1].head.exit_blocked:
            split_by_exit_blocked.append(log[start:i])
            
    plt.figure()
    plt.grid()
    ax1 = plt.gca()
    ax2 = plt.twinx()
    for l in split_by_exit_blocked:
        tm_steps_offset = l[0].mot_transport.steps
        tm_steps = [s.mot_transport.steps - tm_steps_offset for s in l]
        exit_blocked = [s.head.exit_blocked for s in l]
        scan_blocked = [s.head.scan_blocked for s in l]
        mod0_exit_blocked = [s.mod[0].exit_blocked for s in l]
        mod1_exit_blocked = [s.mod[1].exit_blocked for s in l]
        b, = ax1.plot(tm_steps, label="tm_steps-tm_steps[0]", color='b')
        r, = ax2.plot(exit_blocked, label="exit_blocked", color='r')
        g, = ax2.plot(scan_blocked, label="scan_blocked", color='g')
        #plt.plot(mod0_exit_blocked, label="mod0_exit_blocked")
        #plt.plot(mod1_exit_blocked, label="mod1_exit_blocked") 
    ax1.legend([b], ('tm_steps - tm_steps[0]', ), loc=1)
    ax2.legend([r, g], ('exit_blocked', 'scan_blocked'), loc=4)
    
    
    start = -1
    split_by_scan_blocked = []
    for i in xrange(1, len(log)):
        if log[i].head.scan_blocked > log[i-1].head.scan_blocked:
            start = i
        if log[i].head.scan_blocked < log[i-1].head.scan_blocked:
            split_by_scan_blocked.append(log[start:i])
    print len(split_by_scan_blocked)
    split_by_scan_blocked = split_by_scan_blocked[0:]
    
    start = -1
    split_by_scan_open = []
    for i in xrange(1, len(log)):
        if log[i].head.scan_open > log[i-1].head.scan_open:
            start = i
        if log[i].head.scan_open < log[i-1].head.scan_open and start >=0:
            split_by_scan_open.append(log[start:i])
    print len(split_by_scan_open)
    split_by_scan_open = split_by_scan_open[0:]
    
    plt.figure()
    plt.grid()
    time_tick = 0.005
    time_in_ticks = [len(l) for l in split_by_exit_blocked]
    split_by_tm_inside = [fn_split_by_tm_steps(l, 0) for l in split_by_exit_blocked]
    print [len(l) for l in split_by_tm_inside]
    print [len(i) for i in [l for l in split_by_tm_inside][0]]
    mot_steps = []
    for l in split_by_tm_inside:
        #mot_steps = [l[-1].mot_transport.steps - l[0].mot_transport.steps for l in split_by_exit_blocked]
        steps = 0
        for i in l:
            steps += i[-1].mot_transport.steps - i[0].mot_transport.steps
        mot_steps.append(steps)
    #plt.plot( time_in_ticks, label = 'exit_blocked time in ticks')
    #plt.plot( mot_steps, label = 'len in mot steps')
    plt.plot( [steps/(t*time_tick) for t, steps in zip(time_in_ticks, mot_steps)], label = 'speed by exit')
    
    time_in_ticks = [len(l) for l in split_by_scan_blocked]
    mot_steps = [l[-1].mot_transport.steps - l[0].mot_transport.steps for l in split_by_scan_blocked]
    #plt.plot( time_in_ticks, label = 'scan_blocked time in ticks')
    #plt.plot( mot_steps, label = 'len in mot steps')
    plt.plot( [steps/(t*time_tick) for t, steps in zip(time_in_ticks, mot_steps)], label = 'speed by scan')
    
    
    time_in_ticks = [len(l) for l in split_by_scan_open]
    print time_in_ticks
    mot_steps = [l[-1].mot_transport.steps - l[0].mot_transport.steps for l in split_by_scan_open]
    plt.plot( [steps/(t*time_tick) for t, steps in zip(time_in_ticks, mot_steps)], label = 'speed by scan open')
    
    
    split_by_scan_up_exit_up = []
    for i in xrange(1, len(log)):
        if log[i].head.scan_blocked > log[i-1].head.scan_blocked:
            start = i
        if log[i].head.exit_blocked > log[i-1].head.exit_blocked:
            split_by_scan_up_exit_up.append(log[start:i])
    print [len (l) for l in split_by_scan_up_exit_up]
            
    time_in_ticks = [len(l) for l in split_by_scan_up_exit_up]
    mot_steps = [l[-1].mot_transport.steps - l[0].mot_transport.steps for l in split_by_scan_up_exit_up]
    #plt.plot( time_in_ticks, label = 'scan_blocked time in ticks')
    #plt.plot( mot_steps, label = 'len in mot steps')
    plt.plot( [steps/(t*time_tick) for t, steps in zip(time_in_ticks, mot_steps)], label = 'speed by scan_up_exit_up')
    
    split_by_exit_up_scan_down = []
    for i in xrange(1, len(log)):
        if log[i].head.exit_blocked > log[i-1].head.exit_blocked:
            start = i
        if log[i].head.scan_open > log[i-1].head.scan_open:
            split_by_exit_up_scan_down.append(log[start:i])
    print [len (l) for l in split_by_exit_up_scan_down]
            
    time_in_ticks = [len(l) for l in split_by_exit_up_scan_down]
    mot_steps = [l[-1].mot_transport.steps - l[0].mot_transport.steps for l in split_by_exit_up_scan_down]
    #plt.plot( time_in_ticks, label = 'scan_blocked time in ticks')
    #plt.plot( mot_steps, label = 'len in mot steps')
    plt.plot( [steps/(t*time_tick) for t, steps in zip(time_in_ticks, mot_steps)], label = 'speed by split_by_exit_up_scan_down')
     
    plt.legend()
    
    start = -1
    split_by_exit_blocked = []
    for i in xrange(1, len(log)):
        if log[i].head.exit_blocked > log[i-1].head.exit_blocked:
            start = i
        if log[i].head.exit_blocked < log[i-1].head.exit_blocked:
            split_by_exit_blocked.append(log[start:i+60])
    plt.figure()
    plt.grid()
    ax1 = plt.gca()
    ax2 = plt.twinx()
    for l in split_by_exit_blocked[0:]:
        tm_steps_offset = l[0].mot_transport.steps
        tm_steps = [s.mot_transport.steps - tm_steps_offset for s in l]
        exit_blocked = [s.head.exit_blocked for s in l]
        scan_blocked = [s.head.scan_blocked for s in l]
        mod0_exit_blocked = [s.mod[0].exit_blocked for s in l]
        mod1_exit_blocked = [s.mod[1].exit_blocked for s in l]
        b, = ax1.plot(tm_steps, label="tm_steps-tm_steps[0]", color='b')
        r, = ax2.plot(exit_blocked, label="exit_blocked", color='r', linestyle = '--', linewidth=4)
        g, = ax2.plot(scan_blocked, label="scan_blocked", color='g')
        y, = ax2.plot(mod0_exit_blocked, label="mod0_exit_blocked", color='y', linestyle = '-.', linewidth=3)
        k, = ax2.plot(mod1_exit_blocked, label="mod1_exit_blocked", color='k', linestyle = ':', linewidth=2) 
    ax1.legend([b, ], ('tm_steps - tm_steps[0]', ), loc=1)
    ax2.legend([r, g, y, k], ('exit_blocked', 'scan_blocked', "mod0_exit_blocked", "mod0_exit_blocked"), loc=4)
    """
    plt.show()
        
    