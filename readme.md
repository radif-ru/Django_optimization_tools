1. Можно использовать в CBV extra_context вместо get_context_data?

extra_context = {'page_title': 'админка/категории'}

#вместо:
page_title = 'админка/категории'

 def get_context_data(self, *, object_list=None, **kwargs):
	data = super().get_context_data(object_list=None, **kwargs)
	data['page_title'] = self.page_title
	return data

