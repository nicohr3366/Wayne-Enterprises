from django.db import models


class NavItem(models.Model):
	label = models.CharField(max_length=100, help_text='Texto visible en el menú')
	url_name = models.CharField(max_length=100, help_text='Nombre de URL con namespace, por ejemplo ventures:home')
	order = models.IntegerField(default=0, help_text='Orden de aparición')
	is_active = models.BooleanField(default=True, help_text='Mostrar en el menú')
	open_in_new_tab = models.BooleanField(default=False)

	class Meta:
		ordering = ['order']
		verbose_name = 'Nav Item'
		verbose_name_plural = 'Nav Items'

	def __str__(self):
		return f'{self.order}. {self.label}'

	def get_url(self):
		from django.urls import reverse

		try:
			return reverse(self.url_name)
		except Exception:
			return '#'
