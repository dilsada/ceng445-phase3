import os.path
from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from . import forms
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import BoardModel
from django.http import HttpResponse

from .library import Board, BowlingBall, MarbleBall, TennisBall, BookBlock, DominoBlock, Segment, RotatingSegment


import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
from matplotlib import animation
from matplotlib.collections import PatchCollection

class RegisterView(View):
	register_form = forms.RegisterForm()
	def get(self, request):
		return render(request, 'register.html', {'form': self.register_form})

	def post(self, request):
		self.register_form = forms.RegisterForm(data=request.POST)
		if self.register_form.is_valid():
			user = self.register_form.save(commit=False)
			user.set_password(self.register_form.cleaned_data['password'])
			user.save()
		return redirect('/register/')

class LoginView(View):
	login_form = forms.LoginForm()
	def get(self, request):
		return render(request, 'login.html', {'form': self.login_form})

	def post(self, request):
		self.login_form = forms.LoginForm(data=request.POST)
		if self.login_form.is_valid():
			user = authenticate(username=self.login_form.cleaned_data['username'],
								password=self.login_form.cleaned_data['password'])
			if user:
				login(request, user)
				return HttpResponseRedirect(reverse('home'))
		else:
			print('Login failed')
			return HttpResponse("invalid login details")

class LogoutView(View):
	def get(self,request):
		logout(request)
		return HttpResponseRedirect(reverse('login'))

class HomeView(View):
	board_form = forms.BoardForm()

	def get(self, request):
		return render(request, 'home.html', {'form': self.board_form})

	def post(self, request):
		self.board_form = forms.BoardForm(data=request.POST)
		if self.board_form.is_valid():
			selected_board = self.board_form.cleaned_data.get('selected_board')
			return HttpResponseRedirect(reverse('board', kwargs={'board_id': selected_board}))
		else:
			print('Board selection failed')
			return HttpResponse("class HomeView, post error: invalid board selection")

def plotter(state):
	frames = []
	shapes = []
	def init():
		plt.axis('equal')

	def addShapes(ax, shapes):
		for s in shapes:
			if type(s) == mlines.Line2D:
				ax.add_line(s)
			else:
				ax.add_patch(s)

	def animate(dt):
		ax.clear()
		ax.set_xlim((0, 600))
		ax.set_ylim((0, 600))
		addShapes(ax, frames[dt])

	for object in state:
		shape = object[0]
		pos = object[2]

		if shape.getType() == 'bowlingBall':
			x, y, r = float(pos[0]), float(pos[1]), float(shape.bowlingRadius)
			shapes.append(mpatches.Circle((x, y), r))

	frames.append(tuple(shapes))
	fig, ax = plt.subplots()
	anim = animation.FuncAnimation(fig, animate, init_func=init,
								   frames=len(frames), interval=20, blit=False)
	#plt.show()

def createShape(shapeID):
	#shapeID- shape pairs are in forms.py
	x = 200
	y = 200 #gonna get these from forms as well
	newShape = None
	if shapeID == 1:
		newShape = BowlingBall.BowlingBall(center=(x, y))
	elif shapeID == 2:
		newShape = MarbleBall.MarbleBall(center = (x, y))
	elif shapeID == 3:
		newShape = TennisBall.TennisBall(center = (x, y))
	elif shapeID == 4:
		newShape = BookBlock.BookBlock(center = (x,y))
	elif shapeID == 5:
		newShape = DominoBlock.DominoBlock(center = (x,y))
	elif shapeID == 6:
		pass
	elif shapeID == 7:
		newShape = RotatingSegment.RotatingSegment(rotationCenter = (x,y), length = 100,  radius = 5.0)
	else:
		print("invalid shape id")
	return newShape

class BoardView(View):
	boardJSONs = {'1': 'test1.json', '2': 'test2.json', '3': 'test3.json', '4': 'test4.json'}
	shape_form = forms.ShapeForm()

	def __init__(self):
		self.board = None

	def get(self, request, board_id):
		board_name = BoardModel.objects.get(bid=int(board_id))

		return render(request, 'board.html', {'board_id': self.kwargs.get('board_id'), 'form': self.shape_form})

	def post(self, request, board_id):
		self.shape_form = forms.ShapeForm(data=request.POST)
		if self.shape_form.is_valid():
			selected_shape = self.shape_form.cleaned_data.get('selected_shape')
			print("SELECTED SHAPE:::::::")
			print(selected_shape)
			newShape = createShape(shapeID=int(selected_shape))
			board_name = BoardModel.objects.get(bid=int(board_id))
			dir_path = os.path.dirname(os.path.realpath(__file__))
			fname = os.path.join(dir_path, 'library/inputs', self.boardJSONs[board_id])

			self.board = Board.Board(name=board_name)
			self.board.load(fname)
			print(self.board.state())
			print(self.board.boardName)
			self.board.addShape(newShape)
			print(self.board.state())
			return HttpResponse(selected_shape)

		else:
			print('Shape selection failed')
			return HttpResponse("class BoardView, post error: invalid shape selection")

