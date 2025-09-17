import tkinter as tk
import math
import time


class Ball:
	def __init__(self, x, y, r=12, color="orange"):
		self.x = x
		self.y = y
		self.r = r
		self.color = color

		# physics
		self.vx = 0.0
		self.vy = 0.0

	def apply_force(self, ax, dt, max_vx=400):
		# ax : horizontal acceleration (px/s^2)
		self.vx += ax * dt
		# clamp
		if self.vx > max_vx:
			self.vx = max_vx
		if self.vx < -max_vx:
			self.vx = -max_vx

	def update(self, dt, g):
		# g : gravity (px/s^2) positive downward
		self.vy += g * dt
		self.x += self.vx * dt
		self.y += self.vy * dt

    def top(self):
        return self.y-self.r

	def bottom(self):
		return self.y + self.r

	def left(self):
		return self.x - self.r

	def right(self):
		return self.x + self.r


class Platform:
	def __init__(self, x1, y1, x2, y2, color="saddle brown"):
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		self.color = color

	def top(self):
		return self.y1

    def bottom(self):
        return self.y2
    


class Game:
	def __init__(self, width=800, height=600):
		self.width = width
		self.height = height

		# physics params
		self.FPS = 60
		self.dt = 1.0 / self.FPS
		self.g = 1200.0  # px/s^2, tuneable
		self.bounce_height = 140.0  # pixels the ball should reach after each bounce
		# derived bounce velocity (upwards -> negative vy)
		self.v_bounce = math.sqrt(2 * self.g * self.bounce_height)

		self.acc = 1800.0  # horizontal acceleration px/s^2 when key is held

		# tkinter
		self.root = tk.Tk()
		self.root.title("Bounce Ball - Tkinter")
		self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="light sky blue")
		self.canvas.pack()

		# ball
		self.ball = Ball(self.width // 2, 100)

		# simple rectangular terrain (list of Platform)
		self.platforms = []
		self._create_terrain()

		# keys
		self.left_pressed = False
		self.right_pressed = False

		# drawing ids
		self.ball_id = None
		self.platform_ids = []
		self.hud_id = None

		# timing
		self._running = False

		# input
		self.root.bind('<KeyPress-Left>', self._on_left_down)
		self.root.bind('<KeyRelease-Left>', self._on_left_up)
		self.root.bind('<KeyPress-Right>', self._on_right_down)
		self.root.bind('<KeyRelease-Right>', self._on_right_up)

	def _create_terrain(self):
		w, h = self.width, self.height
		# ground
		self.platforms.append(Platform(0, h - 30, w, h, color="#4d2600"))
		# some floating rectangular platforms
		self.platforms.append(Platform(80, h - 150, 260, h - 130))
		self.platforms.append(Platform(340, h - 250, 520, h - 230))
		self.platforms.append(Platform(580, h - 360, 760, h - 340))
		# a low wide platform near the left
		self.platforms.append(Platform(10, h - 260, 160, h - 240))

	def _on_left_down(self, event):
		self.left_pressed = True

	def _on_left_up(self, event):
		self.left_pressed = False

	def _on_right_down(self, event):
		self.right_pressed = True

	def _on_right_up(self, event):
		self.right_pressed = False

	def _apply_physics(self):
		# horizontal input
		ax = 0.0
		if self.left_pressed and not self.right_pressed:
			ax = -self.acc
		elif self.right_pressed and not self.left_pressed:
			ax = self.acc

		# apply horizontal acceleration
		self.ball.apply_force(ax, self.dt)

		prev_x, prev_y = self.ball.x, self.ball.y
		ball_bottom = self.ball.bottom()
        ball_top=self.ball.top()

		# update motion
		self.ball.update(self.dt, self.g)

		# world bounds: left/right
		if self.ball.left() < 0:
			self.ball.x = self.ball.r
			self.ball.vx = 0
		if self.ball.right() > self.width:
			self.ball.x = self.width - self.ball.r
			self.ball.vx = 0

		# collision with platforms (top surface only)
		for p in self.platforms:
			top = p.top()
            bottom = p.bottom()
			# check horizontal overlap (consider ball radius)
			if (self.ball.x + self.ball.r) >= p.x1 and (self.ball.x - self.ball.r) <= p.x2:
				# collision when coming from above (ball_bottom <= top) and now below or touching
				if ball_bottom <= top:
					# place ball on top and set vy so it reaches fixed bounce height
					self.ball.y = top - self.ball.r
					# set upward velocity to reach bounce_height (independent of incoming speed)
					self.ball.vy = -self.v_bounce
                # collision block when coming from other side
                elif ball_top >= bottom:
					self.ball.y = bottom + self.ball.r
                    self.ball.vy = -self.ball.vy*g



	def _draw(self):
		c = self.canvas
		# clear canvas items for redraw
		c.delete('all')

		# draw platforms
		for p in self.platforms:
			c.create_rectangle(p.x1, p.y1, p.x2, p.y2, fill=p.color, outline='black')

		# draw ball
		b = self.ball
		c.create_oval(b.left(), b.y - b.r, b.right(), b.y + b.r, fill=b.color, outline='black')

		# HUD
		text = f"vx={b.vx:.1f} px/s  vy={b.vy:.1f} px/s  bounce_h={self.bounce_height:.0f}px"
		c.create_text(10, 10, anchor='nw', text=text, fill='black', font=('Consolas', 12, 'bold'))
		c.create_text(10, 30, anchor='nw', text='← / → : apply horizontal force', fill='black', font=('Consolas', 10))

	def start(self):
		self._running = True
		self._loop()
		self.root.mainloop()

	def _loop(self):
		if not self._running:
			return
		start = time.time()
		self._apply_physics()
		self._draw()
		elapsed = time.time() - start
		delay = max(1, int((self.dt - elapsed) * 1000))
		# schedule next frame
		self.root.after(delay, self._loop)


if __name__ == '__main__':
	game = Game(800, 600)
	game.start()

