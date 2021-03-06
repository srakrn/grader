from django.db.models import Q
from django.utils import timezone

from rest_framework import viewsets

from .models import *
from .serializers import *

class TestViewSet(viewsets.ModelViewSet):
	serializer_class = TestSerializer

	def get_queryset(self):
		objects = Test.objects.all()

		if not self.request.user.has_perm('problems.change_test'):
			objects = objects.filter(Q(start__lte=timezone.now()) | Q(start=None))

		return objects

class ProblemViewSet(viewsets.ModelViewSet):
	serializer_class = ProblemSerializer

	def get_queryset(self):
		objects = Problem.objects.filter(
			test_id=self.kwargs['test_pk'],
		)

		if not self.request.user.has_perm('problems.change_test'):
			objects = objects.filter(Q(test__start__lte=timezone.now()) | Q(test__start=None))

		return objects
