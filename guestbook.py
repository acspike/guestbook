import datetime
import os
import subprocess

from gpiozero import LED, Button
from signal import pause


class Guestbook(object):
    def __init__(self, hookswitch_pin):
        self.hookswitch = Button(hookswitch_pin)
        self.hookswitch.when_held = self.leave_message
    def leave_message(self):
        inproc = subprocess.Popen(
                ['ffmpeg','-loglevel','quiet', 
                    '-f', 'alsa', '-i', "plughw:CARD=Audio,DEV=0", 
                    '-c:a', 'libmp3lame', '-b:a', '128k', 
                    '-y', f"./messages/message_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"]
            )
        outproc = subprocess.Popen(
            ['ffplay','-loglevel','quiet','-nodisp','-autoexit','greeting.mp3'], 
            env=dict(os.environ, SDL_AUDIODRIVER="alsa", AUDIODEV="plughw:CARD=Audio,DEV=0")
            )
        self.hookswitch.wait_for_release()
        inproc.terminate()
        outproc.terminate()
        subprocess.Popen(['/opt/guestbook/sync_messages.sh'])
    

if __name__ == '__main__':
    guestbook = Guestbook(4)
    pause()
