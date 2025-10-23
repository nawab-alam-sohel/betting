from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django import forms
from .models import User, Role


class RegistrationForm(forms.ModelForm):
	password1 = forms.CharField(widget=forms.PasswordInput)
	password2 = forms.CharField(widget=forms.PasswordInput)
	role = forms.ModelChoiceField(queryset=Role.objects.none())

	class Meta:
		model = User
		fields = ["email", "full_name", "phone", "role"]

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# Public registration: only allow 'user' role by default
		self.fields['role'].queryset = Role.objects.filter(slug='user')

	def clean(self):
		cleaned = super().clean()
		if cleaned.get('password1') != cleaned.get('password2'):
			raise forms.ValidationError("Passwords do not match")
		# Block attempts to select superadmin/admin/agent via tampering
		role = cleaned.get('role')
		if role and role.slug not in ['user']:
			raise forms.ValidationError("Invalid role selection")
		return cleaned

	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		user.is_active = True
		if commit:
			user.save()
		return user


def register(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = form.save()
			messages.success(request, "Registration successful. You can now log in.")
			# Optionally auto-login
			# login(request, user)
			return redirect('/admin/login/?next=/admin/')
	else:
		form = RegistrationForm()
	return render(request, 'users/register.html', { 'form': form })
