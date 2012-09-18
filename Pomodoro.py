import sublime, sublime_plugin
import threading
import time
import datetime

class Pomodoro(threading.Thread):
	
	MAX_SECONDS = 25 * 60

	is_running = False

	def __init__(self):
		threading.Thread.__init__(self)
		self.start_time = None

	def run(self):
		Pomodoro.is_running = True
		self.mark_start_time()
		
		while (Pomodoro.is_running and ( not self.timer_expired() )):
				self.display_ramaining_time()
				time.sleep(1)
		
		if Pomodoro.is_running: # if finished instead of cancelled
			self.status_message('Pomodoro finished!')
			self.message_dialog('Pomodoro finished!')

		Pomodoro.is_running = False

	def mark_start_time(self):
		self.start_time = self.now()

	def now(self):
		return datetime.datetime.now()

	def timer_expired(self):
		return self.elapsed_time().seconds > Pomodoro.MAX_SECONDS

	def elapsed_time(self):
		return self.now() - self.start_time

	def display_ramaining_time(self):
		remaining_seconds = Pomodoro.MAX_SECONDS - self.elapsed_time().seconds
		minutes = remaining_seconds / 60
		seconds = remaining_seconds % 60
		self.status_message( "Pomodoro Time: [{0:02d}:{1:02d}]".format(minutes , seconds))

	def status_message(self, message):
		sublime.set_timeout(lambda: sublime.status_message(message) , 0)

	def message_dialog(self, message):
		sublime.set_timeout(lambda: sublime.message_dialog(message), 0)

class StartPomodoroTimerCommand(sublime_plugin.ApplicationCommand):
	
	def run(self):
		thread = Pomodoro()
		thread.start()
		sublime.status_message("Pomodoro timer started!")
		
	def is_enabled(self):
		return not Pomodoro.is_running

class StopPomodoroTimerCommand(sublime_plugin.ApplicationCommand):
	def run(self):
		sublime.status_message("Pomodoro timer stopped!")
		Pomodoro.is_running = False
				
	def is_enabled(self):
		return Pomodoro.is_running
