# coding:utf8
# func:
# 1. 程序运行打印时间
# 2. 程序间隔10秒打印时间
# 3. 到达指定时间时，结束程序

import time
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, EVENT_SCHEDULER_SHUTDOWN
from pprint import pprint

TIME_FORMAT = "%Y-%m-%d %H-%M-%S"
def get_current_time(): #得到当前时间
    return time.strftime(TIME_FORMAT, time.localtime(time.time()))
def time_to_timestamp(t): #时间转换成时间戳
    return time.mktime(time.strptime(t, TIME_FORMAT))


sched = BlockingScheduler()

# 监听器：判断是否正常运行
def my_listener(event):
    if event.exception:
        print "【程序退出】{}".format(event.exception.message)
        print "退出时间{}".format(get_current_time() )
    else:
        print '任务照常运行...'
    print "打印event的所有值"
    pprint(vars(event))  # 打印extent中的所有值
sched.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR | EVENT_SCHEDULER_SHUTDOWN)

# 任务
cnt =0
@sched.scheduled_job(trigger="interval", args=("[定时调用]", ), seconds=10, id="print_time")
def print_time(param):
    global cnt

    current_time = get_current_time()
    current_timestampe = time_to_timestamp(current_time)
    end_timestampe = time_to_timestamp(end_time)
    if current_timestampe>end_timestampe: #到指定时间关闭程序
        sched.shutdown()
    else:
        print("{} {} {}".format(param, cnt, current_time) )

    cnt += 1
    pass

end_time = "2019-3-31 17-10-00" #【注意！】这个结束时间一定要修改
if __name__ == '__main__':
    print_time("[函数调用]") #立刻先打印一次时间
    sched.start() #开始定时任务，10秒之后再打印
    pass