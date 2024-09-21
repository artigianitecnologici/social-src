# say action

import sys, time

from actionproxy import ActionProxy



ACTION_NAME = 'say'

class SayActionProxy(ActionProxy):

    def __init__(self, actionname):
        ActionProxy.__init__(self, actionname)


    def __del__(self):
        ActionProxy.__del__(self)


    def action_thread(self, params):

        v = params.split('_')
        saystr = v[0]

        if len(v)>1:
            lang = v[1]
        else:
            lang = 'en'
        tm = 1 + saystr.count(' ')

        print("Say [%s]: %s (time:%d)" %(lang,saystr,tm))
        cnt = 0
        dt = 0.5
        while self.do_run and cnt < tm:
            time.sleep(dt)
            cnt += dt

        print('---end say---')

if __name__ == "__main__":

    params = None
    if (len(sys.argv)>1):
        params = sys.argv[1]

    a = SayActionProxy(ACTION_NAME)
    
    if params is not None:
        a.execute(params)  # blocking, CTRL-C to interrupt
    else:
        a.run_server()     # blocking, CTRL-C to interrupt

