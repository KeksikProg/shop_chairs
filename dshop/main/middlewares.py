from .models import Rubric

def rubric_context_processors(request):
	context = {}
	context ['rubrics'] = Rubric.objects.all()
	return context