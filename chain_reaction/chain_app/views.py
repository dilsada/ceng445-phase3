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

from .library import Board, BowlingBall, MarbleBall, TennisBall, BookBlock, DominoBlock, Segment, RotatingSegment, colors
from .library.colors import colors

import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
from matplotlib import animation
from matplotlib.collections import PatchCollection

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import io
import json

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
		return render(request, 'login.html', {'form': self.login_form, 'message' : ''})

	def post(self, request):
		self.login_form = forms.LoginForm(data=request.POST)
		if self.login_form.is_valid():
			user = authenticate(username=self.login_form.cleaned_data['username'],
								password=self.login_form.cleaned_data['password'])
			if user:
				login(request, user)
				return HttpResponseRedirect(reverse('home'))
			else:
				return render(request, 'login.html', {'form': self.login_form, 'message' : 'wrong'})

		else:
			print('Login failed')
			return HttpResponse("invalid login details")

class LogoutView(View):
	def get(self,request):
		logout(request)
		return HttpResponseRedirect(reverse('login'), {'message' : ''})

class HomeView(View):
	board_form = forms.BoardForm()

	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('/login')
		return render(request, 'home.html', {'form': self.board_form})

	def post(self, request):
		self.board_form = forms.BoardForm(data=request.POST)
		if self.board_form.is_valid():
			selected_board = self.board_form.cleaned_data.get('selected_board')
			return HttpResponseRedirect(reverse('board', kwargs={'board_id': selected_board}))
		else:
			print('Board selection failed')
			return HttpResponse("class HomeView, post error: invalid board selection")


def plotter(state, board_id):
	board_name = BoardModel.objects.get(bid=int(board_id))

	state = json.loads(board_name.bstate)
	print('-----')
	print(state)
	print('-----')
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

	for ball in state['balls']:
		shapes.append(mpatches.Circle(ball['center'], 50))

	frames.append(tuple(shapes))
	fig, ax = plt.subplots()
	anim = animation.FuncAnimation(fig, animate, init_func=init,
								   frames=len(frames), interval=20, blit=False)
	# plt.show()
	# return fig
	canvas = FigureCanvas(fig)
	buf = io.BytesIO()
	plt.savefig(buf)
	# plt.close(fig)

	response = HttpResponse(buf.getvalue(), content_type='image/png')
	return response

def createShape(shapeID, x, y):
	#shapeID- shape pairs are in forms.py
	x = float(x)
	y = float(y)
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
		newShape = Segment.Segment(mass=300, p1=[x,y], p2=[x-100,y-100], radius=5)
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
		if not request.user.is_authenticated:
			return redirect('/login')

		board_name = BoardModel.objects.get(bid=int(board_id))
		dir_path = os.path.dirname(os.path.realpath(__file__))
		fname = os.path.join(dir_path, 'library/inputs', self.boardJSONs[board_id])
		self.board = Board.Board(name=board_name)
		self.board.load(fname)
		board_name.save()

		board_name.bstate = json.dumps(self.board.save())
		board_name.save()
		current_state = self.board.save()

		return render(request, 'board.html', {'board_id': self.kwargs.get('board_id'), 'username': request.user, 'form': self.shape_form, 'state': current_state, 'msg' : ''})

	def post(self, request, board_id):
		self.shape_form = forms.ShapeForm(data=request.POST)

		if self.shape_form.is_valid():
			selected_shape = self.shape_form.cleaned_data.get('selected_shape')
			x_coord = self.shape_form.cleaned_data['x']
			y_coord = self.shape_form.cleaned_data['y']
			shape_id_1 = str(self.shape_form.cleaned_data['shape_id_1'])
			shape_id_2 = str(self.shape_form.cleaned_data['shape_id_2'])

			if selected_shape:
				newShape = createShape(shapeID=int(selected_shape), x = x_coord, y = y_coord)
			
			board_name = BoardModel.objects.get(bid=int(board_id))
			dir_path = os.path.dirname(os.path.realpath(__file__))
			fname = os.path.join(dir_path, 'library/inputs', self.boardJSONs[board_id])
			self.board = Board.Board(name=board_name)

			if not board_name.loadFlag:
				self.board.load(fname)
				board_name.loadFlag = True
				board_name.save()

			else:
				self.board.loadstr(board_name.bstate)

			print(self.board.state())
			print(self.board.boardName)
			
			content = ''
			if 'remove' in request.POST:
				if shape_id_1 and shape_id_1 in self.board.allShapes.keys():
					self.board.removeShapeWithID(str(shape_id_1))
			elif 'move' in request.POST:
				if shape_id_1 and shape_id_1 in self.board.allShapes.keys():
					x = int(x_coord)
					y = int(y_coord)
					self.board.moveShape(self.board.allShapes[str(shape_id_1)], x, y)
					content = str(newShape.getType())   + ' moved successfully' + ' by (' + str(x_coord) + ', ' + str(y_coord) + ')'

			elif 'connect' in request.POST:
				if shape_id_1 and shape_id_1 in self.board.allShapes.keys() and shape_id_2 and shape_id_2 in self.board.allShapes.keys():
					shape1 = self.board.allShapes[str(shape_id_1)]
					shape2 = self.board.allShapes[str(shape_id_2)]

					self.board.connect(str(shape_id_1), str(shape_id_2))
					content = str(shape1.getType()) + ' ' + str(shape_id_1) + ' and ' + str(shape2.getType()) + ' ' + str(shape_id_2) + ' are connected successfully.'
			
			elif 'disconnect' in request.POST:
				if shape_id_1 and shape_id_1 in self.board.allShapes.keys() and shape_id_2 and shape_id_2 in self.board.allShapes.keys():
					shape1 = self.board.allShapes[str(shape_id_1)]
					shape2 = self.board.allShapes[str(shape_id_2)]

					self.board.disconnectShapes(str(shape_id_1), str(shape_id_2))
					content = str(shape1.getType()) + ' ' + str(shape_id_1) + ' and ' + str(shape2.getType()) + ' ' + str(shape_id_2) + ' are disconnected successfully.'
			
			elif 'add' in request.POST:
				if selected_shape and x_coord and y_coord:
					self.board.addShape(newShape)
					content = 'New ' + str(newShape.getType()) + ' at coordinte (' + x_coord + ', ' + y_coord  + ') added successfully.'
			
			elif 'pick' in request.POST:
				if x_coord and y_coord:
					x = int(x_coord)
					y = int(y_coord)
					res = self.board.pick(x, y)
					content = str(res)

			else:
				print(colors.writeBold("Invalid button"))
			
			board_name.bstate = json.dumps(self.board.save())
			board_name.save()

			current_state = self.board.save()
			print (colors.writeGreen(str(current_state)))

			return render(request, 'board.html', {'board_id': self.kwargs.get('board_id'), 'form': self.shape_form, 'msg' : content, 'state': current_state})

		else:
			print('Shape selection failed')
			return HttpResponse("class BoardView, post error: invalid shape selection")

