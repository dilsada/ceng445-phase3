from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from chain_app import forms
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

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
			print(selected_board)
			return HttpResponseRedirect(reverse('board', kwargs={'board_id': selected_board}))
		else:
			print('Board selection failed')
			return HttpResponse("class HomeView, post error: invalid board selection")

class BoardView(View):
	def get(self, request, board_id):
		return render(request, 'board.html', {'board_id': self.kwargs.get('board_id')})
